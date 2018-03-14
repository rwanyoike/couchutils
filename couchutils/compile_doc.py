"""Functions to build CouchDB documents from a directory."""

import json
import os
from pathlib import Path


def _get_file_content(path):
    """Return a file's content (json or text).

    :param str path: The file.
    :rtype: object
    """
    path = Path(path)
    file_text = path.read_text()

    if path.suffix == '.json':
        return json.loads(file_text)

    return file_text.strip()


def _get_last_doc_ref(path, doc):
    """Mutate a document top-down using a path.

    :param str parts: The path.
    :param dict doc: The document.
    :rtype: dict
    """
    path = Path(path)

    for part in path.parts:
        if part not in doc:
            doc[part] = {}
        doc = doc[part]

    return doc


def parse_directory(path):
    """Return a document parsed from a directory.

    :param str path: The directory.
    :rtype: dict
    """
    path = Path(path)
    doc = {}

    for root, dirs, files in os.walk(path, topdown=False):
        root_path = Path(root)
        obj = {}
        for file in files:
            file_path = root_path / file
            content = _get_file_content(file_path)
            f = file_path.with_suffix('')
            obj[f.name] = content
        rel_path = root_path.relative_to(path)
        ref = _get_last_doc_ref(rel_path, doc)
        ref.update(obj)

    return doc


def parse_file(path):
    """Return a document parsed from a file.

    :param str path: The file.
    :rtype: dict
    """
    path = Path(path)

    if path.suffix == '.json':
        return json.loads(path.read_text())

    return {}


def compile_doc(target):
    """Build CouchDB documents from a directory.

    :param target: The directory.
    :rtype: dict
    """
    docs = {}

    for child in Path(target).iterdir():
        if child.is_dir():
            doc = parse_directory(child)
        if child.is_file():
            doc = parse_file(child)
        if doc != {}:
            # TODO: Raise exception for missing _ids
            docs[doc['_id']] = doc

    return docs
