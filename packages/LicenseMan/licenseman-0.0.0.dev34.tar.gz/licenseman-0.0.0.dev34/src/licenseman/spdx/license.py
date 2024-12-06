from __future__ import annotations as _annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING
import datetime as _dt
from xml.etree import ElementTree as _ElementTree
from dataclasses import dataclass as _dataclass

from licenseman.spdx.license_text import SPDXLicenseTextPlain
from licenseman.spdx.entry import SPDXEntry

if _TYPE_CHECKING:
    from typing import Literal


@_dataclass
class SPDXLicenseCrossRef:
    """SPDX License cross reference."""
    url: str
    order: int
    timestamp: _dt.datetime
    match: str
    valid: bool
    live: bool
    wayback: bool


class SPDXLicense(SPDXEntry):
    """SPDX License definition.

    Parameters
    ----------
    xml
        SPDX license XML content as a string.

    References
    ----------
    - [SPDX Docs](https://github.com/spdx/license-list-XML/blob/main/DOCS/README.md)
    - [SPDX Docs - XML Fields](https://github.com/spdx/license-list-XML/blob/main/DOCS/xml-fields.md)
    - [XML Schema](https://github.com/spdx/license-list-XML/blob/main/schema/ListedLicense.xsd)
    - [GitHub Repository](https://github.com/spdx/license-list-XML)
    """

    def __init__(self, data: dict, verify: bool = True):
        super().__init__(data=data, entry_type="license", verify=verify)
        return

    def generate_header_plain(
        self,
        title: str | bool = True,
        copyright_notice: str | bool = False,
        optionals: bool | list[bool] = True,
        alts: dict[str, str] | None = None,
        line_length: int = 88,
        list_indent: int = 0,
        item_indent: int = 1,
        item_spacing: int = 1,
        bullet: str | int | None = 1,
        title_centered: bool = False,
        title_underline: Literal["-", "=", "_", "*"] = "=",
        title_underline_full: bool = False,
        subtitle_underline: Literal["-", "=", "_", "*"] = "-",
        line_breaks: int = 2,
    ) -> str:
        if not self.header_xml:
            return ""
        return SPDXLicenseTextPlain(text=self.header_xml).generate(
            title=title,
            copyright_notice=copyright_notice,
            optionals=optionals,
            alts=alts,
            line_length=line_length,
            list_indent=list_indent,
            item_indent=item_indent,
            item_spacing=item_spacing,
            bullet=bullet,
            title_centered=title_centered,
            title_underline=title_underline,
            title_underline_full=title_underline_full,
            subtitle_underline=subtitle_underline,
            line_breaks=line_breaks,
        )

    @property
    def header_plain(self) -> str | None:
        """Original license header in plain text format."""
        return self._data.get("standardLicenseHeader")

    @property
    def header_template(self) -> str | None:
        """License header template."""
        return self._data.get("standardLicenseHeaderTemplate")

    @property
    def header_html(self) -> str | None:
        """Original license header in HTML format."""
        return self._data.get("standardLicenseHeaderHtml")

    @property
    def header_xml(self) -> _ElementTree.Element | None:
        return self._xml.find('.//standardLicenseHeader', self._ns)

    @property
    def header_xml_str(self) -> str | None:
        return self._xml_str(self.header_xml) if self.header_xml else None

    @property
    def cross_refs(self) -> list[SPDXLicenseCrossRef]:
        """URLs to license resources, if any."""
        return [
            SPDXLicenseCrossRef(
                url=ref["url"],
                order=ref["order"],
                timestamp=_dt.datetime.strptime(ref["timestamp"], "%Y-%m-%dT%H:%M:%SZ"),
                match=ref["match"],
                valid=ref["isValid"],
                live=ref["isLive"],
                wayback=ref["isWayBackLink"]
            ) for ref in self._data.get("crossRef", [])
        ]

    @property
    def osi_approved(self) -> bool:
        """Whether the license is OSI approved.

        Returns
        -------
        A boolean, or `None` if the value is not defined in the data.
        """
        return self._data["isOsiApproved"]

    @property
    def fsf_libre(self) -> bool | None:
        """Whether the license is FSF approved.

        Returns
        -------
        A boolean, or `None` if the value is not defined in the data.
        """
        return self._data.get("isFsfLibre")

    def __repr__(self):
        return f"<SPDXLicense {self.id}>"
