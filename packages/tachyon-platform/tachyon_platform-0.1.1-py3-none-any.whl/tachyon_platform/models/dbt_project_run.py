# coding: utf-8



from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from tachyon_platform.models.dbt_project_run_error_state import DbtProjectRunErrorState
from tachyon_platform.models.dbt_project_run_parameter import DbtProjectRunParameter
from typing import Optional, Set
from typing_extensions import Self

class DbtProjectRun(BaseModel):
    """
    DbtProjectRun
    """ # noqa: E501
    id: StrictStr = Field(description="The ID of the dbt project run. This value is generated automatically.")
    resource_name: Optional[StrictStr] = Field(default=None, description="The full GCP resource name of the dbtProject run. It can be used to retrieve a specific run from the GCP API. Reference: https://cloud.google.com/iam/docs/conditions-resource-attributes#resource-name", alias="resourceName")
    version: Optional[StrictInt] = Field(default=None, description="The version associated with the version ID (normalized for convenience).")
    version_id: Optional[StrictStr] = Field(default=None, description="The version ID of the dbt project used to create this run.", alias="versionId")
    parameter: DbtProjectRunParameter
    dbt_project_id: StrictStr = Field(description="The ID of the dbt project to run.", alias="dbtProjectId")
    dbt_project_name: StrictStr = Field(description="The name of the dbt project to run.", alias="dbtProjectName")
    status: StrictStr = Field(description="The status of the underlying Cloud Run job execution.")
    error_state: Optional[DbtProjectRunErrorState] = Field(default=None, alias="errorState")
    create_time: datetime = Field(description="Time when the job is created.", alias="createTime")
    start_time: Optional[datetime] = Field(default=None, description="Time when the job is started.", alias="startTime")
    end_time: Optional[datetime] = Field(default=None, description="Time when the job is ended.", alias="endTime")
    __properties: ClassVar[List[str]] = ["id", "resourceName", "version", "versionId", "parameter", "dbtProjectId", "dbtProjectName", "status", "errorState", "createTime", "startTime", "endTime"]

    @field_validator('status')
    def status_validate_enum(cls, value):
        """Validates the enum"""
        if value not in set(['UNSPECIFIED', 'PENDING', 'RUNNING', 'SUCCEEDED', 'FAILED', 'CANCELLED']):
            raise ValueError("must be one of enum values ('UNSPECIFIED', 'PENDING', 'RUNNING', 'SUCCEEDED', 'FAILED', 'CANCELLED')")
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
        """Create an instance of DbtProjectRun from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of parameter
        if self.parameter:
            _dict['parameter'] = self.parameter.to_dict()
        # override the default output from pydantic by calling `to_dict()` of error_state
        if self.error_state:
            _dict['errorState'] = self.error_state.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of DbtProjectRun from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "resourceName": obj.get("resourceName"),
            "version": obj.get("version"),
            "versionId": obj.get("versionId"),
            "parameter": DbtProjectRunParameter.from_dict(obj["parameter"]) if obj.get("parameter") is not None else None,
            "dbtProjectId": obj.get("dbtProjectId"),
            "dbtProjectName": obj.get("dbtProjectName"),
            "status": obj.get("status"),
            "errorState": DbtProjectRunErrorState.from_dict(obj["errorState"]) if obj.get("errorState") is not None else None,
            "createTime": obj.get("createTime"),
            "startTime": obj.get("startTime"),
            "endTime": obj.get("endTime")
        })
        return _obj


