"""Module containing the class for the EFM Control (Voltage output)"""

from typing import Callable
from WITecSDK.Parameters import COMBoolParameter, COMFloatParameter, COMEnumParameter
from WITecSDK.Modules.HelperStructs import userparam

parampath = userparam + "EFMControl|"

class EFMControl:
    """Implements the EFM Control (Voltage output)"""

    def __init__(self, aGetParameter: Callable):
        self._enableCOM: COMBoolParameter = aGetParameter(parampath + "EnableEFM")
        self._dcVoltageCOM: COMFloatParameter = aGetParameter(parampath + "DCVoltage")
        self._signalOutputDACCOM: COMEnumParameter = aGetParameter(parampath + "SignalOutputDAC")
        self._availableDACs: dict = self._signalOutputDACCOM.AvailableValues

    def Initialize(self, voltage: float):
        """Initializes the output of a given voltage at Aux 1 DAC"""
        self.SetAux1DAC()
        self.Voltage = voltage
        self.Enabled = True

    @property
    def Enabled(self) -> bool:
        """Enables or disables the voltage output"""
        return self._enableCOM.Value
    
    @Enabled.setter
    def Enabled(self, value: bool):
        self._enableCOM.Value = value

    @property
    def Voltage(self) -> float:
        """Defines the voltage in V"""
        return self._dcVoltageCOM.Value
    
    @Voltage.setter
    def Voltage(self, value: float):
        self._dcVoltageCOM.Value = value

    def SetAux1DAC(self):
        """Sets Aux1 DAC as output"""
        self._setDAC("Aux1 DAC")

    def SetAux2DAC(self):
        """Sets Aux2 DAC as output"""
        self._setDAC("Aux2 DAC")

    def SetDitherDAC(self):
        """Sets Dither DAC as output"""
        self._setDAC("Dither DAC")

    def _setDAC(self, dac: str):
        for val, key in self._availableDACs.items():
            if key == dac:
                self._signalOutputDACCOM.Value = val
                return
        raise DACNotAvailableException(f"{dac} is not available")
        

class DACNotAvailableException(Exception):
    pass