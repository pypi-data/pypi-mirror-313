from typing import Callable
from WITecSDK.Parameters import COMFloatParameter

parampath = "UserParameters|ScanTable|"

class ScanTable:

    def __init__(self, aGetParameter: Callable):
        self._positionXCOM: COMFloatParameter = aGetParameter(parampath + "PositionX")
        self._positionYCOM: COMFloatParameter = aGetParameter(parampath + "PositionY")
        self._positionZCOM: COMFloatParameter = aGetParameter(parampath + "PositionZ")

    @property
    def PositionX(self) -> float:
        return self._positionXCOM.Value
    
    @PositionX.setter
    def PositionX(self, posX: float):
        self._positionXCOM.Value = posX

    @property
    def PositionY(self) -> float:
        return self._positionYCOM.Value
    
    @PositionY.setter
    def PositionY(self, posY: float):
        self._positionYCOM.Value = posY

    @property
    def PositionZ(self) -> float:
        return self._positionZCOM.Value
    
    @PositionZ.setter
    def PositionZ(self, posZ: float):
        self._positionZCOM.Value = posZ
