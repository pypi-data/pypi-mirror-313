from typing import Callable
from WITecSDK.Parameters import COMEnumParameter, COMFloatParameter

class Spectrograph:

    def __init__(self, aGetParameter: Callable, specNo: int):
        parampath = "UserParameters|Spectrograph" + str(specNo)
        self._gratingCOM: COMEnumParameter = aGetParameter(parampath + "|Grating")
        self._centerWavelengthCOM: COMFloatParameter = aGetParameter(parampath + "|CenterWavelength")
        self._spectralCenterCOM: COMFloatParameter = aGetParameter(parampath + "|SpectralCenter")
        self._spectralUnitCOM: COMEnumParameter = aGetParameter(parampath + "|SpectralUnit")

    @property
    def CenterWavelength(self) -> float:
        return self._centerWavelengthCOM.Value

    @CenterWavelength.setter
    def CenterWavelength(self, centerWavelength: float):
        self._centerWavelengthCOM.Value = centerWavelength

    @property
    def SpectralCenter(self) -> float:
        return self._spectralCenterCOM.Value

    @SpectralCenter.setter
    def SpectralCenter(self, spectralCenter: float):
        self._spectralCenterCOM.Value = spectralCenter

    @property
    def Grating(self) -> int:
        return self._gratingCOM.Value

    @Grating.setter
    def Grating(self, grating: int):
        self._gratingCOM.Value = grating

    def GetGratings(self) -> dict:
        return self._gratingCOM.AvailableValues
    
    @property
    def Unit(self) -> int:
        return self._spectralUnitCOM.Value

    @Unit.setter
    def Unit(self, unit: int):
        self._spectralUnitCOM.Value = unit

    def GetUnits(self) -> dict:
        return self._spectralUnitCOM.AvailableValues