# coding: utf-8



from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class DatasetExport(BaseModel):
    """
    DatasetExport
    """ # noqa: E501
    id: StrictStr = Field(description="The ID of the dataset export. This value is generated automatically.")
    job_id: StrictStr = Field(description="The ID of the dataset export job.", alias="jobId")
    job_name: StrictStr = Field(description="The name of the dataset export job. dataset-export-<dataset.ID>-<datasetExport.ID>", alias="jobName")
    job_status: StrictStr = Field(description="The status of the export job.", alias="jobStatus")
    create_time: datetime = Field(description="Time when the job was created.", alias="createTime")
    export_uri: Optional[StrictStr] = Field(default=None, description="URI of GCS to which BigQuery Table was exported. gs://mcd-<workspace.ProjectID>-dataset-export/<dataset.ID>/<JobName>.parquet", alias="exportUri")
    __properties: ClassVar[List[str]] = ["id", "jobId", "jobName", "jobStatus", "createTime", "exportUri"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of DatasetExport from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of DatasetExport from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "jobId": obj.get("jobId"),
            "jobName": obj.get("jobName"),
            "jobStatus": obj.get("jobStatus"),
            "createTime": obj.get("createTime"),
            "exportUri": obj.get("exportUri")
        })
        return _obj


