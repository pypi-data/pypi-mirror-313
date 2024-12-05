# coding: utf-8

"""
    Jungfraujoch

    API to control Jungfraujoch developed by the Paul Scherrer Institute (Switzerland). Jungfraujoch is a data acquisition and analysis system for pixel array detectors, primarly PSI JUNGFRAU. Jungfraujoch uses FPGA boards to acquire data at high data rates. 

    The version of the OpenAPI document: 1.0.0-rc.27
    Contact: filip.leonarski@psi.ch
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field
from typing import Any, ClassVar, Dict, List, Union
from typing_extensions import Annotated
from typing import Optional, Set
from typing_extensions import Self

class DatasetSettingsUnitCell(BaseModel):
    """
    Unit cell parameters. Necessary to run indexing. Units of angstrom and degree
    """ # noqa: E501
    a: Union[Annotated[float, Field(strict=True, ge=0)], Annotated[int, Field(strict=True, ge=0)]]
    b: Union[Annotated[float, Field(strict=True, ge=0)], Annotated[int, Field(strict=True, ge=0)]]
    c: Union[Annotated[float, Field(strict=True, ge=0)], Annotated[int, Field(strict=True, ge=0)]]
    alpha: Union[Annotated[float, Field(le=360, strict=True, ge=0)], Annotated[int, Field(le=360, strict=True, ge=0)]]
    beta: Union[Annotated[float, Field(le=360, strict=True, ge=0)], Annotated[int, Field(le=360, strict=True, ge=0)]]
    gamma: Union[Annotated[float, Field(le=360, strict=True, ge=0)], Annotated[int, Field(le=360, strict=True, ge=0)]]
    __properties: ClassVar[List[str]] = ["a", "b", "c", "alpha", "beta", "gamma"]

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
        """Create an instance of DatasetSettingsUnitCell from a JSON string"""
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
        """Create an instance of DatasetSettingsUnitCell from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "a": obj.get("a"),
            "b": obj.get("b"),
            "c": obj.get("c"),
            "alpha": obj.get("alpha"),
            "beta": obj.get("beta"),
            "gamma": obj.get("gamma")
        })
        return _obj


