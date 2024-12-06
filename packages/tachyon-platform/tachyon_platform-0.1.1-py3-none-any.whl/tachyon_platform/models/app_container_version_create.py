# coding: utf-8



from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from tachyon_platform.models.app_container_container import AppContainerContainer
from tachyon_platform.models.app_container_port import AppContainerPort
from tachyon_platform.models.app_container_scaling import AppContainerScaling
from tachyon_platform.models.app_container_vpc_access import AppContainerVpcAccess
from typing import Optional, Set
from typing_extensions import Self

class AppContainerVersionCreate(BaseModel):
    """
    AppContainerVersionCreate
    """ # noqa: E501
    containers: Annotated[List[AppContainerContainer], Field(min_length=1)] = Field(description="The containers to run.")
    port: Optional[AppContainerPort] = None
    vpc_access: Optional[AppContainerVpcAccess] = Field(default=None, alias="vpcAccess")
    execution_environment: Optional[StrictStr] = Field(default=None, description="The execution environment where the application will run.", alias="executionEnvironment")
    use_http2: Optional[StrictBool] = Field(default=None, description="If true, enable HTTP/2 connections.", alias="useHttp2")
    scaling: Optional[AppContainerScaling] = None
    timeout_seconds: Optional[Annotated[int, Field(le=3600, strict=True, ge=1)]] = Field(default=900, description="The request timeout in seconds for the service response.", alias="timeoutSeconds")
    max_instance_request_concurrency: Optional[Annotated[int, Field(le=1000, strict=True, ge=1)]] = Field(default=80, description="The maximum number of concurrent requests that can reach each container instance.", alias="maxInstanceRequestConcurrency")
    __properties: ClassVar[List[str]] = ["containers", "port", "vpcAccess", "executionEnvironment", "useHttp2", "scaling", "timeoutSeconds", "maxInstanceRequestConcurrency"]

    @field_validator('execution_environment')
    def execution_environment_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['GEN1', 'GEN2']):
            raise ValueError("must be one of enum values ('GEN1', 'GEN2')")
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
        """Create an instance of AppContainerVersionCreate from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in containers (list)
        _items = []
        if self.containers:
            for _item_containers in self.containers:
                if _item_containers:
                    _items.append(_item_containers.to_dict())
            _dict['containers'] = _items
        # override the default output from pydantic by calling `to_dict()` of port
        if self.port:
            _dict['port'] = self.port.to_dict()
        # override the default output from pydantic by calling `to_dict()` of vpc_access
        if self.vpc_access:
            _dict['vpcAccess'] = self.vpc_access.to_dict()
        # override the default output from pydantic by calling `to_dict()` of scaling
        if self.scaling:
            _dict['scaling'] = self.scaling.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of AppContainerVersionCreate from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "containers": [AppContainerContainer.from_dict(_item) for _item in obj["containers"]] if obj.get("containers") is not None else None,
            "port": AppContainerPort.from_dict(obj["port"]) if obj.get("port") is not None else None,
            "vpcAccess": AppContainerVpcAccess.from_dict(obj["vpcAccess"]) if obj.get("vpcAccess") is not None else None,
            "executionEnvironment": obj.get("executionEnvironment"),
            "useHttp2": obj.get("useHttp2"),
            "scaling": AppContainerScaling.from_dict(obj["scaling"]) if obj.get("scaling") is not None else None,
            "timeoutSeconds": obj.get("timeoutSeconds") if obj.get("timeoutSeconds") is not None else 900,
            "maxInstanceRequestConcurrency": obj.get("maxInstanceRequestConcurrency") if obj.get("maxInstanceRequestConcurrency") is not None else 80
        })
        return _obj


