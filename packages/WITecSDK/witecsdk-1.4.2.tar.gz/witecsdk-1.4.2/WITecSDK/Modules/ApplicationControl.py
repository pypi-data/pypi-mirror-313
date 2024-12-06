from typing import Callable
from WITecSDK.Parameters import COMTriggerParameter, COMIntStatusParameter

appcontrol = "ApplicationControl|"
appmemstatus = "Status|Software|Application|MemoryStatus|"

class ApplicationControl:
    """Gives access to memory status and can close WITec Control"""

    def __init__(self, aGetParameter: Callable):
        self._updateHardwareCOM: COMTriggerParameter = aGetParameter(appcontrol + "UpdateHardware")
        self._exitControlCOM: COMTriggerParameter = aGetParameter(appcontrol +"ExitApplication")
        self._physicalMemoryCOM: COMIntStatusParameter = aGetParameter(appmemstatus + "PhysicalMemory")
        self._pageFileCOM: COMIntStatusParameter = aGetParameter(appmemstatus + "PageFile")
        self._addressSpaceCOM: COMIntStatusParameter = aGetParameter(appmemstatus + "AddressSpace")

    def UpdateHardware(self):
        """Apllies changes of the user parameters to the hardware and updates the status data afterwards. Only necessary in special cases"""
        self._updateHardwareCOM.ExecuteTrigger()

    def Exit(self):
        """Closes WITec Control"""
        self._exitControlCOM.ExecuteTrigger()

    @property
    def PhysicalMemory(self) -> int:
        """The available physical memory in %"""
        return self._physicalMemoryCOM.Value

    @property
    def PageFile(self) -> int:
        """The available page file space in %"""
        return self._pageFileCOM.Value
    
    @property
    def AddressSpace(self) -> int:
        """The available address space in %"""
        return self._addressSpaceCOM.Value