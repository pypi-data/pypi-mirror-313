"""This module contains functions for encoding and decoding the header and frames."""

import json


def encode_header(led_count: int, fps: int) -> str:
    """led_count must be an integer.

    Examples:
    >>> encode_header(led_count=500, fps=60)
    '{"version": 0, "led_count": 500, "fps": 60}'
    """

    if not isinstance(led_count, int):
        raise TypeError(f"led_count must be int, found {type(led_count)}.")
    if not isinstance(fps, int):
        raise TypeError(f"fps must be int, found {type(fps)}.")

    # Change version if structure of data changes
    version = 0  # 0 for testing  # TODO: increase this
    return json.dumps(
        {
            "version": version,
            "led_count": led_count,
            "fps": fps,
        },
        indent=None,
    )


def decode_header(header: str) -> dict:
    """Decodes a header string into a dictionary.
    Almost the reverse of encode_header. Does not check for correct types.
    Raises a ValueError if the header does not contain a version or if the version is not supported.

    When making header for your personal use just hardcode the version number.
    Older versions will be supported as long as possible.

    Examples:
    >>> header = {"led_count": 500, "fps": 60}
    >>> decode_header(encode_header(**header)) == dict(header, version=0)
    True
    """

    json_header = json.loads(header)
    if "version" not in json_header:
        raise ValueError("Header must contain a version.")

    if json_header["version"] == 0:
        if not all(key in json_header for key in ("led_count", "fps")):
            raise ValueError("Header (version 0) must contain led_count and fps.")
    else:
        raise ValueError(f"Unsupported header version: {json_header['version']}.")

    return json_header


def encode_frame(frame: list, led_count: int) -> str:
    """Encodes a frame into a string of hex values.
    Each led in the frame is represented by a tuple of 3 integers (r, g, b).
    There must be led_count number of tuples in the frame. Will raise a ValueError if the frame is not valid.
    The output string will have 6 characters per led, 2 for each rgb value.

    Examples:
    >>> encode_frame([(0, 1, 2), (3, 4, 5), (0, 150, 255)], 3)
    '0001020304050096ff'
    """

    if len(frame) != led_count:
        raise ValueError(f"frame must have a value for every led, has {len(frame)}/{led_count}.")
    if not all(len(rgb) == 3 and (isinstance(v, int) for v in rgb) for rgb in frame):
        raise ValueError("frame must have an rbg tuple of ints for values.")

    return "".join(hex(v)[2:].zfill(2) for rgb in frame for v in rgb)


def decode_frame(frame: str, led_count: int, version: int) -> list:
    """Decodes a frame string into a list of rgb tuples.
    The frame string must have 6 characters per led, 2 for each rgb value.
    Will raise a ValueError if the frame is not valid.

    If format ever changes so will the version number. This will allow for backwards compatibility.

    Examples:
    >>> decode_frame('0001020304050096ff', 3, version=0)
    [(0, 1, 2), (3, 4, 5), (0, 150, 255)]
    """

    assert version in (0,), f"Unsupported frame version: {version}."
    if not isinstance(frame, str):
        raise TypeError(f"Expected type 'str', found type {type(frame)}.")

    expected_length = 3 * led_count * 2  # 3 * 2 characters per led
    if len(frame) != expected_length:
        raise ValueError(f"Frame has wrong size, expected exactly {expected_length} bytes, found {len(frame)}.")

    return [
        (int(frame[i : i + 2], 16), int(frame[i + 2 : i + 4], 16), int(frame[i + 4 : i + 6], 16))
        for i in range(0, len(frame), 6)
    ]
