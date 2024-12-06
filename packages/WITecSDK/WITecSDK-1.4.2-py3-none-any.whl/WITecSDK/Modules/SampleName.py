from typing import Callable
from WITecSDK.Parameters import COMStringParameter, COMEnumParameter, COMIntParameter

parampath = "UserParameters|Naming|"

class SampleName:

    def __init__(self, aGetParameter: Callable):
        self._sampleNameCOM: COMStringParameter = aGetParameter(parampath + "SampleName")
        self._formatCOM: COMEnumParameter = aGetParameter(parampath + "Format")
        self._counterCOM: COMIntParameter = aGetParameter(parampath + "Counter")

    @property
    def SampleName(self) -> str:
        return self._sampleNameCOM.Value
    
    @SampleName.setter
    def SampleName(self, sampleName: str):
        self._sampleNameCOM.Value = sampleName

    @property
    def Counter(self) -> int:
        return self._counterCOM.Value

    @Counter.setter
    def Counter(self, counter: int):
        self._counterCOM.Value = counter

    def setLongDescription(self):
        self._formatCOM.Value = 0

    def setShortDescription(self):
        self._formatCOM.Value = 1

    def setNameOnly(self):
        self._formatCOM.Value = 2