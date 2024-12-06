# coding: utf-8



from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from typing import Optional, Set
from typing_extensions import Self

class SubscriptionUpdate(BaseModel):
    """
    SubscriptionUpdate
    """ # noqa: E501
    destination_url: Optional[StrictStr] = Field(default=None, description="The URL of the destination.", alias="destinationUrl")
    token_audience: Optional[StrictStr] = Field(default=None, description="Audience used in the generated Open ID Connect token for authenticated push.", alias="tokenAudience")
    ack_deadline: Optional[Annotated[int, Field(le=600, strict=True, ge=10)]] = Field(default=None, description="The acknowledge deadline of the subscription in seconds.", alias="ackDeadline")
    __properties: ClassVar[List[str]] = ["destinationUrl", "tokenAudience", "ackDeadline"]

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
        """Create an instance of SubscriptionUpdate from a JSON string"""
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
        """Create an instance of SubscriptionUpdate from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "destinationUrl": obj.get("destinationUrl"),
            "tokenAudience": obj.get("tokenAudience"),
            "ackDeadline": obj.get("ackDeadline")
        })
        return _obj


