from typing import Callable
from WITecSDK.Parameters import COMStringParameter, COMBoolParameter, COMFloatParameter, COMTriggerParameter
from WITecSDK.Modules.HelperStructs import SamplePositionerPosition, microscopecontrol
from asyncio import sleep
from time import sleep as tsleep

parampath = microscopecontrol + "MotorizedXYZ|XYAxes|"

class XYAxes:   
    
    backlash = SamplePositionerPosition(30,-30)

    def __init__(self, aGetParameter: Callable):
        self._StateCOM: COMStringParameter = aGetParameter(parampath + "State")
        self._MoveAcceleratedCOM: COMBoolParameter = aGetParameter(parampath + "MoveAcceleratedWithMaxSpeed")
        self._MinSpeedCOM: COMFloatParameter = aGetParameter(parampath + "MinSpeed")
        self._MaxSpeedCOM: COMFloatParameter = aGetParameter(parampath + "MaxSpeed")
        self._MinSpeedLimitCOM: COMFloatParameter = aGetParameter(parampath + "MinSpeedLimit")
        self._MaxSpeedLimitCOM: COMFloatParameter = aGetParameter(parampath + "MaxSpeedLimit")
        self._UseSpeedLimitCOM = aGetParameter(parampath + "UseSpeedLimit")
        self._SpeedCOM: COMFloatParameter = aGetParameter(parampath + "Speed")
        self._DesiredSamplePosXCOM: COMFloatParameter = aGetParameter(parampath + "DesiredSamplePositionX")
        self._DesiredSamplePosYCOM: COMFloatParameter = aGetParameter(parampath + "DesiredSamplePositionY")
        self._CurrentSamplePosXCOM: COMFloatParameter = aGetParameter(parampath + "CurrentSamplePositionX")
        self._CurrentSamplePosYCOM: COMFloatParameter = aGetParameter(parampath + "CurrentSamplePositionY")
        self._StopCOM: COMTriggerParameter = aGetParameter(parampath + "Stop")
        self._MoveToDesiredSamplePosCOM: COMTriggerParameter = aGetParameter(parampath + "MoveToDesiredSamplePosition")
        self._zeroSamplePosCOM: COMTriggerParameter = aGetParameter(parampath + "SetSamplePositionToZero")
        self._MoveToCalibrationPosCOM: COMTriggerParameter = aGetParameter(parampath + "MoveToCalibrationPosition")
        self._ResetCoordinateSysCOM: COMTriggerParameter = aGetParameter(parampath + "ResetCoordinateSystem")

    @property
    def State(self) -> str:
        return self._StateCOM.Value

    @property
    def IsMoveAccelerated(self) -> bool:
        return self._MoveAcceleratedCOM.Value

    @IsMoveAccelerated.setter
    def IsMoveAccelerated(self, value: bool):
        #always uses full speed
        self._MoveAcceleratedCOM.Value = value

    @property
    def MinSpeed(self) -> float:
        #µm/s
        return self._MinSpeedCOM.Value

    @property
    def MaxSpeed(self) -> float:
        #µm/s
        return self._MaxSpeedCOM.Value
    
    @property
    def MinSpeedLimit(self) -> float:
        #µm/s
        return self._MinSpeedLimitCOM.Value

    @property
    def MaxSpeedLimit(self) -> float:
        #µm/s
        return self._MaxSpeedLimitCOM.Value

    @property
    def Speed(self) -> float:
        #µm/s
        return self._SpeedCOM.Value

    @Speed.setter
    def Speed(self, value: float):
        #µm/s
        self._SpeedCOM.Value = value

    @property
    def DesiredSoftwarePos(self) -> SamplePositionerPosition:
        return SamplePositionerPosition(self._DesiredSamplePosXCOM.Value, self._DesiredSamplePosYCOM.Value)

    @DesiredSoftwarePos.setter
    def DesiredSoftwarePos(self, xy: SamplePositionerPosition):
        self._DesiredSamplePosXCOM.Value = xy.X
        self._DesiredSamplePosYCOM.Value = xy.Y

    @property
    def CurrentSoftwarePos(self) -> SamplePositionerPosition:
        return SamplePositionerPosition(self._CurrentSamplePosXCOM.Value, self._CurrentSamplePosYCOM.Value)
    
    @property
    def IsNotMoving(self) -> bool:
        currentpos = self.CurrentSoftwarePos
        tsleep(0.1)
        return currentpos == self.CurrentSoftwarePos

    def Stop(self):
        self._StopCOM.ExecuteTrigger()

    def MoveToDesiredSoftwarePos(self):
        self._MoveToDesiredSamplePosCOM.ExecuteTrigger()
        self.verifyNotInUse()

    def ZeroSoftwarePos(self):
        self._zeroSamplePosCOM.ExecuteTrigger()
        tsleep(0.1)
        currentXY = self.CurrentSoftwarePos
        if currentXY.X != 0 or currentXY.Y != 0:
            raise XYAxesZeroNoSuccessException()
        
    def MoveToCalibrationPosition(self):
        self._MoveToCalibrationPosCOM.ExecuteTrigger()

    def ResetCoordinateSystem(self):
        self._ResetCoordinateSysCOM.ExecuteTrigger()

    def verifyNotInUse(self):
        if self.State ==  "Axis In Use":
            raise XYAxesInUseException()

    async def AwaitMoveToSoftwarePos(self, xy: SamplePositionerPosition):
        self.DesiredSoftwarePos = xy
        self.MoveToDesiredSoftwarePos()
        await self.waitForMovingFinished(xy)

    async def AwaitMoveToSoftwarePosBacklashComp(self, xy: SamplePositionerPosition):
        await self.AwaitMoveToSoftwarePos(xy - self.backlash)
        await self.AwaitMoveToSoftwarePos(xy)

    async def AwaitNotMoving(self):
        while not self.IsNotMoving:
            await sleep(0.1)

    async def waitForMovingFinished(self, xy: SamplePositionerPosition = SamplePositionerPosition()):
        while True:
            xyState = self.State

            if xyState == "Desired Position Reached":
                break
            elif xyState == "":
                break
            elif xyState == "Manually Stopped":
                break
            elif xyState == "Position not Reached":
                raise XYAxesPositionNotReachedException(xy)

            await sleep(0.1)
        

class XYAxesPositionNotReachedException(Exception):
    def __init__(self, xy: SamplePositionerPosition):
        super().__init__("Requested Position " + str(xy) + " not reached.")

class XYAxesInUseException(Exception):
    def __init__(self):
        super().__init__("XY axes already in use.")

class XYAxesZeroNoSuccessException(Exception):
    def __init__(self):
        super().__init__("XY axes could not be set to zero.")
