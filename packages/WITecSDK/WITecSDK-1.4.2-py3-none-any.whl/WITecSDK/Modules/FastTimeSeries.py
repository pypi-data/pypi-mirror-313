from typing import Callable
from WITecSDK.Parameters import COMFloatParameter, COMIntParameter, COMTriggerParameter

parampath = "UserParameters|SequencerTimeSeriesFast|"

class FastTimeSeries:
    """Implements the Fast Time Series"""

    def __init__(self, aGetParameter: Callable):
        self._integrationTimeCOM: COMFloatParameter = aGetParameter(parampath + "IntegrationTime")
        self._measurementsCOM: COMIntParameter = aGetParameter(parampath + "AmountOfMeasurements")
        self._startFastTimeSeriesCOM: COMTriggerParameter = aGetParameter(parampath + "Start")

    def Initialize(self, measurements: int, integrationTime: float):
        """Sets number of measurements and integration time"""
        self.Measurements = measurements
        self.IntegrationTime = integrationTime

    @property
    def Measurements(self) -> int:
        """Defines the number of measurements"""
        return self._measurementsCOM.Value

    @Measurements.setter
    def Measurements(self, numberMeasurements: int):
        self._measurementsCOM.Value = numberMeasurements

    @property
    def IntegrationTime(self) -> float:
        """Defines the integration time"""
        return self._integrationTimeCOM.Value

    @IntegrationTime.setter
    def IntegrationTime(self, integrationTime: float):
        self._integrationTimeCOM.Value = integrationTime

    def Start(self):
        """Starts the measurement"""
        self._startFastTimeSeriesCOM.ExecuteTrigger()