from typing import Callable
from WITecSDK.Parameters import COMFloatParameter, COMIntParameter, COMTriggerParameter

parampath = "UserParameters|SpectralStitching|"

class SpectralStitching:

    def __init__(self, aGetParameter: Callable):
        self._integrationTimeCOM: COMFloatParameter = aGetParameter(parampath + "IntegrationTime")
        self._accumulationsCOM: COMIntParameter = aGetParameter(parampath + "NumberOfAccumulations")
        self._startSpectralPosCOM: COMFloatParameter = aGetParameter(parampath + "StartSpectralPosition")
        self._stopSpectralPosCOM: COMFloatParameter = aGetParameter(parampath + "StopSpectralPosition")
        self._startSingleSpectrumCOM: COMTriggerParameter = aGetParameter(parampath + "StartSpectralStitching")

    @property
    def NumberOfAccumulations(self) -> int:
        return self._accumulationsCOM.Value

    @NumberOfAccumulations.setter
    def NumberOfAccumulations(self, numberOfAccumulations: int):
        self._accumulationsCOM.Value = numberOfAccumulations

    @property
    def IntegrationTime(self) -> float:
        return self._integrationTimeCOM.Value
    
    @IntegrationTime.setter
    def IntegrationTime(self, integrationTime: float):
        self._integrationTimeCOM.Value = integrationTime

    @property
    def StartSpectralPosition(self) -> float:
        return self._startSpectralPosCOM.Value
    
    @StartSpectralPosition.setter
    def StartSpectralPosition(self, startSpectralPos: float):
        self._startSpectralPosCOM.Value = startSpectralPos

    @property
    def StopSpectralPosition(self) -> float:
        return self._stopSpectralPosCOM.Value
    
    @StopSpectralPosition.setter
    def StopSpectralPosition(self, stopSpectralPos: float):
        self._stopSpectralPosCOM.Value = stopSpectralPos

    def Start(self):
        self._startSingleSpectrumCOM.ExecuteTrigger()