from licenseman.spdx.entry import SPDXEntry


class SPDXLicenseException(SPDXEntry):
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
        super().__init__(data=data, entry_type="exception", verify=verify)
        return

    def __repr__(self):
        return f"<SPDXLicenseException {self.id}>"
