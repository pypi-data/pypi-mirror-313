from typing import Callable
from WITecSDK.Parameters import COMTriggerParameter, COMEnumParameter
from WITecSDK.Modules import XYAxes, ZAxis, SpectralAutofocus, ActiveSequencer
from WITecSDK.Modules.HelperStructs import XYZPosition, userparam
from asyncio import sleep
from collections.abc import Callable

parampath = userparam + "SequencerTrueSurface|ManualLearning|"

class ManualTopography:
    """Implements the manual topography correction for version 6.1 and higher
    For older versions an automated learning is not possible"""

    def __init__(self, aGetParameter: Callable, xyaxes: XYAxes, zaxis: ZAxis, specaf: SpectralAutofocus, actsequ: ActiveSequencer):
        self._xyaxes = xyaxes
        self._zaxis = zaxis
        self._specaf = specaf
        self._actsequ = actsequ
        self._learnPlaneCOM: COMTriggerParameter = aGetParameter(parampath + "Learn3PointPlane")
        self._learnSurfaceCOM: COMTriggerParameter = aGetParameter(parampath + "Learn5x5Surface")
        self._nextStepCOM: COMTriggerParameter = aGetParameter(parampath + "NextStep")
        self._LASurfaceCorrectionCOM: COMEnumParameter = aGetParameter("UserParameters|SequencerLargeScaleImaging|SurfaceCorrection")

    def LearnPlane(self):
        """Starts the learn plan process (3 points)"""
        self._learnPlaneCOM.ExecuteTrigger()

    def LearnSurface(self):
        """Starts the learn surface process (5x5 points)"""
        self._learnSurfaceCOM.ExecuteTrigger()

    def NextStep(self):
        """Goes to the next step"""
        self._nextStepCOM.ExecuteTrigger()

    async def AutomatePlane(self) -> list[bool]:
        """Automates the learn plan process by doing an autofocus at each point
        Returns a list giving the success for each point"""
        return await self._automate(self.LearnPlane, 3)

    async def AutomateSurface(self) -> list[bool]:
        """Automates the learn surface process by doing an autofocus at each point
        Returns a list giving the success for each point"""
        return await self._automate(self.LearnSurface, 25)

    async def _automate(self, learntrigger: Callable, no: int) -> list[bool]:
        positionlist = []
        successlist = []
        
        # Read xy positions
        learntrigger()
        await sleep(1)
        print("Learn positions")
        for i in range(no):
            await self._xyaxes.AwaitNotMoving()
            await sleep(2)
            xypos = self._xyaxes.CurrentSoftwarePos
            positionlist.append(XYZPosition(xypos.X, xypos.Y, 0))
            self.NextStep()
        await self._actsequ.WaitActiveSequencerFinished()
        
        # Do Autofocus on postions
        print("Autofocus")
        for i in range(no):
            await self._xyaxes.AwaitMoveToSoftwarePos(positionlist[i].SamplePosition)
            self._specaf.Start()
            await self._actsequ.WaitActiveSequencerFinished()
            stat, res = self._actsequ.StatusAndResult
            successlist.append(stat == "Finished")
            positionlist[i].Z = self._zaxis.CurrentSoftwarePos
            print(positionlist[i].Z)

        # Teach z coordinates
        print("Teach z")
        learntrigger()
        await sleep(1)
        for i in range(no):
            await self._xyaxes.AwaitNotMoving()
            await sleep(2)
            await self._zaxis.AwaitMoveToSoftwarePos(positionlist[i].Z)
            self.NextStep()
        await self._actsequ.WaitActiveSequencerFinished()
        self._LASurfaceCorrectionCOM.Value = 1

        return successlist