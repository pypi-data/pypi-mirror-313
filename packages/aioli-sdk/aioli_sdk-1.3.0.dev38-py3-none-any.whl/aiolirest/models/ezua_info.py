# coding: utf-8

"""
    HPE Machine Learning Inference Software (MLIS/Aioli)

    HPE MLIS is *Aioli* -- The AI On-line Inference Platform that enables easy deployment, tracking, and serving of your packaged models regardless of your preferred AI framework.

    The version of the OpenAPI document: 1.3.0-dev38
    Contact: community@determined-ai
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import Any, ClassVar, Dict, List, Optional
from pydantic import BaseModel, StrictBool
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

class EZUAInfo(BaseModel):
    """
    EZUAInfo
    """ # noqa: E501
    air_gapped: Optional[StrictBool] = None
    enabled: Optional[StrictBool] = None
    ngc_enabled: Optional[StrictBool] = None
    show_mlis_signin_page: Optional[StrictBool] = None
    __properties: ClassVar[List[str]] = ["air_gapped", "enabled", "ngc_enabled", "show_mlis_signin_page"]

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True
    }


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of EZUAInfo from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        _dict = self.model_dump(
            by_alias=True,
            exclude={
            },
            exclude_none=True,
        )
        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of EZUAInfo from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "air_gapped": obj.get("air_gapped"),
            "enabled": obj.get("enabled"),
            "ngc_enabled": obj.get("ngc_enabled"),
            "show_mlis_signin_page": obj.get("show_mlis_signin_page")
        })
        return _obj


