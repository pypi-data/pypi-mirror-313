from sonusai.mixture.datatypes import AudioStatsMetrics
from sonusai.mixture.datatypes import AudioT


def _convert_str_with_factors_to_int(x: str) -> int:
    if "k" in x:
        return int(1000 * float(x.replace("k", "")))
    if "M" in x:
        return int(1000000 * float(x.replace("M", "")))
    return int(x)


def calc_audio_stats(audio: AudioT, win_len: float | None = None) -> AudioStatsMetrics:
    from sonusai.mixture import SAMPLE_RATE
    from sonusai.mixture import Transformer

    args = ["stats"]
    if win_len is not None:
        args.extend(["-w", str(win_len)])

    tfm = Transformer()

    _, _, out = tfm.build(
        input_array=audio,
        sample_rate_in=SAMPLE_RATE,
        output_filepath="-n",
        extra_args=args,
        return_output=True,
    )

    if out is None:
        raise SystemError("Call to sox failed")

    stats = {}
    lines = out.split("\n")
    for line in lines:
        split_line = line.split()
        if len(split_line) == 0:
            continue
        value = split_line[-1]
        key = " ".join(split_line[:-1])
        stats[key] = value

    return AudioStatsMetrics(
        dco=float(stats["DC offset"]),
        min=float(stats["Min level"]),
        max=float(stats["Max level"]),
        pkdb=float(stats["Pk lev dB"]),
        lrms=float(stats["RMS lev dB"]),
        pkr=float(stats["RMS Pk dB"]),
        tr=float(stats["RMS Tr dB"]),
        cr=float(stats["Crest factor"]),
        fl=float(stats["Flat factor"]),
        pkc=_convert_str_with_factors_to_int(stats["Pk count"]),
    )
