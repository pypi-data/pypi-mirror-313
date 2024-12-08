from .utils import encode_header, encode_frame


class DataWriter:
    """Writes jelka data to stdout. The data is written in the required format.
    Useful for testing and text files."""

    def __init__(
        self,
        led_count: int = 500,
        fps: int = 60,
    ) -> None:
        # Header values
        self.fps = fps
        self.led_count = led_count

        # Endoded header
        self.header: str = encode_header(
            led_count=self.led_count,
            fps=self.fps,
        )

        # State
        self.printed_header = False
        self.frame_count = 0

    def write_frame(self, frame: list):
        """Writes a frame to stdout. Raises a ValueError if the frame 
        does not have a valid shape (see encode_frame from utils).

        If the header has not been printed yet, it will be printed before the first frame.
        Prefixes encoded frame and header with a "#".
        """

        if not self.printed_header:
            print("#" + self.header)
            self.printed_header = True

        print("#" + encode_frame(frame, self.led_count))
        self.frame_count += 1
