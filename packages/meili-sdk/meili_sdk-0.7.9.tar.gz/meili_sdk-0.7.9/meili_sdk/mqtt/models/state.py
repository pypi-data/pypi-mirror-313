import typing as t
from datetime import datetime

from meili_sdk.exceptions import ValidationError
from meili_sdk.models.base import BaseModel
from meili_sdk.version import VERSION

__all__ = (
    "VDA5050VehiclePosition",
    "VDA5050NodePosition",
    "VDA5050VehicleBatteryState",
    "VDA5050NodeState",
    "VDA5050StateMessage",
)


CURRENT_HEADER_ID = 0


class VDA5050VehiclePosition(BaseModel):
    x: float
    y: float
    positionInitialized: bool
    theta: float

    def __init__(self, **kwargs):
        kwargs.setdefault("positionInitialized", True)
        super().__init__(**kwargs)

    def validate_theta(self):
        if self.theta < 0 or self.theta > 360:
            raise ValidationError("Theta must be between 0 and 360 degrees")


class VDA5050NodePosition(BaseModel):
    x: float
    y: float
    theta: float

    def validate_theta(self):
        if self.theta < 0 or self.theta > 360:
            raise ValidationError("Theta must be between 0 and 360 degrees")


class VDA5050VehicleBatteryState(BaseModel):
    batteryCharge: float
    batteryVoltage: float
    batteryHealth: int
    charging: bool
    reach: t.Optional[float] = None

    def __init__(self, **kwargs):
        kwargs.setdefault("charging", False)
        super().__init__(**kwargs)


class VDA5050NodeState(BaseModel):
    nodeId: str
    sequenceId: str
    nodePosition: VDA5050NodePosition
    released: bool

    def __init__(self, **kwargs):
        kwargs.setdefault("released", False)
        node_position = kwargs.pop("nodePosition")
        if not isinstance(node_position, VDA5050NodePosition):
            node_position = VDA5050NodePosition(**node_position)
        kwargs["nodePosition"] = node_position
        super().__init__(**kwargs)

class VDA5050ActionState(BaseModel):
    actionId: str
    actionStatus: str
    actionDescription: t.Optional[str] = None
    resultDescription: t.Optional[str] = None

    def validate_actionStatus(self):
        if self.actionId not in ["WAITING", "INITIALIZING", 
                                 "RUNNING", "FINISHED", "FAILED"
                                 ]:
            raise ValidationError("""actionStatus must be one of the following: [
                            "WAITING",
                            "INITIALIZING",
                            "RUNNING",
                            "FINISHED",
                            "FAILED"
                        ]""")
        
class VDA5050ErrorReference(BaseModel):
    referenceKey: str
    referenceValue: str


class VDA5050Error(BaseModel):
    errorType: str
    errorLevel: str
    errorReferences: t.Optional[t.List[VDA5050ErrorReference]] = None
    errorDescription: t.Optional[str] = None

    def validatea_errorLevel(self):
        if self.errorLevel not in ["WARNING", "FATAL"]:
            raise ValidationError("""errorLevel must be one of "WARNING" or "FATAL" """)
        
class VDA5050Velocity(BaseModel):
    vx: float
    vy: float
    omega: float

class VDA5050SafetyState(BaseModel):
    eStop: str
    fieldViolation: bool
    
    def __init__(self, **kwargs) -> None:
        kwargs.setdefault("fieldViolation", False)
        super().__init__(**kwargs)
    
    def validate_eStop(self):
        if self.eStop not in ["AUTOACK", "MANUAL", "REMOTE", "NONE"]:
            raise ValidationError("""eStop must be one of the following: ["AUTOACK", "MANUAL", "REMOTE", "NONE"]""")

class VDA5050StateMessage(BaseModel):
    """
    Message to be sent to FMS MQTT Broker

    When initializing the message, headerId and timestamp will be automatically generated
    """

    headerId: int
    timestamp: datetime
    version: str
    manufacturer: str
    serialNumber: str
    orderId: t.Optional[str] = None
    lastNodeId: t.Optional[str] = None
    lastNodeSequenceId: t.Optional[int] = None
    driving: bool
    paused: bool
    newBaseRequested: bool
    nodeStates: t.Optional[t.List[VDA5050NodeState]] = None
    agvPosition: t.Optional[VDA5050VehiclePosition] = None
    batteryState: t.Optional[VDA5050VehicleBatteryState] = None
    operatingMode: str
    velocity: t.Optional[VDA5050Velocity] = None
    actionStates: t.Optional[t.List[VDA5050ActionState]] = None
    errors: t.Optional[t.List[VDA5050Error]] = None
    safetyState: t.Optional[t.List[VDA5050SafetyState]] = None

    def __init__(self, **kwargs):
        global CURRENT_HEADER_ID
        CURRENT_HEADER_ID += 1

        kwargs.setdefault("headerId", CURRENT_HEADER_ID)
        kwargs.setdefault("timestamp", datetime.now())
        kwargs.setdefault("driving", False)
        kwargs.setdefault("paused", False)
        kwargs.setdefault("newBaseRequested", False)
        kwargs.setdefault("version", VERSION)
        kwargs.setdefault("operatingMode", "AUTOMATIC")

        node_states = kwargs.pop("nodeStates", None)
        node_state_objects = []

        if node_states:
            for node_state in node_states:
                if isinstance(node_state, VDA5050NodeState):
                    node_state_objects.append(node_state)
                else:
                    node_state_objects.append(VDA5050NodeState(**node_state))
            kwargs["nodeStates"] = node_state_objects

        if "agvPosition" in kwargs:
            agv_position = kwargs["agvPosition"]
            if not isinstance(agv_position, VDA5050VehiclePosition):
                kwargs["agvPosition"] = VDA5050VehiclePosition(**agv_position)

        if "batteryState" in kwargs:
            battery_state = kwargs["batteryState"]
            if not isinstance(battery_state, VDA5050VehicleBatteryState):
                kwargs["batteryState"] = VDA5050VehicleBatteryState(**battery_state)

        super().__init__(**kwargs)
