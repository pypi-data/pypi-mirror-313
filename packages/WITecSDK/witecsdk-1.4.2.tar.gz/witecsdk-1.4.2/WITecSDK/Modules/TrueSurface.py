from typing import Callable
from WITecSDK.Parameters import COMEnumParameter, COMFloatParameter, COMIntParameter, COMBoolParameter
from WITecSDK.Modules.HelperStructs import microscopecontrol

parampath = microscopecontrol + "TrueSurface|"

class TrueSurface:

    def __init__(self, aGetParameter: Callable):
        self._trueSurfaceStateCOM: COMEnumParameter = aGetParameter(parampath + "State")

    @property
    def State(self) -> int:
        return self._trueSurfaceStateCOM.Value
    
    def GetStates(self) -> dict:
        return self._trueSurfaceStateCOM.AvailableValues

    def setRunning(self):
        self._trueSurfaceStateCOM.Value = 2

    def setPrepare(self):
        self._trueSurfaceStateCOM.Value = 1

    def setOff(self):
        self._trueSurfaceStateCOM.Value = 0


class TrueSurface62(TrueSurface):

    def __init__(self, aGetParameter: Callable):
        super().__init__(aGetParameter)
        self._focusShiftCOM: COMFloatParameter = aGetParameter(parampath + "FocusShift")
        self._minValueCOM: COMFloatParameter = aGetParameter(parampath + "MinValue")
        self._pGainCOM: COMFloatParameter = aGetParameter(parampath + "PGain")
        self._iGainCOM: COMFloatParameter = aGetParameter(parampath + "IGain")
        self._laserIntensityCOM: COMIntParameter = aGetParameter(parampath + "LaserIntensity")
        self._detectorGainCOM: COMEnumParameter = aGetParameter(parampath + "DetectorGain")
        self._useAutomaticGainCOM: COMBoolParameter = aGetParameter(parampath + "UseAutomaticGain")

    @property
    def FocusShift(self) -> float:
        return self._focusShiftCOM.Value
    
    @property
    def MinValue(self) -> float:
        return self._minValueCOM.Value
    
    @property
    def PGain(self) -> float:
        return self._pGainCOM.Value
    
    @property
    def IGain(self) -> float:
        return self._iGainCOM.Value
    
    @property
    def LaserIntensity(self) -> int:
        return self._laserIntensityCOM.Value
        
    @property
    def DetectorGain(self) -> int:
        return self._detectorGainCOM.Value
    
    def GetDetectorGains(self) -> dict:
        return self._detectorGainCOM.AvailableValues
    
    @property
    def UseAutomaticGain(self) -> bool:
        return self._useAutomaticGainCOM.Value
    

# TrueSurface|DetectorGain  <enum>
#    Get the Detector Gain - Enum Values: 0: Low, 1: Medium, 2: High, 3: Maximum
#    This parameter is read only