from __future__ import annotations as _annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING
import re as _re
from xml.etree import ElementTree as ET
from textwrap import TextWrapper as _TextWrapper

import mdit as _mdit

if _TYPE_CHECKING:
    from typing import Any, Literal


class SPDXLicenseText:
    """Base text generator for SPDX licenses.

    This parses the <text> element from an SPDX license XML.
    Subclasses should implement the missing methods to generate the full text and header.

    Parameters
    ----------
    text : xml.etree.ElementTree.Element
        The <text> XML element to parse.


    References
    ----------
    -  official matcher: https://github.com/spdx/spdx-license-matcher
    -  third-party matcher: https://github.com/MikeMoore63/spdx_matcher
    - Matching Guidelines: https://spdx.github.io/spdx-spec/v3.0.1/annexes/license-matching-guidelines-and-templates/
    """

    def __init__(self, text: ET.Element):
        self._text = text
        self._ns_uri = 'http://www.spdx.org/license'
        self._ns = {'': self._ns_uri}
        self._element_processor = {
            "titleText": self.title_text,
            "copyrightText": self.copyright_text,
            "standardLicenseHeader": self.standard_license_header,
            "list": self.list,
            "p": self.p,
            "br": self.br,
            "item": self.item,
            "bullet": self.bullet,
            "optional": self.optional,
            "alt": self.alt,
        }
        self._alt: dict = {}
        self._optionals: bool | list[bool] = True
        return

    def generate(
        self,
        alts: dict[str, str] | None = None,
        optionals: bool | list[bool] = True,
    ) -> Any:
        """Generate license full text and header.

        Parameters
        ----------
        alts : dict[str, int] | None, optional
            A dictionary specifying choices for <alt> elements. Keys are 'name' attributes,
            and values are the value to use.

        Returns
        -------
        The full text of the license, and the license header text, if present.
        """
        self._alt = alts or {}
        self._optionals = optionals
        return self.generate_full(self._text)

    def process(self, element: ET.Element) -> str:
        tag = self.clean_tag(element.tag)
        if tag not in self._element_processor:
            raise ValueError(f"Unsupported element: {tag}")
        processor = self._element_processor[tag]
        return processor(element)

    def get_alt(self, element: ET.Element) -> str:
        """Process an <alt> element by selecting the appropriate alternative based on `self._alt`.

        Parameters
        ----------
        element : xml.etree.ElementTree.Element
            The <alt> element.
        """
        name = element.get('name')
        match = element.get('match')
        if not name:
            raise ValueError("Alt element must have a 'name' attribute")
        if not match:
            raise ValueError("Alt element must have a 'match' attribute")
        text = self._alt.get(name)
        if not text:
            return element.text or ""
        if not _re.match(match, text):
            raise ValueError(f"Alt element '{name}' does not match '{match}'")
        return text

    def clean_tag(self, tag: str) -> str:
        """Strip the namespace URI from XML tag.

        Parameters
        ----------
        tag
            The XML tag with possible namespace.

        Returns
        -------
        The tag without namespace.
        """
        return tag.removeprefix(f'{{{self._ns_uri}}}')

    @staticmethod
    def clean_text(text: str) -> str:
        text_norm = _re.sub(r'\s+', ' ', text)
        if text_norm == " ":
            return ""
        return text_norm

    @staticmethod
    def element_has_text(element: ET.Element) -> bool:
        return bool(element.text and element.text.strip())

    @staticmethod
    def element_has_tail(element: ET.Element) -> bool:
        return bool(element.tail and element.tail.strip())

    def generate_full(self, text: ET.Element):
        raise NotImplementedError

    def generate_notice(self, sandard_license_header: ET.Element):
        raise NotImplementedError

    def title_text(self, element: ET.Element):
        raise NotImplementedError

    def copyright_text(self, element: ET.Element):
        raise NotImplementedError

    def standard_license_header(self, element: ET.Element):
        raise NotImplementedError

    def list(self, element: ET.Element):
        raise NotImplementedError

    def p(self, element: ET.Element):
        raise NotImplementedError

    def br(self, element: ET.Element):
        raise NotImplementedError

    def item(self, element: ET.Element):
        raise NotImplementedError

    def bullet(self, element: ET.Element):
        raise NotImplementedError

    def optional(self, element: ET.Element):
        raise NotImplementedError

    def alt(self, element: ET.Element):
        raise NotImplementedError


class SPDXLicenseTextPlain(SPDXLicenseText):
    """Plain-text generator for SPDX licenses.

    Parameters
    ----------
    text : xml.etree.ElementTree.Element
        The <text> XML element to parse.
    """

    def __init__(self, text: ET.Element):
        super().__init__(text)
        self._title: str | bool = True
        self._copyright: str | bool = False
        self._optionals: bool | list[bool] = True
        self._line_len: int = 88
        self._item_indent: int = 1
        self._item_spacing: int = 1
        self._current_list_nesting: int = 0
        self._list_indent: int = 4
        self._bullet: bool = True
        self._text_wrapper: _TextWrapper | None = None
        self._curr_bullet_len: int = 0
        self._title_centered: bool = True
        self._title_underline_full: bool = True
        self._title_underline: str = "="
        self._subtitle_underline: str = "–"
        self._count_optional = 0
        self._line_breaks = 2
        return

    def generate(
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
        """Generate plain-text license.

        Parameters
        ----------
        title
            Determines how to treat the license title, if any.
            Since the title is [optional](https://spdx.github.io/spdx-spec/v3.0.1/annexes/license-matching-guidelines-and-templates/#license-name-or-title)
            and not used in matching, it can be omitted or replaced with a custom title.
            If True, the title is included as-is. If False, the title is omitted.
            If a string, the title is replaced with the custom string, if a title is present.
        copyright_notice
            Determines how to treat the copyright notice, if any.
            Since the copyright notice is [optional](https://spdx.github.io/spdx-spec/v3.0.1/annexes/license-matching-guidelines-and-templates/#copyright-notice)
            and not used in matching, it can be omitted or replaced with a custom notice.
            If True, the notice is included as-is. If False, the notice is omitted.
            If a string, the notice is replaced with the custom string, if a notice is present.
        optionals : bool, optional
            Whether to include <optional> elements in the output, by default True.
        alts : dict[str, int] | None, optional
            A dictionary specifying choices for <alt> elements. Keys are 'name' attributes,
            and values are the value to use.
        line_length
            The maximum line length for the plain-text output.
        list_indent
            The number of spaces separating list items from the left margin.
        item_indent
            The number of spaces separating list items from the bullet character.
        item_spacing
            The number of newlines separating list items.
        bullet
            If `None`, the license's default bullet characters are used for list items.
            If a string, the specified character is used.
            If an integer, items are numbered starting from the specified number.
        title_centered
            Whether to center the title text.
        title_underline
            The character to use for underlining the title.
            Set to `None` to disable underlining.
        title_underline_full
            Whether to extend the underline to the full line length.
        subtitle_underline
            The character to use for underlining subtitles.
        line_breaks
            Number of newlines to add for each <br> element.

        Returns
        -------
        The plain-text version of the license
        plus the license header text, if present.
        """
        self._title = title
        self._copyright = copyright_notice
        self._optionals = optionals
        self._line_len = line_length
        self._text_wrapper = _TextWrapper(
            width=line_length,
            replace_whitespace=True,
            drop_whitespace=True,
            break_long_words=False,
            break_on_hyphens=False,
        )
        self._current_list_nesting = 0
        self._curr_bullet_len = 0
        self._count_optional = 0
        self._list_indent = list_indent
        self._item_indent = item_indent
        self._item_spacing = item_spacing
        self._bullet = bullet
        self._title_centered = title_centered
        self._title_underline = title_underline
        self._title_underline_full = title_underline_full
        self._subtitle_underline = subtitle_underline
        self._line_breaks = line_breaks
        fulltext = super().generate(alts=alts, optionals=optionals)
        return self.finalize(fulltext)

    def finalize(self, text: str | None) -> str:
        to_wrap_section_indices = []
        cleaned_sections = [[]]
        section_breaks = [0]
        in_break = False
        found_line = False
        for line in text.lstrip("\n").rstrip().splitlines():
            if not line.strip():
                section_breaks[-1] += 1
                in_break = True
                found_line = False
                continue
            if in_break:
                cleaned_sections.append([])
                section_breaks.append(0)
                in_break = False
            line_stripped = line.rstrip()
            if len(line_stripped) <= self._line_len:
                if not found_line:
                    cleaned_sections[-1].append(line_stripped)
                else:
                    line_indent = len(line) - len(line.lstrip())
                    last_line = cleaned_sections[-1][-1]
                    last_line_indent = len(last_line) - len(last_line.lstrip())
                    if last_line_indent == line_indent:
                        cleaned_sections[-1].append(line_stripped)
                    else:
                        cleaned_sections.append([line_stripped])
                        section_breaks.append(0)
                continue
            found_line = True
            if not cleaned_sections[-1]:
                cleaned_sections[-1].append(line_stripped)
            else:
                last_line = cleaned_sections[-1][-1]
                last_line_indent = len(last_line) - len(last_line.lstrip())
                current_line_indent = len(line) - len(line.lstrip())
                if last_line_indent == current_line_indent:
                    cleaned_sections[-1].append(line_stripped)
                else:
                    cleaned_sections.append([line_stripped])
                    section_breaks.append(0)
            to_wrap_section_indices.append(len(cleaned_sections) - 1)
        wrapped_sections = []
        for idx, section in enumerate(cleaned_sections):
            if idx in to_wrap_section_indices:
                wrapped_sections.append(self.wrap_text("\n".join(section)))
            else:
                wrapped_sections.append("\n".join(section))
            wrapped_sections.append("\n" * (section_breaks[idx] + 1))
        return f"{"".join(wrapped_sections).rstrip()}\n".replace(
            " .", "."
        ).replace(
            " ,", ","
        ).replace(
            " :", ":"
        ).replace(
            " ;", ";"
        ).replace(
            " )", ")"
        ).replace(
            " ]", "]"
        ).replace(
            " }", "}"
        ).replace(
            " !", "!"
        ).replace(
            " ?", "?"
        ).replace(
            "( ", "("
        ).replace(
            "[ ", "["
        ).replace(
            "{ ", "{"
        )

    def generate_full(self, text: ET.Element):
        return self.generic(text)

    def generic(
        self,
        element: ET.Element,
        return_list: bool = False,
    ) -> str | list[str]:
        """Recursively processes an XML element and its children.

        Parameters
        ----------
        element : xml.etree.ElementTree.Element
            The XML element to process.
        """
        # If the content begins on the same line as the tag, and has a leading space
        # (i.e. when first line has content with leading space)
        # then one space is added to the stripped text to preserve the leading space.
        # Similarly, if the content ends on the same line as the tag, and has a trailing space,
        # then one space is added to the end of the stripped text.

        # text_lines = text.splitlines()
        # space_start = bool(text_lines[0].strip() and text_lines[0].startswith(" ")) * " "
        # space_end = bool(text_lines[-1].strip() and text_lines[-1].endswith(" ")) * " "
        # space_normalized_text = _re.sub(r'\s+', ' ', text.strip())
        # space_normalized_text = f"{space_start}{space_normalized_text}{space_end}"
        # wrapped_text = self.wrap_text(space_normalized_text)
        # if space_normalized_text.endswith(" "):
        #     wrapped_text += " "
        # return wrapped_text

        out = []
        children = list(element)
        bullet_content = None
        for child_idx, child in enumerate(children):
            tag_name = self.clean_tag(child.tag)
            if tag_name not in self._element_processor:
                raise ValueError(f"Unsupported element: {tag_name}")
            content = self._element_processor[tag_name](child)
            if content:
                if not bullet_content:
                    out.append(content)
                else:
                    bullet_len = len(bullet_content)
                    bullet_content = None
                    self._curr_bullet_len -= bullet_len
                    content_lines = content.strip("\n").splitlines()
                    out.append(f"{content_lines[0].strip()}\n")
                    out.extend([f"{bullet_len * " "}{line}\n" for line in content_lines[1:]])
                    if self._subtitle_underline and len(content_lines) == 1:
                        num_chars = len(content_lines[0].strip()) + bullet_len
                        out.append(f"{self._subtitle_underline * num_chars}\n\n")
                    else:
                        out.append("\n\n")
            if tag_name == "bullet":
                # There is a bullet element outside of a list item.
                if self.element_has_tail(child):
                    if self._subtitle_underline:
                        num_chars = len(content.strip())
                        leading_spaces = (len(content) - len(content.lstrip(' '))) * " "
                        out.append(f"{leading_spaces}{self._subtitle_underline * num_chars}\n\n")
                else:
                    # The bullet has no text after it (example: CPL-1.0);
                    # Add the next element as the list item text.
                    bullet_content = content
                    self._curr_bullet_len += len(content)
        if self.element_has_text(element):
            out.insert(0, self.process_text(element.text))
        if self.element_has_tail(element):
            out.append(self.process_text(element.tail))
        if return_list:
            return out
        # full_raw = "".join([line.rstrip(" ") if line.strip() else "\n" for elem in out for line in elem.splitlines()])
        # paragraphs = [paragraph.strip() for paragraph in _re.split(r'\n\s*\n+', full_raw)]
        # processed = [self.wrap_text(paragraph) for paragraph in paragraphs]
        # return "\n\n".join(processed)
        return _re.sub(r'\n\s*\n\s*\n+', "\n\n", "".join(out)) + " "

    def standard_license_header(self, element: ET.Element):
        return self.generic(element)

    def title_text(self, element: ET.Element) -> str:
        """Process a <titleText> element."""
        if self._title is False:
            return ""
        title = self.generic(element) if self._title is True else self._title
        title_lines = []
        for line in title.splitlines():
            line = line.strip()
            if not line:
                continue
            if self._title_underline and all(char in ("-", "=", "_", "*") for char in line):
                continue
            if self._title_centered:
                line = line.center(self._line_len)
            title_lines.append(line)
        if self._title_underline:
            if self._title_underline_full:
                title_lines.append(self._title_underline * self._line_len)
            else:
                separator_line = self._title_underline * max(len(line) for line in title_lines)
                if self._title_centered:
                    separator_line = separator_line.center(self._line_len)
                title_lines.append(separator_line)
        title_lines.append("\n")
        return "\n".join(title_lines)

    def copyright_text(self, element: ET.Element) -> str:
        """Process a <copyrightText> element."""
        if self._copyright is False:
            return ""
        copyright_text = self.generic(element) if self._copyright is True else self._copyright
        return f"\n\n{copyright_text.strip()}\n\n"

    def optional(self, element: ET.Element) -> str:
        """
        Processes an <optional> element based on the include_optional flag.

        Parameters
        ----------
        element : xml.etree.ElementTree.Element
            The <optional> element.
        """
        include = self._optionals if isinstance(self._optionals, bool) else self._optionals[self._count_optional]
        self._count_optional += 1
        if not include:
            return self.process_text(element.tail or "")
        return self.generic(element)

    def list(self, elem: ET.Element) -> str:
        """
        Processes a <list> element containing <item> elements.

        Parameters
        ----------
        elem : xml.etree.ElementTree.Element
            The <list> element.
        """
        self._current_list_nesting += 1
        if elem.text and elem.text.strip():
            raise ValueError("List element should not have text content")
        if self._bullet:
            bullet_elems = elem.findall("./item/bullet", self._ns) + elem.findall("./item/p/bullet", self._ns)
            max_bullet_width = max([len(bullet.text.strip()) for bullet in bullet_elems], default=0)
        else:
            max_bullet_width = len(str(len(elem)))
        items = []
        for idx, child in enumerate(elem):
            tag = self.clean_tag(child.tag)
            if tag != 'item':
                raise ValueError(f"List element should only contain item elements, not {tag}")
            item_str = self.item(child, idx, max_bullet_width=max_bullet_width)
            item_str_indented = "\n".join(
                [f"{' ' * self._list_indent}{line}" for line in item_str.splitlines()])
            items.append(item_str_indented)
        self._current_list_nesting -= 1
        newlines = max(1, self._item_spacing + 1) * "\n"
        list_str = newlines.join(items)
        return f"{newlines}{list_str}{newlines}"

    def item(self, elem: ET.Element, idx: int, max_bullet_width: int) -> str:
        bullet_elems = elem.findall("./bullet", self._ns) + elem.findall("./p/bullet", self._ns)
        if len(bullet_elems) > 1:
            raise ValueError("Item element should contain at most one bullet element")
        if len(bullet_elems) == 1:
            bullet = bullet_elems[0].text.strip() if not self._bullet else (
                f"{idx + self._bullet}." if isinstance(self._bullet, int) else self._bullet
            )
            bullet_post_space = max_bullet_width + self._item_indent - len(bullet)
            bullet += bullet_post_space * " "
            subsequent_indent = len(bullet) * " "
        else:
            bullet = ""
            subsequent_indent = ""
        self._curr_bullet_len += len(bullet)
        content = []
        if elem.text:
            text = self.process_text(elem.text).lstrip()
            if text:
                content.append(text)
        for child in elem:
            tag = self.clean_tag(child.tag)
            if tag == 'bullet':
                if self.element_has_tail(child):
                    tail = self.process_text(child.tail)
                    content.append(tail)
            else:
                child_str = self.process(child)
                if child_str:
                    content.append(child_str.lstrip(" "))
            # if child.tail:
            #     tail = self.process_text(child.tail)
            #     if tail:
            #         needs_dedent = not content or content[-1].endswith("\n")
            #         content.append(tail.lstrip() if needs_dedent else tail)
        content_raw = "".join(content).strip()

        lines = content_raw.splitlines()
        wrapped = "\n".join(
            [f"{bullet}{lines[0] if lines else ""}"] + [f"{subsequent_indent}{line}" for line in lines[1:]]
        )
        self._curr_bullet_len -= len(bullet)
        return wrapped

    def p(self, element: ET.Element) -> str:
        """
        Processes a <p> element and appends its text to the output.

        Parameters
        ----------
        element : xml.etree.ElementTree.Element
            The <p> element.
        """
        out = [[]]
        if element.text:
            out[-1].append(element.text)
        for child in element:
            tag_name = self.clean_tag(child.tag)
            if tag_name not in self._element_processor:
                raise ValueError(f"Unsupported element: {tag_name}")
            if tag_name == "br":
                out.append([])
                if child.tail:
                    out[-1].append(child.tail)
            elif tag_name != "bullet":
                # Sometimes the <bullet> for <item> is placed inside a <p> element of that item.
                # Here we ignore the <bullet> element since `item()` will handle it.
                content = self._element_processor[tag_name](child)
                if content:
                    out[-1].append(content)
        if element.tail:
            out[-1].append(element.tail)

        paragraphs = []
        for paragraph_components in out:
            paragraph_raw = " ".join(paragraph_components)
            paragraph_normalized = _re.sub(r'\s+', ' ', paragraph_raw).strip()
            paragraphs.append(self.wrap_text(paragraph_normalized))
        return f"\n\n{("\n" * self._line_breaks).join(paragraphs)}\n\n"

    def alt(self, element: ET.Element) -> str:
        """Process an <alt> element by selecting the appropriate alternative based on `self._alt`.

        Parameters
        ----------
        element : xml.etree.ElementTree.Element
            The <alt> element.
        """
        element.text = super().get_alt(element)
        return self.p(element)

    def bullet(self, element: ET.Element) -> str:
        # This is only called when the bullet is outside of a list item.
        if list(element):
            raise ValueError("Bullet element should not have children")
        if not self.element_has_text(element):
            raise ValueError("Bullet element should have text content")
        bullet = f"{element.text.strip()}{" " * self._item_indent}"
        item = f"{bullet}{element.tail.strip()}" if self.element_has_tail(element) else bullet
        return f"\n{self.process_text(item)}\n"

    def br(self, element: ET.Element) -> str:
        if self.element_has_text(element):
            raise ValueError("BR element should not have text content")
        if list(element):
            raise ValueError("BR element should not have children")
        if self.element_has_tail(element):
            tail = self.process_text(element.tail)
        else:
            tail = ""
        return f"{"\n" * self._line_breaks}{tail} "

    def process_text(self, text: str) -> str:
        space_normalized_text = _re.sub(r'\s+', ' ', text.strip())
        wrapped_text = self.wrap_text(space_normalized_text)
        return f"{wrapped_text} "

    def wrap_text(self, text: str) -> str:
        """Wrap text to the specified line length, preserving indentation.

        Parameters
        ----------
        text : str
            The text to wrap.
        """
        if self._current_list_nesting:
            extra_width = (self._current_list_nesting * self._list_indent) + self._curr_bullet_len
        else:
            extra_width = 0
        self._text_wrapper.width = self._line_len - extra_width
        wrapped = self._text_wrapper.fill(text)
        return wrapped


class SPDXLicenseTextMD(SPDXLicenseText):
    """Parses the <text> element from an SPDX license XML and generates a Markdown version of the license.

    Parameters
    ----------
    text : xml.etree.ElementTree.Element
        The <text> XML element to parse.
    """

    def __init__(self, text: ET.Element):
        super().__init__(text)
        return

    def generate(
        self,
        alts: dict[str, str] | None = None,
    ) -> tuple[_mdit.Document, _mdit.Document | None]:
        """Generate Markdown license.

        Returns
        -------
        The Markdown version of the license.
        """
        return super().generate(alts)
