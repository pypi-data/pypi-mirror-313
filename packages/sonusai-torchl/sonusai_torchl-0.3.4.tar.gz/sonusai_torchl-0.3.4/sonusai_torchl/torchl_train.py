"""sonusai torchl_train

usage: torchl_train [-hgv] (-m MODEL) (-l VLOC) [-w WEIGHTS] [-k CKPT]
                    [-e EPOCHS] [-b BATCH] [-t TSTEPS] [-p ESP] TLOC

options:
    -h, --help
    -v, --verbose                   Be verbose.
    -m MODEL, --model MODEL         Python .py file with MyHyperModel custom PL class definition.
    -l VLOC, --vloc VLOC            Location of SonusAI mixture database to use for validation.
    -w WEIGHTS, --weights WEIGHTS   Optional PL checkpoint file for initializing model weights.
    -k CKPT, --ckpt CKPT            Optional PL checkpoint file for full resume of training.
    -e EPOCHS, --epochs EPOCHS      Number of epochs to use in training. [default: 8].
    -b BATCH, --batch BATCH         Batch size.
    -t TSTEPS, --tsteps TSTEPS      Timesteps.
    -p ESP, --patience ESP          Early stopping patience. [default: 12]
    -g, --loss-batch-log            Enable per-batch loss log. [default: False]

Train a Pytorch Lightning model defined in MODEL .py using SonusAI mixture data in TLOC.

Inputs:
    TLOC    A SonusAI mixture database directory to use for training data.
    VLOC    A SonusAI mixture database directory to use for validation data.

Results are written into subdirectory <MODEL>-<TIMESTAMP>.
Per-batch loss history, if enabled, is written to <basename>-history-lossb.npy

"""

import signal


def signal_handler(_sig, _frame):
    import sys

    from sonusai import logger

    logger.info("Canceled due to keyboard interrupt")
    sys.exit(1)


signal.signal(signal.SIGINT, signal_handler)


def main() -> None:
    from docopt import docopt
    from sonusai.utils import trim_docstring

    import sonusai_torchl

    args = docopt(trim_docstring(__doc__), version=sonusai_torchl.__version__, options_first=True)

    verbose = args["--verbose"]
    model_path = args["--model"]
    weights_name = args["--weights"]
    ckpt_path = args["--ckpt"]
    v_name = args["--vloc"]
    epochs = int(args["--epochs"])
    batch_size = args["--batch"]
    timesteps = args["--tsteps"]
    esp = int(args["--patience"])
    loss_batch_log = args["--loss-batch-log"]
    t_name = args["TLOC"]
    use_speaker_id_loader = False

    from os import makedirs
    from os.path import join

    from lightning import __version__ as lightning_version
    from lightning.pytorch import Trainer
    from lightning.pytorch.callbacks import EarlyStopping
    from lightning.pytorch.callbacks import ModelCheckpoint
    from lightning.pytorch.loggers import TensorBoardLogger
    from lightning.pytorch.profilers import AdvancedProfiler
    from pytorch_lightning.loggers.csv_logs import CSVLogger
    from sonusai import __version__ as sonusai_version
    from sonusai import create_file_handler
    from sonusai import initial_log_messages
    from sonusai import logger
    from sonusai import update_console_handler
    from sonusai.mixture import MixtureDatabase
    from sonusai.utils import create_ts_name
    from torch import __version__ as torch_version
    from torchinfo import summary

    from sonusai_torchl.data_generator import TorchFromMixtureDatabase
    from sonusai_torchl.data_generator import TorchFromSpeakerIDMixtureDatabase
    from sonusai_torchl.utils.torchl_utils import torchl_build_model
    from sonusai_torchl.utils.torchl_utils import torchl_hparam_override
    from sonusai_torchl.utils.torchl_utils import torchl_load_ckpt
    from sonusai_torchl.utils.torchl_utils import torchl_load_litmodel

    # Import model file first to check, expects Sonusai convention of a PL class named MyHyperModel
    litmodel, model_base, model_root = torchl_load_litmodel(model_path)

    if batch_size is not None:
        batch_size = int(batch_size)

    if timesteps is not None:
        timesteps = int(timesteps)

    if ckpt_path is not None:
        ckpt, hparams, ckpt_base, ckpt_root = torchl_load_ckpt(ckpt_path)

    # Setup logging file and print initial messages
    output_dir = create_ts_name(model_root)
    makedirs(output_dir, exist_ok=True)
    base_name = join(output_dir, model_root)

    logger.info(f"Created output subdirectory {output_dir}")
    create_file_handler(join(output_dir, "torchl_train.log"))
    update_console_handler(verbose)
    initial_log_messages(f"torchl_train {sonusai_torchl.__version__}", subprocess=sonusai_version)
    logger.info(f"sonusai_torchl  {sonusai_torchl.__version__}")
    logger.info(f"torch           {torch_version}")
    logger.info(f"lightning       {lightning_version}")
    logger.info(f"Imported model from {model_base}")

    if ckpt_path is not None:
        logger.info(f"Loading full checkpoint and will resume training from {ckpt_base}")
        # Override hyperparameters, changes are typically in batch_size and timesteps,
        hparams, timesteps = torchl_hparam_override(
            hparams, batch_size, timesteps
        )  # return timesteps which returns model status
        logger.info(f'Building model with batch_size={hparams["batch_size"]}, timesteps={hparams["timesteps"]}')
        model, hparams = torchl_build_model(litmodel, hparams, training=True, ckpt=ckpt)

        # TODO: this is broken... 'training' is not defined
        hparams["training"] = training  # SonusAI convention to ignore training-only objects like GAN and loss models
        model, hparams = litmodel.MyHyperModel(**hparams)
    else:
        if batch_size is not None:
            model = litmodel.MyHyperModel(batch_size=batch_size)
        else:
            model = litmodel.MyHyperModel()  # build model using its default hyperparameters

    if verbose:
        logger.info("")
        logger.info(summary(model, depth=8, input_size=tuple([batch_size] + model.input_shape)))
    logger.info("")
    logger.info(f"feature       {model.hparams.feature}")
    logger.info(f"input_shape   {model.input_shape}")
    logger.info(f"batch_size    {batch_size}")
    logger.info(f"timesteps     {model.hparams.timesteps}")
    logger.info("")

    t_mixdb = MixtureDatabase(t_name)
    logger.info(f"Training: found {t_mixdb.num_mixtures} mixtures with {t_mixdb.num_classes} classes from {t_name}")

    v_mixdb = MixtureDatabase(v_name)
    logger.info(f"Validation: found {v_mixdb.num_mixtures} mixtures with {v_mixdb.num_classes} classes from {v_name}")

    t_mixid = t_mixdb.mixids_to_list()
    v_mixid = v_mixdb.mixids_to_list()

    # Use SonusAI DataGenerator to create validation feature/truth on the fly
    sampler = None  # TBD how to stratify, also see stratified_shuffle_split_mixid(t_mixdb, vsplit=0)
    if use_speaker_id_loader:
        t_datagen = TorchFromSpeakerIDMixtureDatabase(
            mixdb=t_mixdb,
            mixids=t_mixid,
            utterances=model.m_utt,
            speakers=model.n_spkr,
            cut_len=model.hparams.timesteps,
            drop_last=False,
            shuffle=False,
            random_cut=True,
            random_utterance=False,
            sampler=sampler,
            pin_memory=False,
            num_workers=4,
        )

        v_datagen = TorchFromSpeakerIDMixtureDatabase(
            mixdb=v_mixdb,
            mixids=v_mixid,
            utterances=model.m_utt,  # must be same as training dataset
            speakers=8,
            cut_len=640,
            drop_last=False,
            shuffle=False,
            random_cut=True,
            random_utterance=False,
            sampler=sampler,
            pin_memory=False,
            num_workers=4,
        )
    else:
        t_datagen = TorchFromMixtureDatabase(
            mixdb=t_mixdb,
            mixids=t_mixid,
            batch_size=model.hparams.batch_size,
            cut_len=model.hparams.timesteps,
            random_cut=True,
            sampler=sampler,
            drop_last=True,
            num_workers=4,
        )

        v_datagen = TorchFromMixtureDatabase(
            mixdb=v_mixdb,
            mixids=v_mixid,
            batch_size=1,
            cut_len=0,
            random_cut=False,
            sampler=sampler,
            drop_last=True,
            num_workers=0,
        )

    csvl = CSVLogger(output_dir, name="logs", version="")
    tbl = TensorBoardLogger(output_dir, "logs", "", log_graph=True, default_hp_metric=False)
    es_cb = EarlyStopping(monitor="val_loss", min_delta=0.00, patience=esp, verbose=False, mode="min")
    ckpt_topv = ModelCheckpoint(
        dirpath=output_dir + "/ckpt/",
        save_top_k=5,
        monitor="val_loss",
        mode="min",
        filename=model_root + "-{epoch:03d}-{val_loss:.3g}",
    )
    # lr_monitor = LearningRateMonitor(logging_interval="step")
    ckpt_last = ModelCheckpoint(dirpath=output_dir + "/ckpt/", save_last=True)
    # lr_monitor = LearningRateMonitor(logging_interval="step")
    # callbacks = [ModelSummary(max_depth=2), ckpt_topv, es_cb, ckpt_last]  # , lr_monitor]
    callbacks = [ckpt_topv, es_cb, ckpt_last]  # , lr_monitor]

    profiler = None  # 'advanced'
    if profiler == "advanced":
        profiler = AdvancedProfiler(dirpath=output_dir, filename="perf_logs")
    else:
        profiler = None

    if weights_name is not None and ckpt_path is None:
        # TODO: needs fix and to make sure this only loads weights... 'torchl_module' is not defined
        logger.info(f"Loading weights from {weights_name}")
        model = torchl_module.MyHyperModel.load_from_checkpoint(
            weights_name,
            feature=t_mixdb.feature,
            # num_classes=t_mixdb.num_classes,
            timesteps=timesteps,
            batch_size=batch_size,
        )

    # if ckpt_name is not None:
    #     logger.info(f'Loading full checkpoint and resuming training from {ckpt_name}')
    #     ckpt_path = ckpt_name
    # else:
    #     ckpt_path = None

    logger.info(f"Starting training with max epoch {epochs} and early stopping patience = {esp} ...")
    logger.info("")

    trainer = Trainer(
        max_epochs=epochs,
        default_root_dir=output_dir,
        logger=[tbl, csvl],
        log_every_n_steps=100,
        profiler=profiler,
        # detect_anomaly=True,
        # precision='16',
        # accelerator="cpu",
        # devices=4,
        callbacks=callbacks,
    )
    trainer.fit(model, t_datagen, v_datagen, ckpt_path=ckpt_path)


if __name__ == "__main__":
    main()
