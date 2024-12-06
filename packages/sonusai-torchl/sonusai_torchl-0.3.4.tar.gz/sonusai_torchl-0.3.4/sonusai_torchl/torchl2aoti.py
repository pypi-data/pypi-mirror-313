"""sonusai torchl2aoti

usage: torchl2aoti [-hvf] [-b BATCH] [-t TSTEPS] [-o OUTPUT] MODEL CKPT

options:
    -h, --help
    -v, --verbose                   Be verbose
    -b BATCH, --batch BATCH         Batch size override
    -t TSTEPS, --tsteps TSTEPS      Timesteps override
    -o OUTPUT, --output OUTPUT      Output directory.
    -f, --write-fp16-model          Also write a float16 model (*_fp16.so)

Generate a Pytorch AOTInductor .so file from a trained Pytorch Lightning checkpoint.  Weights and hyper-parameters are
loaded from the checkpoint, and the model definition is as *.py file (using SonusAI torch lightning conventions)

Inputs:
    MODEL       SonusAI Pytorch Lightning custom module file (.py)
    CKPT        A Pytorch Lightning checkpoint file (.ckpt)
    BATCH       Batch size used in exported model, overrides value in ckpt. Use -1 to set to dynamic.
    TSTEPS      Timestep dimension size using in exported model, overrides value in model ckpt if
                the model has a timestep dimension.  Else it is ignored.  Use -1 to set to dynamic.
    output_dir  Directory name where .so, .log files are written.

Outputs:
                <CKPT>.so           AOT Inductor .so file for use in a cpp inference application.  If the file exists,
                                    then date and timestamps are appended to basename.
                torchl2aoti.log     Log file
"""

from sonusai import logger


def main() -> None:
    import sonusai
    from docopt import docopt
    from sonusai.utils import trim_docstring

    args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

    verbose = args["--verbose"]
    batch_size = args["--batch"]
    timesteps = args["--tsteps"]
    model_path = args["MODEL"]
    ckpt_path = args["CKPT"]
    output_dir = args["--output"]
    fp16_enable = args["--write-fp16-model"]

    from datetime import datetime
    from os import makedirs
    from os.path import dirname
    from os.path import exists
    from os.path import isdir
    from os.path import join
    from os.path import splitext

    import torch
    from sonusai import create_file_handler
    from sonusai import initial_log_messages
    from sonusai import logger
    from sonusai import update_console_handler
    from torchinfo import summary

    from sonusai_torchl.utils.torchl_utils import torchl_build_model
    from sonusai_torchl.utils.torchl_utils import torchl_hparam_override
    from sonusai_torchl.utils.torchl_utils import torchl_load_ckpt
    from sonusai_torchl.utils.torchl_utils import torchl_load_litmodel

    if batch_size is not None:
        batch_size = int(batch_size)

    if timesteps is not None:
        timesteps = int(timesteps)

    # Import checkpoint file first to check
    ckpt, hparams, ckpt_base, ckpt_root = torchl_load_ckpt(ckpt_path)
    # Import model file, expects Sonusai convention of a PL class named MyHyperModel
    litmodel, model_base, model_root = torchl_load_litmodel(model_path)

    # create output log and open vino filenames with ckpt path and basename
    if output_dir is None:
        output_dir = dirname(ckpt_root)
    else:
        if not isdir(output_dir):
            makedirs(output_dir, exist_ok=True)

    ofname_so = join(output_dir, ckpt_root + ".so")

    # First try, then add date
    if exists(ofname_so):
        ts = datetime.now()
        ofname_so = join(output_dir, ckpt_root + "-" + ts.strftime("%Y%m%d") + ".so")
        if exists(ofname_so):  # add hour-min-sec
            ofname_so = join(output_dir, ckpt_root + "-" + ts.strftime("%Y%m%d-%H%M%S") + ".so")

    ofname_root = splitext(ofname_so)[0]

    # Setup logging file
    create_file_handler(ofname_root + "-aoti.log")
    update_console_handler(verbose)
    initial_log_messages("torchl_aoti")
    logger.info(f"Imported Pytorch Lightning model from {model_base}")
    logger.info(f"Loaded checkpoint from {ckpt_base}")

    # Override hyper-parameters, especially batch_size and timesteps, return timesteps from model status (i.e. maybe 0)
    hparams, timesteps = torchl_hparam_override(hparams, batch_size, timesteps)

    # Build model, updates hparams for missing SonusAI params (need for model prediction feature gen compatibility)
    model, hparams = torchl_build_model(litmodel, hparams, training=False, ckpt=ckpt)
    model.eval()  # Prepare model example input for export

    # for m in model.modules():
    #     if 'instancenorm' in m.__class__.__name__.lower():
    #         logger.debug(f'Forcing train=false for instancenorm instance {m}, {m.__class__.__name__.lower()}, '
    #                     f'orig_state: {m.train}')
    #         m.train(False)
    #         # m.track_running_stats=True  # has problems

    dynamic_axes = None
    if batch_size == -1 and timesteps != -1:
        logger.info("Overriding input batch dimension to be dynamic size. Note AOT Inductor has a max limit of 15)")
        example_shape = [batch_size] + hparams["input_shape"].copy()
        example_shape[0] = 2  # AOT wants >1 value for example
        # input_sample = torch.randn(tuple([batch_size] + model.input_shape))
        batch_dim = torch.export.Dim("batch", min=1, max=15)  # note aot inductor seems to have limit of 15
        dynamic_axes = {"x": {0: batch_dim}}
        # dynamic_axes = {'input': {0: 'batch_size'},   # variable length axes, batch_size is always dimension 0
        #                 'output': {0: 'batch_size'}}
    elif batch_size > 0 and timesteps == -1:
        logger.info(f"Overriding timestep dimension 1 with dynamic size of {timesteps} (TBD not working)")
        example_shape = [batch_size] + hparams["input_shape"].copy()
        example_shape[1] = 2  # AOT wants >1 value for example
        # TBD tstep input_sample dim size needs to be >1
        tstep_dim = torch.export.Dim("timesteps", min=1, max=15)
        dynamic_axes = {"x": {1: tstep_dim}}
        # dynamic_axes = {'input': {1: 'timesteps'},   # variable length axes, timesteps is always dimension 1
        #                 'output': {1: 'timesteps'}}
    elif batch_size == -1 and timesteps == -1:
        logger.info("Overriding batch_size and timestep dimensions 0,1 with dynamic sizes.")
        example_shape = [batch_size] + hparams["input_shape"].copy()
        example_shape[0] = 2  # AOT wants >1 value for example dynamic dims
        example_shape[1] = 2  # AOT wants >1 value for example dynamic dims
        batch_dim = torch.export.Dim("batch", min=1, max=15)
        tstep_dim = torch.export.Dim("timesteps", min=1, max=16383)
        dynamic_axes = {"x": {0: batch_dim, 1: tstep_dim}}
        # dynamic_axes = {'input': {0: 'batch_size', 1: 'timesteps'},  # variable length axes
        #             'output': {0: 'batch_size', 1: 'timesteps'}}
    else:
        example_shape = [hparams["batch_size"]] + hparams["input_shape"].copy()

    if verbose:
        logger.info(summary(model, depth=8, input_size=example_shape))
        logger.info("")
        logger.info(f"feature       {model.hparams.feature}")
        logger.info(f"num_classes   {model.num_classes}")
        logger.info(f"batch_size    {model.hparams.batch_size}")
        logger.info(f"timesteps     {model.hparams.timesteps}")
        logger.info(f"flatten       {model.flatten}")
        logger.info(f"add1ch        {model.add1ch}")
        logger.info(f"truth_mutex   {model.truth_mutex}")
        logger.info(f"input_shape   {model.input_shape}")
        logger.info("")

    with torch.no_grad():
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model = model.to(device=device)
        logger.info(f"Generating Torch AOT .so file for device {device}")
        input_sample = torch.randn(example_shape)
        example_inputs = (input_sample.to(device),)
        if dynamic_axes is not None:
            logger.info(f"Input has a dynamic size dim (-1): batch_size={batch_size}, timesteps={timesteps}")
            logger.info(f"Note dynamic size dims example input must have size >1, used shape is {input_sample.shape}")
            so_path = torch._export.aot_compile(
                model,
                example_inputs,
                # Specify the first dimension of the input x as dynamic
                dynamic_shapes=dynamic_axes,
                # Specify the generated shared library path
                options={"aot_inductor.output_path": ofname_so},
            )
        else:
            logger.info(f"Input has fixed dimension sizes: batch_size={batch_size}, timesteps={timesteps}")
            so_path = torch._export.aot_compile(model, example_inputs, options={"aot_inductor.output_path": ofname_so})

    logger.info(f"Wrote Torch AOT .so file to {ofname_so}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Canceled due to keyboard interrupt")
        exit()
