from typing import Callable
from WITecSDK.Parameters import COMFloatParameter
from WITecSDK.Modules.HelperStructs import microscopecontrol

parampath = microscopecontrol + "OpticControl|"

class ApertureFieldStop:
    """Gives access to motorized aperture and field stop if available"""

    def __init__(self, aGetParameter: Callable):
        self._fieldStopCOM: COMFloatParameter = aGetParameter(parampath + "FieldStop")
        self._apertureStopCOM: COMFloatParameter = aGetParameter(parampath + "ApertureStop")

    @property
    def FieldStop(self) -> float:
        """Field stop position in %"""
        return self._fieldStopCOM.Value

    @FieldStop.setter
    def FieldStop(self, value: float):
        self._fieldStopCOM.Value = value

    @property
    def ApertureStop(self) -> float:
        """Aperture stop position in %"""
        return self._apertureStopCOM.Value

    @ApertureStop.setter
    def ApertureStop(self, value: float):
        self._apertureStopCOM.Value = value