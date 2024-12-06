#!/usr/bin/env python3
import json
from dataclasses import dataclass, field
from typing import NamedTuple, Union, List, Tuple
from pymavlink.dialects.v20.ardupilotmega import \
    MAV_FRAME_GLOBAL_RELATIVE_ALT, MAV_MISSION_TYPE_FENCE, MAV_CMD_NAV_FENCE_RETURN_POINT, \
    MAV_CMD_NAV_FENCE_POLYGON_VERTEX_INCLUSION, MAV_CMD_NAV_FENCE_POLYGON_VERTEX_EXCLUSION, \
    MAV_CMD_NAV_FENCE_CIRCLE_INCLUSION, MAV_CMD_NAV_FENCE_CIRCLE_EXCLUSION, \
    MAV_CMD_NAV_RALLY_POINT, MAV_MISSION_TYPE_RALLY, MAV_MISSION_TYPE_MISSION

LON_LAT_FACTOR = 1e7


class Point2D(NamedTuple):
    x: float
    y: float


class Point3D(NamedTuple):
    x: float
    y: float
    z: float


class MissionItemArguments(NamedTuple):
    seq: int
    frame: int
    command: int
    current: int
    auto_continue: int


class ParamList(NamedTuple):
    param1: float
    param2: float
    param3: float
    param4: float
    x: float
    y: float
    z: float


@dataclass
class MissionItem:
    arguments: MissionItemArguments
    params: ParamList
    mission_type: int


@dataclass
class GeofenceItem:
    inclusion: bool


@dataclass
class Circle(GeofenceItem):
    center: Point2D
    radius: float


@dataclass
class Polygon(GeofenceItem):
    points: List[Point2D]


@dataclass
class Waypoint:
    # pylint: disable=too-many-instance-attributes
    auto_continue: bool
    command: int
    do_jump_id: int
    frame: int
    params: ParamList
    type_: str
    amsl_alt_above_terrain: Union[float, None]
    altitude: Union[float, None]
    altitude_mode: Union[int, None]


@dataclass
class HasMissionItemRepresentation:
    def get_mission_item_representation(self) -> List[MissionItem]:
        pass


@dataclass
class Mission(HasMissionItemRepresentation):
    cruise_speed: float
    firmware_type: int
    global_plan_altitude_mode: int
    hover_speed: float

    waypoints: List[Waypoint]

    def get_mission_item_representation(self) -> Tuple[int, List[MissionItem]]:
        mission_item_list = []
        seq_n = 0

        for waypoint in self.waypoints:
            mission_item_list.append(
                MissionItem(
                    arguments=MissionItemArguments(
                        seq=seq_n,
                        command=waypoint.command,
                        auto_continue=waypoint.auto_continue,
                        current=0,
                        frame=waypoint.frame,
                    ),
                    params=ParamList(
                        param1=waypoint.params.param1,
                        param2=waypoint.params.param2,
                        param3=waypoint.params.param3,
                        param4=waypoint.params.param4,
                        x=int(waypoint.params.x * LON_LAT_FACTOR),
                        y=int(waypoint.params.y * LON_LAT_FACTOR),
                        z=waypoint.params.z,
                    ),
                    mission_type=MAV_MISSION_TYPE_MISSION
                )
            )
            seq_n += 1
        return seq_n, mission_item_list


@dataclass
class GeoFence(HasMissionItemRepresentation):
    breach_return: Union[Point3D, None]
    circles: List[Circle]
    polygons: List[Polygon]

    def get_mission_item_representation(self) -> Tuple[int, List[MissionItem]]:
        mission_item_list = []
        seq_n = 0
        if self.breach_return is not None:
            mission_item_list.append(
                MissionItem(
                    arguments=MissionItemArguments(
                        seq=seq_n,
                        command=MAV_CMD_NAV_FENCE_RETURN_POINT,
                        auto_continue=0,
                        current=0,
                        frame=MAV_FRAME_GLOBAL_RELATIVE_ALT,
                    ),
                    params=ParamList(
                        param1=0,
                        param2=0,
                        param3=0,
                        param4=0,
                        x=int(self.breach_return.x * LON_LAT_FACTOR),
                        y=int(self.breach_return.y * LON_LAT_FACTOR),
                        z=self.breach_return.z
                    ),
                    mission_type=MAV_MISSION_TYPE_FENCE
                )
            )
            seq_n += 1

        for polygon in self.polygons:
            for point in polygon.points:
                command = (MAV_CMD_NAV_FENCE_POLYGON_VERTEX_INCLUSION if polygon.inclusion else
                           MAV_CMD_NAV_FENCE_POLYGON_VERTEX_EXCLUSION)
                mission_item_list.append(
                    MissionItem(
                        arguments=MissionItemArguments(
                            seq=seq_n,
                            command=command,
                            auto_continue=0,
                            current=0,
                            frame=MAV_FRAME_GLOBAL_RELATIVE_ALT,
                        ),
                        params=ParamList(
                            param1=len(polygon.points),
                            param2=0,
                            param3=0,
                            param4=0,
                            x=int(point.x * LON_LAT_FACTOR),
                            y=int(point.y * LON_LAT_FACTOR),
                            z=0
                        ),
                        mission_type=MAV_MISSION_TYPE_FENCE
                    )
                )
                seq_n += 1

        for circle in self.circles:
            command = (MAV_CMD_NAV_FENCE_CIRCLE_INCLUSION if circle.inclusion else
                       MAV_CMD_NAV_FENCE_CIRCLE_EXCLUSION)
            mission_item_list.append(
                MissionItem(
                    arguments=MissionItemArguments(
                        seq=seq_n,
                        command=command,
                        auto_continue=0,
                        current=0,
                        frame=MAV_FRAME_GLOBAL_RELATIVE_ALT,
                    ),
                    params=ParamList(
                        param1=circle.radius,
                        param2=0,
                        param3=0,
                        param4=0,
                        x=int(circle.center.x * LON_LAT_FACTOR),
                        y=int(circle.center.y * LON_LAT_FACTOR),
                        z=0
                    ),
                    mission_type=MAV_MISSION_TYPE_FENCE
                )
            )
            seq_n += 1

        return seq_n, mission_item_list


@dataclass
class Rally(HasMissionItemRepresentation):
    points: List[Point3D]

    def get_mission_item_representation(self) -> Tuple[int, List[MissionItem]]:
        mission_item_list = []
        seq_n = 0

        for point in self.points:
            mission_item_list.append(
                MissionItem(
                    arguments=MissionItemArguments(
                        seq=seq_n,
                        command=MAV_CMD_NAV_RALLY_POINT,
                        auto_continue=0,
                        current=0,
                        frame=MAV_FRAME_GLOBAL_RELATIVE_ALT,
                    ),
                    params=ParamList(
                        param1=0,
                        param2=0,
                        param3=0,
                        param4=0,
                        x=int(point.x * LON_LAT_FACTOR),
                        y=int(point.y * LON_LAT_FACTOR),
                        z=point.z
                    ),
                    mission_type=MAV_MISSION_TYPE_RALLY
                )
            )
            seq_n += 1

        return seq_n, mission_item_list


@dataclass
class Plan:
    path: str

    type: str = field(init=False)
    gc: str = field(init=False)

    geofence: GeoFence = field(init=False)
    mission: Mission = field(init=False)
    rally_points: Rally = field(init=False)

    def __post_init__(self):
        data = {}
        with open(self.path, encoding='utf-8') as f:
            data = json.load(f)

        self.type = data['fileType']
        self.gc = data['groundStation']

        self.rally_points = Rally([
            Point3D(*x) for x in data['rallyPoints']['points']
        ])

        self.geofence = GeoFence(
            breach_return=None if (gf := data['geoFence'].get('breachReturn')) is None else
            Point3D(*gf),
            circles=[
                Circle(
                    center=Point2D(*x['circle']['center']),
                    radius=x['circle']['radius'],
                    inclusion=x.get('inclusion', False))
                for x in data['geoFence']['circles']
            ],
            polygons=[
                Polygon(
                    points=[Point2D(*p) for p in x['polygon']],
                    inclusion=x.get('inclusion', False)
                ) for x in data['geoFence']['polygons']
            ]
        )

        self.mission = Mission(
            cruise_speed=(mission := data['mission'])['cruiseSpeed'],
            firmware_type=mission['firmwareType'],
            global_plan_altitude_mode=mission['globalPlanAltitudeMode'],
            hover_speed=mission['hoverSpeed'],
            waypoints=[
                Waypoint(
                    amsl_alt_above_terrain=x.get('AMSLAltAboveTerrain'),
                    altitude=x.get('Altitude'),
                    altitude_mode=x.get('AltitudeMode'),
                    do_jump_id=x['doJumpId'],
                    auto_continue=x['autoContinue'],
                    command=x['command'],
                    frame=x['frame'],
                    params=ParamList(*x['params']),
                    type_=x['type']
                ) for x in mission['items']
            ]
        )
