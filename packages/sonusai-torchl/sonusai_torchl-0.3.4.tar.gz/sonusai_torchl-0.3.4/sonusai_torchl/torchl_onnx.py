"""sonusai torchl_onnx

usage: torchl_onnx [-hvsf] [-b BATCH] [-t TSTEPS] [-o OUTPUT] [--openvino PREC] MODEL CKPT

options:
    -h, --help
    -v, --verbose                   Be verbose
    -b BATCH, --batch BATCH         Batch size override
    -t TSTEPS, --tsteps TSTEPS      Timesteps override
    -o OUTPUT, --output OUTPUT      Output directory.
    -s, --run-onnx-simplify         Run onnx_simplify() on onnx model before save
    -f, --write-fp16-model          Also write a float16 onnx model (*_fp16.onnx)
    --openvino PREC                 Optionally create an OpenVINO model from the onnx model. [default: None]

Convert a trained Pytorch Lightning checkpoint to Onnx.  The weights and hyper-parameters are loaded from the
checkpoint, and the model definition is specified as an sctl_*.py model file (sctl: sonusai custom torch lightning)

Inputs:
    MODEL       SonusAI Pytorch Lightning custom model file (sctl_*.py)
    CKPT        A Pytorch Lightning checkpoint file (.ckpt)
    BATCH       Batch size used in onnx conversion, overrides value in model ckpt. Use -1 to set to dynamic.
    TSTEPS      Timestep dimension size using in onnx conversion, overrides value in model ckpt if
                the model has a timestep dimension.  Else it is ignored.  Use -1 to set to dynamic.
    output_dir  Directory name where .onnx, .log, and optional OpenVINO .xml, .bin files are written.

Outputs:
                <CKPT>.onnx        ONNX model file with weights, with checkpoint file basename and .onnx extension.
                                   If file exists, then date and timestamps are appended to basename.
                torchl_onnx.log    Log file
                <CKPT>{.xml, .bin} Optional OpenVINO uncompiled model files.
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
    run_onnx_simplify = args["--run-onnx-simplify"]
    fp16_enable = args["--write-fp16-model"]
    ovino_prec = args["--openvino"]

    from datetime import datetime
    from os import makedirs
    from os.path import dirname
    from os.path import exists
    from os.path import isdir
    from os.path import join
    from os.path import splitext

    import numpy as np
    import onnx
    import openvino as ov
    import torch
    from onnxconverter_common import float16
    from onnxsim import simplify
    from sonusai import create_file_handler
    from sonusai import initial_log_messages
    from sonusai import logger
    from sonusai import update_console_handler
    from sonusai.utils.onnx_utils import add_sonusai_metadata
    from sonusai.utils.onnx_utils import get_and_check_inputs
    from sonusai.utils.onnx_utils import get_and_check_outputs
    from torch import randn
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

    ofname_onnx = join(output_dir, ckpt_root + ".onnx")

    # First try, then add date
    if exists(ofname_onnx):
        ts = datetime.now()
        ofname_onnx = join(output_dir, ckpt_root + "-" + ts.strftime("%Y%m%d") + ".onnx")
        if exists(ofname_onnx):  # add hour-min-sec
            ofname_onnx = join(output_dir, ckpt_root + "-" + ts.strftime("%Y%m%d-%H%M%S") + ".onnx")

    ofname_root = splitext(ofname_onnx)[0]

    # Setup logging file
    create_file_handler(ofname_root + "-onnx.log")
    update_console_handler(verbose)
    initial_log_messages("torchl_onnx")
    logger.info(f"Imported model from {model_base}")
    logger.info(f"Loaded checkpoint from {ckpt_base}")

    # Override hyper-parameters, especially batch_size and timesteps, return timesteps which returns model status
    hparams, timesteps = torchl_hparam_override(hparams, batch_size, timesteps)

    # Build model, updates hparams for missing SonusAI params (need for model prediction feature gen compatibility)
    model, hparams = torchl_build_model(litmodel, hparams, training=False, ckpt=ckpt)

    if verbose:
        logger.info(summary(model))
        # from lightning.pytorch import Trainer
        # from lightning.pytorch.callbacks import ModelSummary
        # trainer = Trainer(callbacks=[ModelSummary(max_depth=2)])
        # logger.info(trainer.summarize())
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

    # Prepare model for export
    model.eval()
    insample_shape = model.input_shape
    insample_shape.insert(0, hparams["batch_size"])
    input_sample = randn(insample_shape)
    logger.info(f"Creating onnx model using pytorch.to_onnx writing to {ofname_onnx} ...")

    for m in model.modules():
        if "instancenorm" in m.__class__.__name__.lower():
            logger.debug(
                f"Forcing train=false for instancenorm instance {m}, {m.__class__.__name__.lower()}, "
                f"orig_state: {m.train}"
            )
            m.train(False)
            # m.track_running_stats=True  # has problems

    dynamic_axes = None
    if batch_size == -1 and timesteps != -1:
        logger.info("Overriding input dimension 0 with dynamic size of 'batch_size'")
        dynamic_axes = {
            "input": {0: "batch_size"},  # variable length axes, batch_size is always dimension 0
            "output": {0: "batch_size"},
        }
    elif batch_size != -1 and timesteps == -1:
        logger.info("Overriding timestep dimension 1 with dynamic size of 'timesteps'")
        dynamic_axes = {
            "input": {1: "timesteps"},  # variable length axes, timesteps is always dimension 1
            "output": {1: "timesteps"},
        }
    elif batch_size == -1 and timesteps == -1:
        logger.info(
            "Overriding batch_size and timestep dimensions 0,1 with dynamic sizes of 'batch_size' and 'timesteps'"
        )
        dynamic_axes = {
            "input": {0: "batch_size", 1: "timesteps"},  # variable length axes
            "output": {0: "batch_size", 1: "timesteps"},
        }

    # Export model depending on dynamic_axes specified or not
    # For ref, previous method from lightning docs which is very inflexible:
    #    model.to_onnx(file_path=ofname_onnx, input_sample=input_sample, export_params=True, verbose=verbose)
    # Note: new onnx export method coming from onnx, but currently issues warnings, switch to it TBD
    #    onnx_program = torch.onnx.dynamo_export(model, input_sample)
    if dynamic_axes is not None:
        # Export the model with dynamic size(s)
        torch.onnx.export(
            model,
            input_sample,  # model input (or a tuple for multiple inputs)
            ofname_onnx,  # where to save the model (can be a file or file-like object)
            export_params=True,  # store the trained parameter weights inside the model file
            # opset_version=10,   # the ONNX version to export the model to, use default
            do_constant_folding=False,  # whether to execute constant folding for optimization
            input_names=["input"],  # the model's input names, sonusai convention to use only 1 input
            output_names=["output"],  # the model's output names, sonusai convention to use only 1 output
            dynamic_axes=dynamic_axes,
        )  # variable length axes
    else:
        # Export the model without dynamic sizes
        torch.onnx.export(
            model,
            input_sample,
            ofname_onnx,
            export_params=True,
            do_constant_folding=False,
            input_names=["input"],
            output_names=["output"],
        )

    logger.debug("Loading onnx model to check, add metadata, and optimize if requested.")
    omodel = onnx.load(ofname_onnx)
    logger.info(f"Base onnx model uses ir_version {omodel.ir_version}")
    onnx_inputs, inshapes = get_and_check_inputs(omodel)  # Note: logs warning if # inputs > 1
    logger.info(f"Base onnx model input has {len(inshapes[0])} dims with shape (0 means dynamic): {inshapes[0]}")
    onnx_outputs, oshapes = get_and_check_outputs(omodel)
    logger.info(f"Base onnx model output has {len(oshapes[0])} dims with shape (0 means dynamic): {oshapes[0]}")

    # Add hyper-parameters as metadata in onnx model under hparams key
    omodel = add_sonusai_metadata(omodel, hparams)
    # assert eval(str(hparams)) == hparams       # Note hparams should be a dict (extracted from checkpoint)
    # meta = omodel.metadata_props.add()
    # meta.key = "hparams"
    # meta.value = str(hparams)

    if run_onnx_simplify:
        logger.info("Running onnx_simplify() with optimizations and constant folding ...")
        omodel, check = simplify(omodel)
        if check is not True:
            logger.warning("Onnx simplify check failed. Model may have problems.")

        # omodel_simp, check = simplify(omodel, perform_optimization=False)
        # onnx.save(omodel_simp, 'simp_noopt.onnx')  # test only
        # omodel_simp, check = simplify(omodel, skip_constant_folding=True)
        # onnx.save(omodel_simp, 'simp_nofold.onnx') # test only

    onnx.save(omodel, ofname_onnx)

    if fp16_enable:
        omodel_fp16 = float16.convert_float_to_float16(omodel)
        base16name = splitext(ofname_onnx)[0]
        ofname_onnx_fp16 = base16name + "_fp16.onnx"
        onnx.save(omodel_fp16, ofname_onnx_fp16)
        logger.info(f"Wrote float16 onnx model to {ofname_onnx_fp16}")

    if ovino_prec != "None":
        # Write an OpenVINO ucompiled model, default is to compress to fp16
        # TBD check if == INT8 and do post-training quantization with OpenVINO API
        logger.info("Creating OpenVINO model ...")
        ov_model = ov.convert_model(ofname_onnx, example_input=input_sample, verbose=True)
        logger.info(f"Created OpenVino Model, confirming input shape: {ov_model.inputs[0].partial_shape}")
        # Note open vino uncompiled model saves to .xml and .bin, but only need .xml for save
        basefname = splitext(ofname_onnx)[0]
        ofname_vino = join(basefname + ".xml")  # basefname inlcudes output_dir
        logger.info("Saving OpenVINO uncompiled model (.xml, .bin) ...")
        if not output_dir:
            ov.save_model(
                ov_model, ofname_vino, compress_to_fp16=True
            )  # default fp16-compress is True, rarely needs fp32
        else:
            # openvino save needs to be in same directory (no path) as it writes out two files
            ov.save_model(ov_model, ofname_vino, compress_to_fp16=True)
            # # TBD move to subdir, save, then return
            # import sh
            # pwd = sh.pwd()
            # sh.cd(output_dir)

        ## Alternate convertion method using new torch dynamo export fails on atan2
        # from torch.export import export
        # from openvino import convert_model
        # exported_model = export(model, (model.example_input_array,))
        # ov_model = convert_model(exported_model)  # fails on atan2

        ovino_test = False
        if ovino_test:
            # test compile and prediction run using sample, TBD make this optional
            core = ov.Core()
            compiled_model = core.compile_model(ov_model, "CPU")
            # compiled_model = ov.compile_model(ov_model, "AUTO")   # compile model
            # ov_model_input = ov_model.input(0)
            # input_type = ov_model_input.get_element_type()
            inp_sample_np = np.ones(insample_shape, dtype=np.single)
            results = compiled_model({"input": inp_sample_np})  # single blocking call

            shared_in = ov.Tensor(array=inp_sample_np, shared_memory=True)  # Create tensor, external memory, from numpy
            infer_request = compiled_model.create_infer_request()
            infer_request.set_input_tensor(shared_in)  # Set input tensor for model with one input
            input_tensor = infer_request.get_input_tensor()  # for debug
            output_tensor = infer_request.get_output_tensor()  # for debug

            infer_request.start_async()
            infer_request.wait()
            output = infer_request.get_output_tensor()  # Get output tensor for model with one output
            output_buffer = output.data  # output_buffer[] - accessing output tensor data

            # infer_request.infer({input_tensor_name: input_sample.numpy()})
            #
            # shared_in = ov.Tensor(input_sample.numpy(), shared_memory=True)  # use rand sample from torch above in shared-mem
            # results = compiled_model(inputs={0: shared_in}) # simple call to CompiledModel directly
            # using infer_request:
            # infer_request = compiled_model.create_infer_request()
            # infer_request.infer(inputs={0: shared_in})  # run inference async mode


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Canceled due to keyboard interrupt")
        exit()

    # from onnx.tools import update_model_dims
    # # Here both "seq", "batch" and -1 are dynamic using dim_param.
    # omodel_vl = update_model_dims.update_inputs_outputs_dims(model, {"input_name": ["seq", "batch", 3, -1]},
    #                                                                      {"output_name": ["seq", "batch", 1, -1]})

    # if batch_size is not None:
    #     batch_size = int(batch_size)
    # if batch_size != 1:
    #     batch_size = 1
    #     logger.info(f'For now prediction only supports batch_size = 1, forcing it to 1 now')

    # model_base = basename(model_path)
    # #model = load_model(model_name=model_path, ckpt_name=ckpt_path)  # builds model with default hparams in ckpt
    # model = torchl_load_ckpt_and_model(model_name=model_path, ckpt_name=ckpt_path)
