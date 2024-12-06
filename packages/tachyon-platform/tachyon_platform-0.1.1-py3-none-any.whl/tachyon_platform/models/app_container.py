# coding: utf-8



from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from tachyon_platform.models.app_container_auth import AppContainerAuth
from typing import Optional, Set
from typing_extensions import Self

class AppContainer(BaseModel):
    """
    AppContainer
    """ # noqa: E501
    id: StrictStr = Field(description="The ID of the app container. This value is generated automatically.")
    name: Annotated[str, Field(min_length=1, strict=True, max_length=35)] = Field(description="The name of the app container. It can be between 1 and 35 characters in length and can consist of lowercase letters, numbers and '-'.")
    description: Annotated[str, Field(strict=True, max_length=512)] = Field(description="The display name of the workspace. It can be up to 512 characters in length.")
    latest_version: StrictInt = Field(description="The latest version of the app container. This value is automatically incremented on creation of new version.", alias="latestVersion")
    latest_ready_version_id: StrictStr = Field(description="The ID of the latest ready version of the app container.", alias="latestReadyVersionId")
    auth: Optional[AppContainerAuth] = None
    uri: Optional[StrictStr] = Field(default=None, description="The URI mapped to the app container.")
    status: StrictStr = Field(description="The status of the resource")
    __properties: ClassVar[List[str]] = ["id", "name", "description", "latestVersion", "latestReadyVersionId", "auth", "uri", "status"]

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
        """Create an instance of AppContainer from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of auth
        if self.auth:
            _dict['auth'] = self.auth.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of AppContainer from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "name": obj.get("name"),
            "description": obj.get("description"),
            "latestVersion": obj.get("latestVersion"),
            "latestReadyVersionId": obj.get("latestReadyVersionId"),
            "auth": AppContainerAuth.from_dict(obj["auth"]) if obj.get("auth") is not None else None,
            "uri": obj.get("uri"),
            "status": obj.get("status")
        })
        return _obj


