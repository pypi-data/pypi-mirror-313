# coding: utf-8



from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from tachyon_platform.models.pipeline_notification_config import PipelineNotificationConfig
from typing import Optional, Set
from typing_extensions import Self

class PipelineUpdate(BaseModel):
    """
    PipelineUpdate
    """ # noqa: E501
    description: Optional[Annotated[str, Field(strict=True, max_length=128)]] = Field(default=None, description="The description of the pipeline.")
    schedule: Optional[StrictStr] = Field(default=None, description="Scheduler settings for periodic execution. It is defined using the unix-cron string format like \"* * * * *\".")
    notification_config: Optional[PipelineNotificationConfig] = Field(default=None, alias="notificationConfig")
    __properties: ClassVar[List[str]] = ["description", "schedule", "notificationConfig"]

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
        """Create an instance of PipelineUpdate from a JSON string"""
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
        """Create an instance of PipelineUpdate from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "description": obj.get("description"),
            "schedule": obj.get("schedule"),
            "notificationConfig": PipelineNotificationConfig.from_dict(obj["notificationConfig"]) if obj.get("notificationConfig") is not None else None
        })
        return _obj


