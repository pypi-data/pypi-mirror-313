from __future__ import annotations as _annotations
from typing import TYPE_CHECKING as _TYPE_CHECKING
from pathlib import Path as _Path
import json as _json

import platformdirs as _platdir
import pylinks as _pl
from pylinks.exception.api import WebAPIError as _WebAPIError

from licenseman import data as _data
from licenseman.spdx.exception import SPDXLicenseException
from licenseman.spdx.license_db import SPDXLicenseDB
from licenseman.spdx.exception_db import SPDXLicenseExceptionDB
from licenseman.spdx.license_list import SPDXLicenseList
from licenseman.spdx.exception_list import SPDXExceptionList
from licenseman.spdx.license import SPDXLicense
from licenseman.spdx import expression
from licenseman import logger

if _TYPE_CHECKING:
    from typing import Literal


URL_TEMPLATE_LICENSE_XML = "https://raw.githubusercontent.com/spdx/license-list-data/refs/heads/main/license-list-XML/{}.xml"
URL_TEMPLATE_LICENSE_JSON = "https://raw.githubusercontent.com/spdx/license-list-data/refs/heads/main/json/details/{}.json"

URL_TEMPLATE_EXCEPTION_XML = "https://raw.githubusercontent.com/spdx/license-list-data/refs/heads/main/license-list-XML/exceptions/{}.xml"
URL_TEMPLATE_EXCEPTION_JSON = "https://raw.githubusercontent.com/spdx/license-list-data/refs/heads/main/json/exceptions/{}.json"

URL_LICENSE_LIST = "https://spdx.org/licenses/licenses.json"
URL_EXCEPTION_LIST = "https://spdx.org/licenses/exceptions.json"


def license_db(
    path: str | _Path = _platdir.site_cache_path(
        appauthor="RepoDynamics",
        appname="LicenseMan",
    ) / "SPDX_DB" / "licenses",
    force_update: bool = False,
    verify: bool = True,
    in_memory: bool = False,
) -> SPDXLicenseDB:
    return _db(
        typ="license",
        path=_Path(path),
        force_update=force_update,
        verify=verify,
        in_memory=in_memory,
    )


def exception_db(
    path: str | _Path = _platdir.site_cache_path(
        appauthor="RepoDynamics",
        appname="LicenseMan",
    ) / "SPDX_DB" / "exceptions",
    force_update: bool = False,
    verify: bool = True,
    in_memory: bool = False,
) -> SPDXLicenseExceptionDB:
    return _db(
        typ="exception",
        path=_Path(path),
        force_update=force_update,
        verify=verify,
        in_memory=in_memory,
    )


def license_list() -> SPDXLicenseList:
    """Get the latest version of the [SPDX license list](https://spdx.org/licenses/) from SPDX website."""
    data = _pl.http.request(URL_LICENSE_LIST, response_type="json")
    return SPDXLicenseList(data)


def exception_list() -> SPDXExceptionList:
    """Get the latest version of the [SPDX exception list](https://spdx.org/licenses/exceptions-index.html) from SPDX website."""
    data = _pl.http.request(URL_EXCEPTION_LIST, response_type="json")
    return SPDXExceptionList(data)


def license(license_id: str, verify: bool = True) -> SPDXLicense:
    """Get an SPDX license.

    Parameters
    ----------
    license_id
        SPDX license ID, e.g., 'MIT', 'GPL-2.0-or-later'.
    """
    return _license(license_id, "license", verify)


def exception(exception_id: str, verify: bool = True) -> SPDXLicenseException:
    """Get an SPDX license exception.

    Parameters
    ----------
    exception_id
        SPDX license exception ID, e.g., 'Autoconf-exception-2.0'.
    """
    return _license(exception_id, "exception", verify)


def license_xml(license_id: str) -> str:
    """Get an SPDX license definition in XML format from SPDX
    [license-list-data](https://github.com/spdx/license-list-data) repository.

    Parameters
    ----------
    license_id
        SPDX license ID, e.g., 'MIT', 'GPL-2.0-or-later'.
    """
    return _download(license_id, format="xml")


def license_json(license_id: str) -> dict:
    """Get an SPDX license definition in XML format from SPDX
    [license-list-data](https://github.com/spdx/license-list-data) repository.

    Parameters
    ----------
    license_id
        SPDX license ID, e.g., 'MIT', 'GPL-2.0-or-later'.
    """
    return _download(license_id, format="json")


def exception_xml(exception_id: str) -> str:
    """Get an SPDX license exception definition in XML format from SPDX
    [license-list-data](https://github.com/spdx/license-list-data) repository.

    Parameters
    ----------
    exception_id
        SPDX license exception ID, e.g., 'Autoconf-exception-2.0'.
    """
    return _download(exception_id, format="xml", exception=True)


def exception_json(exception_id: str) -> dict:
    """Get an SPDX license exception definition in XML format from SPDX
    [license-list-data](https://github.com/spdx/license-list-data) repository.

    Parameters
    ----------
    exception_id
        SPDX license exception ID, e.g., 'Autoconf-exception-2.0'.
    """
    return _download(exception_id, format="json", exception=True)


def trove_classifier(license_id: str) -> str | None:
    """Get the Trove classifier for an SPDX license.

    Parameters
    ----------
    license_id
        SPDX license ID, e.g., 'MIT', 'GPL-2.0-or-later'.
    """
    return _get_global_trove_mapping().get(license_id)


def _db(
    typ: Literal["license", "exception"],
    path: _Path,
    force_update: bool = False,
    verify: bool = True,
    in_memory: bool = False,
) -> SPDXLicenseDB | SPDXLicenseExceptionDB:
    if typ == "license":
        name = "license"
        class_ = SPDXLicenseDB
        func = license
        list_ = _get_global_license_list()
    else:
        name = "license exception"
        class_ = SPDXLicenseExceptionDB
        func = exception
        list_ = _get_global_exception_list()

    name_title = name.title()
    ids = list_.ids
    if force_update or not path.is_dir():
        missing_ids = ids
        intro = "Force update is enabled" if force_update else f"SPDX {name} database not found at {path}"
        logger.log(
            "info" if force_update else "notice",
            f"SPDX {name_title} Database Load",
            f"{intro}; downloading all latest SPDX {name} data."
        )
    else:
        missing_ids = []
        for license_id in ids:
            if not (path / f"{license_id}.json").is_file():
                missing_ids.append(license_id)
        if not missing_ids:
            logger.success(
                f"SPDX {name_title} Database Load",
                f"Loaded database from {path}; all {len(ids)} {name}s files found."
            )
            return class_(
                list_,
                path,
                in_memory,
                verify,
            )
        num_missing = len(missing_ids)
        num_available = len(ids) - num_missing
        logger.log(
            "notice",
            f"SPDX {name_title} Database Load",
            f"Loaded database from {path}; "
            f"found {num_missing} missing license files (available: {num_available})."
        )
    path.mkdir(parents=True, exist_ok=True)
    licenses = {}
    for missing_id in missing_ids:
        output_path = path / f"{missing_id}.json"
        data = func(missing_id, verify=False if in_memory else verify)
        with open(output_path, "w") as f:
            _json.dump(data.raw_data, f)
        logger.success(
            f"SPDX {name_title} Database Update",
            f"Downloaded '{missing_id}' to 'file://{output_path}'.",
        )
        if in_memory:
            licenses[missing_id] = data
    return class_(
        list_,
        path,
        in_memory,
        verify,
        licenses,
    )


def _license(spdx_id: str, typ: Literal["license", "exception"], verify: bool = True) -> SPDXLicense | SPDXLicenseException:
    """Get an SPDX license or exception.

    Parameters
    ----------
    SPDX_id
        SPDX ID, e.g., 'MIT', 'GPL-2.0-or-later'.
    """
    if typ == "license":
        name = "license"
        func_json = license_json
        func_xml = license_xml
        class_ = SPDXLicense
        list_ = _get_global_license_list()
    else:
        name = "license exception"
        func_json = exception_json
        func_xml = exception_xml
        class_ = SPDXLicenseException
        list_ = _get_global_exception_list()

    data = func_json(spdx_id)
    data["xml"] = func_xml(spdx_id)
    name_title = name.title()

    for list_entry_key, list_entry_val in list_[spdx_id].items():
        # 'detailsUrl', 'reference', 'referenceNumber' are not present in JSON data
        if list_entry_key not in data:
            data[list_entry_key] = list_entry_val
            logger.info(
                f"SPDX JSON {name_title} Load",
                f"Added missing '{list_entry_key}' entry to '{spdx_id}' JSON data from {name} list."
            )
        elif data[list_entry_key] != list_entry_val:
            logger.warning(
                f"SPDX JSON {name_title} Load",
                f"Mismatched '{list_entry_key}' entry in '{spdx_id}' JSON data.",
                "JSON content:",
                logger.pretty(data[list_entry_key]),
                f"{name.capitalize()} list content:",
                logger.pretty(list_entry_val),
            )
    return class_(data, verify=verify)


def _download(
    spdx_id: str,
    format: Literal["xml", "json"],
    exception: bool = False,
) -> str | dict:
    if exception:
        url = URL_TEMPLATE_EXCEPTION_XML if format == "xml" else URL_TEMPLATE_EXCEPTION_JSON
    else:
        url = URL_TEMPLATE_LICENSE_XML if format == "xml" else URL_TEMPLATE_LICENSE_JSON
    try:
        data = _pl.http.request(
            url.format(spdx_id),
            response_type="str" if format == "xml" else "json"
        )
    except _WebAPIError as e:
        msg_typ = "license" if not exception else "license exception"
        msg_format = "XML" if format == "xml" else "JSON"
        msg = f"Error downloading {msg_typ} {msg_format} for ID '{spdx_id}"
        raise Exception(msg) from e
    return data


def _get_global_license_list() -> SPDXLicenseList:
    global _LICENSE_LIST
    if _LICENSE_LIST is None:
        _LICENSE_LIST = license_list()
    return _LICENSE_LIST


def _get_global_exception_list() -> SPDXExceptionList:
    global _EXCEPTION_LIST
    if _EXCEPTION_LIST is None:
        _EXCEPTION_LIST = exception_list()
    return _EXCEPTION_LIST


def _get_global_trove_mapping() -> dict[str, str]:
    global _TROVE_MAPPING
    if _TROVE_MAPPING is None:
        _TROVE_MAPPING = _data.spdx_to_trove_mapping()["map"]
    return _TROVE_MAPPING


_LICENSE_LIST: SPDXLicenseList | None = None
_EXCEPTION_LIST: SPDXExceptionList | None = None
_TROVE_MAPPING: dict[str, str] | None = None