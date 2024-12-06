from __future__ import annotations as annotations

from typing import TYPE_CHECKING as TYPE_CHECKING
import json as _json

from licenseman.spdx.exception import SPDXLicenseException as _SPDXLicenseException

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Sequence, Generator
    from licenseman.spdx.exception_list import SPDXExceptionList


class SPDXLicenseExceptionDB:

    def __init__(
        self,
        exception_list: SPDXExceptionList,
        db_path: Path,
        in_memory: bool = False,
        verify: bool = True,
        exceptions: dict[str, _SPDXLicenseException] | None = None,
    ):
        self._exception_list = exception_list
        self._db_path = db_path
        self._in_memory = in_memory
        self._verify = verify
        self._exceptions: dict[str, _SPDXLicenseException] = exceptions or {}
        if in_memory:
            self.load(verify=verify)
        elif verify:
            for _ in self.get(verify=True):
                pass
        return

    def load(self, exception_ids: Sequence[str] | None = None, verify: bool | None = None):
        exception_ids = exception_ids or self._exception_list.ids
        for exception_id, exception_data in zip(exception_ids, self.get(exception_ids, verify=verify)):
            self._exceptions[exception_id] = exception_data
        return

    def get(self, exception_ids: Sequence[str] | None = None, verify: bool | None = None) -> Generator[_SPDXLicenseException]:
        for exception_id in exception_ids or self._exception_list.ids:
            if exception_id in self._exceptions:
                yield self._exceptions[exception_id]
            else:
                with open(self._db_path / f"{exception_id}.json") as f:
                    data = _json.load(f)
                yield _SPDXLicenseException(
                    data,
                    verify=verify if verify is not None else self._verify,
                )

    def alts(self, exception_ids: Sequence[str] | None = None):
        exception_ids = exception_ids or self._exception_list.ids
        alts: dict[str, list[dict[str, str]]] = {}
        for exception in self.get(exception_ids):
            for alt_name, alt_data in exception.alts.items():
                alts.setdefault(alt_name, []).append({"id": exception.id, **alt_data})
        return alts

    def __getitem__(self, exception_id: str) -> _SPDXLicenseException:
        return self.get([exception_id]).__next__()

    def __contains__(self, exception_id: str) -> bool:
        return exception_id in self._exception_list

