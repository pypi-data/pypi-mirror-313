# coding: utf-8



from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from tachyon_platform.models.dbt_project_notification_config import DbtProjectNotificationConfig
from typing import Optional, Set
from typing_extensions import Self

class DbtProject(BaseModel):
    """
    DbtProject
    """ # noqa: E501
    id: StrictStr = Field(description="The ID of the dbt project. This value is generated automatically.")
    name: Annotated[str, Field(min_length=1, strict=True, max_length=128)] = Field(description="The name of the dbt project.")
    description: Annotated[str, Field(strict=True, max_length=128)] = Field(description="The description of the dbt project.")
    labels: Optional[Annotated[List[StrictStr], Field(max_length=10)]] = Field(default=None, description="Arbitrary labels specified by user.")
    latest_version: StrictInt = Field(description="The latest version of this dbt project. Automatically incremented on upload.", alias="latestVersion")
    latest_version_id: StrictStr = Field(description="The ID of the latest version of this dbt project.", alias="latestVersionId")
    status: StrictStr = Field(description="The status of the resource.")
    is_docs_generated: StrictBool = Field(description="When true, the dbt documentation has been successfully generated.", alias="isDocsGenerated")
    schedule: StrictStr = Field(description="Scheduler settings for periodic execution. It is defined using the unix-cron string format like \"* * * * *\".")
    notification_config: Optional[DbtProjectNotificationConfig] = Field(default=None, alias="notificationConfig")
    __properties: ClassVar[List[str]] = ["id", "name", "description", "labels", "latestVersion", "latestVersionId", "status", "isDocsGenerated", "schedule", "notificationConfig"]

    @field_validator('status')
    def status_validate_enum(cls, value):
        """Validates the enum"""
        if value not in set(['INVALID', 'INITIALIZED', 'READY', 'DELETED']):
            raise ValueError("must be one of enum values ('INVALID', 'INITIALIZED', 'READY', 'DELETED')")
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
        """Create an instance of DbtProject from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of notification_config
        if self.notification_config:
            _dict['notificationConfig'] = self.notification_config.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of DbtProject from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "name": obj.get("name"),
            "description": obj.get("description"),
            "labels": obj.get("labels"),
            "latestVersion": obj.get("latestVersion"),
            "latestVersionId": obj.get("latestVersionId"),
            "status": obj.get("status"),
            "isDocsGenerated": obj.get("isDocsGenerated"),
            "schedule": obj.get("schedule"),
            "notificationConfig": DbtProjectNotificationConfig.from_dict(obj["notificationConfig"]) if obj.get("notificationConfig") is not None else None
        })
        return _obj


