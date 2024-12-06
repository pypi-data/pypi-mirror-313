"""sonusai audiofe

usage: audiofe [-hvds] [--version] [-i INPUT] [-l LENGTH] [-m MODEL] [-a ASR] [-w WMODEL]

options:
    -h, --help
    -v, --verbose                   Be verbose.
    -d, --debug                     Write debug data to H5 file.
    -s, --show                      Display a list of available audio inputs.
    -i INPUT, --input INPUT         Input audio.
    -l LENGTH, --length LENGTH      Length of audio in seconds. [default: -1].
    -m MODEL, --model MODEL         ONNX model.
    -a ASR, --asr ASR               ASR method to use.
    -w WMODEL, --whisper WMODEL     Model used in whisper, aixplain_whisper and faster_whisper methods. [default: tiny].

Aaware SonusAI Audio Front End.

Capture LENGTH seconds of audio from INPUT. If LENGTH is < 0, then capture until key is pressed. If INPUT is a valid
audio file name, then use the audio data from the specified file. In this case, if LENGTH is < 0, process entire file;
otherwise, process min(length(INPUT), LENGTH) seconds of audio from INPUT. Audio is saved to
audiofe_capture_<TIMESTAMP>.wav.

If a model is specified, run prediction on audio data from this model. Then compute the inverse transform of the
prediction result and save to audiofe_predict_<TIMESTAMP>.wav.

Also, if a model is specified, save plots of the capture data (time-domain signal and feature) to
audiofe_capture_<TIMESTAMP>.png and predict data (time-domain signal and feature) to
audiofe_predict_<TIMESTAMP>.png.

If an ASR is specified, run ASR on the captured audio and print the results. In addition, if a model was also specified,
run ASR on the predict audio and print the results.  Examples: faster_whisper, google,

If the debug option is enabled, write capture audio, feature, reconstruct audio, predict, and predict audio to
audiofe_<TIMESTAMP>.h5.

"""

import signal

import numpy as np

from sonusai.mixture import AudioT


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
    length = float(args["--length"])
    input_name = args["--input"]
    model_name = args["--model"]
    asr_name = args["--asr"]
    whisper_name = args["--whisper"]
    debug = args["--debug"]
    show = args["--show"]

    from os.path import exists

    import h5py
    import pyaudio

    from sonusai import create_file_handler
    from sonusai import initial_log_messages
    from sonusai import logger
    from sonusai import update_console_handler
    from sonusai.mixture import SAMPLE_RATE
    from sonusai.mixture import get_audio_from_feature
    from sonusai.mixture import get_feature_from_audio
    from sonusai.utils import calc_asr
    from sonusai.utils import create_timestamp
    from sonusai.utils import get_input_devices
    from sonusai.utils import load_ort_session
    from sonusai.utils import write_audio

    ts = create_timestamp()
    capture_name = f"audiofe_capture_{ts}"
    capture_wav = capture_name + ".wav"
    capture_png = capture_name + ".png"
    predict_name = f"audiofe_predict_{ts}"
    predict_wav = predict_name + ".wav"
    predict_png = predict_name + ".png"
    h5_name = f"audiofe_{ts}.h5"

    # Setup logging file
    create_file_handler("audiofe.log")
    update_console_handler(verbose)
    initial_log_messages("audiofe")

    if show:
        logger.info("List of available audio inputs:")
        logger.info("")
        p = pyaudio.PyAudio()
        for name in get_input_devices(p):
            logger.info(f"{name}")
        logger.info("")
        p.terminate()
        return

    if input_name is not None and exists(input_name):
        capture_audio = get_frames_from_file(input_name, length)
    else:
        try:
            capture_audio = get_frames_from_device(input_name, length)
        except ValueError as e:
            logger.exception(e)
            return
        # Only write if capture from device, not for file input
        write_audio(capture_wav, capture_audio, SAMPLE_RATE)
        logger.info("")
        logger.info(f"Wrote capture audio with shape {capture_audio.shape} to {capture_wav}")

    if debug:
        with h5py.File(h5_name, "a") as f:
            if "capture_audio" in f:
                del f["capture_audio"]
            f.create_dataset("capture_audio", data=capture_audio)
        logger.info(f"Wrote capture feature data with shape {capture_audio.shape} to {h5_name}")

    if asr_name is not None:
        logger.info(f"Running ASR on captured audio with {asr_name} ...")
        capture_asr = calc_asr(capture_audio, engine=asr_name, whisper_model_name=whisper_name).text
        logger.info(f"Capture audio ASR: {capture_asr}")

    if model_name is not None:
        session, options, model_root, hparams, sess_inputs, sess_outputs = load_ort_session(model_name)
        if hparams is None:
            logger.error("Error: ONNX model does not have required SonusAI hyperparameters, cannot proceed.")
            raise SystemExit(1)
        feature_mode = hparams["feature"]
        in0name = sess_inputs[0].name
        in0type = sess_inputs[0].type
        out_names = [n.name for n in session.get_outputs()]

        # frames x stride x feat_params
        feature = get_feature_from_audio(audio=capture_audio, feature_mode=feature_mode)
        save_figure(capture_png, capture_audio, feature)
        logger.info(f"Wrote capture plots to {capture_png}")

        if debug:
            with h5py.File(h5_name, "a") as f:
                if "feature" in f:
                    del f["feature"]
                f.create_dataset("feature", data=feature)
            logger.info(f"Wrote feature with shape {feature.shape} to {h5_name}")

        if in0type.find("float16") != -1:
            logger.info("Detected input of float16, converting all feature inputs to that type.")
            feature = np.float16(feature)  # type: ignore[assignment]

        # Run inference, ort session wants batch x timesteps x feat_params, outputs numpy BxTxFP or BxFP
        # Note full reshape not needed here since we assume speech enhancement type model, so a transpose suffices
        predict = np.transpose(
            session.run(out_names, {in0name: np.transpose(feature, (1, 0, 2))})[0],
            (1, 0, 2),
        )

        if debug:
            with h5py.File(h5_name, "a") as f:
                if "predict" in f:
                    del f["predict"]
                f.create_dataset("predict", data=predict)
            logger.info(f"Wrote predict with shape {predict.shape} to {h5_name}")

        predict_audio = get_audio_from_feature(feature=predict, feature_mode=feature_mode)
        write_audio(predict_wav, predict_audio, SAMPLE_RATE)
        logger.info(f"Wrote predict audio with shape {predict_audio.shape} to {predict_wav}")
        if debug:
            with h5py.File(h5_name, "a") as f:
                if "predict_audio" in f:
                    del f["predict_audio"]
                f.create_dataset("predict_audio", data=predict_audio)
            logger.info(f"Wrote predict audio with shape {predict_audio.shape} to {h5_name}")

        save_figure(predict_png, predict_audio, predict)
        logger.info(f"Wrote predict plots to {predict_png}")

        if asr_name is not None:
            logger.info(f"Running ASR on model-enhanced audio with {asr_name} ...")
            predict_asr = calc_asr(predict_audio, engine=asr_name, whisper_model_name=whisper_name).text
            logger.info(f"Predict audio ASR: {predict_asr}")


def get_frames_from_device(input_name: str | None, length: float, chunk: int = 1024) -> AudioT:
    from select import select
    from sys import stdin

    import pyaudio

    from sonusai import logger
    from sonusai.mixture import CHANNEL_COUNT
    from sonusai.mixture import SAMPLE_RATE
    from sonusai.utils import get_input_device_index_by_name
    from sonusai.utils import get_input_devices

    p = pyaudio.PyAudio()

    input_devices = get_input_devices(p)
    if not input_devices:
        raise ValueError("No input audio devices found")

    if input_name is None:
        input_name = input_devices[0]

    try:
        device_index = get_input_device_index_by_name(p, input_name)
    except ValueError as e:
        msg = f"Could not find {input_name}\n"
        msg += "Available devices:\n"
        for input_device in input_devices:
            msg += f"  {input_device}\n"
        raise ValueError(msg) from e

    logger.info(f"Capturing from {p.get_device_info_by_index(device_index).get('name')}")
    stream = p.open(
        format=pyaudio.paFloat32,
        channels=CHANNEL_COUNT,
        rate=SAMPLE_RATE,
        input=True,
        input_device_index=device_index,
    )
    stream.start_stream()

    print()
    print("+---------------------------------+")
    print("| Press Enter to stop             |")
    print("+---------------------------------+")
    print()

    elapsed = 0.0
    seconds_per_chunk = float(chunk) / float(SAMPLE_RATE)
    raw_frames = []
    while elapsed < length or length == -1:
        raw_frames.append(stream.read(num_frames=chunk, exception_on_overflow=False))
        elapsed += seconds_per_chunk
        if select(
            [
                stdin,
            ],
            [],
            [],
            0,
        )[0]:
            stdin.read(1)
            length = elapsed

    stream.stop_stream()
    stream.close()
    p.terminate()
    frames = np.frombuffer(b"".join(raw_frames), dtype=np.float32)
    return frames


def get_frames_from_file(input_name: str, length: float) -> AudioT:
    from sonusai import logger
    from sonusai.mixture import SAMPLE_RATE
    from sonusai.mixture import read_audio

    logger.info(f"Capturing from {input_name}")
    frames = read_audio(input_name)
    if length != -1:
        num_frames = int(length * SAMPLE_RATE)
        if len(frames) > num_frames:
            frames = frames[:num_frames]
    return frames


def save_figure(name: str, audio: np.ndarray, feature: np.ndarray) -> None:
    import matplotlib.pyplot as plt
    from scipy.interpolate import CubicSpline

    from sonusai.mixture import SAMPLE_RATE
    from sonusai.utils import unstack_complex

    spectrum = 20 * np.log(np.abs(np.squeeze(unstack_complex(feature)).transpose()))
    frames = spectrum.shape[1]
    samples = (len(audio) // frames) * frames
    length_in_s = samples / SAMPLE_RATE
    interp = samples // frames

    ts = np.arange(0.0, length_in_s, interp / SAMPLE_RATE)
    t = np.arange(0.0, length_in_s, 1 / SAMPLE_RATE)

    spectrum = CubicSpline(ts, spectrum, axis=-1)(t)

    fig, (ax1, ax2) = plt.subplots(nrows=2)
    ax1.set_title(name)
    ax1.plot(t, audio[:samples])
    ax1.set_ylabel("Signal")
    ax1.set_xlim(0, length_in_s)
    ax1.set_ylim(-1, 1)

    ax2.imshow(spectrum, origin="lower", aspect="auto")
    ax2.set_xticks([])
    ax2.set_ylabel("Feature")

    plt.savefig(name, dpi=300)


if __name__ == "__main__":
    main()
