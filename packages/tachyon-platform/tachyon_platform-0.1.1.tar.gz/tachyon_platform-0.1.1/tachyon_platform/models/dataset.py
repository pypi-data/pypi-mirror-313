# coding: utf-8



from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from tachyon_platform.models.dataset_clustering import DatasetClustering
from tachyon_platform.models.dataset_created_by import DatasetCreatedBy
from tachyon_platform.models.dataset_field_schema import DatasetFieldSchema
from tachyon_platform.models.dataset_notification_config import DatasetNotificationConfig
from tachyon_platform.models.dataset_range_partitioning import DatasetRangePartitioning
from tachyon_platform.models.dataset_time_partitioning import DatasetTimePartitioning
from typing import Optional, Set
from typing_extensions import Self

class Dataset(BaseModel):
    """
    Dataset
    """ # noqa: E501
    id: StrictStr = Field(description="The ID of the dataset. This value is generated automatically.")
    name: Annotated[str, Field(strict=True, max_length=128)] = Field(description="The name of the dataset. It is used as the BigQuery table name.")
    description: Annotated[str, Field(strict=True, max_length=128)] = Field(description="The description of the dataset.")
    bq_dataset: StrictStr = Field(description="Name of the BigQuery dataset where this dataset will be stored.", alias="bqDataset")
    status: StrictStr = Field(description="The status of the resource.")
    created_by: DatasetCreatedBy = Field(alias="createdBy")
    auto_add_import_timestamp: StrictBool = Field(description="When true, add import _IMPORTTIMESTAMP_ field to schema automatically, and populate it using a default value.", alias="autoAddImportTimestamp")
    auto_add_import_job_id: Optional[StrictBool] = Field(default=None, description="When true, add _IMPORTJOBID_ field to schema automatically to enable deleting import.", alias="autoAddImportJobId")
    var_schema: List[DatasetFieldSchema] = Field(description="Schema describes the fields in a BigQuery table.", alias="schema")
    time_partitioning: Optional[DatasetTimePartitioning] = Field(default=None, alias="timePartitioning")
    range_partitioning: Optional[DatasetRangePartitioning] = Field(default=None, alias="rangePartitioning")
    clustering: Optional[DatasetClustering] = None
    write_disposition: Optional[StrictStr] = Field(default=None, description="WriteDisposition specifies how existing data in a destination table is treated. Default is WriteAppend.", alias="writeDisposition")
    importable: StrictBool = Field(description="If true, data import can be performed.")
    notification_config: Optional[DatasetNotificationConfig] = Field(default=None, alias="notificationConfig")
    __properties: ClassVar[List[str]] = ["id", "name", "description", "bqDataset", "status", "createdBy", "autoAddImportTimestamp", "autoAddImportJobId", "schema", "timePartitioning", "rangePartitioning", "clustering", "writeDisposition", "importable", "notificationConfig"]

    @field_validator('status')
    def status_validate_enum(cls, value):
        """Validates the enum"""
        if value not in set(['INVALID', 'INITIALIZED', 'READY', 'DELETED']):
            raise ValueError("must be one of enum values ('INVALID', 'INITIALIZED', 'READY', 'DELETED')")
        return value

    @field_validator('write_disposition')
    def write_disposition_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['WRITE_APPEND', 'WRITE_TRUNCATE']):
            raise ValueError("must be one of enum values ('WRITE_APPEND', 'WRITE_TRUNCATE')")
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
        """Create an instance of Dataset from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of created_by
        if self.created_by:
            _dict['createdBy'] = self.created_by.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in var_schema (list)
        _items = []
        if self.var_schema:
            for _item_var_schema in self.var_schema:
                if _item_var_schema:
                    _items.append(_item_var_schema.to_dict())
            _dict['schema'] = _items
        # override the default output from pydantic by calling `to_dict()` of time_partitioning
        if self.time_partitioning:
            _dict['timePartitioning'] = self.time_partitioning.to_dict()
        # override the default output from pydantic by calling `to_dict()` of range_partitioning
        if self.range_partitioning:
            _dict['rangePartitioning'] = self.range_partitioning.to_dict()
        # override the default output from pydantic by calling `to_dict()` of clustering
        if self.clustering:
            _dict['clustering'] = self.clustering.to_dict()
        # override the default output from pydantic by calling `to_dict()` of notification_config
        if self.notification_config:
            _dict['notificationConfig'] = self.notification_config.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of Dataset from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "name": obj.get("name"),
            "description": obj.get("description"),
            "bqDataset": obj.get("bqDataset"),
            "status": obj.get("status"),
            "createdBy": DatasetCreatedBy.from_dict(obj["createdBy"]) if obj.get("createdBy") is not None else None,
            "autoAddImportTimestamp": obj.get("autoAddImportTimestamp"),
            "autoAddImportJobId": obj.get("autoAddImportJobId"),
            "schema": [DatasetFieldSchema.from_dict(_item) for _item in obj["schema"]] if obj.get("schema") is not None else None,
            "timePartitioning": DatasetTimePartitioning.from_dict(obj["timePartitioning"]) if obj.get("timePartitioning") is not None else None,
            "rangePartitioning": DatasetRangePartitioning.from_dict(obj["rangePartitioning"]) if obj.get("rangePartitioning") is not None else None,
            "clustering": DatasetClustering.from_dict(obj["clustering"]) if obj.get("clustering") is not None else None,
            "writeDisposition": obj.get("writeDisposition"),
            "importable": obj.get("importable"),
            "notificationConfig": DatasetNotificationConfig.from_dict(obj["notificationConfig"]) if obj.get("notificationConfig") is not None else None
        })
        return _obj


