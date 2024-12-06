from __future__ import annotations as annotations

from typing import TYPE_CHECKING as TYPE_CHECKING
import json as _json

from licenseman.spdx.license import SPDXLicense as _SPDXLicense

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Sequence, Generator
    from licenseman.spdx.license_list import SPDXLicenseList


class SPDXLicenseDB:

    def __init__(
        self,
        license_list: SPDXLicenseList,
        db_path: Path,
        in_memory: bool = False,
        verify: bool = True,
        licenses: dict[str, _SPDXLicense] | None = None,
    ):
        self._license_list = license_list
        self._db_path = db_path
        self._in_memory = in_memory
        self._verify = verify
        self._licenses: dict[str, _SPDXLicense] = licenses or {}
        if in_memory:
            self.load(verify=verify)
        elif verify:
            for _ in self.get(verify=True):
                pass
        return

    def load(self, license_ids: Sequence[str] | None = None, verify: bool | None = None):
        license_ids = license_ids or self._license_list.ids
        for license_id, license_data in zip(license_ids, self.get(license_ids, verify=verify)):
            self._licenses[license_id] = license_data
        return

    def get(self, license_ids: Sequence[str] | None = None, verify: bool | None = None) -> Generator[_SPDXLicense]:
        for license_id in license_ids or self._license_list.ids:
            if license_id in self._licenses:
                yield self._licenses[license_id]
            else:
                with open(self._db_path / f"{license_id}.json") as f:
                    data = _json.load(f)
                yield _SPDXLicense(
                    data,
                    verify=verify if verify is not None else self._verify,
                )

    def alts(self, license_ids: Sequence[str] | None = None):
        license_ids = license_ids or self._license_list.ids
        alts: dict[str, list[dict[str, str]]] = {}
        for license in self.get(license_ids):
            for alt_name, alt_data in license.alts.items():
                alts.setdefault(alt_name, []).append({"id": license.id, **alt_data})
        return alts

    def __getitem__(self, license_id: str) -> _SPDXLicense:
        return self.get([license_id]).__next__()

    def __contains__(self, license_id: str) -> bool:
        return license_id in self._license_list

