import sys
import signal
from pathlib import Path
from datetime import datetime
from functools import wraps

### Monkey patching vidgears permission check
import vidgear.gears.writegear

vidgear.gears.writegear.check_WriteAccess = wraps(
    vidgear.gears.writegear.check_WriteAccess
)(lambda *args, **kwargs: True)

from vidgear.gears import CamGear
from vidgear.gears import WriteGear

from environs import Env

env = Env()
SOURCE: str = env("SOURCE")
SINK: Path = env.path("SINK", None)
SINK_SUFFIX: str = env("SINK_SUFFIX", "")
SINK_COMPRESSION: bool = env.bool("SINK_COMPRESSION", True)
SINK_CONFIG: dict = env.dict("SINK_CONFIG", {})
VERBOSE: bool = env.bool("VERBOSE", False)


def record(stream: CamGear, writer: WriteGear):
    # Frame-wise loop
    while True:
        frame = stream.read()
        if frame is None:
            break
        writer.write(frame)


if __name__ == "__main__":

    # Open source stream
    stream = CamGear(source=SOURCE, logging=VERBOSE).start()

    # Create the path to the sink
    if SINK:
        sink_path = SINK if SINK.is_absolute() else Path("recordings") / SINK
    else:
        sink_path = Path("recordings") / f"{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    # Add suffix
    sink_path = sink_path.with_suffix(
        (
            SINK_SUFFIX
            if SINK_SUFFIX.startswith(".") or not SINK_SUFFIX
            else f".{SINK_SUFFIX}"
        )
        + sink_path.suffix
    )

    # Make sure the parent path exists
    sink_path.parent.mkdir(parents=True, exist_ok=True)

    # Define writer
    default_config = {"-input_framerate": stream.framerate}
    writer = WriteGear(
        output_filename=str(sink_path.absolute()),
        logging=VERBOSE,
        compression_mode=SINK_COMPRESSION,
        **{**default_config, **SINK_CONFIG},
    )

    # Set up signal handlers
    def signal_handler(_signo, _stack_frame):
        print("Gracefully stopped!")
        stream.stop()
        writer.close()
        sys.exit(0)

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    # Start recording!
    record(stream, writer)
