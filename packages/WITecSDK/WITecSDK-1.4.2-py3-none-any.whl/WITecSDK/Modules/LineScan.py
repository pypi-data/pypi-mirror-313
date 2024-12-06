"""Module containing the classes for the Line Scan"""

from typing import Callable
from WITecSDK.Parameters import COMIntParameter, COMTriggerParameter, COMFloatParameter, COMEnumParameter
from WITecSDK.Modules.SingleSpectrum import SingleSpectrumBase
from WITecSDK.Modules.HelperStructs import XYZPosition, userparam

parampath = userparam + "SequencerScanLine|"

class LineScan(SingleSpectrumBase):
    """Implements the Line Scan"""

    def __init__(self, aGetParameter: Callable):
        super().__init__(aGetParameter)
        self._numberPointsCOM: COMIntParameter = aGetParameter(parampath + "SamplePoints")
        self._startLineScanCOM: COMTriggerParameter = aGetParameter(parampath + "Start")
        self._startXCOM: COMFloatParameter = aGetParameter(parampath + "StartPoint|X")
        self._startYCOM: COMFloatParameter = aGetParameter(parampath + "StartPoint|Y")
        self._startZCOM: COMFloatParameter = aGetParameter(parampath + "StartPoint|Z")
        self._endXCOM: COMFloatParameter = aGetParameter(parampath + "EndPoint|X")
        self._endYCOM: COMFloatParameter = aGetParameter(parampath + "EndPoint|Y")
        self._endZCOM: COMFloatParameter = aGetParameter(parampath + "EndPoint|Z")

    def Initialize(self, numberPoints: int, startPoint: XYZPosition, endPoint: XYZPosition, integrationTime: float, numberOfAccumulations: int):
        """Initializes a Line scan with the necessary parameters."""
        self.NumberPoints = numberPoints
        self.StartPoint = startPoint
        self.EndPoint = endPoint
        self.NumberOfAccumulations = numberOfAccumulations
        self.IntegrationTime = integrationTime

    @property
    def NumberOfPoints(self) -> int:
        """Defines the number of points along the line"""
        return self._numberPointsCOM.Value
    
    @NumberOfPoints.setter
    def NumberOfPoints(self, numberOfPoints: int):
        self._numberPointsCOM.Value = numberOfPoints

    @property
    def StartPoint(self) -> XYZPosition:
        """Defines the start point"""
        return XYZPosition(self._startXCOM.Value, self._startYCOM.Value, self._startZCOM.Value)

    @StartPoint.setter
    def StartPoint(self, startPoint: XYZPosition):
        self._startXCOM.Value = startPoint.X
        self._startYCOM.Value = startPoint.Y
        self._startZCOM.Value = startPoint.Z
        
    @property
    def EndPoint(self) -> XYZPosition:
        """Defines the end point"""
        return XYZPosition(self._endXCOM.Value, self._endYCOM.Value, self._endZCOM.Value)

    @EndPoint.setter
    def EndPoint(self, endPoint: XYZPosition):
        self._endXCOM.Value = endPoint.X
        self._endYCOM.Value = endPoint.Y
        self._endZCOM.Value = endPoint.Z

    def Start(self):
        """Starts the Line Scan"""
        self._startLineScanCOM.ExecuteTrigger()


class LineScan62(LineScan):
    """Extension of the LineScan class for version 6.2 and higher"""
    
    def __init__(self, aGetParameter: Callable):
        super().__init__(aGetParameter)
        self._integrationTimeCOM: COMFloatParameter = aGetParameter(parampath + "IntegrationTime")
        self._accumulationsCOM: COMIntParameter = aGetParameter(parampath + "NrOfAccumulations")
        self._startCurrentCOM: COMTriggerParameter = aGetParameter(parampath + "StartAtCurrentPosition")
        self._centerCurrentCOM: COMTriggerParameter = aGetParameter(parampath + "CenterAtCurrentPosition")
        self._endCurrentCOM: COMTriggerParameter = aGetParameter(parampath + "EndAtCurrentPosition")
        self._scanModeCOM: COMEnumParameter = aGetParameter(parampath + "PreferredScanMode")

    @property
    def IntegrationTime(self) -> float:
        """Defines the integration time in seconds"""
        return self._integrationTimeCOM.Value
    
    @IntegrationTime.setter
    def IntegrationTime(self, value: float):
        self._integrationTimeCOM.Value = value

    @property
    def NumberOfAccumulations(self) -> int:
        """Defines the number of accumulations (only for Stepwise mode)"""
        return self._accumulationsCOM.Value
    
    @NumberOfAccumulations.setter
    def NumberOfAccumulations(self, value: int):
        self._accumulationsCOM.Value = value

    @property
    def PreferedScanMode(self) -> tuple[str,int]:
        """Returns the current prefered measurement mode"""
        return self._scanModeCOM.EnumValue
    
    def setScanModeToStepwise(self):
        """Defines Stepwise as measurement mode"""
        self._scanModeCOM.Value = 0

    def setScanModeToContinuous(self):
        """Defines Continuous as prefered measurement mode"""
        self._scanModeCOM.Value = 1

    def StartAtCurrentPosition(self):
        """Sets the current position as start"""
        self._startCurrentCOM.ExecuteTrigger()

    def CenterAtCurrentPosition(self):
        """Sets the current position as center"""
        self._centerCurrentCOM.ExecuteTrigger()

    def EndAtCurrentPosition(self):
        """Sets the current position as end"""
        self._endCurrentCOM.ExecuteTrigger()