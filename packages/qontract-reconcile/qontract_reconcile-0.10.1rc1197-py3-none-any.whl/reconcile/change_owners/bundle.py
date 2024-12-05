from abc import abstractmethod
from dataclasses import dataclass
from enum import StrEnum
from typing import (
    Any,
    Protocol,
)

from pydantic import (
    BaseModel,
    Field,
)

from reconcile.utils.gql import get_diff

DATAFILE_PATH_FIELD_NAME = "path"
DATAFILE_SHA256SUM_FIELD_NAME = "$file_sha256sum"
DATAFILE_SCHEMA_FIELD_NAME = "$schema"


class BundleFileType(StrEnum):
    DATAFILE = "datafile"
    RESOURCEFILE = "resourcefile"


@dataclass(frozen=True)
class FileRef:
    """
    A reference to a file in a bundle.
    """

    file_type: BundleFileType
    path: str
    schema: str | None
    json_path: str | None = None

    def __str__(self) -> str:
        return f"{self.file_type.value}:{self.path}"


DATAFILE_CONTENT_CLEANUP_FIELDS = [
    DATAFILE_SHA256SUM_FIELD_NAME,
    DATAFILE_PATH_FIELD_NAME,
    DATAFILE_SCHEMA_FIELD_NAME,
]
"""
Datafile metadata fields that should be removed from the datafile content
during BundleFileChange initialization.
"""


#
# The following dataclasses represent the data returned by the
# qontract-server /diff endpoint.
#


class QontractServerDatafileDiff(BaseModel):
    """
    Represents a datafile diff of an individual datafile returned by the qontract-server /diff endpoint.
    """

    datafilepath: str
    datafileschema: str
    old: dict[str, Any] | None
    new: dict[str, Any] | None

    @property
    def old_datafilepath(self) -> str | None:
        return self.old.get(DATAFILE_PATH_FIELD_NAME) if self.old else None

    @property
    def new_datafilepath(self) -> str | None:
        return self.new.get(DATAFILE_PATH_FIELD_NAME) if self.new else None

    @property
    def old_data_sha(self) -> str | None:
        return self.old.get(DATAFILE_SHA256SUM_FIELD_NAME) if self.old else None

    @property
    def new_data_sha(self) -> str | None:
        return self.new.get(DATAFILE_SHA256SUM_FIELD_NAME) if self.new else None

    @property
    def cleaned_old_data(self) -> dict[str, Any] | None:
        return _clean_datafile_content(self.old)

    @property
    def cleaned_new_data(self) -> dict[str, Any] | None:
        return _clean_datafile_content(self.new)


def _clean_datafile_content(data: dict[str, Any] | None) -> dict[str, Any] | None:
    """
    Sadly, datafiles mix and match data and metadata in the same file. This
    function removes some metadata that is otherwise annoying to deal with.
    """
    if data is None:
        return None
    return {k: v for k, v in data.items() if k not in DATAFILE_CONTENT_CLEANUP_FIELDS}


class QontractServerResourcefileBackref(BaseModel):
    """
    Represents a backref from a resourcefile to a datafile
    """

    path: str
    datafileschema: str = Field(..., alias="datafileSchema")
    jsonpath: str = Field(..., alias="jsonpath")


class QontractServerResourcefileDiffState(BaseModel):
    """
    Represents the old or new state of a resourcefile returned by the qontract-server /diff endpoint.
    """

    path: str
    content: str
    resourcefileschema: str | None = Field(..., alias="$schema")
    sha256sum: str
    backrefs: list[QontractServerResourcefileBackref] | None


class QontractServerResourcefileDiff(BaseModel):
    """
    Represents a resourcefile diff of an individual resourcefile returned by the qontract-server /diff endpoint.
    """

    resourcepath: str
    old: QontractServerResourcefileDiffState | None = None
    new: QontractServerResourcefileDiffState | None = None

    @property
    def resourcefileschema(self) -> str | None:
        old_schema = self.old.resourcefileschema if self.old else None
        new_schema = self.new.resourcefileschema if self.new else None
        return new_schema or old_schema


class QontractServerDiff(BaseModel):
    """
    Top level datastructure for datafile and resourcefile diffs returned by the qontract-server /diff endpoint.
    """

    datafiles: dict[str, QontractServerDatafileDiff]
    resources: dict[str, QontractServerResourcefileDiff]


#
# File diff resolver help finding differences between two versions of a file.
#


class FileDiffResolver(Protocol):
    """
    A protocol to lookup the diff of a file given its FileRef.
    """

    @abstractmethod
    def lookup_file_diff(
        self, file_ref: FileRef
    ) -> tuple[dict[str, Any] | None, dict[str, Any] | None]: ...


@dataclass
class QontractServerFileDiffResolver:
    """
    An implementation of the FileDiffResolver protocol that uses the comparison
    SHA from a qontract-server to lookup the diff of a file.
    """

    comparison_sha: str

    def lookup_file_diff(
        self, file_ref: FileRef
    ) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
        data = get_diff(
            old_sha=self.comparison_sha,
            file_type=file_ref.file_type.value,
            file_path=file_ref.path,
        )
        return data.get("old"), data.get("new")


class NoOpFileDiffResolver:
    """
    A resolver that is used in contexts where it is required from a typing
    perspective, but where the actual lookup is not needed.
    """

    def lookup_file_diff(
        self, file_ref: FileRef
    ) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
        raise Exception(
            "NoOpFileDiffResolver is not supposed to be used in "
            "runtime contexts where lookups are needed"
        )
