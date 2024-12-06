from typing import Callable
from WITecSDK.Parameters import COMTriggerParameter, COMIntParameter, COMFloatParameter, COMBoolParameter
from WITecSDK.Modules.SlowTimeSeriesBase import SlowSeriesBase

class LaserPowerSeries(SlowSeriesBase):
    """Implements the Laser power series"""

    def __init__(self, aGetParameter: Callable):
        super().__init__(aGetParameter)
        parampath = self._parampath + "LaserPowerSeries|"
        self._startLaserPowerSeriesCOM: COMTriggerParameter = aGetParameter(parampath + "StartLaserPowerSeries")
        self._numberOfLasersCOM: COMIntParameter = aGetParameter(parampath + "NumberOfLaserPowerValues")
        self._startLaserPowerCOM: COMFloatParameter = aGetParameter(parampath + "StartLaserPower")
        self._stopLaserPowerCOM: COMFloatParameter = aGetParameter(parampath + "StopLaserPower")
        self._forwardAndBackwardCOM: COMBoolParameter = aGetParameter(parampath + "ForwardAndBackward")
        self._keepDoseConstantCOM: COMBoolParameter = aGetParameter(parampath + "KeepDoseConstant")

    @property
    def NumberOfValues(self) -> int:
        """Defines the number of datapoints"""
        return self._numberOfLasersCOM.Value

    @NumberOfValues.setter
    def NumberOfValues(self, numval: int):
        self._numberOfLasersCOM.Value = numval
        
    def Start(self):
        """Starts the laser power series"""
        self._startLaserPowerSeriesCOM.ExecuteTrigger()

    @property
    def StartLaserPower(self) -> float:
        """Defines the initial laser power"""
        return self._startLaserPowerCOM.Value

    @StartLaserPower.setter
    def StartLaserPower(self, laserPower: float):
        self._startLaserPowerCOM.Value = laserPower

    @property
    def StopLaserPower(self) -> float:
        """Defines the final laser power"""
        return self._stopLaserPowerCOM.Value

    @StopLaserPower.setter
    def StopLaserPower(self, laserPower: float):
        self._stopLaserPowerCOM.Value = laserPower

    @property
    def ForwardAndBackward(self) -> bool:
        """Goes to stop laser power and back to start"""
        return self._forwardAndBackwardCOM.Value

    @ForwardAndBackward.setter
    def ForwardAndBackward(self, state: bool):
        self._forwardAndBackwardCOM.Value = state

    @property
    def KeepDoseConstant(self) -> bool:
        """If active adopts the integration time to compensate the laser power change"""
        return self._keepDoseConstantCOM.Value

    @KeepDoseConstant.setter
    def KeepDoseConstant(self, state: bool):
        self._keepDoseConstantCOM.Value = state