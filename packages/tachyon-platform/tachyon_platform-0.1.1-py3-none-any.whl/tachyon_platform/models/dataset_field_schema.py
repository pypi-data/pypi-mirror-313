# coding: utf-8



from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class DatasetFieldSchema(BaseModel):
    """
    DatasetFieldSchema
    """ # noqa: E501
    name: StrictStr
    type: StrictStr
    mode: Optional[StrictStr] = None
    fields: Optional[List[DatasetFieldSchema]] = None
    description: Optional[StrictStr] = None
    max_length: Optional[StrictStr] = Field(default=None, alias="maxLength")
    precision: Optional[StrictStr] = None
    scale: Optional[StrictStr] = None
    collation: Optional[StrictStr] = None
    default_value_expression: Optional[StrictStr] = Field(default=None, alias="defaultValueExpression")
    __properties: ClassVar[List[str]] = ["name", "type", "mode", "fields", "description", "maxLength", "precision", "scale", "collation", "defaultValueExpression"]

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
        """Create an instance of DatasetFieldSchema from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in fields (list)
        _items = []
        if self.fields:
            for _item_fields in self.fields:
                if _item_fields:
                    _items.append(_item_fields.to_dict())
            _dict['fields'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of DatasetFieldSchema from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "name": obj.get("name"),
            "type": obj.get("type"),
            "mode": obj.get("mode"),
            "fields": [DatasetFieldSchema.from_dict(_item) for _item in obj["fields"]] if obj.get("fields") is not None else None,
            "description": obj.get("description"),
            "maxLength": obj.get("maxLength"),
            "precision": obj.get("precision"),
            "scale": obj.get("scale"),
            "collation": obj.get("collation"),
            "defaultValueExpression": obj.get("defaultValueExpression")
        })
        return _obj

# TODO: Rewrite to not use raise_errors
DatasetFieldSchema.model_rebuild(raise_errors=False)

