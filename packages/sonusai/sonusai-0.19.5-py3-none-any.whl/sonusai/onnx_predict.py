"""sonusai onnx_predict

usage: onnx_predict [-hvlwr] [--include GLOB] [-i MIXID] MODEL DATA ...

options:
    -h, --help
    -v, --verbose               Be verbose.
    -i MIXID, --mixid MIXID     Mixture ID(s) to generate if input is a mixture database. [default: *].
    --include GLOB              Search only files whose base name matches GLOB. [default: *.{wav,flac}].
    -w, --write-wav             Calculate inverse transform of prediction and write .wav files

Run prediction (inference) using an ONNX model on a SonusAI mixture dataset or audio files from a glob path.
The ONNX Runtime (ort) inference engine is used to execute the inference.

Inputs:
    MODEL       ONNX model .onnx file of a trained model (weights are expected to be in the file).

    DATA        The input data must be one of the following:
                * WAV
                  Using the given model, generate feature data and run prediction. A model file must be
                  provided. The MIXID is ignored.

                * directory
                  Using the given SonusAI mixture database directory, generate feature and truth data if not found.
                  Run prediction. The MIXID is required.


Note there are multiple ways to process model prediction over multiple audio data files:
1. TSE (timestep single extension): mixture transform frames are fit into the timestep dimension and the model run as
   a single inference call.  If batch_size is > 1 then run multiple mixtures in one call with shorter mixtures
   zero-padded to the size of the largest mixture.
2. TME (timestep multi-extension): mixture is split into multiple timesteps, i.e. batch[0] is starting timesteps, ...
   Note that batches are run independently, thus sequential state from one set of timesteps to the next will not be
   maintained, thus results for such models (i.e. conv, LSTMs, in the timestep dimension) would not match using
   TSE mode.

TBD not sure below make sense, need to continue ??
2. BSE (batch single extension): mixture transform frames are fit into the batch dimension. This make sense only if
   independent predictions are made on each frame w/o considering previous frames (timesteps=1) or there is no
   timestep dimension in the model (timesteps=0).
3. Classification

Outputs the following to opredict-<TIMESTAMP> directory:
    <id>
        predict.pkl
    onnx_predict.log

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

    import sonusai
    from sonusai.utils import trim_docstring

    args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

    verbose = args["--verbose"]
    wav = args["--write-wav"]
    mixids = args["--mixid"]
    include = args["--include"]
    model_path = args["MODEL"]
    data_paths = args["DATA"]

    from os import makedirs
    from os.path import abspath
    from os.path import basename
    from os.path import isdir
    from os.path import join
    from os.path import normpath
    from os.path import realpath
    from os.path import splitext

    import h5py
    import numpy as np
    import onnxruntime as ort

    from sonusai import create_file_handler
    from sonusai import initial_log_messages
    from sonusai import logger
    from sonusai import update_console_handler
    from sonusai.mixture import MixtureDatabase
    from sonusai.mixture import get_audio_from_feature
    from sonusai.utils import PathInfo
    from sonusai.utils import braced_iglob
    from sonusai.utils import create_ts_name
    from sonusai.utils import load_ort_session
    from sonusai.utils import reshape_inputs
    from sonusai.utils import write_audio

    mixdb_path = None
    mixdb: MixtureDatabase | None = None
    p_mixids: list[int] = []
    entries: list[PathInfo] = []

    if len(data_paths) == 1 and isdir(data_paths[0]):
        # Assume it's a single path to SonusAI mixdb subdir
        in_basename = basename(normpath(data_paths[0]))
        mixdb_path = data_paths[0]
    else:
        # search all data paths for .wav, .flac (or whatever is specified in include)
        in_basename = ""

    output_dir = create_ts_name("opredict-" + in_basename)
    makedirs(output_dir, exist_ok=True)

    # Setup logging file
    create_file_handler(join(output_dir, "onnx-predict.log"))
    update_console_handler(verbose)
    initial_log_messages("onnx_predict")

    providers = ort.get_available_providers()
    logger.info(f"Loaded ONNX Runtime, available providers: {providers}.")

    session, options, model_root, hparams, sess_inputs, sess_outputs = load_ort_session(model_path)
    if hparams is None:
        logger.error("Error: ONNX model does not have required SonusAI hyperparameters, cannot proceed.")
        raise SystemExit(1)
    if len(sess_inputs) != 1:
        logger.error(f"Error: ONNX model does not have 1 input, but {len(sess_inputs)}. Exit due to unknown input.")

    in0name = sess_inputs[0].name
    in0type = sess_inputs[0].type
    out_names = [n.name for n in session.get_outputs()]

    logger.info(f"Read and compiled ONNX model from {model_path}.")

    if mixdb_path is not None:
        # Assume it's a single path to SonusAI mixdb subdir
        logger.debug(f"Attempting to load mixture database from {mixdb_path}")
        mixdb = MixtureDatabase(mixdb_path)
        logger.info(f"SonusAI mixdb: found {mixdb.num_mixtures} mixtures with {mixdb.num_classes} classes")
        p_mixids = mixdb.mixids_to_list(mixids)
        if len(p_mixids) != mixdb.num_mixtures:
            logger.info(f"Processing a subset of {p_mixids} from available mixtures.")
    else:
        for p in data_paths:
            location = join(realpath(abspath(p)), "**", include)
            logger.debug(f"Processing {location}")
            for file in braced_iglob(pathname=location, recursive=True):
                name = file
                entries.append(PathInfo(abs_path=file, audio_filepath=name))
        logger.info(f"{len(data_paths)} data paths specified, found {len(entries)} audio files.")

    if in0type.find("float16") != -1:
        model_is_fp16 = True
        logger.info("Detected input of float16, converting all feature inputs to that type.")
    else:
        model_is_fp16 = False

    if mixdb is not None and hparams["batch_size"] == 1:
        # mixdb input
        # Assume (of course) that mixdb feature, etc. is what model expects
        if hparams["feature"] != mixdb.feature:
            logger.warning("Mixture feature does not match model feature, this inference run may fail.")
        # no choice, can't use hparams.feature since it's different from the mixdb
        feature_mode = mixdb.feature

        for mixid in p_mixids:
            # frames x stride x feature_params
            feature, _ = mixdb.mixture_ft(mixid)
            if hparams["timesteps"] == 0:
                # no timestep dimension, reshape will handle
                timesteps = 0
            else:
                # fit frames into timestep dimension (TSE mode)
                timesteps = feature.shape[0]

            feature, _ = reshape_inputs(
                feature=feature,
                batch_size=1,
                timesteps=timesteps,
                flatten=hparams["flatten"],
                add1ch=hparams["add1ch"],
            )
            if model_is_fp16:
                feature = np.float16(feature)  # type: ignore[assignment]
            # run inference, ort session wants i.e. batch x timesteps x feat_params, outputs numpy BxTxFP or BxFP
            predict = session.run(out_names, {in0name: feature})[0]
            # predict, _ = reshape_outputs(predict=predict[0], timesteps=frames)  # frames x feat_params
            output_fname = join(output_dir, mixdb.mixtures[mixid].name)
            with h5py.File(output_fname, "a") as f:
                if "predict" in f:
                    del f["predict"]
                f.create_dataset("predict", data=predict)
            if wav:
                # note only makes sense if model is predicting audio, i.e., timestep dimension exists
                # predict_audio wants [frames, channels, feature_parameters] equivalent to timesteps, batch, bins
                predict = np.transpose(predict, [1, 0, 2])
                predict_audio = get_audio_from_feature(feature=predict, feature_mode=feature_mode)
                owav_name = splitext(output_fname)[0] + "_predict.wav"
                write_audio(owav_name, predict_audio)


if __name__ == "__main__":
    main()
