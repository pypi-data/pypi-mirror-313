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

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictFloat, StrictInt, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional, Union
from typing_extensions import Annotated
from typing import Optional, Set
from typing_extensions import Self

class MeasurementStatistics(BaseModel):
    """
    MeasurementStatistics
    """ # noqa: E501
    file_prefix: Optional[StrictStr] = None
    run_number: Optional[StrictInt] = Field(default=None, description="Number of data collection run. This can be either automatically incremented or provided externally for each data collection. ")
    experiment_group: Optional[StrictStr] = Field(default=None, description="Name of group owning the data (e.g. p-group or proposal number). ")
    images_expected: Optional[StrictInt] = None
    images_collected: Optional[StrictInt] = Field(default=None, description="Images collected by the receiver. This number will be lower than images expected if there were issues with data collection performance. ")
    images_sent: Optional[StrictInt] = Field(default=None, description="Images sent to the writer.  The value does not include images discarded by lossy compression filter and images not forwarded due to full ZeroMQ queue. ")
    images_discarded_lossy_compression: Optional[StrictInt] = Field(default=None, description="Images discarded by the lossy compression filter")
    max_image_number_sent: Optional[StrictInt] = None
    collection_efficiency: Optional[Union[Annotated[float, Field(le=1.0, strict=True, ge=0.0)], Annotated[int, Field(le=1, strict=True, ge=0)]]] = None
    compression_ratio: Optional[Union[Annotated[float, Field(strict=True, ge=0.0)], Annotated[int, Field(strict=True, ge=0)]]] = None
    cancelled: Optional[StrictBool] = None
    max_receiver_delay: Optional[StrictInt] = None
    indexing_rate: Optional[Union[StrictFloat, StrictInt]] = None
    detector_width: Optional[StrictInt] = None
    detector_height: Optional[StrictInt] = None
    detector_pixel_depth: Optional[StrictInt] = None
    bkg_estimate: Optional[Union[StrictFloat, StrictInt]] = None
    unit_cell: Optional[StrictStr] = None
    __properties: ClassVar[List[str]] = ["file_prefix", "run_number", "experiment_group", "images_expected", "images_collected", "images_sent", "images_discarded_lossy_compression", "max_image_number_sent", "collection_efficiency", "compression_ratio", "cancelled", "max_receiver_delay", "indexing_rate", "detector_width", "detector_height", "detector_pixel_depth", "bkg_estimate", "unit_cell"]

    @field_validator('detector_pixel_depth')
    def detector_pixel_depth_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set([2, 4]):
            raise ValueError("must be one of enum values (2, 4)")
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
        """Create an instance of MeasurementStatistics from a JSON string"""
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
        """Create an instance of MeasurementStatistics from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "file_prefix": obj.get("file_prefix"),
            "run_number": obj.get("run_number"),
            "experiment_group": obj.get("experiment_group"),
            "images_expected": obj.get("images_expected"),
            "images_collected": obj.get("images_collected"),
            "images_sent": obj.get("images_sent"),
            "images_discarded_lossy_compression": obj.get("images_discarded_lossy_compression"),
            "max_image_number_sent": obj.get("max_image_number_sent"),
            "collection_efficiency": obj.get("collection_efficiency"),
            "compression_ratio": obj.get("compression_ratio"),
            "cancelled": obj.get("cancelled"),
            "max_receiver_delay": obj.get("max_receiver_delay"),
            "indexing_rate": obj.get("indexing_rate"),
            "detector_width": obj.get("detector_width"),
            "detector_height": obj.get("detector_height"),
            "detector_pixel_depth": obj.get("detector_pixel_depth"),
            "bkg_estimate": obj.get("bkg_estimate"),
            "unit_cell": obj.get("unit_cell")
        })
        return _obj


