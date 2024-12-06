# coding: utf-8



from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from typing import Optional, Set
from typing_extensions import Self

class SubscriptionCreate(BaseModel):
    """
    SubscriptionCreate
    """ # noqa: E501
    name: StrictStr = Field(description="The name of the subscription.")
    target: StrictStr = Field(description="The target of the subscription. Allowed values are: import, dbt and pipeline.")
    destination_url: StrictStr = Field(description="The URL of the destination.", alias="destinationUrl")
    filter: Optional[StrictStr] = Field(default=None, description="The filter to apply to the subscription. The message has attributes due to the target of the subscription as follows. import   - datasetId, datasetName, importId dbt      - dbtProjectId, dbtProjectName, dbtRunId pipeline - pipelineId, pipelineName, pipelineRunId See https://cloud.google.com/pubsub/docs/subscription-message-filter for the filter syntax.")
    token_audience: Optional[StrictStr] = Field(default=None, description="Audience used in the generated Open ID Connect token for authenticated push. If not specified, it will be set to the push-endpoint. See https://cloud.google.com/sdk/gcloud/reference/pubsub/subscriptions/create#--push-auth-token-audience", alias="tokenAudience")
    ack_deadline: Optional[Annotated[int, Field(le=600, strict=True, ge=10)]] = Field(default=None, description="The acknowledge deadline of the subscription in seconds.", alias="ackDeadline")
    __properties: ClassVar[List[str]] = ["name", "target", "destinationUrl", "filter", "tokenAudience", "ackDeadline"]

    @field_validator('target')
    def target_validate_enum(cls, value):
        """Validates the enum"""
        if value not in set(['import', 'dbt', 'pipeline']):
            raise ValueError("must be one of enum values ('import', 'dbt', 'pipeline')")
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
        """Create an instance of SubscriptionCreate from a JSON string"""
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
        """Create an instance of SubscriptionCreate from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "name": obj.get("name"),
            "target": obj.get("target"),
            "destinationUrl": obj.get("destinationUrl"),
            "filter": obj.get("filter"),
            "tokenAudience": obj.get("tokenAudience"),
            "ackDeadline": obj.get("ackDeadline")
        })
        return _obj


