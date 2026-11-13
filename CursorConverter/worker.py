from io import BytesIO
from pathlib import Path
from typing import Dict, List, Tuple

import cv2
from cursorgen.parser import open_blob
from cursorgen.writer import to_xcursor


def process(arg: Tuple[BytesIO, str, Path, Dict[str, List[str]], List[int]]) -> None:
    stream, name, output, mapping, sizes = arg
    cursors = open_blob(stream.getvalue())
    result = to_xcursor(frames=cursors.frames, sizes=sizes)

    if name in mapping:
        for xcursor_name in mapping[name]:
            with open(xcursor_name, "wb") as fs:
                fs.write(result)

    if name != "idle":
        return

    thumbnail = cv2.resize(
        cursors.frames[0].images[0].image,
        (320, 320),
        interpolation=cv2.INTER_NEAREST_EXACT,
    )
    if not cv2.imwrite(str(output / "thumb.png"), thumbnail):
        raise OSError(f"Could not write thumbnail: {output / 'thumb.png'}")
