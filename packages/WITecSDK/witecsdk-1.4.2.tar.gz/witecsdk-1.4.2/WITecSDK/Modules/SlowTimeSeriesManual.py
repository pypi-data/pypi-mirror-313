from typing import Callable
from WITecSDK.Parameters import COMTriggerParameter
from WITecSDK.Modules.SlowTimeSeriesBase import SlowTimeSeriesBase
from WITecSDK.Modules.ActiveSequencer import ActiveSequencer
from asyncio import sleep

class SlowTimeSeriesManual(SlowTimeSeriesBase):

    def __init__(self, aGetParameter: Callable, aActiveSequencer: ActiveSequencer):
        super().__init__(aGetParameter)
        self.activeSequencer = aActiveSequencer
        self._nextMeasurementCOM: COMTriggerParameter = aGetParameter(self._parampath + "NextMeasurement")
        self._startSubSequenceCOM: COMTriggerParameter = aGetParameter(self._parampath + "SubSequence|StartSubSequence")
    
    def Initialize(self, numberOfMeasurements: int, numberOfAccumulations: int, integrationTime: float):
        super().Initialize(numberOfMeasurements, numberOfAccumulations, integrationTime)
        self.setMeasurementModeToManual()

    def setMeasurementModeToManual(self):
        self._measurementModeCOM.Value = 0

    async def PerformNextMeasurement(self):
        await self.waitForNextMeasurement()    
        self._nextMeasurementCOM.ExecuteTrigger()
        await self.waitForMeasurementStarted()
        await self.waitForNextMeasurement()

    async def PerformAutofocus(self):
        await self.waitForNextMeasurement()
        self._startSubSequenceCOM.ExecuteTrigger()
        await self.waitForMeasurementStarted()
        await self.waitForNextMeasurement()

    async def waitForNextMeasurement(self):
        while True:
            await sleep(0.2)
            currentActivity = self.activeSequencer.CurrentActivity
            if currentActivity == "Waiting for next Measurement":
                break
            elif currentActivity is None:
                break

    async def waitForMeasurementStarted(self):
        while True:
            await sleep(0.1)
            currentActivity = self.activeSequencer.CurrentActivity
            if currentActivity != "Waiting for next Measurement":
                break