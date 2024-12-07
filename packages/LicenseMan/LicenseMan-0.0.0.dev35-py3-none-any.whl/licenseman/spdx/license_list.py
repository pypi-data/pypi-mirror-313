from __future__ import annotations

import datetime as _dt


class SPDXLicenseList:
    """SPDX license list."""

    def __init__(self, data: dict):
        self._data = data
        self._map = {licence["licenseId"]: licence for licence in data["licenses"]}
        return

    @property
    def licenses(self) -> list[dict]:
        """List of SPDX licenses."""
        return self._data["licenses"]

    @property
    def ids(self) -> list[str]:
        """List of SPDX license IDs."""
        return list(self._map.keys())

    @property
    def release_date(self) -> _dt.date:
        """Release date of the SPDX license list."""
        return _dt.datetime.fromisoformat(self._data["releaseDate"]).date()

    @property
    def version(self) -> str:
        """Version of the SPDX license list."""
        return self._data["licenseListVersion"]

    def get(self, key: str) -> dict | None:
        """Get a license by its key."""

        return self._map.get(key)

    def __getitem__(self, key: str) -> dict:
        return self._map[key]

    def __contains__(self, key: str) -> bool:
        return key in self._map

    def __repr__(self):
        return f"<SPDXLicenseList {self.version}>"
