"""sonusai plot

usage: plot [-hve] [-i MIXID] [-m MODEL] [-l CSV] [-o OUTPUT] INPUT

options:
    -h, --help
    -v, --verbose               Be verbose.
    -i MIXID, --mixid MIXID     Mixture to plot if input is a mixture database.
    -m MODEL, --model MODEL     Trained model ONNX file.
    -l CSV, --labels CSV        Optional CSV file of class labels (from SonusAI gentcst).
    -o OUTPUT, --output OUTPUT  Optional output HDF5 file for prediction.
    -e, --energy                Use energy plots.

Plot SonusAI audio, feature, truth, and prediction data. INPUT must be one of the following:

    * WAV
      Using the given model, generate feature data and run prediction. A model file must be
      provided. The MIXID is ignored. If --energy is specified, plot predict data as energy.

    * directory
      Using the given SonusAI mixture database directory, generate feature and truth data if not found.
      Run prediction if a model is given. The MIXID is required. (--energy is ignored.)

Prediction data will be written to OUTPUT if a model file is given and OUTPUT is specified.

There will be one plot per active truth index. In addition, the top 5 prediction classes are determined and
plotted if needed (i.e., if they were not already included in the truth plots). For plots generated using a
mixture database, then the target will also be displayed. If mixup is active, then each target involved will
be added to the corresponding truth plot.

Inputs:
    MODEL   A SonusAI trained ONNX model file. If a model file is given, prediction data will be
            generated.
    INPUT   A WAV file, or
            a directory containing a SonusAI mixture database

Outputs:
    {INPUT}-plot.pdf or {INPUT}-mix{MIXID}-plot.pdf
    plot.log
    OUTPUT (if MODEL and OUTPUT are both specified)

"""

import signal

import numpy as np
from matplotlib import pyplot as plt

from sonusai.mixture import AudioT
from sonusai.mixture import Feature
from sonusai.mixture import Predict
from sonusai.mixture import Truth


def signal_handler(_sig, _frame):
    import sys

    from sonusai import logger

    logger.info("Canceled due to keyboard interrupt")
    sys.exit(1)


signal.signal(signal.SIGINT, signal_handler)


def spec_plot(
    mixture: AudioT,
    feature: Feature,
    predict: Predict | None = None,
    target: AudioT | None = None,
    labels: list[str] | None = None,
    title: str = "",
) -> plt.Figure:
    from sonusai.mixture import SAMPLE_RATE

    num_plots = 4 if predict is not None else 2
    fig, ax = plt.subplots(num_plots, 1, constrained_layout=True, figsize=(11, 8.5))

    # Plot the waveform
    x_axis = np.arange(len(mixture), dtype=np.float32) / SAMPLE_RATE
    ax[0].plot(x_axis, mixture, label="Mixture")
    ax[0].set_xlim(x_axis[0], x_axis[-1])
    ax[0].set_ylim([-1.025, 1.025])
    if target is not None:
        # Plot target time-domain waveform on top of mixture
        color = "tab:blue"
        ax[0].plot(x_axis, target, color=color, label="Target")
        ax[0].set_ylabel("magnitude", color=color)
    ax[0].set_title("Waveform")

    # Plot the spectrogram
    ax[1].imshow(np.transpose(feature), aspect="auto", interpolation="nearest", origin="lower")
    ax[1].set_title("Feature")

    if predict is not None:
        if labels is None:
            raise ValueError("Provided predict without labels")

        # Plot and label the model output scores for the top-scoring classes.
        mean_predict = np.mean(predict, axis=0)
        num_classes = predict.shape[-1]
        top_n = min(10, num_classes)
        top_class_indices = np.argsort(mean_predict)[::-1][:top_n]
        ax[2].imshow(
            np.transpose(predict[:, top_class_indices]),
            aspect="auto",
            interpolation="nearest",
            cmap="gray_r",
        )
        y_ticks = range(0, top_n)
        ax[2].set_yticks(y_ticks, [labels[top_class_indices[x]] for x in y_ticks])
        ax[2].set_ylim(-0.5 + np.array([top_n, 0]))
        ax[2].set_title("Class Scores")

        # Plot the probabilities
        ax[3].plot(predict[:, top_class_indices])
        ax[3].legend(np.array(labels)[top_class_indices], loc="best")
        ax[3].set_title("Class Probabilities")

    fig.suptitle(title)

    return fig


def spec_energy_plot(
    mixture: AudioT, feature: Feature, truth_f: Truth | None = None, predict: Predict | None = None
) -> plt.Figure:
    from sonusai.mixture import SAMPLE_RATE

    num_plots = 2
    if truth_f is not None:
        num_plots += 1
    if predict is not None:
        num_plots += 1

    fig, ax = plt.subplots(num_plots, 1, constrained_layout=True, figsize=(11, 8.5))

    # Plot the waveform
    p = 0
    x_axis = np.arange(len(mixture), dtype=np.float32) / SAMPLE_RATE
    ax[p].plot(x_axis, mixture, label="Mixture")
    ax[p].set_xlim(x_axis[0], x_axis[-1])
    ax[p].set_ylim([-1.025, 1.025])
    ax[p].set_title("Waveform")

    # Plot the spectrogram
    p += 1
    ax[p].imshow(np.transpose(feature), aspect="auto", interpolation="nearest", origin="lower")
    ax[p].set_title("Feature")

    if truth_f is not None:
        p += 1
        ax[p].imshow(
            np.transpose(truth_f),
            aspect="auto",
            interpolation="nearest",
            origin="lower",
        )
        ax[p].set_title("Truth")

    if predict is not None:
        p += 1
        ax[p].imshow(
            np.transpose(predict),
            aspect="auto",
            interpolation="nearest",
            origin="lower",
        )
        ax[p].set_title("Predict")

    return fig


def class_plot(
    mixture: AudioT,
    target: AudioT | None = None,
    truth_f: Truth | None = None,
    predict: Predict | None = None,
    label: str = "",
) -> plt.Figure:
    """Plot mixture waveform with optional prediction and/or truth together in a single plot

    The target waveform can optionally be provided, and prediction and truth can have multiple classes.

    Inputs:
      mixture       required, numpy array [samples, 1]
      target        optional, list of numpy arrays [samples, 1]
      truth_f       optional, numpy array [frames, 1]
      predict       optional, numpy array [frames, 1]
      label         optional, label name to use when plotting

    """
    from sonusai import SonusAIError
    from sonusai.mixture import SAMPLE_RATE

    if mixture.ndim != 1:
        raise SonusAIError("Too many dimensions in mixture")

    if target is not None and target.ndim != 1:
        raise SonusAIError("Too many dimensions in target")

    # Set default to 1 frame when there is no truth or predict data
    frames = 1
    if truth_f is not None and predict is not None:
        if truth_f.ndim != 1:
            raise SonusAIError("Too many dimensions in truth_f")
        t_frames = len(truth_f)

        if predict.ndim != 1:
            raise SonusAIError("Too many dimensions in predict")
        p_frames = len(predict)

        frames = min(t_frames, p_frames)
    elif truth_f is not None:
        if truth_f.ndim != 1:
            raise SonusAIError("Too many dimensions in truth_f")
        frames = len(truth_f)
    elif predict is not None:
        if predict.ndim != 1:
            raise SonusAIError("Too many dimensions in predict")
        frames = len(predict)

    samples = (len(mixture) // frames) * frames

    # x-axis in sec
    x_axis = np.arange(samples, dtype=np.float32) / SAMPLE_RATE

    fig, ax = plt.subplots(1, 1, constrained_layout=True, figsize=(11, 8.5))

    # Plot the time-domain waveforms then truth/prediction on second axis
    ax.plot(x_axis, mixture[0:samples], color="mistyrose", label="Mixture")
    color = "red"
    ax.set_xlim(x_axis[0], x_axis[-1])
    ax.set_ylim((-1.025, 1.025))
    ax.set_ylabel("Amplitude", color=color)
    ax.tick_params(axis="y", labelcolor=color)

    # Plot target time-domain waveform
    if target is not None:
        ax.plot(x_axis, target[0:samples], color="blue", label="Target")

    # instantiate 2nd y-axis that shares the same x-axis
    if truth_f is not None or predict is not None:
        y_label = "Truth/Predict"
        if truth_f is None:
            y_label = "Predict"
        if predict is None:
            y_label = "Truth"

        ax2 = ax.twinx()

        color = "black"
        ax2.set_xlim(x_axis[0], x_axis[-1])
        ax2.set_ylim((-0.025, 1.025))
        ax2.set_ylabel(y_label, color=color)
        ax2.tick_params(axis="y", labelcolor=color)

        if truth_f is not None:
            ax2.plot(
                x_axis,
                expand_frames_to_samples(truth_f, samples),
                color="green",
                label="Truth",
            )

        if predict is not None:
            ax2.plot(
                x_axis,
                expand_frames_to_samples(predict, samples),
                color="brown",
                label="Predict",
            )

    # set only on last/bottom plot
    ax.set_xlabel("time (s)")

    fig.suptitle(label)

    return fig


def expand_frames_to_samples(x: np.ndarray, samples: int) -> np.ndarray:
    samples_per_frame = samples // len(x)
    return np.reshape(np.tile(np.expand_dims(x, 1), [1, samples_per_frame]), samples)


def main() -> None:
    from docopt import docopt

    import sonusai
    from sonusai.utils import trim_docstring

    args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

    from dataclasses import asdict
    from os.path import basename
    from os.path import exists
    from os.path import isdir
    from os.path import splitext

    import h5py
    from matplotlib.backends.backend_pdf import PdfPages
    from pyaaware import FeatureGenerator
    from pyaaware import Predict

    from sonusai import SonusAIError
    from sonusai import create_file_handler
    from sonusai import initial_log_messages
    from sonusai import logger
    from sonusai import update_console_handler
    from sonusai.mixture import FeatureGeneratorConfig
    from sonusai.mixture import MixtureDatabase
    from sonusai.mixture import get_feature_from_audio
    from sonusai.mixture import get_truth_indices_for_mixid
    from sonusai.mixture import read_audio
    from sonusai.utils import get_label_names
    from sonusai.utils import print_mixture_details

    verbose = args["--verbose"]
    model_name = args["--model"]
    output_name = args["--output"]
    labels_name = args["--labels"]
    mixid = args["--mixid"]
    energy = args["--energy"]
    input_name = args["INPUT"]

    if mixid is not None:
        mixid = int(mixid)

    create_file_handler("plot.log")
    update_console_handler(verbose)
    initial_log_messages("plot")

    if not exists(input_name):
        raise SonusAIError(f"{input_name} does not exist")

    logger.info("")
    logger.info(f"Input:  {input_name}")
    if model_name is not None:
        logger.info(f"Model:  {model_name}")
    if output_name is not None:
        logger.info(f"Output: {output_name}")
    logger.info("")

    ext = splitext(input_name)[1]

    model = None
    target_audio = None
    truth_f = None
    t_indices = []

    if model_name is not None:
        model = Predict(model_name)

    if ext == ".wav":
        if model is None:
            raise SonusAIError("Must specify MODEL when input is WAV")

        mixture_audio = read_audio(input_name)
        feature = get_feature_from_audio(audio=mixture_audio, feature_mode=model.feature)
        fg_config = FeatureGeneratorConfig(
            feature_mode=model.feature,
            num_classes=model.output_shape[-1],
            truth_mutex=False,
        )
        fg = FeatureGenerator(**asdict(fg_config))
        fg_step = fg.step
        mixdb = None
        logger.debug(f"Audio samples      {len(mixture_audio)}")
        logger.debug(f"Feature shape      {feature.shape}")

    elif isdir(input_name):
        if mixid is None:
            raise SonusAIError("Must specify mixid when input is mixture database")

        mixdb = MixtureDatabase(input_name)
        fg_step = mixdb.fg_step

        print_mixture_details(mixdb=mixdb, mixid=mixid, desc_len=24, print_fn=logger.info)

        logger.info(f"Generating data for mixture {mixid}")
        mixture_audio = mixdb.mixture_mixture(mixid)
        target_audio = mixdb.mixture_target(mixid)
        feature, truth_f = mixdb.mixture_ft(mixid)
        t_indices = [x - 1 for x in get_truth_indices_for_mixid(mixdb=mixdb, mixid=mixid)]

        target_files = [mixdb.target_file(target.file_id) for target in mixdb.mixtures[mixid].targets]
        truth_functions = list({sub2.function for sub1 in target_files for sub2 in sub1.truth_configs})
        energy = "energy_f" in truth_functions or "snr_f" in truth_functions

        logger.debug(f"Audio samples      {len(mixture_audio)}")
        logger.debug("Targets:")
        mixture = mixdb.mixture(mixid)
        for target in mixture.targets:
            target_file = mixdb.target_file(target.file_id)
            name = target_file.name
            duration = target_file.duration
            augmentation = target.augmentation
            logger.debug(f"  Name             {name}")
            logger.debug(f"  Duration         {duration}")
            logger.debug(f"  Augmentation     {augmentation}")

        logger.debug(f"Feature shape      {feature.shape}")
        logger.debug(f"Truth shape        {truth_f.shape}")

    else:
        raise SonusAIError(f"Unknown file type for {input_name}")

    predict = None
    labels = None
    indices = []
    if model is not None:
        logger.debug("")
        logger.info(f"Running prediction on mixture {mixid}")
        logger.debug(f"Model feature name {model.feature}")
        logger.debug(f"Model input shape  {model.input_shape}")
        logger.debug(f"Model output shape {model.output_shape}")

        if feature.shape[0] < model.input_shape[0]:
            raise SonusAIError(
                f"Mixture {mixid} contains {feature.shape[0]} "
                f"frames of data which is not enough to run prediction; "
                f"at least {model.input_shape[0]} frames are needed for this model.\n"
                f"Consider using a model with a smaller batch size or a mixture with more data."
            )

        predict = model.execute(feature)

        labels = get_label_names(num_labels=predict.shape[1], file=labels_name)

        # Report the highest-scoring classes and their scores.
        p_max = np.max(predict, axis=0)
        p_indices = np.argsort(p_max)[::-1][:5]
        p_max_len = max([len(labels[i]) for i in p_indices])

        logger.info("Top 5 active prediction classes by max:")
        for p_index in p_indices:
            logger.info(f"  {labels[p_index]:{p_max_len}s} {p_max[p_index]:.3f}")
        logger.info("")

        indices = list(p_indices)

    # Add truth indices for target (if needed)
    for t_index in t_indices:
        if t_index not in indices:
            indices.append(t_index)

    base_name = basename(splitext(input_name)[0])
    if mixdb is not None:
        title = f"{input_name} Mixture {mixid}"
        pdf_name = f"{base_name}-mix{mixid}-plot.pdf"
    else:
        title = f"{input_name}"
        pdf_name = f"{base_name}-plot.pdf"

    # Original size [frames, stride, feature_parameters]
    # Decimate in the stride dimension
    # Reshape to get frames*decimated_stride, feature_parameters
    if feature.ndim != 3:
        raise SonusAIError("feature does not have 3 dimensions: frames, stride, feature_parameters")
    spectrogram = feature[:, -fg_step:, :]
    spectrogram = np.reshape(spectrogram, (spectrogram.shape[0] * spectrogram.shape[1], spectrogram.shape[2]))

    with PdfPages(pdf_name) as pdf:
        pdf.savefig(
            spec_plot(
                mixture=mixture_audio,
                feature=spectrogram,
                predict=predict,
                labels=labels,
                title=title,
            )
        )
        for index in indices:
            if energy:
                t_tmp = None
                if truth_f is not None:
                    t_tmp = 10 * np.log10(truth_f + np.finfo(np.float32).eps)

                p_tmp = None
                if predict is not None:
                    p_tmp = 10 * np.log10(predict + np.finfo(np.float32).eps)

                pdf.savefig(
                    spec_energy_plot(
                        mixture=mixture_audio,
                        feature=spectrogram,
                        truth_f=t_tmp,
                        predict=p_tmp,
                    )
                )
            else:
                p_tmp = None
                if predict is not None:
                    p_tmp = predict[:, index]

                l_tmp = None
                if labels is not None:
                    l_tmp = labels[index]

                pdf.savefig(
                    class_plot(
                        mixture=mixture_audio,
                        target=target_audio[index],
                        truth_f=truth_f[:, index],
                        predict=p_tmp,
                        label=l_tmp,
                    )
                )
        logger.info(f"Wrote {pdf_name}")

    if output_name:
        with h5py.File(output_name, "w") as f:
            f.create_dataset(name="predict", data=predict)
            logger.info(f"Wrote {output_name}")


if __name__ == "__main__":
    main()
