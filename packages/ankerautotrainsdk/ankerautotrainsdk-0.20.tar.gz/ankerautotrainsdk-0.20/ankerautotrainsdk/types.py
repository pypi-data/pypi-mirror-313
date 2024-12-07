from typing import Optional
from pydantic import BaseModel

class Resolution(BaseModel):
    width: int
    height: int

class FileMeta(BaseModel):
    resolution: Optional[Resolution] = None
    tokenLength: int
    duration: int

class UploadFileResponse(BaseModel):
    url: str
    bucket: str
    storage_id: str
    object_name: str
    uid: str
    meta: Optional[FileMeta] = None

class UploadRawDataResponse(BaseModel):
    raw_data_id: str

class UploadFileWithInfoResponse(BaseModel):
    url: str
    bucket: str
    storage_id: str
    object_name: str
    uid: str
    raw_data_id: str
    meta: Optional[FileMeta] = None

class UploadAnnotationDataResponse(BaseModel):
    annotation_data_id: str

class CreateDataSetResponse(BaseModel):
    dataset_id: str

class SummaryAndDownloadDataSetResponse(BaseModel):
    url: str
    bucket: str
    object_name: str


class CreateDatasetRequest(BaseModel): 
    """
    "bg": "string",
        "owner": "string",
        "labelMethod": "string",
        "modelVersion": "string",
        "modelName": "string",
        "annotationType": "detection",
        "labelQuery": {
          "label": "string",
          "score": 1
        },
        "mutipleLabelQuery": [
          {
            "label": "string",
            "score": 1
          }
        ],
        "dataId": "string",
        "modelType": "",
        "processState": "teacher",
        "startTime": "string",
        "endTime": "string"
    """
    bg: str = ""
    owner: str = ""
    labelMethod: str = ""
    modelVersion: str = ""
    modelName: str = ""
    annotationType: str = ""
    labelQuery: dict = {}
    mutipleLabelQuery: list = []
    dataId: str = ""
    modelType: str = ""
    processState: str = ""
    startTime: str = ""
    endTime: str = ""

class GetRawDataResponse(BaseModel):
    num_video: int
    num_image: int
    num_device: int
    num_label: int
    num_hardcase: int
    task_hardcase: int

class LabelStat(BaseModel):
    label: str
    count: int
    percent: float = 0

class LabelStatsResponse(BaseModel):
    datasetId: str
    datasetName: str
    labelStats: list[LabelStat]
    totalCount: int
    totalDataCount: int = 0
