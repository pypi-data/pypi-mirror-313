# coding: utf-8



from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from tachyon_platform.models.app_container_container_env_inner import AppContainerContainerEnvInner
from tachyon_platform.models.app_container_container_secret_inner import AppContainerContainerSecretInner
from tachyon_platform.models.app_container_resource_requirements import AppContainerResourceRequirements
from typing import Optional, Set
from typing_extensions import Self

class AppContainerContainer(BaseModel):
    """
    AppContainerContainer
    """ # noqa: E501
    image: StrictStr = Field(description="The name of the container image.")
    command: Optional[List[StrictStr]] = Field(default=None, description="The entrypoint of the container. If not provided, the docker image's ENTRYPOINT is used.")
    args: Optional[List[StrictStr]] = Field(default=None, description="The arguments to the entrypoint. If not provided, the docker image's CMD is used.")
    working_dir: Optional[StrictStr] = Field(default=None, description="The working directory of the container. If not provided, the container runtime's default will be used, which might be configured in the container image.", alias="workingDir")
    env: Optional[List[AppContainerContainerEnvInner]] = Field(default=None, description="The environment variables to set in the container.")
    secret: Optional[List[AppContainerContainerSecretInner]] = Field(default=None, description="The mapping of secrets managed by Secret Manager to environment variables.")
    resource_requirements: Optional[AppContainerResourceRequirements] = Field(default=None, alias="resourceRequirements")
    __properties: ClassVar[List[str]] = ["image", "command", "args", "workingDir", "env", "secret", "resourceRequirements"]

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
        """Create an instance of AppContainerContainer from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in env (list)
        _items = []
        if self.env:
            for _item_env in self.env:
                if _item_env:
                    _items.append(_item_env.to_dict())
            _dict['env'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in secret (list)
        _items = []
        if self.secret:
            for _item_secret in self.secret:
                if _item_secret:
                    _items.append(_item_secret.to_dict())
            _dict['secret'] = _items
        # override the default output from pydantic by calling `to_dict()` of resource_requirements
        if self.resource_requirements:
            _dict['resourceRequirements'] = self.resource_requirements.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of AppContainerContainer from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "image": obj.get("image"),
            "command": obj.get("command"),
            "args": obj.get("args"),
            "workingDir": obj.get("workingDir"),
            "env": [AppContainerContainerEnvInner.from_dict(_item) for _item in obj["env"]] if obj.get("env") is not None else None,
            "secret": [AppContainerContainerSecretInner.from_dict(_item) for _item in obj["secret"]] if obj.get("secret") is not None else None,
            "resourceRequirements": AppContainerResourceRequirements.from_dict(obj["resourceRequirements"]) if obj.get("resourceRequirements") is not None else None
        })
        return _obj


