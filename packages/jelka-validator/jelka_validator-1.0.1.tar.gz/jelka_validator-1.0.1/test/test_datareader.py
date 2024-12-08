# type: ignore UnusedExpression

import pytest

from src.jelka_validator import DataReader
from src.jelka_validator.utils import encode_header, encode_frame

from random import Random
from os import linesep
import json


def random_frame(led_count, seed):
    rnd = Random()
    rnd.seed(seed)
    randint = rnd.randint
    return [(randint(0, 255), randint(0, 255), randint(0, 255)) for _ in range(led_count)]


def header(led_count, fps):
    hd = "#" + encode_header(led_count, fps) + linesep
    return BytesMaker(led_count, [hd], user=[], jelka=[])


class BytesMaker:
    """Helper class for creating bytes from strings and frames - bad design, don't reuse this code"""

    def __init__(self, led_count, entries=None, user=None, jelka=None):
        self.entries = entries or []
        self.user = user or []
        self.jelka = jelka or []
        self.led_count = led_count

    def __add__(self, other: "str | int"):
        """Jelka data"""
        if isinstance(other, int):
            frame = random_frame(self.led_count, other)
            self.jelka.append(frame)
            self.entries.append("#" + encode_frame(frame, self.led_count) + linesep)
        else:
            self.entries.append(other)
            self.user.append(other)

        return self

    def copy(self):
        return BytesMaker(self.led_count, self.entries.copy(), self.user.copy(), self.jelka.copy())

    def as_bytes(self):
        return "".join(self.entries).encode("utf-8")

    def read(self):
        bs = self.as_bytes()
        self.entries.clear()
        return bs


class TestDataReader:
    def test_header(self):
        data = header(led_count=1, fps=60)

        dr = DataReader(data.read)
        dr.update()
        assert dr.header == {
            "led_count": 1,
            "fps": 60,
            "version": 0,
        }

    def test_header_comment(self):
        data = header(led_count=150, fps=60) + "This is a random comment"

        dr = DataReader(data.read)
        dr.update()

        assert dr.header == {
            "led_count": 150,
            "fps": 60,
            "version": 0,
        }

    def test_comment_header(self):
        data = header(led_count=500, fps=60)
        data.entries.insert(0, "This is a random comment" + linesep)

        dr = DataReader(data.read)
        dr.update()

        assert dr.header == {
            "led_count": 500,
            "fps": 60,
            "version": 0,
        }

    def test_invalid_header(self):
        data = header(led_count=1, fps=60)
        data.entries[0] = "#Invalid header" + linesep

        dr = DataReader(data.read)
        dr.update_buffer()
        with pytest.raises(ValueError):
            dr.try_read_header()

        assert dr.header is None

    def test_invalid_header_values(self):
        data = header(led_count=1, fps=60)
        d = {"abc": 1}
        data.entries[0] = f"#{json.dumps(d)}" + linesep

        dr = DataReader(data.read)
        dr.update_buffer()
        with pytest.raises(ValueError):
            dr.try_read_header()

        assert dr.header is None

    def test_header_not_atomic(self):
        data = header(led_count=1, fps=60)
        h = data.entries[0]
        data.entries[0] = h[: len(h) // 2]

        dr = DataReader(data.read)
        dr.update()

        assert dr.header is None

        data.entries.insert(1, h[len(h) // 2 :])
        dr.update()

        assert dr.header is not None

    def test_frame(self):
        data = header(led_count=1, fps=60) + 0

        dr = DataReader(data.read)
        dr.update()

        assert dr.frames == [data.jelka[0]]

    def test_comments(self, capfd):
        # Here we actually print stuff, so newline must be used normally
        data = header(led_count=1, fps=60) + "abc" + 0 + "This is a random comment" + "nst\n" + "hmhm"
        data.entries.insert(0, "This is a random comment before everything")
        data.user.insert(0, "This is a random comment before everything")

        dr = DataReader(data.read)
        dr.update()

        assert dr.frames == [data.jelka[0]]
        assert data.user == ["This is a random comment before everything", "abc", "This is a random comment", "nst\n", "hmhm"]

        dr.user_print()
        out, err = capfd.readouterr()
        assert out == "This is a random comment before everythingabcThis is a random commentnst\nhmhm"

    def test_frames(self):
        data = header(led_count=1, fps=60) + 0 + 1

        dr = DataReader(data.read)

        for i, frame in enumerate(dr):
            if i == 4:
                break

            assert frame == data.jelka[i]

            if i == 1:
                # add some more frames
                data + 2 + 3

    def test_frames_missing(self):
        data = header(led_count=1, fps=60) + 0 + 1

        dr = DataReader(data.read)

        for i, frame in enumerate(dr):
            if i == 4:
                break
            # missing frames should be the last avaiable frame
            assert frame == data.jelka[min(i, len(data.jelka) - 1)]

        assert len(dr.frames) == 2

    def test_no_frames(self):
        data = header(led_count=5, fps=60)

        dr = DataReader(data.read)

        for i, frame in enumerate(dr):
            if i == 4:
                break
            assert frame == [(0, 0, 0)] * 5

    def test_frames_late(self):
        """First frames come after they were required, the last two frames never come."""

        data = header(led_count=5, fps=60)

        dr = DataReader(data.read)

        for i, frame in enumerate(dr):
            if i == 4:
                break
            if i <= 1:
                assert frame == [(0, 0, 0)] * 5
            if i == 1:
                data + 0 + 1
            if i >= 2:
                assert frame == random_frame(5, 1)

    def test_invalid_frame(self):
        data = header(led_count=1, fps=60)
        data.entries.append("#Invalid frame" + linesep)

        dr = DataReader(data.read)

        with pytest.raises(ValueError):
            dr.update()

    def test_frame_not_atomic(self):
        data = header(led_count=1, fps=60) + 0

        dr = DataReader(data.read)

        # cut the frame in half
        f = data.entries[-1]
        data.entries[-1] = f[: len(f) // 2]

        dr.update()
        assert dr.frames == []
        data.entries.append(f[len(f) // 2 :])
        dr.update()
        assert dr.frames == [data.jelka[0]]

        # last byte is missing
        data + 1

        f = data.entries[-1]
        data.entries[-1] = f[:-2]
        dr.update()
        assert dr.frames == [data.jelka[0]]
        data.entries.append(f[-2:])
        dr.update()
        assert dr.frames == [data.jelka[0], data.jelka[1]]

        # first byte is missing
        data + 2

        f = data.entries[-1]
        data.entries[-1] = f[1]
        dr.update()
        assert dr.frames == [data.jelka[0], data.jelka[1]]
        data.entries.append(f[1:])
        dr.update()

    def test_all_basic(self):
        led_count = 3
        duration = 4
        data = header(led_count=led_count, fps=60) + 0 + "Random text" + 1 + 2 + 4 + "jabfhsb"

        dr = DataReader(data.copy().read)

        dr.update_buffer()
        dr.try_read_header()

        assert dr.header == {
            "led_count": led_count,
            "fps": 60,
            "version": 0,
        }

        dr.try_read_frames()

        assert dr.frames == data.jelka

        for framei, frame in enumerate(DataReader(data.copy().read)):
            if framei == duration:
                break

            assert frame == data.jelka[framei]
