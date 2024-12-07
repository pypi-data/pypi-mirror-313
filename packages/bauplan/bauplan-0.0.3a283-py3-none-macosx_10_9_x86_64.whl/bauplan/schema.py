from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class _BauplanData(BaseModel):
    def __str__(self) -> str:
        return self.__repr__()


class APIMetadata(_BauplanData):
    error: Optional[str]
    pagination_token: Optional[str]
    request_id: Optional[str]
    request_ts: Optional[int]
    request_ms: Optional[int]


class APIResponse(_BauplanData):
    data: Any
    metadata: APIMetadata


class RefMetadata(_BauplanData):
    """
    Some metadata about a reference.
    """

    message: str
    committer: str
    authors: list[str]
    commit_time: str
    author_time: str
    parent_commit_hashes: list[str]
    num_commits_ahead: Optional[int]
    num_commits_behind: Optional[int]
    common_ancestor_hash: Optional[str]
    num_total_commits: int

    @classmethod
    def from_dict(cls, metadata: Optional[dict] = None) -> Optional[RefMetadata]:
        """Convert a dictionary of reference metadata to a DataCatalogRefMetadata object."""
        if metadata is None:
            return None
        return cls(
            message=metadata['commitMetaOfHEAD']['message'],
            committer=metadata['commitMetaOfHEAD']['committer'],
            authors=metadata['commitMetaOfHEAD']['authors'],
            commit_time=metadata['commitMetaOfHEAD']['commitTime'],
            author_time=metadata['commitMetaOfHEAD']['authorTime'],
            parent_commit_hashes=metadata['commitMetaOfHEAD']['parentCommitHashes'],
            num_commits_ahead=metadata['numCommitsAhead'],
            num_commits_behind=metadata['numCommitsBehind'],
            common_ancestor_hash=metadata['commonAncestorHash'],
            num_total_commits=metadata['numTotalCommits'],
        )


class Ref(_BauplanData):
    """
    A branch or a tag
    """

    name: str
    hash: str
    metadata: Optional[RefMetadata] = None

    def __str__(self) -> str:
        if self.hash:
            return f'{self.name}@{self.hash}'
        return self.name

    @classmethod
    def from_dict(cls, data: Dict) -> Ref:
        return cls(
            name=data.get('name'),
            hash=data.get('hash'),
            metadata=RefMetadata.from_dict(data.get('metadata')),
        )


class Branch(Ref):
    pass


class Namespace(_BauplanData):
    name: str


class Entry(_BauplanData):
    name: str
    namespace: str
    kind: str

    @property
    def fqn(self) -> str:
        return f'{self.namespace}.{self.name}'


class TableField(_BauplanData):
    id: int
    name: str
    required: bool
    type: str


class PartitionField(_BauplanData):
    name: str
    transform: str


class Table(Entry):
    kind: str = 'TABLE'


class TableWithMetadata(Table):
    id: str
    records: Optional[int]
    size: Optional[int]
    last_updated_ms: int
    fields: List[TableField]
    snapshots: Optional[int]
    partitions: List[PartitionField]
    metadata_location: str
    current_snapshot_id: Optional[int]
    current_schema_id: Optional[int]
    raw: Optional[Dict]
