# coding: utf-8



from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from tachyon_platform.models.dataset_field_schema import DatasetFieldSchema
from tachyon_platform.models.file_format import FileFormat
from typing import Optional, Set
from typing_extensions import Self

class File(BaseModel):
    """
    File
    """ # noqa: E501
    id: StrictStr = Field(description="The id of the file.")
    resource_name: StrictStr = Field(description="The full Dataplex GCP resource name of the file. It can be used to retrieve a specific file from the GCP API. Reference: https://cloud.google.com/iam/docs/conditions-resource-attributes#resource-name", alias="resourceName")
    description: Optional[Annotated[str, Field(strict=True, max_length=1024)]] = Field(default=None, description="The description of the file.")
    data_path: StrictStr = Field(description="The storage path of the file data. For Cloud Storage data, this is the fully-qualified path to the entity, such as gs://bucket/path/to/data.", alias="dataPath")
    format: FileFormat
    var_schema: Optional[List[DatasetFieldSchema]] = Field(default=None, description="Schema describes the fields in a BigQuery table.", alias="schema")
    is_schema_inference_failed: Optional[StrictBool] = Field(default=None, description="Whether schema inference failed.", alias="isSchemaInferenceFailed")
    schema_inference_error: Optional[StrictStr] = Field(default=None, description="The error message when schema inference failed.", alias="schemaInferenceError")
    size_bytes: StrictInt = Field(description="The size of the file in bytes.", alias="sizeBytes")
    type: StrictStr = Field(description="The type of the response.")
    create_time: datetime = Field(description="Time when the file is created.", alias="createTime")
    update_time: Optional[datetime] = Field(default=None, description="Time when the file is updated.", alias="updateTime")
    __properties: ClassVar[List[str]] = ["id", "resourceName", "description", "dataPath", "format", "schema", "isSchemaInferenceFailed", "schemaInferenceError", "sizeBytes", "type", "createTime", "updateTime"]

    @field_validator('type')
    def type_validate_enum(cls, value):
        """Validates the enum"""
        if value not in set(['FILE', 'FOLDER']):
            raise ValueError("must be one of enum values ('FILE', 'FOLDER')")
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
        """Create an instance of File from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of format
        if self.format:
            _dict['format'] = self.format.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in var_schema (list)
        _items = []
        if self.var_schema:
            for _item_var_schema in self.var_schema:
                if _item_var_schema:
                    _items.append(_item_var_schema.to_dict())
            _dict['schema'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of File from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "resourceName": obj.get("resourceName"),
            "description": obj.get("description"),
            "dataPath": obj.get("dataPath"),
            "format": FileFormat.from_dict(obj["format"]) if obj.get("format") is not None else None,
            "schema": [DatasetFieldSchema.from_dict(_item) for _item in obj["schema"]] if obj.get("schema") is not None else None,
            "isSchemaInferenceFailed": obj.get("isSchemaInferenceFailed"),
            "schemaInferenceError": obj.get("schemaInferenceError"),
            "sizeBytes": obj.get("sizeBytes"),
            "type": obj.get("type"),
            "createTime": obj.get("createTime"),
            "updateTime": obj.get("updateTime")
        })
        return _obj


