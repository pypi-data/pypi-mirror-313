"""Functions for retrieving package data files."""

from __future__ import annotations as _annotations

from pathlib import Path as _Path

import pkgdata as _pkgdata
import pyserials as _ps

__all__ = ["get_filepath"]


def get_filepath(relative_path: str) -> _Path:
    """Get the absolute path to a package data file.

    Parameters
    ----------
    relative_path
        Path to the file relative to the package's data directory.
    """
    path_data_dir = _Path(_pkgdata.get_package_path_from_caller(top_level=False))
    filepath = path_data_dir / relative_path
    if not filepath.is_file():
        from licenseman.exception.data import DataFileNotFoundError

        raise DataFileNotFoundError(
            path_relative=relative_path,
            path_absolute=filepath,
        )
    return filepath


def spdx_to_trove_mapping() -> dict[str, str]:
    """Get the SPDX to Trove classifier mapping."""
    rel_path = "spdx/trove_classifiers.yaml"
    abs_path = get_filepath(rel_path)
    return _ps.read.yaml_from_file(abs_path)
