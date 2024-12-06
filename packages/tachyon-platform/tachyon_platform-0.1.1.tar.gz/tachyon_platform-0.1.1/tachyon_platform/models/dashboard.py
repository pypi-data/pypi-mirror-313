# coding: utf-8



from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from tachyon_platform.models.dashboard_superset_user import DashboardSupersetUser
from typing import Optional, Set
from typing_extensions import Self

class Dashboard(BaseModel):
    """
    Dashboard
    """ # noqa: E501
    id: StrictInt
    changed_on_delta_humanized: Optional[StrictStr] = None
    dashboard_title: StrictStr
    owners: List[DashboardSupersetUser]
    status: StrictStr
    url: StrictStr
    __properties: ClassVar[List[str]] = ["id", "changed_on_delta_humanized", "dashboard_title", "owners", "status", "url"]

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
        """Create an instance of Dashboard from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in owners (list)
        _items = []
        if self.owners:
            for _item_owners in self.owners:
                if _item_owners:
                    _items.append(_item_owners.to_dict())
            _dict['owners'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of Dashboard from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "changed_on_delta_humanized": obj.get("changed_on_delta_humanized"),
            "dashboard_title": obj.get("dashboard_title"),
            "owners": [DashboardSupersetUser.from_dict(_item) for _item in obj["owners"]] if obj.get("owners") is not None else None,
            "status": obj.get("status"),
            "url": obj.get("url")
        })
        return _obj


