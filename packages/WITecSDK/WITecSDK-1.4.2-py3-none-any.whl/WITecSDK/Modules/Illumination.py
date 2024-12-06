from typing import Callable
from WITecSDK.Parameters import COMBoolParameter, COMFloatParameter
from WITecSDK.Modules.BeamPath import AutomatedCoupler
from WITecSDK.Modules.HelperStructs import microscopecontrol

parampath = microscopecontrol + "WhiteLight|"

class Illumination:
    """Base class for the ligth sources"""

    def __init__(self, aGetParameter: Callable, illuType: str):
        illupath = parampath + illuType
        self._illuminationOnCOM: COMBoolParameter = aGetParameter(illupath + "|On")
        self._brightnessPercentageCOM: COMFloatParameter = aGetParameter(illupath + "|BrightnessPercentage")

    @property
    def SwitchedOn(self) -> bool:
        """This property can switch on and off the illumination"""
        return self._illuminationOnCOM.Value

    @SwitchedOn.setter
    def SwitchedOn(self, isOn: bool):
        self._illuminationOnCOM.Value = isOn

    @property
    def BrightnessPercentage(self) -> float:
        """This property controls the illumination brightness in %"""
        return self._brightnessPercentageCOM.Value

    @BrightnessPercentage.setter
    def BrightnessPercentage(self, spectralCenter: float):
        self._brightnessPercentageCOM.Value = spectralCenter

class TopIllumination(Illumination):
    """Class for controlling the top illumination"""

    def __init__(self, aGetParameter: Callable):
        super().__init__(aGetParameter, "Top")
        self.WhiteLightCoupler = AutomatedCoupler(aGetParameter, parampath + "WhiteLightCoupler")

class BottomIllumination(Illumination):
    """Class for controlling the bottom illumination"""

    def __init__(self, aGetParameter: Callable):
        super().__init__(aGetParameter, "Bottom")