import hashlib
import math
import os
import random
import shutil
import string
import uuid
import zipfile
from datetime import date, datetime
from pathlib import Path
from types import GeneratorType
from typing import List, Any, Iterator

from pydantic import BaseModel


def id_generator() -> str:
    return str(uuid.uuid4())


def generate_random_string(length: int = 32, *, lower: bool = True, upper: bool = True, digit: bool = True) -> str:
    candidates = []
    if lower: candidates += string.ascii_lowercase
    if upper: candidates += string.ascii_uppercase
    if digit: candidates += string.digits
    assert len(candidates) > 0, 'Invalid random string generator, missing candidates.'
    return ''.join(random.choice(candidates) for i in range(length))


def is_pydantic_field_empty(obj: BaseModel, field: str) -> bool:
    return not hasattr(obj, field) or getattr(obj, field) is None


def date_to_datetime(d: date) -> datetime:
    if isinstance(d, date):
        return datetime.combine(d, datetime.min.time())
    return d


def datetime_to_date(d: datetime) -> date:
    if isinstance(d, datetime):
        return d.date()
    return d


# _hashu = lambda word: ctypes.c_uint64(hash(word)).value


def hash_string(arg: str) -> str:
    hash_object = hashlib.md5(arg.encode())
    return hash_object.hexdigest()

    # return str(hash(args))
    # return _hashu("".join(args)).to_bytes(8, "big").hex()


def slice_to_list(items: List[Any], slice_size: int) -> List[List[Any]]:
    """Convert 1D list to 2D list"""
    slices: List[List[Any]] = []
    current_slice: List[Any] = []
    for _d in items:
        current_slice.append(_d)
        if len(current_slice) >= slice_size:
            slices.append(current_slice)
            current_slice = []
    if len(current_slice) > 0:
        slices.append(current_slice)
    return slices


def bad_utf8_str_encoding(str_: str) -> str:
    return repr(str_)[1:-1]


def get_first_match(items: list, key_fn, value):
    """Return first match item in a list"""
    filtered = list(filter(lambda x: key_fn(x) == value, items))
    if len(filtered) >= 1:
        return filtered[0]
    # return None for not found
    return None


def ensure_has_folder(path: str) -> str:
    exist = os.path.exists(path)
    if not exist:
        # Create a new directory because it does not exist
        os.makedirs(path)
    return path


def yield_files(folder: str) -> Iterator[str | Path]:
    for filename in os.listdir(folder):
        f = os.path.join(folder, filename)
        if os.path.isfile(f):
            yield f
        elif os.path.isdir(f):
            yield from yield_files(f)


def get_files(folder: str) -> List[str | Path]:
    all_files = []
    for filename in os.listdir(folder):
        f = os.path.join(folder, filename)
        if os.path.isfile(f):
            all_files.append(f)
        elif os.path.isdir(f):
            all_files += get_files(f)
    return all_files


def zip_dir(folder: Path | str, zip_filepath: Path | str):
    """Zip the provided directory without navigating to that directory using `pathlib` module"""

    # Convert to Path object
    dir = Path(folder)

    with zipfile.ZipFile(zip_filepath, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for entry in dir.rglob("*"):
            zip_file.write(entry, entry.relative_to(dir))


def remove_dir(dir: Path | str):
    shutil.rmtree(dir, ignore_errors=True)


def wait_generator_stop(generator: GeneratorType, *, max_generate: int = 1000):
    generated = []
    attempts = 0
    while True:
        try:
            next_item = next(generator)
            generated.append(next_item)
        except StopIteration:
            break
        attempts += 1
        if attempts > max_generate:
            raise ValueError(f"Generator exceeded max generate allowance {max_generate}")


def is_mime_prefix_in(mime, mime_start: List[str]):
    assert mime is not None and "/" in mime, f"Invalid mime found: {mime}"
    start = mime.split('/')[0]
    return start in mime_start


def is_mime_image(mime: str):
    return is_mime_prefix_in(mime, ["image"])


video_mimes = [
    "video/x-msvideo",  # .avi
    "video/mp4",  # .mp4, .m4v
    "video/mpeg",  # .mpeg, .mpg
    "video/quicktime",  # .mov, .qt
    "video/vnd.vivo",  # .viv, .vivo
    "video/x-ms-wmv",  # .wmv
    "video/x-ms-asf",  # .asf, .asx
    "video/x-ms-wm",  # .wm
    "video/x-ms-wmx",  # .wmx
    "video/x-ms-wvx",  # .wvx
    "video/3gpp",  # .3gp, .3gpp
    "video/3gpp2",  # .3g2
    "video/h263",  # .h263
    "video/webm",  # .webm
    "video/x-matroska",  # .mkv
    "video/x-flv",  # .flv
    "video/ogg",  # .ogg, .ogv
    "video/h264",  # .h264
    "video/h265",  # .h265, .hevc
    "video/x-m4v",  # .m4v
    "application/x-troff-msvideo",  # .avi
    "video/avi",  # .avi
    "video/msvideo",  # .avi
    "video/x-dv",  # .dv
    "video/x-ivf",  # .ivf
    "video/x-la-asf",  # .lsf, .lsx
    "video/x-mng",  # .mng
    "video/x-ms-asf-plugin",  # .asf
    "video/x-ms-vob",  # .vob
    "video/x-mpg",  # .mpg
    "video/x-mpeg",  # .mpeg
    "video/x-mpeg2a",  # .mp2
    "video/x-pv-pvx",  # .pvx
    "video/x-qtc",  # .qtc
    "video/x-sgi-movie",  # .movie
]

audio_mimes = [
    "audio/3gpp",  # .3ga
    "audio/8svx",  # .8svx
    "audio/aac",  # .aac
    "audio/ac3",  # .ac3
    "audio/aiff",  # .aif, .aiff
    "audio/alac",  # .alac
    "audio/amr",  # .amr
    "audio/ape",  # .ape
    "audio/basic",  # .au
    "audio/x-dss",  # .dss
    "audio/flac",  # .flac
    "audio/x-flv",  # .flv
    "audio/mp4",  # .m4a, .m4b, .m4p, .m4r
    "audio/mpeg",  # .mp3, .mpga
    "audio/ogg",  # .ogg, .oga, .mogg
    "audio/opus",  # .opus
    "audio/qcelp",  # .qcp
    "audio/x-tta",  # .tta
    "audio/voc",  # .voc
    "audio/wav",  # .wav
    "audio/x-ms-wma",  # .wma
    "audio/wavpack",  # .wv
]

ms_excel_mimes = [
    "application/vnd.ms-excel",  # .xls
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",  # .xlsx
    "application/vnd.openxmlformats-officedocument.spreadsheetml.template",  # .xltx
    "application/vnd.ms-excel.sheet.macroEnabled.12",  # .xlsm
    "application/vnd.ms-excel.template.macroEnabled.12",  # .xltm
    "application/vnd.ms-excel.addin.macroEnabled.12",  # .xlam
    "application/vnd.ms-excel.sheet.binary.macroEnabled.12",  # .xlsb
]


def is_mime_video(mime: str):
    return is_mime_prefix_in(mime, ["video"]) or mime in video_mimes


def is_mime_audio(mime: str):
    return is_mime_prefix_in(mime, ["audio"]) or mime in audio_mimes


def is_mime_media(mime: str):
    return is_mime_prefix_in(mime, ["image", "video", "audio"])


def is_mime_ms_excel(mime: str):
    return mime in ms_excel_mimes


def is_mime_csv(mime: str):
    return mime == "text/csv"


def inline_string(string: str, max_len: int = 30):
    if string is None: return "<None Value>"
    s = string.replace("\n", "").replace("\t", "")
    if len(s) > max_len:
        return " < " + s[0:max_len] + "... > "
    else:
        return " < " + s + " > "