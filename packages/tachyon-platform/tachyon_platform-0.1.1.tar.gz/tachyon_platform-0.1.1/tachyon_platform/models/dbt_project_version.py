# coding: utf-8



from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from tachyon_platform.models.dbt_project_run_parameter import DbtProjectRunParameter
from typing import Optional, Set
from typing_extensions import Self

class DbtProjectVersion(BaseModel):
    """
    DbtProjectVersion
    """ # noqa: E501
    id: StrictStr = Field(description="The ID of the dbt project version. This value is generated automatically.")
    version: StrictInt = Field(description="The number of the dbt project version.")
    default_run_parameter: DbtProjectRunParameter = Field(alias="defaultRunParameter")
    sha256: Optional[Annotated[str, Field(min_length=64, strict=True, max_length=64)]] = Field(default=None, description="The SHA-256 hash value of the dbt project zip file, encoded in lower case hexadecimal format.")
    updated_at: datetime = Field(description="The ISO 8601 formatted timestamp representing the update time of the dbt project version.", alias="updatedAt")
    __properties: ClassVar[List[str]] = ["id", "version", "defaultRunParameter", "sha256", "updatedAt"]

    @field_validator('sha256')
    def sha256_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if value is None:
            return value

        if not re.match(r"^[0-9a-f]*$", value):
            raise ValueError(r"must validate the regular expression /^[0-9a-f]*$/")
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
        """Create an instance of DbtProjectVersion from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of default_run_parameter
        if self.default_run_parameter:
            _dict['defaultRunParameter'] = self.default_run_parameter.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of DbtProjectVersion from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "version": obj.get("version"),
            "defaultRunParameter": DbtProjectRunParameter.from_dict(obj["defaultRunParameter"]) if obj.get("defaultRunParameter") is not None else None,
            "sha256": obj.get("sha256"),
            "updatedAt": obj.get("updatedAt")
        })
        return _obj


