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

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class InstrumentMetadata(BaseModel):
    """
    Metadata for a measurement instrument
    """ # noqa: E501
    source_name: StrictStr
    source_type: Optional[StrictStr] = Field(default='', description="Type of radiation source. NXmx gives a fixed dictionary, though Jungfraujoch is not enforcing compliance.  https://manual.nexusformat.org/classes/base_classes/NXsource.html#nxsource NXsource allows the following:  Spallation Neutron Source Pulsed Reactor Neutron Source Reactor Neutron Source Synchrotron X-ray Source Pulsed Muon Source Rotating Anode X-ray Fixed Tube X-ray UV Laser Free-Electron Laser Optical Laser Ion Source UV Plasma Source Metal Jet X-ray ")
    instrument_name: StrictStr
    pulsed_source: Optional[StrictBool] = Field(default=False, description="Settings specific to XFEL (e.g., every image has to come from TTL trigger, save pulse ID and event code) ")
    electron_source: Optional[StrictBool] = Field(default=False, description="Settings specific to electron source (e.g., wavelength definition) ")
    __properties: ClassVar[List[str]] = ["source_name", "source_type", "instrument_name", "pulsed_source", "electron_source"]

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
        """Create an instance of InstrumentMetadata from a JSON string"""
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
        """Create an instance of InstrumentMetadata from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "source_name": obj.get("source_name"),
            "source_type": obj.get("source_type") if obj.get("source_type") is not None else '',
            "instrument_name": obj.get("instrument_name"),
            "pulsed_source": obj.get("pulsed_source") if obj.get("pulsed_source") is not None else False,
            "electron_source": obj.get("electron_source") if obj.get("electron_source") is not None else False
        })
        return _obj


