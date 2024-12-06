"""
This file defines utilities for working with data and files of various types.
"""
import os
import csv
import dataclasses
import gzip
import itertools
import json
import logging
import os
import pandas as pd
from urllib.parse import urlparse
from collections.abc import Iterator
from functools import partial
from pathlib import Path
from typing import Any, Sequence, Union
import blobfile as bf
import lz4.frame
import pydantic
import pyzstd

logger = logging.getLogger(__name__)

DEFAULT_PATHS = [Path.cwd() / "data", Path.home() / ".llmbench/data", Path.cwd() / "../data", Path(os.path.dirname(__file__) + "/../../data")]


def open_by_file_pattern(filepath: str, mode: str = "r", **kwargs: Any) -> Any:
    """Can read/write to files on gcs/local with or without gzipping. If file
    is stored on gcs, streams with blobfile. Otherwise use vanilla python open. If
    filename endswith gz, then zip/unzip contents on the fly (note that gcs paths and
    gzip are compatible)"""
    open_fn = partial(bf.BlobFile, **kwargs)

    try:
        if filepath.endswith(".gz"):
            return gzip_open(filepath, openhook=open_fn, mode=mode)
        elif filepath.endswith(".lz4"):
            return lz4_open(filepath, openhook=open_fn, mode=mode)
        elif filepath.endswith(".zst"):
            return zstd_open(filepath, openhook=open_fn, mode=mode)
        else:
            scheme = urlparse(filepath).scheme
            if scheme == "" or scheme == "file":
                return open_fn(filepath, mode=mode)
            return open_fn(filepath, mode=mode)
    except Exception as e:
        raise RuntimeError(f"Failed to open: {filepath}") from e


def gzip_open(filename: str, mode: str = "rb", openhook: Any = open) -> gzip.GzipFile:
    """Wrap the given openhook in gzip."""
    if mode and "b" not in mode:
        mode += "b"

    return gzip.GzipFile(fileobj=openhook(filename, mode), mode=mode)


def lz4_open(filename: str, mode: str = "rb", openhook: Any = open) -> lz4.frame.LZ4FrameFile:
    if mode and "b" not in mode:
        mode += "b"

    return lz4.frame.LZ4FrameFile(openhook(filename, mode), mode=mode)


def zstd_open(filename: str, mode: str = "rb", openhook: Any = open) -> pyzstd.ZstdFile:
    if mode and "b" not in mode:
        mode += "b"

    return pyzstd.ZstdFile(openhook(filename, mode), mode=mode)


def _get_jsonl_file(path, max_line_num: int = 5000):
    logger.info(f"Fetching {path}")
    with open_by_file_pattern(path, mode="r") as f:
        lines = []
        for line in f.readlines()[:max_line_num]:
            if len(line) > 5:
                data = json.loads(line)
                lines.append(data)
                # lines.append("\n".join(content).lstrip())
        return lines


def _get_json_file(path):
    logger.info(f"Fetching {path}")
    with open_by_file_pattern(path, mode="r") as f:
        return json.loads(f.read())


def _stream_jsonl_file(path) -> Iterator:
    logger.info(f"Streaming {path}")
    with bf.BlobFile(path, "r", streaming=True) as f:
        for line in f:
            yield json.loads(line)


def get_lines(path) -> list[dict]:
    """
    Get a list of lines from a file.
    """
    with open_by_file_pattern(path, mode="r") as f:
        return f.readlines()


def get_jsonl(path: str, max_line_num: int) -> list[dict]:
    """
    Extract json lines from the given path.
    If the path is a directory, look in subpaths recursively.

    Return all lines from all jsonl files as a single list.
    """
    if bf.isdir(path):
        result = []
        for filename in bf.listdir(path):
            if filename.endswith(".jsonl"):
                result += get_jsonl(os.path.join(path, filename))
        return result
    return _get_jsonl_file(path, max_line_num)


def get_jsonls(paths: Sequence[str], line_limit=None) -> list[dict]:
    return list(iter_jsonls(paths, line_limit))


def get_json(path) -> dict:
    if bf.isdir(path):
        raise ValueError("Path is a directory, only files are supported")
    return _get_json_file(path)


def iter_jsonls(paths: Union[str, list[str]], line_limit=None) -> Iterator[dict]:
    """
    For each path in the input, iterate over the jsonl files in that path.
    Look in subdirectories recursively.

    Use an iterator to conserve memory.
    """
    if isinstance(paths, str):
        paths = [paths]

    def _iter():
        for path in paths:
            if bf.isdir(path):
                for filename in bf.listdir(path):
                    if filename.endswith(".jsonl"):
                        yield from iter_jsonls([os.path.join(path, filename)])
            else:
                yield from _stream_jsonl_file(path)

    return itertools.islice(_iter(), line_limit)


def get_csv(path, fieldnames=None):
    with bf.BlobFile(path, "r", cache_dir="/tmp/bf_cache", streaming=False) as f:
        reader = csv.DictReader(f, fieldnames=fieldnames)
        return [row for row in reader]


def _to_py_types(o: Any) -> Any:
    if isinstance(o, dict):
        return {k: _to_py_types(v) for k, v in o.items()}
    if isinstance(o, list):
        return [_to_py_types(v) for v in o]

    if dataclasses.is_dataclass(o):
        return _to_py_types(dataclasses.asdict(o))

    # pydantic data classes
    if isinstance(o, pydantic.BaseModel):
        return json.loads(o.json())

    return o


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> str:
        return _to_py_types(o)


def jsondumps(o: Any, ensure_ascii: bool = False, **kwargs: Any) -> str:
    return json.dumps(o, cls=EnhancedJSONEncoder, ensure_ascii=ensure_ascii, **kwargs)


def jsondump(o: Any, fp: Any, ensure_ascii: bool = False, **kwargs: Any) -> None:
    json.dump(o, fp, cls=EnhancedJSONEncoder, ensure_ascii=ensure_ascii, **kwargs)


def jsonloads(s: str, **kwargs: Any) -> Any:
    return json.loads(s, **kwargs)


def jsonload(fp: Any, **kwargs: Any) -> Any:
    return json.load(fp, **kwargs)


def get_file_lines(dataset: str, max_line_num: int = 5000):
    for file_path in DEFAULT_PATHS:
        for root, dirs, files in os.walk(file_path):
            for file in files:
                if Path(file).stem == dataset:
                    if Path(file).suffix.endswith(".txt"):
                        return get_lines(os.path.join(root, file))
                    if Path(file).suffix.endswith(".jsonl"):
                        return get_jsonl(os.path.join(root, file), max_line_num)
                    if Path(file).suffix.endswith(".xlsx"):
                        df = pd.read_excel(os.path.join(root, file))
                        return df.to_dict(orient='records')
