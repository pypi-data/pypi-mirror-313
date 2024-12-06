from typing import Callable
from WITecSDK.Parameters import COMFloatParameter, COMTriggerParameter
from WITecSDK.Modules.HelperStructs import SamplePositionerPosition
from asyncio import sleep

parampath = "UserParameters|SamplePositioning|"
statuspath = "Status|Software|SamplePositioner|"

class SamplePositionerBase:

    positionPollInterval = 0.1
    _moveToPositionCOM = None
        
    def __init__(self, aGetParameter: Callable):
        self._absolutePositionXCOM: COMFloatParameter = aGetParameter(parampath + "AbsolutePositionX")
        self._absolutePositionYCOM: COMFloatParameter = aGetParameter(parampath + "AbsolutePositionY")
        self._stopDrivingCOM: COMTriggerParameter = aGetParameter(parampath + "StopDriving")
        self._currentPositionXCOM: COMFloatParameter = aGetParameter(statuspath + "CurrentPositionX")
        self._currentPositionYCOM: COMFloatParameter = aGetParameter(statuspath + "CurrentPositionY")

    async def MoveTo(self, x: float, y: float):
        await self._moveTo(x, y)

    async def _moveTo(self, x: float, y: float):
        retryCounter = 0

        while True:
            try:
                self._absolutePositionXCOM.Value = x
                self._absolutePositionYCOM.Value = y
                break;

            except:
                if retryCounter == 3:
                     raise

                retryCounter += 1
                await sleep(0.1 * retryCounter)

        self._moveToPositionCOM.ExecuteTrigger();
        await self.waitForMovingFinished()

    async def waitForMovingFinished(self):
        positionNotChangedCounter = 0
        lastX = 0
        lastY = 0

        while True:
            if self.isTargetPositionReached():
                await sleep(0.1)
                break

            currentX = self._currentPositionXCOM.Value
            currentY = self._currentPositionYCOM.Value

            if lastX == currentX and lastY == currentY:
                positionNotChangedCounter += 1
            else:
                positionNotChangedCounter = 0;

            lastX = currentX
            lastY = currentY

            if positionNotChangedCounter >= 5:
                self._stopDrivingCOM.ExecuteTrigger()
                raise SamplePositionerPositionNotReachedException("Requested Position not reached, check End Switches")

            await sleep(self.positionPollInterval)
        

    def isTargetPositionReached(self) -> bool:
        diffX = abs(self._absolutePositionXCOM.Value - self._currentPositionXCOM.Value)
        diffY = abs(self._absolutePositionYCOM.Value - self._currentPositionYCOM.Value)

        if diffX <= 0.2 and diffY <= 0.2:
            return True
        else:
            return False

    @property
    def CurrentPosition(self) -> SamplePositionerPosition:
        return SamplePositionerPosition(self._currentPositionXCOM.Value, self._currentPositionYCOM.Value)


class SamplePositioner(SamplePositionerBase):
    def __init__(self, aGetParameter: Callable):
        super().__init__(aGetParameter)
        self._moveToPositionCOM: COMTriggerParameter = aGetParameter(parampath + "GoToPosition")


class SamplePositioner51(SamplePositionerBase):
    def __init__(self, aGetParameter: Callable):
        super().__init__(aGetParameter)
        self._moveToPositionCOM: COMTriggerParameter = aGetParameter(parampath + "GoToPositionWithoutQuery")


class SamplePositionerPositionNotReachedException(Exception):
    pass