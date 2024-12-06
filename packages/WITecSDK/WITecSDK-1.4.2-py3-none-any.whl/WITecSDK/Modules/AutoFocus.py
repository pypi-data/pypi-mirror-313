from typing import Callable
from WITecSDK.Parameters import COMTriggerParameter, COMEnumParameter
from WITecSDK.Modules.HelperStructs import microscopecontrol
from asyncio import sleep

class AutoFocus:
    """Gives access to the video autofocus if available"""

    _parampath = microscopecontrol + "Video|"

    def __init__(self, aGetParameter: Callable):
        self._executeAutoFocusCOM: COMTriggerParameter = aGetParameter(self._parampath + "AutoFocus|Execute")

    async def ExecuteAutoFocus(self) -> bool:
        """Coroutine that starts the autofocus and waits to be finished"""
        self._executeAutoFocusCOM.ExecuteTrigger()
        return await self._waitForAutoFocus()

    async def _waitForAutoFocus(self) -> bool:
        await sleep(5)
        return True
    
class AutoFocus61(AutoFocus):
    """Extension of the AutoFocus class for version 6.1 and higher"""

    def __init__(self, aGetParameter: Callable):
        super().__init__(aGetParameter)
        self._statusAutoFocusCOM: COMEnumParameter = aGetParameter(self._parampath + "AutoFocus|Status")

    @property
    def Status(self) -> int:
        """Returns the status of the last autofocus"""
        return self._statusAutoFocusCOM.Value
    
    @property
    def StatusValues(self) -> dict[int, str]:
        """Returns the available status values (Running, LastSucceeded, LastFailed)"""
        return self._statusAutoFocusCOM.AvailableValues

    async def _waitForAutoFocus(self) -> bool:
        afstate: int = 0
        while afstate == 0:
            await sleep(0.1)
            afstate = self.Status
        return afstate == 1