"""The DataReader class reads jelka data from stdin. The data must be in the required format.

Data format:
Before any values for LEDs are given, a header must be present.
There are 2 types of data: user output (mainly for debugging) and jelka data.
All jelka data must be prefixed with a "#". The header must be the first jelka data.

The header starts with a "#" and must be in a single line.
It can be any JSON object with the following keys
For version 0:
- version: 0
- led_count: int
- fps: int

Current version is 0. Older versions will be supported as long as possible.

An example header:
'#{"version": 0, "led_count": 500, "fps": 60}\n'

After the header, there are frames. Each frame is a single line prefixed
by a "#". For every LED there are 3 values r, g, b - hex values 00-ff (0 - 255).
The values are concatenated in the order r, g, b.

For example a 3 LED frame with values (0, 1, 2), (3, 4, 5), (0, 150, 255) would be
"#0001020304050096ff\n".

All lines that are not prefixed with a "#" are considered user output and
can be printed to stdout."""

from .utils import decode_header, decode_frame
import os
linesepb = os.linesep.encode(encoding="utf-8")


class BytesReader:
    """Reads jelka data from bytes. The data must be in the required format.
    You can feed it bytes in chunks. The data will not be decoded and returned
    until it is required."""

    def __init__(self) -> None:
        self.mode = "user"
        self.jelka_buffer = b""
        self.user_buffer = b""
        self.version: "None | int" = None
        self.led_count: "None | int" = None

    def read_more(self, inp: bytes):
        user_add = []  # new other stuff
        jelka_add = []  # new jelka data

        if not inp:
            return
        
        i = 0
        while i < len(inp):
            byte = inp[i]
            if self.mode == "user" and byte == ord("#"):
                self.mode = "jelka"

            if self.mode == "jelka":
                jelka_add.append(byte.to_bytes(length=1, byteorder="big"))
            elif self.mode == "user":
                user_add.append(byte.to_bytes(length=1, byteorder="big"))

            # Things that can are used for newlines
            if self.mode == "jelka" and inp[i : i + len(linesepb)] == linesepb:
                self.mode = "user"
                jelka_add.append(linesepb[1:])
                i += len(linesepb)
                continue
            
            i += 1

        self.user_buffer += b"".join(user_add)
        self.jelka_buffer += b"".join(jelka_add)

    def try_get_header(self) -> "None | dict":
        # find the end of the header (newline)
        header_end = self.jelka_buffer.find(linesepb)

        if header_end == -1:
            return None

        text = self.jelka_buffer[0 : header_end + 1].decode(encoding="utf-8")
        text = text.lstrip("#")
        text = text.strip()
        header = decode_header(text)

        # some values are required to parse frames
        self.version = header["version"]
        self.led_count = header["led_count"]

        # remove what has already been used
        self.jelka_buffer = self.jelka_buffer[header_end + 1 :]

        return header

    def try_get_frames(self) -> list:
        if self.version is None:
            raise ValueError("Header must be read before frames.")
        self.version  # type: int

        # find the end of the frame (newline)
        frame_end = self.jelka_buffer.find(linesepb)
        if frame_end == -1:
            return []

        frame_start = 0
        frames = []
        while frame_end != -1:
            text = self.jelka_buffer[frame_start : frame_end + 1].decode(encoding="utf-8")
            text = text.strip(os.linesep)
            text = text.lstrip("#")

            # Get the frame
            frame = decode_frame(text, self.led_count, self.version)  # type: ignore
            frames.append(frame)

            # find the start and the end of the next frame
            frame_start = frame_end + len(linesepb)
            frame_end = self.jelka_buffer.find(linesepb, frame_start + 1)

        # remove what has already been used
        self.jelka_buffer = self.jelka_buffer[frame_start + len(linesepb) :]

        return frames

    def user_print(self, flush=True, end=""):
        print(self.user_buffer.decode(encoding="utf-8"), end=end, flush=flush)
        self.user_buffer = b""


class DataReader:
    def __init__(self, bytes_getter) -> None:
        """Reads data to Python objects. bytes_getter is a function that returns bytes.
        It will probably be something like sys.stdin.buffer.read or Popen.stdin.read1."""
        self.header = None

        # Header values
        self.version = None
        self.led_count = None
        self.fps = None

        # Frame values
        self.frames = []
        self.frame_count = 0  # the last frame that should be read
        # actual frame data (latest avaiable that should already be read)
        self.current_frame = None

        # Getting input
        self.bytes_getter = bytes_getter
        self.bytes_reader = BytesReader()

    def update(self):
        self.update_buffer()
        if not self.header:
            self.try_read_header()
        self.try_read_frames()

    def update_buffer(self):
        self.bytes_reader.read_more(self.bytes_getter())

    def user_print(self, flush=True, end=""):
        self.bytes_reader.user_print(flush=flush, end=end)

    def try_read_header(self):
        header = self.bytes_reader.try_get_header()
        if header:
            self.header = header
            self.version = header["version"]
            self.led_count = header["led_count"]
            self.fps = header["fps"]

    def try_read_frames(self):
        if not self.header:
            return

        frames = self.bytes_reader.try_get_frames()
        self.frames.extend(frames)

    def __iter__(self):
        return self

    def __next__(self):
        self.update()

        self.frame_count += 1

        if self.frames:
            # best apporximation of the present
            return self.frames[min(self.frame_count - 1, len(self.frames) - 1)]

        # if there are no frames, return black
        return [(0, 0, 0)] * (self.led_count or 0)
