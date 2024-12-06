"""Module containing the class for the Distance curve"""

from typing import Callable
from WITecSDK.Parameters import COMIntParameter, COMTriggerParameter, COMFloatParameter
from WITecSDK.Modules.HelperStructs import userparam

parampath = userparam + "SequencerForceDistanceCurve|"

class DistanceCurve:
    """Implements the Distance Curve (AFM)"""

    def __init__(self, aGetParameter: Callable):
        self._numberPointsCOM: COMIntParameter = aGetParameter(parampath + "MeasurePoints")
        self._startCOM: COMTriggerParameter = aGetParameter(parampath + "Start")
        self._retractionCOM: COMFloatParameter = aGetParameter(parampath + "Retraction")
        self._indentationCOM: COMFloatParameter = aGetParameter(parampath + "Indentation")
        self._speedCOM: COMFloatParameter = aGetParameter(parampath + "Speed")

    def Initialize(self, numberPoints: int, retraction: float, indentation: float, speed: float):
        """Initializes a Distance curve with the necessary parameters."""
        self.SamplePoints = numberPoints
        self.Pull = retraction
        self.Push = indentation
        self.Speed = speed

    @property
    def SamplePoints(self) -> int:
        """Defines the number of data points of the curve"""
        return self._numberPointsCOM.Value
    
    @SamplePoints.setter
    def SamplePoints(self, value: int):
        self._numberPointsCOM.Value = value

    @property
    def Pull(self) -> float:
        """Defines the retract distance in µm"""
        return self._retractionCOM.Value
    
    @Pull.setter
    def Pull(self, value: float):
        self._retractionCOM.Value = value

    @property
    def Push(self) -> float:
        """Defines the push distance in µm"""
        return self._indentationCOM.Value
    
    @Push.setter
    def Push(self, value: float):
        self._indentationCOM.Value = value

    @property
    def Speed(self) -> float:
        """Defines the speed of the movement in µm/s"""
        return self._speedCOM.Value
    
    @Speed.setter
    def Speed(self, value: float):
        self._speedCOM.Value = value

    def Start(self):
        """Starts the Distance curve"""
        self._startCOM.ExecuteTrigger()
