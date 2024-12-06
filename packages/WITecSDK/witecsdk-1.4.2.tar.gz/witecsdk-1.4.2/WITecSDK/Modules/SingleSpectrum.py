from typing import Callable
from WITecSDK.Modules.HelperStructs import specchannelpath
from WITecSDK.Parameters import COMFloatParameter, COMIntParameter, COMBoolParameter, COMTriggerParameter, ParameterNotAvailableException

parampath = "UserParameters|SequencerSingleSpectrum|"

class SingleSpectrumBase:

    def __init__(self, aGetParameter: Callable):
        self._integrationTimeCOM: COMFloatParameter = aGetParameter(parampath + "IntegrationTime")
        self._accumulationsCOM: COMIntParameter = aGetParameter(parampath + "NrOfAccumulations")

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


class SingleSpectrum(SingleSpectrumBase):

    def __init__(self, aGetParameter: Callable):
        super().__init__(aGetParameter)
        self._infiniteAccCOM: COMBoolParameter = aGetParameter(parampath + "InfiniteAccumulation")
        self._startSingleSpectrumCOM: COMTriggerParameter = aGetParameter(parampath + "Start")
        self._showSpectrum1COM: COMBoolParameter = aGetParameter(specchannelpath + "SpectralCamera1Data|SingleSpectrum|Show")
        self._showSpectrum2COM: COMBoolParameter = None
        self._showSpectrum3COM: COMBoolParameter = None
        try:
            self._showSpectrum2COM = aGetParameter(specchannelpath + "SpectralCamera2Data|SingleSpectrum|Show")
            self._showSpectrum3COM = aGetParameter(specchannelpath + "SpectralCamera3Data|SingleSpectrum|Show")
        except ParameterNotAvailableException:
            pass
        except Exception as e:
            raise e

    def Initialize(self, numberOfAccumulations: int, integrationTime: float):
        self.NumberOfAccumulations = numberOfAccumulations
        self.IntegrationTime = integrationTime
        self._infiniteAccCOM.Value = False

    def DeactivateShowSpectrum(self) -> bool:
        self._showSpectrum1COM.Value = False
        if self._showSpectrum2COM is not None:
            self._showSpectrum2COM.Value = False
        if self._showSpectrum3COM is not None:
            self._showSpectrum3COM.Value = False
    
    def Start(self):
        self._startSingleSpectrumCOM.ExecuteTrigger()