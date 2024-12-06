# coding: utf-8



from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class PipelineVersionInputsValue(BaseModel):
    """
    PipelineVersionInputsValue
    """ # noqa: E501
    type: StrictStr
    default_value: Optional[Any] = Field(default=None, alias="defaultValue")
    __properties: ClassVar[List[str]] = ["type", "defaultValue"]

    @field_validator('type')
    def type_validate_enum(cls, value):
        """Validates the enum"""
        if value not in set(['STRING', 'NUMBER_INTEGER', 'NUMBER_DOUBLE', 'BOOLEAN', 'LIST', 'STRUCT']):
            raise ValueError("must be one of enum values ('STRING', 'NUMBER_INTEGER', 'NUMBER_DOUBLE', 'BOOLEAN', 'LIST', 'STRUCT')")
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
        """Create an instance of PipelineVersionInputsValue from a JSON string"""
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
        # set to None if default_value (nullable) is None
        # and model_fields_set contains the field
        if self.default_value is None and "default_value" in self.model_fields_set:
            _dict['defaultValue'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of PipelineVersionInputsValue from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "type": obj.get("type"),
            "defaultValue": obj.get("defaultValue")
        })
        return _obj


