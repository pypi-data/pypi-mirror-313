from typing import Callable
from WITecSDK.Parameters.COMClient import IBUCSSubSystemsList

class COMSubSystemsList:
    """Implements the IBUCSSubSystemsList"""

    def __init__(self, aSubSystemList: IBUCSSubSystemsList):
        self._subSystemListObj = aSubSystemList

    @property
    def NumberOfSystems(self) -> int:
        return self._subSystemListObj.GetNumberOfSystems()
    
    @property
    def BaseName(self) -> str:
        return self._subSystemListObj.GetBaseName()
    
    def GetSubSystemName(self, index: int) -> str:
        return self._subSystemListObj.GetSubSystemName(index)
    
    def GetSystemSubSystemsList(self, index: int) -> "COMSubSystemsList":
        return COMSubSystemsList(self._subSystemListObj.GetSystemSubSystemsList(index))
    
    def GetSubSystemNameAndIId(self, index: int) -> tuple[str, str]:
        return self._subSystemListObj.GetSubSystemNameAndIId(index)
    
    @property
    def SubSystemsNameList(self) -> list[str]:
        return self._loopList(self.GetSubSystemName)
    
    @property
    def SubSystemsNameAndIIdList(self) -> list[tuple[str, str]]:
        return self._loopList(self.GetSubSystemNameAndIId)
    
    @property
    def SubSystemsListList(self) -> list["COMSubSystemsList"]:
        return self._loopList(self.GetSystemSubSystemsList)

    def _loopList(self, aMethod: Callable[[int], list]) -> list:
        subSystemsList = []
        for i in range(self.NumberOfSystems):
           subSystemsList.append(aMethod(i))
        return subSystemsList
