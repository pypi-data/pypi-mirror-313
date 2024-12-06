from typing import Callable
from WITecSDK.Parameters import COMIntParameter, COMFloatParameter
from WITecSDK.Modules.HelperStructs import microscopecontrol

parampath = microscopecontrol + "ObjectiveTurrets|Top|"

class ObjectiveTurret:
    """Gives access to the motorized objective turret"""

    def __init__(self, aGetParameter: Callable):
        self._selectedSlotCOM: COMIntParameter = aGetParameter(parampath + "SelectedSlot")
        self._changeDistanceCOM: COMFloatParameter = aGetParameter(parampath + "ObjectiveChangeDistance")

    @property
    def Slot(self) -> int:
        """Defines the objective slot"""
        return self._selectedSlotCOM.Value

    @Slot.setter
    def Slot(self, slot: int):
        self._selectedSlotCOM.Value = slot

    @property
    def ChangeDistance(self) -> float:
        """Defines the retract distance while changing the objective"""
        return self._changeDistanceCOM.Value

    @ChangeDistance.setter
    def ChangeDistance(self, slot: float):
        self._changeDistanceCOM.Value = slot