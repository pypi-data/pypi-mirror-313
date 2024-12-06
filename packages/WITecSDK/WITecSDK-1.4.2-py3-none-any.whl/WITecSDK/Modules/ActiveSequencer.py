from typing import Callable
from _ctypes import COMError
from WITecSDK.Parameters import COMBoolStatusParameter, COMStringStatusParameter, COMTriggerParameter, COMEnumParameter, COMBoolParameter
from asyncio import sleep

def CatchException(func):
    
    def wrapper(arg):
        wrapper.__doc__ =  func.__doc__
        val = None
        try:
            val = func(arg)
        except COMError as e:
            # Throws an exception, if there is no active sequencer. 
            # This can happen, if a sequencer stops working inbetween two operations.
            if e.hresult != -2147024891: #UnauthorizedAccessException
                raise e
        except Exception as e:
            raise e
        return val
    return wrapper

class ActiveSequencer:
    """Gives access to current running operation"""
    
    _parampath = "Status|Software|Sequencers|"

    def __init__(self, aGetParameter: Callable):
        self._isASequencerActiveCOM: COMBoolStatusParameter = aGetParameter(self._parampath + "IsASequencerActive")
        self._activeSequencerNameCOM: COMStringStatusParameter = aGetParameter(self._parampath + "ActiveSequencer|Name")
        self._currentActivityCOM: COMStringStatusParameter = aGetParameter(self._parampath + "ActiveSequencer|CurrentActivity")
        self._stopSequencerCOM: COMTriggerParameter = aGetParameter("UserParameters|StopSequencer")
        self._showViewersCOM: COMEnumParameter = aGetParameter("UserParameters|CreateViewers")
        
    @property
    @CatchException
    def ActiveSequencerName(self) -> str:
        """Name of the operation currently running"""
        return self._activeSequencerNameCOM.Value

    @property
    @CatchException
    def CurrentActivity(self) -> str:
        """Retrieves the current activity as string. Possible values are documented in the help."""
        return self._currentActivityCOM.Value

    @property
    def IsASequencerActive(self) -> bool:
        """Can be used to poll a task to be completed"""
        return self._isASequencerActiveCOM.Value
    
    @property
    def ShowViewers(self) -> bool:
        """Can prevent windows from opening when a new measurment starts.
        Recommended for reccuring measurements that should be saved in one project."""
        return bool(self._showViewersCOM.Value)
    
    @ShowViewers.setter
    def ShowViewers(self, value: bool):
        self._showViewersCOM.Value = int(value)

    async def WaitActiveSequencerFinished(self):
        """Coroutine that waits until the current task is finished"""
        while self.IsASequencerActive:
            await sleep(0.1)

    def StopActiveSequencer(self):
        """Stops the current measurement or task"""
        self._stopSequencerCOM.ExecuteTrigger()
     
    async def StopActiveSequencerAndWaitUntilFinished(self):
        """Coroutine that stops the current activity and waits until it is finished"""
        self.StopActiveSequencer()
        await self.WaitActiveSequencerFinished()


class ActiveSequencer60(ActiveSequencer):
    """Extension of the ActiveSequencer class for version 6.0 and higher"""
    
    def __init__(self, aGetParameter: Callable):
        super().__init__(aGetParameter)
        self._statusOrResultCOM: COMStringStatusParameter = aGetParameter(self._parampath + "StatusOrResult")

    @property
    def StatusAndResult(self) -> tuple[str, str]:
        """Retrieves status information if available
        Possible Status values: "Running", "Finished", "Warning", "Error", "StoppedByUser" """
        value = self._statusOrResultCOM.Value.split('|')
        status = value[0]
        result = ''
        if len(value) == 2:
            result = value[1]
        return status, result


class ActiveSequencer62(ActiveSequencer60):
    """Extension of the ActiveSequencer class for version 6.2 and higher"""

    def __init__(self, aGetParameter: Callable):
        super().__init__(aGetParameter)
        self._askForUserOKCOM: COMBoolParameter = aGetParameter("UserParameters|AskForUserOK")

    @property
    def AskForUserOK(self) -> bool:
        """Turns off questions to the user that prevent a measurement from running"""
        return self._askForUserOKCOM.Value
    
    @AskForUserOK.setter
    def AskForUserOK(self, value: bool):
        self._askForUserOKCOM.Value = value