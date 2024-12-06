# coding: utf-8



from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from tachyon_platform.models.dataset_import_csv_options import DatasetImportCsvOptions
from typing import Optional, Set
from typing_extensions import Self

class DatasetImportCreate(BaseModel):
    """
    DatasetImportCreate
    """ # noqa: E501
    name: Optional[StrictStr] = Field(default=None, description="The name of the dataset import.")
    source_format: StrictStr = Field(description="SourceFormat is the format of the data to be read. Allowed values are: CSV and PARQUET.", alias="sourceFormat")
    max_bad_records: Optional[StrictInt] = Field(default=None, description="MaxBadRecords is the maximum number of bad records that will be ignored when reading data.", alias="maxBadRecords")
    csv_options: Optional[DatasetImportCsvOptions] = Field(default=None, alias="csvOptions")
    with_snapshot: Optional[StrictBool] = Field(default=None, description="If true, create a snapshot of the BigQuery table before import.", alias="withSnapshot")
    __properties: ClassVar[List[str]] = ["name", "sourceFormat", "maxBadRecords", "csvOptions", "withSnapshot"]

    @field_validator('source_format')
    def source_format_validate_enum(cls, value):
        """Validates the enum"""
        if value not in set(['CSV', 'PARQUET']):
            raise ValueError("must be one of enum values ('CSV', 'PARQUET')")
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
        """Create an instance of DatasetImportCreate from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of csv_options
        if self.csv_options:
            _dict['csvOptions'] = self.csv_options.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of DatasetImportCreate from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "name": obj.get("name"),
            "sourceFormat": obj.get("sourceFormat"),
            "maxBadRecords": obj.get("maxBadRecords"),
            "csvOptions": DatasetImportCsvOptions.from_dict(obj["csvOptions"]) if obj.get("csvOptions") is not None else None,
            "withSnapshot": obj.get("withSnapshot")
        })
        return _obj


