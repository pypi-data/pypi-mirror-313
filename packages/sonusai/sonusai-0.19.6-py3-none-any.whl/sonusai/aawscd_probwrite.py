#!/usr/bin/env python3
"""aawscd_probwrite

usage: aawscd_probwrite [-h] [-m MACHINE] [-f FRAMES] FILE

options:
   -h, --help
   -m MACHINE, --machine MACHINE    IP address of aawscd platform. [default: localhost].
   -f FRAMES, --frames FRAMES       Number of frames to capture. [default: 10].

aawscd_probwrite connects to an Aaware platform running aawscd and writes the sound classification
probability output to an HDF5 file.

"""

from threading import Condition

import numpy as np

from sonusai.utils import track

CLIENT: str = "aawscd_probwrite"
TOPIC: str = "aawscd/sc/prob"
DONE: Condition = Condition()
FRAMES: int = 10
FRAME_COUNT: int = 0
DATA: np.ndarray | None = None
PROGRESS: track | None = None


def shutdown(_signum, _frame) -> None:
    global DONE
    with DONE:
        DONE.notify()


def unpack_prob_entry(entry: int) -> tuple[int, int, int]:
    """Decode the packed probability data: [ 16-bit label | 8-bit zone | 8-bit probability ]."""
    data = np.array(entry, dtype=np.uint32)
    label = np.right_shift(data, 16)
    zone = np.bitwise_and(np.right_shift(data, 8), 0xFF)
    value = np.bitwise_and(entry, 0xFF)
    return int(zone), int(label), int(value)


def parse_prob(payload: list) -> np.ndarray:
    """Parse MQTT probability payload from aawscd.

    The 'aawscd/sc/prob' payload is a list of uint32. Each item contains packed data and is
    unpacked/decoded and inserted into an array.
    """

    # First pass: get the zones and labels to determine the size of the array
    zones = set()
    labels = set()
    for entry in payload:
        zone, label, _ = unpack_prob_entry(entry)
        zones.add(zone)
        labels.add(label)

    # Create the array
    prob = np.zeros((len(list(labels)), len(list(zones))), dtype=np.uint8)

    # Second pass: fill in the array probability values.
    for entry in payload:
        zone, label, value = unpack_prob_entry(entry)
        prob[label, zone] = value

    # Return the array
    return prob


def on_message(_client, _userdata, message):
    import paho.mqtt.client as mqtt
    import yaml

    global TOPIC
    if mqtt.topic_matches_sub(TOPIC, message.topic):
        payload = yaml.safe_load(str(message.payload.decode("utf-8")))
        prob = parse_prob(payload["prob"])

        global DATA
        global FRAMES
        if DATA is None:
            DATA = np.zeros((FRAMES, prob.shape[0], prob.shape[1]), dtype=prob.dtype)

        global FRAME_COUNT
        DATA[FRAME_COUNT] = prob
        FRAME_COUNT += 1

        global PROGRESS
        PROGRESS.update()

        if FRAME_COUNT == FRAMES:
            global DONE
            with DONE:
                DONE.notify()


def main() -> None:
    from docopt import docopt

    args = docopt(__doc__, version="1.0.0", options_first=True)

    import signal

    import h5py
    import paho.mqtt.client as mqtt

    machine = args["--machine"]

    global FRAMES
    FRAMES = int(args["--frames"])

    file = args["FILE"]

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    global CLIENT
    client = mqtt.Client(client_id=CLIENT)
    client.on_message = on_message
    client.connect(host=machine)
    client.loop_start()
    global TOPIC
    client.subscribe(topic=TOPIC)

    global PROGRESS
    PROGRESS = track(total=FRAMES, desc=file)

    with DONE:
        DONE.wait()

    PROGRESS.close()

    client.unsubscribe(topic=TOPIC)
    client.loop_stop()
    client.disconnect()

    global DATA
    with h5py.File(file, "w") as f:
        f.create_dataset(name="prob", data=DATA)

    print(f"Wrote {file}")


if __name__ == "__main__":
    main()
