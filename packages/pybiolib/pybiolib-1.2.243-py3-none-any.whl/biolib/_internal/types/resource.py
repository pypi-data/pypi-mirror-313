from .app import AppSlimDict
from .data_record import DataRecordSlimDict
from .experiment import ExperimentSlimDict
from .typing import Optional, TypedDict


class ResourceDict(TypedDict):
    uuid: str
    uri: str
    name: str
    created_at: str
    app: Optional[AppSlimDict]
    data_record: Optional[DataRecordSlimDict]
    experiment: Optional[ExperimentSlimDict]
