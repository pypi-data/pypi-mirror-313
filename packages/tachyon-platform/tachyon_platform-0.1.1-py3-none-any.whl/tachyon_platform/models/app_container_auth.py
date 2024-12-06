# coding: utf-8



from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from tachyon_platform.models.app_container_auth_api import AppContainerAuthApi
from tachyon_platform.models.app_container_auth_frontend import AppContainerAuthFrontend
from typing import Optional, Set
from typing_extensions import Self

class AppContainerAuth(BaseModel):
    """
    The authentication setting.
    """ # noqa: E501
    mode: StrictStr = Field(description="The authentication mode.")
    api: Optional[AppContainerAuthApi] = None
    frontend: Optional[AppContainerAuthFrontend] = None
    __properties: ClassVar[List[str]] = ["mode", "api", "frontend"]

    @field_validator('mode')
    def mode_validate_enum(cls, value):
        """Validates the enum"""
        if value not in set(['API', 'FRONTEND']):
            raise ValueError("must be one of enum values ('API', 'FRONTEND')")
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
        """Create an instance of AppContainerAuth from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of api
        if self.api:
            _dict['api'] = self.api.to_dict()
        # override the default output from pydantic by calling `to_dict()` of frontend
        if self.frontend:
            _dict['frontend'] = self.frontend.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of AppContainerAuth from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "mode": obj.get("mode"),
            "api": AppContainerAuthApi.from_dict(obj["api"]) if obj.get("api") is not None else None,
            "frontend": AppContainerAuthFrontend.from_dict(obj["frontend"]) if obj.get("frontend") is not None else None
        })
        return _obj


