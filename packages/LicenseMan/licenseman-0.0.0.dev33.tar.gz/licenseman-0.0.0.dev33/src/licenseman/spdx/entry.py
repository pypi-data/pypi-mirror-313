from __future__ import annotations as _annotations

import copy as _copy
from typing import TYPE_CHECKING as _TYPE_CHECKING
import datetime as _dt
from xml.etree import ElementTree as _ElementTree

from licenseman import logger as _logger
from licenseman.spdx.license_text import SPDXLicenseTextPlain

if _TYPE_CHECKING:
    from typing import Literal, Any



class SPDXEntry:
    """SPDX License or exception definition.

    References
    ----------
    - [SPDX Docs](https://github.com/spdx/license-list-XML/blob/main/DOCS/README.md)
    - [SPDX Docs - XML Fields](https://github.com/spdx/license-list-XML/blob/main/DOCS/xml-fields.md)
    - [XML Schema](https://github.com/spdx/license-list-XML/blob/main/schema/ListedLicense.xsd)
    - [GitHub Repository](https://github.com/spdx/license-list-XML)
    """

    def __init__(self, data: dict, entry_type: Literal["license", "exception"], verify: bool = True):
        try:
            root = _ElementTree.fromstring(data["xml"])
        except _ElementTree.ParseError as e:
            raise Exception(f"Error parsing license XML content.") from e
        self._ns_url = 'http://www.spdx.org/license'
        self._ns: dict = {'': self._ns_url}
        self._xml: _ElementTree.Element = root.find(entry_type, self._ns)
        self._entry_type: Literal["license", "exception"] = entry_type
        self._data: dict = data
        if verify:
            self.verify()
        return

    def verify(self):

        def log(key_json: str, missing_in: Literal["xml", "json"], data: Any, key_xml: str | None = None):
            if key_xml is None:
                key_xml = key_json
            if missing_in == "xml":
                missing_source = "XML"
                existing_source = "JSON"
                missing_key = key_xml
                existing_key = key_json
            else:
                missing_source = "JSON"
                existing_source = "XML"
                missing_key = key_json
                existing_key = key_xml
            _logger.notice(
                f"{self.id} License{" Exception" if self._entry_type == "exception" else ""} Verification",
                f"The value of '{missing_key}' is not defined in the {missing_source} data. "
                f"Using the {existing_source} data value of '{existing_key}':",
                _logger.pretty(data)
            )
            return

        def osi_approved():
            key = "isOsiApproved"
            xml_raw = self._xml.attrib.get(key)
            if xml_raw == "true":
                xml = True
            elif xml_raw == "false":
                xml = False
            else:
                if xml_raw is not None:
                    raise Exception(f"Invalid value for '{key}' in XML data: {xml_raw}")
                xml = None
            json = self._data[key]
            if json != xml:
                if xml is None:
                    log(key, "xml", json)
                    return
                if json is None:
                    log(key, "json", xml)
                    self._data[key] = xml
                    return
                raise Exception(
                    "OSI approved mismatch between XML and JSON data. "
                    f"XML: {xml}, JSON: {json}"
                )
            return

        def deprecated_version():
            key = "deprecatedVersion"
            xml = self._xml.attrib.get(key)
            json = self._data.get(key)
            if json != xml:
                if xml is None:
                    log(key_json=key, missing_in="xml", data=json)
                elif json is None:
                    log(key_json=key, missing_in="json", data=xml)
                    self._data[key] = xml
                else:
                    raise Exception(
                        "Deprecated version mismatch between XML and JSON data. "
                        f"XML: {xml}, JSON: {json}"
                    )
            return

        def cross_refs():
            xml_elem = self._xml.find('crossRefs', self._ns)
            xml = sorted(
                [ref.text.strip() for ref in xml_elem.findall('crossRef', self._ns)]
            ) if xml_elem else []
            json_seealso = sorted(self._data.get("seeAlso", []))

            if json_seealso != xml:
                if not xml:
                    log("seeAlso", "xml", data=json_seealso)
                    return
                if not json_seealso:
                    log("seeAlso", "json", data=xml, key_xml="crossRefs")
                    self._data["seeAlso"] = xml
                    return
                raise Exception(
                    "Cross references mismatch between XML and JSON data. "
                    f"XML: {xml}, JSON: {json_seealso}"
                )
            if self._entry_type == "license":
                json = sorted([ref["url"] for ref in self._data.get("crossRef", [])])
                if json != json_seealso:
                    raise Exception(
                        "Cross references mismatch between 'crossRefs' and 'seeAlso' JSON data. ",
                        f"CrossRefs: {json}, SeeAlso: {json_seealso}"
                    )
            return

        if self.id != self._xml.attrib.get('licenseId'):
            raise Exception("License ID mismatch between XML and JSON data.")
        if self._data["name"] != self._xml.attrib.get('name'):
            raise Exception("License name mismatch between XML and JSON data.")

        deprecated_version()
        cross_refs()
        if self._entry_type == "license":
            osi_approved()
        return

    def generate_text_plain(
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
        return SPDXLicenseTextPlain(text=self.text_xml).generate(
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
    def raw_data(self) -> dict:
        """Raw license data."""
        return self._data

    @property
    def id(self) -> str:
        """SPDX license ID."""
        return self._data["licenseId" if self._entry_type == "license" else "licenseExceptionId"]

    @property
    def name(self) -> str:
        """Full name of the license"""
        return self._data["name"]

    @property
    def text_plain(self) -> str:
        """Original license text in plain text format."""
        return self._data["licenseText" if self._entry_type == "license" else "licenseExceptionText"]

    @property
    def text_template(self) -> str | None:
        """License text template."""
        return self._data.get("standardLicenseTemplate" if self._entry_type == "license" else "licenseExceptionTemplate")

    @property
    def text_html(self) -> str | None:
        """Original license text in HTML format."""
        return self._data.get("licenseTextHtml" if self._entry_type == "license" else "exceptionTextHtml")

    @property
    def text_xml(self) -> _ElementTree.Element:
        return self._xml.find('text', self._ns)

    @property
    def text_xml_str(self) -> str:
        return self._xml_str(self.text_xml)

    @property
    def title_text_xml(self) -> _ElementTree.Element | None:
        """Title of the license as defined in the text, if any."""
        return self._xml.find('.//titleText', self._ns)

    @property
    def copyright_text_xml(self) -> _ElementTree.Element | None:
        """Copyright notice of the license is defined in the text, if any."""
        return self._xml.find('.//copyrightText', self._ns)

    @property
    def optionals_xml(self) -> list[_ElementTree.Element]:
        """Optional fields in the license text, if any."""
        return self._xml.findall('.//optional', self._ns)

    @property
    def optionals_xml_str(self) -> list[str]:
        """Optional fields in the license text, if any."""
        out = []
        for optional in self.optionals_xml:
            out.append(self._xml_str(optional))
        return out

    @property
    def alts(self) -> dict[str, dict[str, str]]:
        """

        Returns
        -------
        A dictionary where keys are the alternative field names, and values are dictionaries with keys:
        `text` : str

            Default value.
        `match` : str

            Regular expression (RegEx) pattern to validate user input for `text`.
        """
        alts = {}
        for alt in self._xml.findall('.//alt', self._ns):
            alts[alt.attrib['name']] = {'text': alt.text, 'match': alt.attrib['match']}
        return alts

    @property
    def reference_number(self) -> int:
        """Reference number of the license."""
        return self._data["referenceNumber"]

    @property
    def url_reference(self) -> str:
        """URL to the license reference page at SPDX.org."""
        return self._data["reference"]

    @property
    def url_json(self) -> str:
        """URL to the license JSON data."""
        return self._data["detailsUrl"]

    @property
    def url_cross_refs(self) -> list[str]:
        """URLs to license resources, if any."""
        return self._data.get("seeAlso", [])

    @property
    def deprecated(self) -> bool:
        """Whether the license is deprecated.

        Returns
        -------
        A boolean, or `None` if the value is not defined in the data.
        """
        return self._data["isDeprecatedLicenseId"]

    @property
    def version_deprecated(self) -> str | None:
        """Version of the SPDX License List in which the license was deprecated, if applicable.

        Returns
        -------
        Version number string, or `None` if the value is not defined in the data.
        """
        return self._data.get("deprecatedVersion")

    @property
    def obsoleted_by(self) -> list[dict[str, str]] | None:
        """New licenses that obsolete this license, if any.

        Returns
        -------
        A list of dictionaries with keys:
        `id` : str

             SPDX license ID of the successor license.
        `expression` : str

             [SPDX license expression](https://spdx.github.io/spdx-spec/v3.0.1/annexes/spdx-license-expressions/)
             which is obsoleted by the successor license;
             in most cases, this is the same as the current license's ID, unless the current license
             is a complex expression, and only a part of it is obsoleted by the successor.
        """
        return [
            {"id": elem.text, "expression": elem.attrib.get("expression")}
            for elem in self._xml.findall('.//obsoletedBy', self._ns)
        ]

    @property
    def version_added(self) -> str | None:
        """Version of the SPDX License List in which the license was first added.

        Returns
        -------
        Version number string, or `None` if the value is not defined in the data.
        """
        return self._xml.attrib.get('listVersionAdded')

    @property
    def comments(self) -> str | None:
        """Comments about the license, if any."""
        return self._data.get("licenseComments")

    @property
    def notes(self) -> str | None:
        """General comments about the entry, if any."""
        elem = self._xml.find('notes', self._ns)
        return elem.text if elem is not None else None

    @property
    def xml(self) -> _ElementTree.Element:
        return self._xml

    @property
    def xml_attributes(self) -> dict[str, str]:
        return self._xml.attrib

    @property
    def xml_tags(self) -> list[str]:
        """Set of all XML tags used in the license."""
        def traverse(elem):
            tags.add(elem.tag.removeprefix(f"{{{self._ns_url}}}"))
            for child in elem:
                traverse(child)
            return

        tags = set()
        traverse(self._xml)
        return list(tags)

    def xml_tag_paths(self, tag: str) -> list[str]:
        """Get all paths to XML elements with a specific tag."""

        def find_paths(current_element, current_path):
            # Construct the current element's path
            current_tag = current_element.tag.removeprefix(f"{{{self._ns_url}}}")
            new_path = f"{current_path}/{current_tag}" if current_path else current_tag
            if current_tag == tag:
                paths.append(new_path)
            for child in current_element:
                find_paths(child, new_path)
            return

        paths = []
        find_paths(self._xml, "")
        return paths

    def __repr__(self):
        return f"<SPDXEntry {self.id}>"

    def __str__(self):
        return self.text_plain

    @staticmethod
    def _xml_str(element: _ElementTree.Element):
        optional_copy = _copy.deepcopy(element)
        optional_copy.tail = None
        return _ElementTree.tostring(
            optional_copy,
            encoding='unicode',
            xml_declaration=True,
        )