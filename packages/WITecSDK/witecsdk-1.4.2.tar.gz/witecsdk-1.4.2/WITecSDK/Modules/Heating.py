from typing import Callable
from WITecSDK.Parameters import COMBoolParameter, COMFloatParameter, COMTriggerParameter, COMFloatStatusParameter
from WITecSDK.Modules.HelperStructs import userparam, datachannelpath
from asyncio import sleep

parampath = userparam + "Heating|"

class Heating:
    """Gives access to the WITec heating stage"""

    def __init__(self, aGetParameter: Callable):
        self._enabledCOM: COMBoolParameter = aGetParameter(parampath + "Enabled")
        self._setpointCOM: COMFloatParameter = aGetParameter(parampath + "Setpoint")
        self._rampEndCOM: COMFloatParameter = aGetParameter(parampath + "TemperatureRamp|RampEnd")
        self._gradientCOM: COMFloatParameter = aGetParameter(parampath + "TemperatureRamp|Gradient")
        self._startGradientCOM: COMTriggerParameter = aGetParameter(parampath + "TemperatureRamp|StartGradient")
        self._stopGradientCOM: COMTriggerParameter = aGetParameter(parampath + "TemperatureRamp|StopGradient")
        self._currentTempCOM: COMFloatStatusParameter = aGetParameter(datachannelpath + "HeatingStageTemperature")

    def Initialize(self, gradient: float, tempSetpoint: float):
        """Sets the gradient and the final temperature"""
        self.Gradient = gradient
        self.TemperatureSetpoint = tempSetpoint
        self.Enabled = True

    @property
    def Gradient(self) -> float:
        """Defines the temperature gradient"""
        return self._gradientCOM.Value

    @Gradient.setter
    def Gradient(self, gradient: float):
        self._gradientCOM.Value = gradient
    
    @property
    def TemperatureSetpoint(self) -> float:
        """Defines the final temperature"""
        return self._rampEndCOM.Value

    @TemperatureSetpoint.setter
    def TemperatureSetpoint(self, tempSetpoint: float):
        self._rampEndCOM.Value = tempSetpoint

    @property
    def CurrentSetpoint(self) -> float:
        """This property defines the current desired temperature"""
        return self._setpointCOM.Value

    @CurrentSetpoint.setter
    def CurrentSetpoint(self, setpointTemp: float):
        self._setpointCOM.Value = setpointTemp

    @property
    def Enabled(self) -> bool:
        """This property can switch on and off the heating stage"""
        return self._enabledCOM.Value
    
    @Enabled.setter
    def Enabled(self, value):
        self._enabledCOM.Value = value

    @property
    def CurrentTemperature(self) -> float:
        """Retrieves the current temperature"""
        return self._currentTempCOM.Value

    def StartGradient(self):
        """Starts heating"""
        self._startGradientCOM.ExecuteTrigger()

    def StopGradient(self):
        """Stops heating"""
        self._stopGradientCOM.ExecuteTrigger()