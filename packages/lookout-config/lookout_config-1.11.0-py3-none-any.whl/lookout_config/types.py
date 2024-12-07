# Updates here should also be made to:
# * lookout_interfaces/msg/Config.msg
# * lookout_config_manager/mappers.py

from typing import Optional, Any
from enum import Enum
from pydantic import BaseModel, field_validator, ConfigDict
from pydantic.fields import Field

from greenstream_config.types import Camera, Offsets


class Mode(str, Enum):
    SIMULATOR = "simulator"
    HARDWARE = "hardware"
    STUBS = "stubs"
    ROSBAG = "rosbag"

    def __str__(self):
        return self.value


class PositioningSystem(str, Enum):
    NONE = "none"
    SEPTENTRIO_INS = "septentrio_ins"
    ADNAV_INS = "advanced_navigation_ins"
    NMEA_2000_SAT_COMPASS = "nmea_2000_sat_compass"
    NMEA_2000_COMPASS = "nmea_2000_compass"
    NMEA_0183_SAT_COMPASS = "nmea_0183_sat_compass"
    NMEA_0183_COMPASS = "nmea_0183_compass"

    def __str__(self):
        return self.value


class LogLevel(str, Enum):
    INFO = "info"
    DEBUG = "debug"

    def __str__(self):
        return self.value


class Network(str, Enum):
    SHARED = "shared"
    HOST = "host"

    def __str__(self):
        return self.value


class GeolocationMode(str, Enum):
    NONE = "none"
    RELATIVE_BEARING = "relative_bearing"
    ABSOLUTE_BEARING = "absolute_bearing"
    RANGE_BEARING = "range_bearing"

    def __str__(self):
        return self.value


class Point(BaseModel):
    x: int
    y: int

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False


class Polygon(BaseModel):
    points: list[Point]


class CameraExtended(Camera):
    ignore_regions: list[Polygon] = Field(default_factory=list)

    @field_validator("ignore_regions")
    def check_polygon(cls, ignore_regions):
        if ignore_regions:
            for polygon in ignore_regions:
                if len(polygon.points) < 4:  # 3 points for a triangle, 1 to close the polygon
                    raise ValueError("Polygon must have at least 3 sides (4 points)")
                if polygon.points[0] != polygon.points[-1]:
                    raise ValueError("Polygon must close. Must have same start and end point")
        return ignore_regions


class VesselOffsets(BaseModel):
    name: str
    baselink_to_ins: Offsets
    baselink_to_waterline: Offsets


class LookoutConfig(BaseModel):
    # So enum values are written and read to the yml correctly
    model_config = ConfigDict(
        use_enum_values=False,
        json_encoders={
            Mode: lambda v: v.value,
            LogLevel: lambda v: v.value,
            Network: lambda v: v.value,
            GeolocationMode: lambda v: v.value,
            PositioningSystem: lambda v: v.value,
        },
    )
    ros_domain_id: int = Field(
        default=0,
        description="ROS domain ID for the vessel. This only applies if 'simple_discovery' is true.",
    )
    namespace_vessel: str = "vessel_1"
    gama_vessel: bool = False
    mode: Mode = Mode.HARDWARE
    log_level: LogLevel = LogLevel.INFO
    cameras: list[CameraExtended] = Field(default_factory=list)
    network: Network = Network.HOST
    gpu: bool = True
    geolocation_mode: GeolocationMode = GeolocationMode.NONE
    positioning_system: PositioningSystem = PositioningSystem.NONE
    offsets: VesselOffsets = VesselOffsets(
        name="mars.stl",
        baselink_to_ins=Offsets(forward=1.4160, left=0.153, up=0.184),
        baselink_to_waterline=Offsets(
            up=0.3,
        ),
    )
    components: Any = Field(default_factory=dict)
    prod: bool = True
    log_directory: str = "~/greenroom/lookout/logs"
    recording_directory: str = "~/greenroom/lookout/recordings"
    with_discovery_server: bool = Field(
        default=True, description="Run the discovery server. It will bind to 0.0.0.0:11811"
    )
    simple_discovery: bool = Field(
        default=False,
        description="Use simple discovery. This should NOT be used in production due to performance issues.",
    )
    discovery_server_ip: str = Field(
        default="0.0.0.0",
        description="IP/host/interface of the discovery server. Assumes port of 11811",
    )
    own_ip: str = Field(
        default="0.0.0.0",
        description="IP/host/interface address of the primary network interface. This is where DDS traffic will route to.",
    )
