"""Process SPDX [license expressions](https://spdx.github.io/spdx-spec/v3.0.1/annexes/spdx-license-expressions/).

See Also
--------
- https://pypi.org/project/license-expression/
"""

import re as _re

from licenseman import spdx as _spdx


def ids(expression: str) -> tuple[list[str], list[str]]:
    """Get all SPDX license and exception IDs from an expression.

    Parameters
    ----------
    expression
        SPDX license expression.

    Returns
    -------
    List of registered and custom SPDX license and exception IDs in the expression.
    """
    license_ids, license_ids_custom = license_ids(expression)
    exception_ids, exception_ids_custom = exception_ids(expression)
    return license_ids + exception_ids, license_ids_custom + exception_ids_custom


def license_ids(expression: str) -> tuple[list[str], list[str]]:
    """Get all SPDX license IDs from an expression.

    Parameters
    ----------
    expression
        SPDX license expression.

    Returns
    -------
    List of registered and custom SPDX license IDs in the expression.
    """
    return _get_ids(expression, exception=False)


def exception_ids(expression: str) -> tuple[list[str], list[str]]:
    """Get all SPDX license exception IDs from an expression.

    Parameters
    ----------
    expression
        SPDX license expression.

    Returns
    -------
    List of registered and custom SPDX license exception IDs in the expression.
    """
    return _get_ids(expression, exception=True)


def _get_ids(expression: str, exception: bool):
    list_ = _spdx._get_global_exception_list() if exception else _spdx._get_global_license_list()
    ids = sorted(list_.ids, key=len, reverse=True)  # Sort by length to match longest IDs first, e.g. 'GPL-3.0-only' before 'GPL-3.0'
    registered = _re.findall(
        rf"({'|'.join(_re.escape(exception_id) for exception_id in ids)})",
        expression
    )
    customs = _re.findall(
        rf"(?:DocumentRef-[a-zA-Z0-9-.]+:)?{'AdditionRef' if exception else 'LicenseRef'}-[a-zA-Z0-9.-]+",
        expression
    )
    return registered, customs
