"""FPS correction utility for recordings made on 2021-12-21"""

from pathlib import Path

import cv2

### Monkey patching vidgears permission check
from functools import wraps
import vidgear.gears.writegear

vidgear.gears.writegear.check_WriteAccess = wraps(
    vidgear.gears.writegear.check_WriteAccess
)(lambda *args, **kwargs: True)

from vidgear.gears import WriteGear

SOURCE = Path("recordings").absolute()

SINK = Path("processed").absolute()

print(f"SOURCE: {SOURCE}")
print(f"SINK: {SINK}")

for path in SOURCE.glob("*.mp4"):

    print(f"Processing {path}")

    stream = cv2.VideoCapture(str(path))
    # Check if camera opened successfully
    if not stream.isOpened():
        print(f"Error opening {path}")
        continue

    writer = WriteGear(
        output_filename=str(SINK / path.name),
        logging=True,
        compression_mode=False,
        **{"-fps": 13},
    )

    # Read until video is completed
    while stream.isOpened():
        # Capture frame-by-frame
        ret, frame = stream.read()
        if ret == True:

            writer.write(frame)

        # Break the loop
        else:
            break

    # When everything done, release the video capture object and close the writer
    stream.release()
    writer.close()
