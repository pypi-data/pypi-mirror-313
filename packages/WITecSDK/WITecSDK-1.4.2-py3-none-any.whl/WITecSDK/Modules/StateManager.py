from typing import Callable
from WITecSDK.Parameters import COMStringParameter, COMTriggerParameter
from WITecSDK.Modules.HelperStructs import microscopecontrol

parampath = microscopecontrol + "StateManager|"

class StateManager:

    def __init__(self, aGetParameter: Callable):
        self._stateNameCOM: COMStringParameter = aGetParameter(parampath + "StateName")
        self._resetAllCOM: COMTriggerParameter = aGetParameter(parampath + "ResetAll")

    @property
    def State(self) -> str:
        return self._stateNameCOM.Value
    
    @State.setter
    def State(self, value: str):
        self._stateNameCOM.Value = value

    def ResetAll(self):
        self._resetAllCOM.ExecuteTrigger()