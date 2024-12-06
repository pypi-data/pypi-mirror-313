"""sonusai torchl_predict

usage: torchl_predict [-hvw] [-i MIXID] [-l PMETH] [-d DLCPU] [-b BATCH] [-t TSTEPS]
                      [-a ACCEL] [-n NDEV] [-p PREC] (-m MODEL) (-k CKPT)  DATA ...

options:
    -h, --help
    -v, --verbose                   Be verbose.
    -i MIXID, --mixid MIXID         Mixture ID(s) to use if input is a mixture database. [default: *].
    -l PMETH, --pred-method PMETH   Prediction method: plstep, pydlen, pynodl,  [default: plstep]
    -d DLCPU, --dataloader-cpus     Number of workers/cpus for dataloader. [default: 0]
    -a ACCEL, --accelerator ACCEL   Accelerator to use in PL trainer in non-reset mode [default: auto]
    -n NDEV, --num-devices NDEV     Number of accelerator devices/threads to use [default: auto]
    -p PREC, --precision PREC       Precision to use in PL trainer in non-reset mode. [default: 32]
    -m MODEL, --model MODEL         PL model .py file path.
    -k CKPT, --checkpoint CKPT      PL checkpoint file with weights.
    -b BATCH, --batch BATCH         Batch size (deprecated and forced to 1). [default: 1]
    -t TSTEPS, --tsteps TSTEPS      Timesteps. If 0, dim is not included/expected in model. [default: 0]
    -w, --wavdbg                    Write debug .wav files of feature input, truth, and predict. [default: False]

Run PL (Pytorch Lightning) prediction with model and checkpoint input using input data from either a
SonusAI mixture database or an audio file glob.

The PL model is imported from MODEL .py file and weights loaded from checkpoint file CKPT.

Several prediction methods are available: (see SonusAI dataloader info below)
 plstep:  Use pytorch lightning model predict step and PL builtin loop code (requires mixdb input).
          This method supports Lightning distributed mode across multiple GPUs and nodes of GPUs
 pydlen:  Use pytorch dataloader enumeration (requires mixdb input). See SonusAI dataloader info below.
          Supports cpu and cuda in single device mode.
 pynodl:  Use pytorch with no dataloader. Forced to use this if input data is an audio file glob.

Inputs:
    ACCEL       Accelerator used for PL prediction. As of PL v2.0.8:  auto, cpu, cuda, hpu, ipu, mps, tpu
    PREC        Precision used in PL prediction. PL trainer will convert model+weights to specified prec.
                As of PL v2.0.8:
                ('16-mixed', 'bf16-mixed', '32-true', '64-true', 64, 32, 16, '64', '32', '16', 'bf16')
    MODEL       Path to a .py with MyHyperModel PL model class definition
    CKPT        A PL checkpoint file with weights.
    DATA        The input data must be one of the following:
                * directory
                  Use SonusAI mixture database directory, generate feature and truth data if not found.
                  Run prediction on the feature. The MIXID is required (or default which is *)

                * Single WAV file or glob of WAV files
                  Using the given model, generate feature data and run prediction. A model file must be
                  provided. The MIXID is ignored.

Outputs the following to tpredict-<TIMESTAMP> directory:
    <id>.h5
        dataset:    predict
    torch_predict.log

"""

import signal

from lightning.pytorch.callbacks import BasePredictionWriter


def signal_handler(_sig, _frame):
    import sys

    from sonusai import logger

    logger.info("Canceled due to keyboard interrupt")
    sys.exit(1)


signal.signal(signal.SIGINT, signal_handler)


class CustomWriter(BasePredictionWriter):
    def __init__(self, output_dir, write_interval):
        super().__init__(write_interval)
        self.output_dir = output_dir

    def write_on_epoch_end(self, trainer, pl_module, predictions, batch_indices):
        from os.path import join

        import h5py
        from sonusai import logger

        # this will create N (num processes) files in `output_dir` each containing
        # the predictions of its respective rank
        # torch.save(predictions, os.path.join(self.output_dir, f"predictions_{trainer.global_rank}.pt"))

        # optionally, you can also save `batch_indices` to get the information about the data index
        # from your prediction data
        num_dev = len(batch_indices)
        logger.debug(f"Num dev: {num_dev}, prediction writer global rank: {trainer.global_rank}")
        len_pred = len(predictions)  # for debug, should be num_dev
        logger.debug(f"len predictions: {len_pred}, len batch_indices0 {len(batch_indices[0])}")
        logger.debug(f"Prediction writer batch indices: {batch_indices}")

        logger.info(f"Predictions returned: {len(predictions)}, writing to .h5 files ...")
        for ndi in range(num_dev):  # iterate over list devices (num of batch groups)
            num_batches = len(batch_indices[ndi])  # num batches in dev
            for bi in range(num_batches):  # iterate over list of batches per dev
                bsz = len(batch_indices[ndi][bi])  # batch size
                for di in range(bsz):
                    gid = batch_indices[0][bi][di]
                    # gid = (bgi+1)*bi + bi
                    # gid = bgi + bi
                    logger.debug(f"{ndi}, {bi}, {di}: global id: {gid}")
                    output_name = join(self.output_dir, trainer.predict_dataloaders.dataset.mixdb.mixtures[gid].name)
                    # output_name = join(output_dir, mixdb.mixtures[i].name)
                    pdat = predictions[bi][di, None].cpu().numpy()
                    logger.debug(f"Writing predict shape {pdat.shape} to {output_name}")
                    with h5py.File(output_name, "a") as f:
                        if "predict" in f:
                            del f["predict"]
                        f.create_dataset("predict", data=pdat)

        # output_name = join(self.output_dir,trainer.predict_dataloaders.dataset.mixdb.mixtures[0].name)
        # logger.debug(f'Writing predict shape {pdat.shape} to {output_name}')
        # torch.save(batch_indices, os.path.join(self.output_dir, f"batch_indices_{trainer.global_rank}.pt"))


def main() -> None:
    from docopt import docopt
    from sonusai.utils import trim_docstring

    import sonusai_torchl

    args = docopt(trim_docstring(__doc__), version=sonusai_torchl.__version__, options_first=True)

    verbose = args["--verbose"]
    mixids = args["--mixid"]
    pmeth = args["--pred-method"]
    dlcpu = int(args["--dataloader-cpus"])
    accel = args["--accelerator"]
    num_dev = args["--num-devices"]
    prec = args["--precision"]
    model_path = args["--model"]
    ckpt_path = args["--checkpoint"]
    batch_size = args["--batch"]
    timesteps = args["--tsteps"]
    wavdbg = args["--wavdbg"]  # write .wav if true
    datapaths = args["DATA"]

    from os import makedirs
    from os.path import abspath
    from os.path import basename
    from os.path import isdir
    from os.path import join
    from os.path import normpath
    from os.path import realpath
    from os.path import splitext

    import h5py
    import psutil
    import torch
    from lightning import __version__ as lightning_version
    from lightning.pytorch import Trainer
    from numpy import transpose as np_transpose
    from pyaaware import InverseTransform
    from sonusai import __version__ as sonusai_version
    from sonusai import create_file_handler
    from sonusai import initial_log_messages
    from sonusai import logger
    from sonusai import update_console_handler
    from sonusai.mixture import MixtureDatabase
    from sonusai.mixture import get_audio_from_feature
    from sonusai.mixture import get_feature_from_audio
    from sonusai.mixture import read_audio
    from sonusai.utils import PathInfo
    from sonusai.utils import braced_iglob
    from sonusai.utils import create_ts_name
    from sonusai.utils import write_audio as write_wav
    from torch import __version__ as torch_version
    from torchinfo import summary

    from sonusai_torchl.data_generator import TorchFromMixtureDatabase
    from sonusai_torchl.utils.torchl_utils import torchl_build_model
    from sonusai_torchl.utils.torchl_utils import torchl_hparam_override
    from sonusai_torchl.utils.torchl_utils import torchl_load_ckpt
    from sonusai_torchl.utils.torchl_utils import torchl_load_litmodel

    if batch_size is not None:
        batch_size = int(batch_size)
    if batch_size != 1:
        batch_size = 1
        logger.info("For now prediction only supports batch_size = 1, forcing it to 1 now")

    if timesteps is not None:
        timesteps = int(timesteps)

    # Import checkpoint file first to check
    ckpt, hparams, ckpt_base, ckpt_root = torchl_load_ckpt(ckpt_path)
    # Import model file, expects Sonusai convention of a PL class named MyHyperModel
    litmodel, model_base, model_root = torchl_load_litmodel(model_path)

    mixdb_path = None
    entries: list[PathInfo] = []
    in_basename = ""
    if len(datapaths) == 1 and isdir(datapaths[0]):  # Assume it's a single path to sonusai mixdb subdir
        in_basename = basename(normpath(datapaths[0]))
        mixdb_path = datapaths[0]
        logger.debug(f"Attempting to load mixture database from {mixdb_path}")
        mixdb = MixtureDatabase(mixdb_path)
        logger.debug(f"Sonusai mixture db load success: found {mixdb.num_mixtures} mixtures.")
        p_mixids = mixdb.mixids_to_list(mixids)
    else:  # search all datapaths for .wav, .flac (or whatever is specified in include)
        for p in datapaths:
            location = join(realpath(abspath(p)), "**", "*.{wav,flac}")
            logger.debug(f"Processing {location}")
            for file in braced_iglob(pathname=location, recursive=True):
                name = file
                entries.append(PathInfo(abs_path=file, audio_filepath=name))
        if len(entries) == 0:
            logger.exception("No valid audio files or mixture database input provided. Exiting.")
            raise SystemExit(1)

    output_dir = create_ts_name("tpredict-" + in_basename)
    makedirs(output_dir, exist_ok=True)

    # Setup logging file
    logger.info(f"Created output subdirectory {output_dir}")
    create_file_handler(join(output_dir, "torchl_predict.log"))
    update_console_handler(verbose)
    initial_log_messages("torchl_predict", subprocess=sonusai_version)
    logger.info(f"sonusai_torchl  {sonusai_torchl.__version__}")
    logger.info(f"torch           {torch_version}")
    logger.info(f"lightning       {lightning_version}")
    logger.info(f"Imported model from {model_base}")
    logger.info(f"Loaded checkpoint from {ckpt_base}")

    # Setup dataloader for mixdb or file glob and set prediction mode
    logger.info("")
    if mixdb_path is not None:  # mixdb input, already loaded
        logger.info(f"Sonusai mixture db load success: found {mixdb.num_mixtures} mixtures")
        feature_mode = mixdb.feature  # no choice, must use mixdb feature
        logger.info(f"Mixdb Feature: {feature_mode}")
        sov_mode = False  # Check for stride-overlap mode (SO)
        if hparams["feature"] != mixdb.feature:  # Check mixdb feature, etc. is what model expects
            # if mixdb feature has stride-overlap and model was trained with tsteps dimension
            if 1 < mixdb.fg_info.stride != mixdb.fg_info.step and hparams["timesteps"] > 0:
                # Optional checks probably not necessary:  if hparams['flatten'] is False
                # if int(hparams["feature"][7:])==1 and (hparams["feature"][6]=='s' or hparams["feature"][6]=='d'):
                stride = mixdb.fg_info.stride
                step = mixdb.fg_info.step
                logger.info(f"Detected stride-overlap mode with stride and step of {stride},{step}")
                logger.info(f"for stride-overlap mode, forcing flatten=False and timesteps={stride}.")
                timesteps = stride
                # hparams["timesteps"] = timesteps   # leave for hparam override later
                sov_mode = True
            else:
                logger.warning("Mixture feature does not match model feature, this inference run may fail.")
                # TBD setup for predict loop on list of files

        logger.info(f"- Forward Transform: {mixdb.fg_info.ft_config}")
        logger.info(f"- Inverse Transform: {mixdb.fg_info.it_config}")
        it_config = mixdb.fg_info.it_config
        logger.info(f"- Effective Forward Transform: {mixdb.fg_info.eft_config}")
        logger.info(f"- Feature #parameters: {mixdb.feature_parameters}")
        # Override hyperparameters, changes are typically in batch_size and timesteps,
        hparams, timesteps = torchl_hparam_override(
            hparams, batch_size, timesteps
        )  # return timesteps which returns model status

        sampler = None
        p_datagen = TorchFromMixtureDatabase(
            mixdb=mixdb,
            mixids=p_mixids,
            batch_size=hparams["batch_size"],
            cut_len=0,
            random_cut=False,
            sampler=sampler,
            drop_last=False,
            num_workers=dlcpu,
        )
    else:
        logger.info(f"Found {len(entries)} audio files, no dataloader will be used.")
        pmeth = "pynodl"  # must use Pytorch model in eval mode with no dataloader
        # TBD - maybe have to setup Inv transform ?? fg =, it_config =

    # Setup for audio file debug: inverse transform and audio
    enable_truth_wav = False  # TBD not working
    enable_mix_wav = True
    if wavdbg:
        itf = InverseTransform(
            length=it_config.length,
            overlap=it_config.overlap,
            bin_start=it_config.bin_start,
            bin_end=it_config.bin_end,
            ttype=it_config.ttype,
        )

        if mixdb.target_files[0].truth_settings[0].function == "target_mixture_f":
            enable_mix_wav = True
            enable_truth_wav = True
        elif mixdb.target_files[0].truth_settings[0].function == "target_f":
            enable_truth_wav = False

    # Build model, updates hparams for missing SonusAI params (need for model prediction feature gen compatibility)
    model, hparams = torchl_build_model(litmodel, hparams, training=False, ckpt=ckpt)
    model.eval()
    logger.info("")
    logger.info(summary(model, input_size=tuple([batch_size] + model.input_shape)))
    logger.info("")
    logger.info(f"feature       {model.hparams.feature}")
    logger.info(f"batch_size    {model.hparams.batch_size}")
    logger.info(f"timesteps     {model.hparams.timesteps}")
    logger.info(f"flatten       {model.flatten}")
    logger.info(f"add1ch        {model.add1ch}")
    logger.info(f"truth_mutex   {model.truth_mutex}")
    logger.info(f"num_classes   {model.num_classes}")
    logger.info(f"input_shape   {model.input_shape}")
    logger.info(f"Model default device {model.device}")
    num_cpu = psutil.cpu_count()
    cpu_percent = psutil.cpu_percent(interval=1)
    logger.info(f"#CPUs: {num_cpu}, current CPU utilization: {cpu_percent}%")
    logger.info(f"Memory utilization: {psutil.virtual_memory().percent}%")
    if torch.cuda.is_available():
        logger.info(torch.cuda.get_device_name(0))
        logger.info(f"Total Memory: {round(torch.cuda.get_device_properties(0).total_memory / 1024 ** 3, 1)}GB")
        logger.info(f"Allocated: {round(torch.cuda.memory_allocated(0) / 1024 ** 3, 1)}GB")
        logger.info(f"Cached: {round(torch.cuda.memory_reserved(0) / 1024 ** 3, 1)}GB")
        if accel == "auto" or "cuda":
            device_use = "cuda"
    else:
        logger.info("No cuda devices present, using cpu")
        device_use = "cpu"
        if num_dev == "auto":
            use_cpu = int(num_cpu * (0.9 - cpu_percent / 100))  # default use 80% of available cpus
        else:
            use_cpu = min(max(int(num_dev), 1), num_cpu)
        # Inter-op parallelism setting
        torch.set_num_interop_threads(use_cpu)
        # Intra-op parallelism setting
        torch.set_num_threads(use_cpu)
        logger.info(f"Setting torch to use {use_cpu} threads.")

    logger.info("")

    if pmeth == "pydlen":
        device = model.device
        if sov_mode:
            logger.info(f"Running {len(p_mixids)} mixtures with stride-overlap feature and dataloader enumeration ...")
        else:
            logger.info(f"Running {len(p_mixids)} mixtures with dataloader enumeration ...")

        for idx, val in enumerate(p_datagen):
            # truth = val[1]   # batch x frames x bin (w/reduction) or batch x frames x stride x bins (wo/reduction)
            feat_dat = val[0].to(device)
            batchidx = val[2]  # vector of length batch
            nframes = val[0].shape[1]  # nframes from val[0]=feature data [batch x frames x stride x bins]
            # TBD loop through batches
            mixidx = p_mixids[batchidx[0]]
            if sov_mode:
                feat_dat = torch.reshape(feat_dat, (batch_size * nframes, stride, mixdb.feature_parameters))

            # Hack for mag/pha stack until added to Sonusai
            magpha_special = True
            if magpha_special:
                bins = feat_dat.shape[-1] // 2
                real = feat_dat[..., :bins].unsqueeze(1)  # [batch,1,tstep,bins]
                imag = feat_dat[..., bins:].unsqueeze(1)  # [batch,1,tstep,bins]
                mix_mag = torch.sqrt(real**2 + imag**2)  # [batch,1,tstep,bins]
                mix_pha = torch.atan2(imag, real)
                feat_dat = torch.cat([mix_mag, mix_pha], -1).squeeze(1)  # stack mag, phase in -1 fp dim

            # Prediction with model in eval mode, input and output either [b,t,fp] or [b,fp]
            with torch.no_grad():
                ypred = model(feat_dat)

            if isinstance(ypred, tuple):  # Sonusai convention only support first output
                ypred = ypred[0]

            if sov_mode:
                ypred = ypred[:, step:, :]  # trim older overlap
                # reshape back to (batch, frames, step, bins)  then batch x tsteps x bins
                ypred = torch.reshape(ypred, (batch_size, nframes, step, mixdb.feature_parameters))
                ypred = torch.reshape(ypred, (batch_size, nframes * step, mixdb.feature_parameters))

            output_name = join(output_dir, mixdb.mixtures[mixidx].name)
            pdat = ypred.cpu().detach().numpy()  # batch x tsteps x num_classes  or  batch x num_classes
            if timesteps > 0:
                logger.debug(f"In and out tsteps: {feat_dat.shape[1]},{pdat.shape[1]}")
            logger.debug(f"Writing predict shape {pdat.shape} to {output_name}")
            with h5py.File(output_name, "a") as f:
                if "predict" in f:
                    del f["predict"]
                f.create_dataset("predict", data=pdat)

            if wavdbg:
                owav_base = splitext(output_name)[0]
                # Method1: predict_audio wants numpy [frames, channels, feature_parameters] equiv. to tsteps, batch, fp
                # Specified directly from feature name and has builtin unstack() and uncompress()
                pdat = np_transpose(pdat, [1, 0, 2])
                # Use model feature even when dataloader might be in stride-overlap feature mode
                predict_audio = get_audio_from_feature(feature=pdat, feature_mode=hparams["feature"])
                write_wav(owav_base + "_pred.wav", predict_audio, 16000)

                # # Method2: This method doesn't work when itf is TorchInverseTransform shape problems no matter how tmp gets shaped
                # inv transform is possible, unstack and [b,tstep,bins] -> [frames,bins] where batch_size=1
                # tmp = torch.complex(ypred[..., :itf.bins], ypred[..., itf.bins:]).permute(1,2,0).squeeze(2).detach()
                # predwav, _ = get_audio_from_transform(tmp,itf,trim=True )

                # # Method3: Works using Pyaaware TorchInverseTransform:
                # tmp = power_uncompress(ypred[..., :itf.bins], ypred[..., itf.bins:])   # ... ,2  where in is B,T,FP
                # tmp = torch.complex(tmp[...,0], tmp[...,1]).permute(2, 0, 1).detach()  #
                # itf.reset()
                # predwav, _ = itf.execute_all(tmp)
                # write_wav(owav_base + '.wav', predwav.permute([1, 0]).numpy(), 16000)

                if enable_mix_wav:
                    if sov_mode:  # feat_dat will be batch,tsteps,bins*2 needs to be 1,tsteps,bins*2
                        feat_dat = torch.reshape(
                            feat_dat[:, step:, :], (batch_size, nframes, step, mixdb.feature_parameters)
                        )
                        # reshape back to (batch, frames, step, bins)  then 1 x tsteps x 2*bins
                        feat_dat = torch.reshape(feat_dat, (batch_size, nframes, step, mixdb.feature_parameters))
                        feat_dat = torch.reshape(feat_dat, (batch_size, nframes * step, mixdb.feature_parameters))

                    # predict_audio wants numpy [frames, channels, feature_parameters] equiv. to tsteps, batch, fp
                    feat_dat = feat_dat.permute(1, 0, 2).cpu().detach().numpy()
                    predict_audio = get_audio_from_feature(feature=feat_dat, feature_mode=hparams["feature"])
                    write_wav(owav_base + "_mix.wav", predict_audio, 16000)

                if enable_truth_wav:  # TBD not working
                    # Check truth[0] type for target_f or target_mixture_f (support inv transform)
                    if mixdb.target_files[0].truth_settings[0].function == "target_mixture_f" or "target_f":
                        # Also for features with stride, the truth reduction function needs to be None for itf to make sense
                        # TBD if mixdb.target_files[0].truth_settings[0].reduction
                        # truth = val[1] is batch x frames x bin (w/reduction) or batch x frames x stride x bins (wo/reduction)
                        truth_dat = torch.reshape(val[1], (batch_size * nframes, stride, mixdb.feature_parameters))
                        tmp = (
                            torch.complex(val[0][..., : itf.bins], val[0][..., itf.bins : 2 * itf.bins])
                            .permute(2, 0, 1)
                            .detach()
                        )
                        itf.reset()
                        truthwav, _ = itf.execute_all(tmp)
                        write_wav(owav_base + "_truth.wav", truthwav.permute([1, 0]).numpy(), 16000)
                    else:
                        logger.info(f"Truth[0] does not support inverse transform, ignoring for {owav_base} ...")

    elif pmeth == "plstep":
        # Use model predict step and lightning prediction logic
        logger.info(f"Running {len(p_mixids)} mixtures with model builtin prediction loop ...")
        # PL logic returns a list to write_on_epoch in pred_writer, writes all files after entire epoch is run
        pred_writer = CustomWriter(output_dir=output_dir, write_interval="epoch")
        trainer = Trainer(
            default_root_dir=output_dir, callbacks=[pred_writer], precision=prec, devices="auto", accelerator=accel
        )  # prints avail GPU, TPU, IPU, HPU and selected device
        # logger.info(f'Strategy: {trainer.strategy.strategy_name}')  # doesn't work for ddp strategy
        logger.info(f"Accelerator stats: {trainer.accelerator.get_device_stats(device=None)}")
        logger.info(f"World size: {trainer.world_size}")
        logger.info(f"Nodes: {trainer.num_nodes}")
        logger.info(f"Devices: {trainer.accelerator.auto_device_count()}")

        # Use builtin lightning prediction loop, returns a list
        # predictions = trainer.predict(model, p_datagen)  # standard method, but no support distributed
        with torch.no_grad():
            trainer.predict(model, p_datagen)

        logger.info(f"Saved results to {output_dir}")

    elif pmeth == "pynodl":
        # File glob data input so no mixdb or dataloader available, iterate through list using manual transforms
        model_feature = hparams["feature"]
        logger.info(f"Running prediction on {len(entries)} audio files, with model feature {model_feature}")
        for file in entries:
            # Convert audio to feature data
            audio_in = read_audio(file)
            feature = get_feature_from_audio(audio=audio_in, feature_mode=model_feature)

            with torch.no_grad():
                predict = model(torch.tensor(feature))

            audio_out = get_audio_from_feature(feature=predict.numpy(), feature_mode=model.hparams.feature)

            output_name = join(output_dir, splitext(basename(file))[0] + ".h5")
            with h5py.File(output_name, "a") as f:
                if "audio_in" in f:
                    del f["audio_in"]
                f.create_dataset(name="audio_in", data=audio_in)

                if "feature" in f:
                    del f["feature"]
                f.create_dataset(name="feature", data=feature)

                if "predict" in f:
                    del f["predict"]
                f.create_dataset(name="predict", data=predict)

                if "audio_out" in f:
                    del f["audio_out"]
                f.create_dataset(name="audio_out", data=audio_out)

            output_name = join(output_dir, splitext(basename(file))[0] + "_predict.wav")
            write_wav(output_name, audio_out, 16000)

        logger.info(f"Saved results to {output_dir}")
        del model

    return


if __name__ == "__main__":
    main()
