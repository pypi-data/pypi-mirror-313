from enum import Enum
from typing import Optional, List, Union, Dict

from pydantic import BaseModel, Field
from pydantic_geojson import PolygonModel, MultiPolygonModel


class TargetSensor(Enum):
    SENTINEL2 = 'Sentinel-2'
    PS2 = 'PS2'


class ResamplingMethod(Enum):
    BILINEAR = "bilinear"
    CUBIC = "cubic"
    CUBICSPLINE = "cubicspline"
    LANCZOS = "lanczos"
    AVERAGE = "average"
    MODE = "mode"
    MIN = "min"
    MAX = "max"
    MED = "med"
    Q1 = "q1"
    Q3 = "q3"


class PixelType(Enum):
    Unsigned8bit = "8U"
    Unsigned16bit = "16U"
    Signed16bit = "16S"
    FloatingPoint32Bit = "32R"


class CompositeGroup(Enum):
    ORDER = 'order'
    STRIP = 'strip_id'


class Format(Enum):
    COG = 'COG'
    PL_NITF = 'PL_NITF'


class BandMathObject(BaseModel):
    """
    See https://developers.planet.com/apis/orders/tools/#band-math and
    https://developers.planet.com/apis/orders/bandmath-numpy-routines/ to learn more.
    """
    b1: Optional[str] = None
    b2: Optional[str] = None
    b3: Optional[str] = None
    b4: Optional[str] = None
    b5: Optional[str] = None
    b6: Optional[str] = None
    b7: Optional[str] = None
    b8: Optional[str] = None
    b9: Optional[str] = None
    b10: Optional[str] = None
    b11: Optional[str] = None
    b12: Optional[str] = None
    b13: Optional[str] = None
    b14: Optional[str] = None
    b15: Optional[str] = None
    expression: Optional[str] = None
    pixel_type: Optional[PixelType] = None


class SceneClipObject(BaseModel):
    aoi: Union[PolygonModel, MultiPolygonModel]


class BasemapClipObject(BaseModel):
    # There are no parameters for this operation. Just initialize the class and go!
    clip: Dict = {}


class CompositeObject(BaseModel):
    group_by: Optional[CompositeGroup] = None


class CoRegisterObject(BaseModel):
    anchor_item: str


class FileFormatObject(BaseModel):
    format: Format


class HarmonizeObject(BaseModel):
    target_sensor: TargetSensor = Field(description='Sentinel-2 or PS2')


class MergeObject(BaseModel):
    # There are no parameters for this operation. Just initialize the class and go!
    merge: Dict = {}


class ToarObject(BaseModel):
    scale_factor: float


class ReprojectObject(BaseModel):
    projection: str
    kernel: Optional[ResamplingMethod] = None
    resolution: Optional[float] = None


class TileObject(BaseModel):
    name_template: Optional[str] = None
    origin_x: Optional[float] = None
    origin_y: Optional[float] = None
    pixel_size: Optional[float] = None
    tile_size: float
    conformal_x_scaling: bool = Field(default=False)


class CloudFilterObject(BaseModel):
    clear_min: float
    cloud_max: float


class HasToolsList(BaseModel):
    tools: List[Union[HarmonizeObject,
    CoRegisterObject, ToarObject, SceneClipObject, BasemapClipObject,
    ReprojectObject, BandMathObject, CompositeObject, TileObject,
    CloudFilterObject, FileFormatObject, MergeObject]] = []


class CouldHaveToolsList(BaseModel):
    tools: Optional[List[Union[HarmonizeObject,
    CoRegisterObject, ToarObject, SceneClipObject, BasemapClipObject,
    ReprojectObject, BandMathObject, CompositeObject, TileObject, CloudFilterObject,
    FileFormatObject, MergeObject]]] = None
