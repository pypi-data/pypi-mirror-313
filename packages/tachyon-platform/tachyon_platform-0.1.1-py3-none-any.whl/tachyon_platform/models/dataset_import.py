# coding: utf-8



from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from tachyon_platform.models.dataset_import_action import DatasetImportAction
from tachyon_platform.models.dataset_import_csv_options import DatasetImportCsvOptions
from typing import Optional, Set
from typing_extensions import Self

class DatasetImport(BaseModel):
    """
    DatasetImport
    """ # noqa: E501
    id: StrictStr = Field(description="The ID of the dataset import. This value is generated automatically.")
    name: StrictStr = Field(description="The name of the dataset import.")
    dataset_id: Optional[StrictStr] = Field(default=None, description="The ID of the target dataset for this import.", alias="datasetId")
    dataset_name: StrictStr = Field(description="The name of the target dataset for this import.", alias="datasetName")
    action: DatasetImportAction
    message: StrictStr = Field(description="BigQuery error messages output when running this import job.")
    status: StrictStr = Field(description="The status of the dataset import job.")
    imported_rows: StrictInt = Field(description="The number of rows imported in a dataset import job.", alias="importedRows")
    create_time: datetime = Field(description="Time when the job created.", alias="createTime")
    start_time: datetime = Field(description="Time when the job started.", alias="startTime")
    end_time: datetime = Field(description="Time when the job ended.", alias="endTime")
    max_bad_records: Optional[StrictInt] = Field(default=None, description="MaxBadRecords is the maximum number of bad records that will be ignored when reading data.", alias="maxBadRecords")
    source_format: StrictStr = Field(description="SourceFormat is the format of the data to be read. Allowed values are: CSV and PARQUET.", alias="sourceFormat")
    csv_options: Optional[DatasetImportCsvOptions] = Field(default=None, alias="csvOptions")
    with_snapshot: StrictBool = Field(description="If true, create a snapshot of the BigQuery table before import.", alias="withSnapshot")
    __properties: ClassVar[List[str]] = ["id", "name", "datasetId", "datasetName", "action", "message", "status", "importedRows", "createTime", "startTime", "endTime", "maxBadRecords", "sourceFormat", "csvOptions", "withSnapshot"]

    @field_validator('status')
    def status_validate_enum(cls, value):
        """Validates the enum"""
        if value not in set(['INVALID', 'INITIALIZED', 'FINISHED', 'FAILED', 'INPROGRESS', 'DELETED']):
            raise ValueError("must be one of enum values ('INVALID', 'INITIALIZED', 'FINISHED', 'FAILED', 'INPROGRESS', 'DELETED')")
        return value

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
        """Create an instance of DatasetImport from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of action
        if self.action:
            _dict['action'] = self.action.to_dict()
        # override the default output from pydantic by calling `to_dict()` of csv_options
        if self.csv_options:
            _dict['csvOptions'] = self.csv_options.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of DatasetImport from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "name": obj.get("name"),
            "datasetId": obj.get("datasetId"),
            "datasetName": obj.get("datasetName"),
            "action": DatasetImportAction.from_dict(obj["action"]) if obj.get("action") is not None else None,
            "message": obj.get("message"),
            "status": obj.get("status"),
            "importedRows": obj.get("importedRows"),
            "createTime": obj.get("createTime"),
            "startTime": obj.get("startTime"),
            "endTime": obj.get("endTime"),
            "maxBadRecords": obj.get("maxBadRecords"),
            "sourceFormat": obj.get("sourceFormat"),
            "csvOptions": DatasetImportCsvOptions.from_dict(obj["csvOptions"]) if obj.get("csvOptions") is not None else None,
            "withSnapshot": obj.get("withSnapshot")
        })
        return _obj


