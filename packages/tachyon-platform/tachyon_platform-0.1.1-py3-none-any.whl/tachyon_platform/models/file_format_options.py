# coding: utf-8



from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class FileFormatOptions(BaseModel):
    """
    The CSV format of the file data.
    """ # noqa: E501
    encoding: Optional[StrictStr] = Field(default=None, description="The encoding of the file.")
    delimiter: Optional[StrictStr] = Field(default=None, description="The delimiter of the CSV file.")
    header_rows: Optional[StrictInt] = Field(default=None, description="The number of header rows in the CSV file.", alias="headerRows")
    quote: Optional[StrictStr] = Field(default=None, description="The quote character of the CSV file.")
    metadata_location: Optional[StrictStr] = Field(default=None, description="The location of the metadata file of the Iceberg table.", alias="metadataLocation")
    __properties: ClassVar[List[str]] = ["encoding", "delimiter", "headerRows", "quote", "metadataLocation"]

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
        """Create an instance of FileFormatOptions from a JSON string"""
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
        """Create an instance of FileFormatOptions from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "encoding": obj.get("encoding"),
            "delimiter": obj.get("delimiter"),
            "headerRows": obj.get("headerRows"),
            "quote": obj.get("quote"),
            "metadataLocation": obj.get("metadataLocation")
        })
        return _obj


