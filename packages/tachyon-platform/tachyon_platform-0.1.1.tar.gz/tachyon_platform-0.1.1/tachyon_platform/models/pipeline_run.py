# coding: utf-8



from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from tachyon_platform.models.pipeline_run_error_state import PipelineRunErrorState
from typing import Optional, Set
from typing_extensions import Self

class PipelineRun(BaseModel):
    """
    PipelineRun
    """ # noqa: E501
    id: StrictStr = Field(description="The ID of the pipeline run. This value is generated automatically.")
    name: StrictStr = Field(description="The name of the pipeline run. This is used as both DisplayName and PipelineJobID of the vertex ai pipeline run.")
    resource_name: StrictStr = Field(description="The full GCP resource name of the pipeline run. It can be used to retrieve a specific run from the GCP API. Reference: https://cloud.google.com/iam/docs/conditions-resource-attributes#resource-name", alias="resourceName")
    version: Optional[StrictInt] = Field(default=None, description="The version associated with the version ID (normalized for convenience)")
    version_id: Optional[StrictStr] = Field(default=None, description="The version ID of the pipeline used to create this run.", alias="versionId")
    pipeline_id: StrictStr = Field(description="The ID of the pipeline to run", alias="pipelineId")
    pipeline_name: StrictStr = Field(description="The name of the pipeline to run", alias="pipelineName")
    status: StrictStr = Field(description="The execution status of Vertex AI")
    create_time: datetime = Field(description="Time when the job created", alias="createTime")
    start_time: Optional[datetime] = Field(default=None, description="Time when the job started", alias="startTime")
    end_time: Optional[datetime] = Field(default=None, description="Time when the job ended", alias="endTime")
    error_state: Optional[PipelineRunErrorState] = Field(default=None, alias="errorState")
    inputs: Optional[Dict[str, Any]] = Field(default=None, description="Input parameters to be used when executing this pipeline run.")
    executor_id: Optional[StrictStr] = Field(default=None, description="The ID of the user who created the pipeline run.", alias="executorId")
    executor_type: StrictStr = Field(description="The type of the user who created the pipeline run.", alias="executorType")
    __properties: ClassVar[List[str]] = ["id", "name", "resourceName", "version", "versionId", "pipelineId", "pipelineName", "status", "createTime", "startTime", "endTime", "errorState", "inputs", "executorId", "executorType"]

    @field_validator('status')
    def status_validate_enum(cls, value):
        """Validates the enum"""
        if value not in set(['UNSPECIFIED', 'QUEUED', 'PENDING', 'RUNNING', 'SUCCEEDED', 'FAILED', 'CANCELLING', 'CANCELLED', 'PAUSED', 'EXPIRED', 'UPDATING']):
            raise ValueError("must be one of enum values ('UNSPECIFIED', 'QUEUED', 'PENDING', 'RUNNING', 'SUCCEEDED', 'FAILED', 'CANCELLING', 'CANCELLED', 'PAUSED', 'EXPIRED', 'UPDATING')")
        return value

    @field_validator('executor_type')
    def executor_type_validate_enum(cls, value):
        """Validates the enum"""
        if value not in set(['UNKNOWN', 'USER', 'INTERNAL']):
            raise ValueError("must be one of enum values ('UNKNOWN', 'USER', 'INTERNAL')")
        return value

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
        """Create an instance of PipelineRun from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of error_state
        if self.error_state:
            _dict['errorState'] = self.error_state.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of PipelineRun from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "name": obj.get("name"),
            "resourceName": obj.get("resourceName"),
            "version": obj.get("version"),
            "versionId": obj.get("versionId"),
            "pipelineId": obj.get("pipelineId"),
            "pipelineName": obj.get("pipelineName"),
            "status": obj.get("status"),
            "createTime": obj.get("createTime"),
            "startTime": obj.get("startTime"),
            "endTime": obj.get("endTime"),
            "errorState": PipelineRunErrorState.from_dict(obj["errorState"]) if obj.get("errorState") is not None else None,
            "inputs": obj.get("inputs"),
            "executorId": obj.get("executorId"),
            "executorType": obj.get("executorType")
        })
        return _obj


