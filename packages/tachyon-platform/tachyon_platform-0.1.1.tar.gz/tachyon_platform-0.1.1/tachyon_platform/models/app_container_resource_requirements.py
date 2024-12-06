# coding: utf-8



from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class AppContainerResourceRequirements(BaseModel):
    """
    The resource requirements for the container. If not provided, the container will have default limitations.
    """ # noqa: E501
    cpu_limit: Optional[StrictStr] = Field(default=None, description="The maximum amount of CPU the container can use. If not provided, the container will have default CPU limit.", alias="cpuLimit")
    memory_limit: Optional[StrictStr] = Field(default=None, description="The maximum amount of memory the container can use. If not provided, the container will have default memory limit.", alias="memoryLimit")
    cpu_always_on: Optional[StrictBool] = Field(default=None, description="Determines whether CPU should be always on for the container.", alias="cpuAlwaysOn")
    startup_cpu_boost: Optional[StrictBool] = Field(default=None, description="Determines whether CPU should be boosted on startup of a new container.", alias="startupCPUBoost")
    __properties: ClassVar[List[str]] = ["cpuLimit", "memoryLimit", "cpuAlwaysOn", "startupCPUBoost"]

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
        """Create an instance of AppContainerResourceRequirements from a JSON string"""
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
        """Create an instance of AppContainerResourceRequirements from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "cpuLimit": obj.get("cpuLimit"),
            "memoryLimit": obj.get("memoryLimit"),
            "cpuAlwaysOn": obj.get("cpuAlwaysOn"),
            "startupCPUBoost": obj.get("startupCPUBoost")
        })
        return _obj


