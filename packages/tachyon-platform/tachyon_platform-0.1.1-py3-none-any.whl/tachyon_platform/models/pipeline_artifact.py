# coding: utf-8



from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List
from typing import Optional, Set
from typing_extensions import Self

class PipelineArtifact(BaseModel):
    """
    PipelineArtifact
    """ # noqa: E501
    id: StrictStr = Field(description="The ID of the pipeline artifact This value is generated automatically.")
    task_id: StrictInt = Field(description="The task id within the pipeline associated with the artifact", alias="taskId")
    task_name: StrictStr = Field(description="The task name within the pipeline associated with the artifact", alias="taskName")
    parent_task_id: StrictInt = Field(description="The task id within the pipeline associated with the artifact's task parent", alias="parentTaskId")
    name: StrictStr = Field(description="User defined name of the artifact output within the task")
    output_resource_name: StrictStr = Field(description="The GCP \"resource name\" for this artifact", alias="outputResourceName")
    output_schema_title: StrictStr = Field(description="The schema title associated with the artifact Details: cloud.google.com/vertex-ai/docs/ml-metadata/system-schemas#system_schema_examples", alias="outputSchemaTitle")
    uri: StrictStr = Field(description="The actual path to the artifact within GCS")
    __properties: ClassVar[List[str]] = ["id", "taskId", "taskName", "parentTaskId", "name", "outputResourceName", "outputSchemaTitle", "uri"]

    @field_validator('output_schema_title')
    def output_schema_title_validate_enum(cls, value):
        """Validates the enum"""
        if value not in set(['system.Artifact', 'system.Dataset', 'system.Model', 'system.Metrics']):
            raise ValueError("must be one of enum values ('system.Artifact', 'system.Dataset', 'system.Model', 'system.Metrics')")
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
        """Create an instance of PipelineArtifact from a JSON string"""
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
        """Create an instance of PipelineArtifact from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "taskId": obj.get("taskId"),
            "taskName": obj.get("taskName"),
            "parentTaskId": obj.get("parentTaskId"),
            "name": obj.get("name"),
            "outputResourceName": obj.get("outputResourceName"),
            "outputSchemaTitle": obj.get("outputSchemaTitle"),
            "uri": obj.get("uri")
        })
        return _obj


