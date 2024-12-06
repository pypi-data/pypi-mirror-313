# coding: utf-8



from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from tachyon_platform.models.user_role import UserRole
from typing import Optional, Set
from typing_extensions import Self

class UserInvitation(BaseModel):
    """
    UserInvitation
    """ # noqa: E501
    organization_id: StrictStr = Field(description="The ID of the organization in Auth0 to which the user will be invited.", alias="organizationId")
    inviter_name: StrictStr = Field(description="The name of the user who is inviting the new user.", alias="inviterName")
    invitee_email_address: StrictStr = Field(description="Email address of the user to invite.", alias="inviteeEmailAddress")
    roles: List[UserRole] = Field(description="List of roles to assign to the invited user. If no roles are specified, the user will be invited as a member without any roles.")
    created_at: Optional[datetime] = Field(default=None, description="The ISO 8601 formatted timestamp representing the creation time of the invitation.", alias="createdAt")
    expires_at: Optional[datetime] = Field(default=None, description="The ISO 8601 formatted timestamp representing the expiration time of the invitation.", alias="expiresAt")
    __properties: ClassVar[List[str]] = ["organizationId", "inviterName", "inviteeEmailAddress", "roles", "createdAt", "expiresAt"]

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
        """Create an instance of UserInvitation from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in roles (list)
        _items = []
        if self.roles:
            for _item_roles in self.roles:
                if _item_roles:
                    _items.append(_item_roles.to_dict())
            _dict['roles'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of UserInvitation from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "organizationId": obj.get("organizationId"),
            "inviterName": obj.get("inviterName"),
            "inviteeEmailAddress": obj.get("inviteeEmailAddress"),
            "roles": [UserRole.from_dict(_item) for _item in obj["roles"]] if obj.get("roles") is not None else None,
            "createdAt": obj.get("createdAt"),
            "expiresAt": obj.get("expiresAt")
        })
        return _obj


