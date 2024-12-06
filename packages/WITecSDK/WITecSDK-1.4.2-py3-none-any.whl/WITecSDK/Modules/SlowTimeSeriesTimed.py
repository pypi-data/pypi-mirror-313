from typing import Callable
from WITecSDK.Parameters import COMFloatParameter
from WITecSDK.Modules.SlowTimeSeriesBase import SlowTimeSeriesBase

class SlowTimeSeriesTimed(SlowTimeSeriesBase):

    def __init__(self, aGetParameter: Callable):
        super().__init__(aGetParameter)
        self._intervalCOM: COMFloatParameter = aGetParameter(self._parampath + "MeasurementInterval")
        
    def Initialize(self, numberOfMeasurements: int, numberOfAccumulations: int, integrationTime: float, interval: float):
        super().Initialize(numberOfMeasurements, numberOfAccumulations, integrationTime)
        self.Interval = interval
        self.setMeasurementModeToTimed()

    @property
    def Interval(self) -> float:
        return self._intervalCOM.Value
    
    @Interval.setter
    def Interval(self, interval: float):
        self._intervalCOM.Value = interval

    def setMeasurementModeToTimed(self):
        self._measurementModeCOM.Value = 1