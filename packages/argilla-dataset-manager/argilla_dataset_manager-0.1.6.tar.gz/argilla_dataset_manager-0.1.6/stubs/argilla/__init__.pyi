from typing import Any, Dict, List, Optional, Union, Sequence
from datetime import datetime

class Argilla:
    def __init__(
        self,
        api_url: str,
        api_key: str,
        headers: Optional[Dict[str, str]] = None
    ) -> None: ...
    
    def workspaces(self, name: Optional[str] = None) -> Optional["Workspace"]: ...
    def get_workspace(self, name: str) -> "Workspace": ...
    def create_workspace(self, name: str) -> "Workspace": ...
    def get_dataset(self, name: str, workspace: str) -> "Dataset": ...
    def datasets(self, name: str, workspace: Optional[str] = None) -> Optional["Dataset"]: ...
    
    @property
    def http_client(self) -> Any: ...

class Workspace:
    name: str
    client: Argilla
    
    def __init__(self, name: str, client: Optional[Argilla] = None) -> None: ...
    def create(self) -> "Workspace": ...
    def delete(self) -> None: ...

class Dataset:
    name: str
    workspace: str
    settings: Dict[str, Any]
    client: Argilla
    records: "Records"
    
    def __init__(
        self,
        name: str,
        workspace: str,
        settings: Optional[Union[Dict[str, Any], "Settings"]] = None,
        client: Optional[Argilla] = None
    ) -> None: ...
    
    def create(self) -> "Dataset": ...
    def delete(self) -> None: ...
    def add_records(self, records: List["Record"]) -> None: ...

class Records:
    def log(self, records: List["Record"]) -> None: ...

class Record:
    fields: Dict[str, Any]
    metadata: Dict[str, Any]
    
    def __init__(
        self,
        fields: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> None: ...

class TextField:
    name: str
    required: bool
    title: Optional[str]
    use_markdown: bool
    
    def __init__(
        self,
        name: str,
        required: bool = False,
        title: Optional[str] = None,
        use_markdown: bool = False
    ) -> None: ...

class LabelQuestion:
    name: str
    title: Optional[str]
    description: Optional[str]
    labels: List[str]
    
    def __init__(
        self,
        name: str,
        labels: List[str],
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> None: ...

class RatingQuestion:
    name: str
    title: Optional[str]
    description: Optional[str]
    values: List[int]
    
    def __init__(
        self,
        name: str,
        values: List[int],
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> None: ...

class TermsMetadataProperty:
    name: str
    title: Optional[str]
    description: Optional[str]
    values: List[str]
    
    def __init__(
        self,
        name: str,
        values: List[str],
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> None: ...

class Settings:
    guidelines: str
    fields: List[TextField]
    metadata_properties: List[Dict[str, Any]]
    questions: List[Union[LabelQuestion, RatingQuestion]]
    allow_extra_metadata: bool
    
    def __init__(
        self,
        guidelines: str = "",
        fields: Optional[List[TextField]] = None,
        metadata_properties: Optional[List[Dict[str, Any]]] = None,
        questions: Optional[List[Union[LabelQuestion, RatingQuestion]]] = None,
        allow_extra_metadata: bool = True
    ) -> None: ... 