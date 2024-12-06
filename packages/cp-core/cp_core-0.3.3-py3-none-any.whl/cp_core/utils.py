import base64
import io
import platform

# import PySimpleGUIWx as sg  # noqa
# import PySimpleGUIQt as sg
# import PySimpleGUI as sg
from dataclasses import dataclass

import pandas as pd


def is_windows():
    return platform.system() == "Windows"


def read_csv(filename) -> pd.DataFrame:
    """read csv encoding utf-8 or gbk"""
    try:
        data = pd.read_csv(filename)
    except UnicodeDecodeError:
        data = pd.read_csv(filename, encoding="gbk")
    return data


@dataclass
class Resp:
    status: str = "success"
    msg: str = "success"
    data: object = None

    def success(self):
        self.status = "success"
        return self

    def is_success(self):
        return self.status == "success"

    def failed(self):
        self.status = "failed"
        return self

    def is_failed(self):
        return self.status == "failed"


def convert_to_bytes(file_or_bytes, resize=None):
    """
    Will convert into bytes and optionally resize an image that is a file or a base64 bytes object.
    Turns into  PNG format in the process so that can be displayed by tkinter
    :param file_or_bytes: either a string filename or a bytes base64 image object
    :type file_or_bytes:  (Union[str, bytes])
    :param resize:  optional new size
    :type resize: (Tuple[int, int] or None)
    :return: (bytes) a byte-string object
    :rtype: (bytes)
    """
    import PIL.Image

    if isinstance(file_or_bytes, str):
        img = PIL.Image.open(file_or_bytes)
    else:
        try:
            img = PIL.Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
        except Exception as e:
            dataBytesIO = io.BytesIO(file_or_bytes)
            img = PIL.Image.open(dataBytesIO)

    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        scale = min(new_height / cur_height, new_width / cur_width)
        img = img.resize(
            (int(cur_width * scale), int(cur_height * scale)), PIL.Image.ANTIALIAS
        )
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()
