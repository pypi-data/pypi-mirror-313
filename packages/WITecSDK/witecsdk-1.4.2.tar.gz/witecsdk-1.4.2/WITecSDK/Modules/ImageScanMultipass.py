from typing import Callable
from WITecSDK.Parameters import COMFloatParameter, COMTriggerParameter
from WITecSDK.Modules.HelperStructs import userparam

parampath = userparam + "SequencerScanImageMultiPass|"

class ImageScanMultipass:
    """Gives access to the Multipass Image scan for AFM Lift modes if available"""
    
    def __init__(self, aGetParameter: Callable):
        
        self._startCOM: COMTriggerParameter = aGetParameter(parampath + "Start")
        self._zOffsetCOM: COMFloatParameter = aGetParameter(parampath + "ZOffsetForMeasurement")
        self._lookaheadCOM: COMFloatParameter = aGetParameter(parampath + "LookAheadOffset")
        
    @property
    def ZOffset(self) -> float:
        return self._zOffsetCOM.Value

    @ZOffset.setter
    def ZOffset(self, value: float):
        self._zOffsetCOM.Value = value

    @property
    def LookAhead(self) -> float:
        return self._lookaheadCOM.Value

    @LookAhead.setter
    def LookAhead(self, value: float):
        self._lookaheadCOM.Value = value

    def Start(self):
        self._startCOM.ExecuteTrigger()