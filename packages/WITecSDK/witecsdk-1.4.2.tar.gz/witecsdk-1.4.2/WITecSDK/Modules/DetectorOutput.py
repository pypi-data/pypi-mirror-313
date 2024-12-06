from typing import Callable
from WITecSDK.Parameters import COMStringParameter, COMTriggerParameter
from WITecSDK.Modules.HelperStructs import microscopecontrol

parampath = microscopecontrol + "DetectorOutput|"

class DetectorOutput:
    """Gives control over the output. In normal case the output is selcted by the configuration."""

    def __init__(self, aGetParameter: Callable):
        self._selectedCOM: COMStringParameter = aGetParameter(parampath + "Selected")
        self._setAllOutCOM: COMTriggerParameter = aGetParameter(parampath + "AllOut")
        self._setNoOutputCOM: COMTriggerParameter = aGetParameter(parampath + "NoOutput")
        self._setCCD1COM: COMTriggerParameter = aGetParameter(parampath + "CCD1")
        self._setCCD2COM: COMTriggerParameter = aGetParameter(parampath + "CCD2")
        self._setCCD3COM: COMTriggerParameter = aGetParameter(parampath + "CCD3")
        self._setSinglePhotonCounting1COM: COMTriggerParameter = aGetParameter(parampath + "SinglePhotonCounting1")
        self._setSinglePhotonCounting2COM: COMTriggerParameter = aGetParameter(parampath + "SinglePhotonCounting2")
        self._setSinglePhotonCounting3COM: COMTriggerParameter = aGetParameter(parampath + "SinglePhotonCounting3")

    def SetAllOut(self):
        """Moves automated output coupler out of the beampath"""
        self._setAllOutCOM.ExecuteTrigger()

    def SetNoOutput(self):
        """No output is used"""
        self._setNoOutputCOM.ExecuteTrigger()

    def SetCCD1(self):
        """Sets CCD1 as output"""
        self._setCCD1COM.ExecuteTrigger()
    
    def SetCCD2(self):
        """Sets CCD2 as output"""
        self._setCCD1COM.ExecuteTrigger()

    def SetCCD3(self):
        """Sets CCD3 as output"""
        self._setCCD1COM.ExecuteTrigger()
    
    def SetSinglePhotonCounting1(self):
        """Sets SinglePhotonCounting1 as output"""
        self._setSinglePhotonCounting1COM.ExecuteTrigger()
    
    def SetSinglePhotonCounting2(self):
        """Sets SinglePhotonCounting2 as output"""
        self._setSinglePhotonCounting2COM.ExecuteTrigger()

    def SetSinglePhotonCounting3(self):
        """Sets SinglePhotonCounting3 as output"""
        self._setSinglePhotonCounting3COM.ExecuteTrigger()

    @property
    def SelectedOutput(self) -> str:
        """Returns the currently selected output"""
        return self._selectedCOM.Value