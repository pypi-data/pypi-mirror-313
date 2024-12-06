from WITecSDK.Modules.HelperStructs import XYZPosition, LargeAreaSettings, specchannelpath, userparam
from typing import Callable
from WITecSDK.Parameters import COMEnumParameter, COMIntParameter, COMFloatParameter, COMTriggerParameter, COMBoolParameter, ParameterNotAvailableException

parampath = userparam + "SequencerLargeScaleImaging|"

class LargeAreaScan:
    """Implements the Large Area Scan"""

    def __init__(self, aGetParameter: Callable):
        self._scanMethodCOM: COMEnumParameter = aGetParameter(parampath + "ScanMethod")
        self._pointsPerLineCOM: COMIntParameter = aGetParameter(parampath + "PointsPerLine")
        self._linesPerImageCOM: COMIntParameter = aGetParameter(parampath + "LinesPerImage")
        self._layersPerScanCOM: COMIntParameter = aGetParameter(parampath + "LayersPerScan")
        self._widthCOM: COMFloatParameter = aGetParameter(parampath + "Geometry|Width")
        self._heightCOM: COMFloatParameter = aGetParameter(parampath + "Geometry|Height")
        self._depthCOM: COMFloatParameter = aGetParameter(parampath + "Geometry|Depth")
        self._centerAtCurrentPosCOM: COMTriggerParameter = aGetParameter(parampath + "Geometry|CenterAtCurrentPosition")
        self._centerXCOM: COMFloatParameter = aGetParameter(parampath + "Geometry|CenterX")
        self._centerYCOM: COMFloatParameter = aGetParameter(parampath + "Geometry|CenterY")
        self._centerZCOM: COMFloatParameter = aGetParameter(parampath + "Geometry|CenterZ")
        self._gammaCOM: COMFloatParameter = aGetParameter(parampath + "Geometry|Gamma")
        self._startCOM: COMTriggerParameter = aGetParameter(parampath + "Start")
        self._integrationTimeCOM: COMFloatParameter = aGetParameter(parampath + "SmoothScanIntegrationTime")
        self._FilterManager1: COMBoolParameter = aGetParameter(specchannelpath + "SpectralCamera1Data|LargeScaleImaging|CreateFilterManager")
        self._FilterManager2: COMBoolParameter = None
        self._FilterManager3: COMBoolParameter = None
        try:
            self._FilterManager2 = aGetParameter(specchannelpath + "SpectralCamera2Data|LargeScaleImaging|CreateFilterManager")
            self._FilterManager3 = aGetParameter(specchannelpath + "SpectralCamera3Data|LargeScaleImaging|CreateFilterManager")
        except ParameterNotAvailableException:
            pass
        except Exception as e:
            raise e
        
    def _initialize(self, points: int, lines: int, width: float, integrationTime: float, center: XYZPosition, gamma: float):
        if center is not None:
            self.Center = center
        else:
            self.centerAtCurrenPos()
        self.Gamma = gamma
        self.IntegrationTime = integrationTime
        self._pointsPerLineCOM.Value = points
        self._linesPerImageCOM.Value = lines
        self._widthCOM.Value = width

    def InitializeArea(self, points: int, lines: int, width: float, height: float, integrationTime: float, center: XYZPosition = None, gamma: float = 0):
        """Initializes an Area scan with the necessary parameters.
        Without defining a center the current position will be used as center."""
        self._initialize(points, lines, width, integrationTime, center, gamma)
        self.setScanMethodToArea()
        self._heightCOM.Value = height   

    def InitializeDepth(self, points: int, lines: int, width: float, depth: float, integrationTime: float, center: XYZPosition = None, gamma: float = 0):
        """Initializes a Depth scan with the necessary parameters.
        Without defining a center the current position will be used as center."""
        self._initialize(points, lines, width, integrationTime, center, gamma)
        self.setScanMethodToDepth()
        self._depthCOM.Value = depth

    def InitializeStack(self, points: int, lines: int, layers: int, width: float, height: float, depth: float, integrationTime: float, center: XYZPosition = None, gamma: float = 0):
        """Initializes a Stack scan with the necessary parameters.
        Without defining a center the current position will be used as center."""
        self._initialize(points, lines, width, integrationTime, center, gamma)
        self.setScanMethodToStack()
        self._layersPerScanCOM.Value = layers
        self._heightCOM.Value = height
        self._depthCOM.Value = depth

    def GetAllParameters(self) -> LargeAreaSettings:
        """Returns all parameters as LargeAreaSettings object"""
        return LargeAreaSettings(self._scanMethodCOM.Value, self._pointsPerLineCOM.Value, self._linesPerImageCOM.Value,
                                 self._layersPerScanCOM.Value, self._widthCOM.Value, self._heightCOM.Value,
                                 self._depthCOM.Value, self.IntegrationTime, self.Center, self.Gamma)

    def SetAllParameters(self, LAStruct: LargeAreaSettings):
        """Initializes the Large Area Scan based on the parameters in the LargeAreaSettings object"""
        if LAStruct.Mode == 1:
            self.InitializeArea(LAStruct.Points, LAStruct.Lines, LAStruct.Width, LAStruct.Height,
                                LAStruct.IntegrationTime, LAStruct.Center, LAStruct.Gamma)
        elif LAStruct.Mode == 2:
            self.InitializeDepth(LAStruct.Points, LAStruct.Lines, LAStruct.Width, LAStruct.Depth,
                                 LAStruct.IntegrationTime, LAStruct.Center, LAStruct.Gamma)
        elif LAStruct.Mode == 3:
            self.InitializeStack(LAStruct.Points, LAStruct.Lines, LAStruct.Layers ,LAStruct.Width,
                                 LAStruct.Height, LAStruct.Depth, LAStruct.IntegrationTime, LAStruct.Center, LAStruct.Gamma)
        else:
            raise Exception('Mode is not supported')
    
    @property
    def ScanMethod(self) -> tuple[str,int]:
        """Returns the current measurement mode"""
        return self._scanMethodCOM.EnumValue
    
    def setScanMethodToStepwise(self):
        """Defines Stepwise Raster as measurement mode"""
        self._scanMethodCOM.Value = 0

    def setScanMethodToArea(self):
        """Defines Area as measurement mode"""
        self._scanMethodCOM.Value = 1

    def setScanMethodToDepth(self):
        """Defines Depth as measurement mode"""
        self._scanMethodCOM.Value = 2

    def setScanMethodToStack(self):
        """Defines Stack as measurement mode"""
        self._scanMethodCOM.Value = 3

    def centerAtCurrenPos(self):
        """Defines the current position as center"""
        self._centerAtCurrentPosCOM.ExecuteTrigger()

    def DeactivateFilterViewer(self):
        """Deactivates the Filter viewer for the Large Area scan.
        Is valid until the configuration is reloaded"""
        self._FilterManager1.Value = False
        if self._FilterManager2 is not None:
            self._FilterManager2.Value = False
        if self._FilterManager3 is not None:
            self._FilterManager3.Value = False

    @property
    def Center(self) -> XYZPosition:
        """Defines the center using a XYZPosition object"""
        return XYZPosition(self._centerXCOM.Value, self._centerYCOM.Value, self._centerZCOM.Value)
    
    @Center.setter
    def Center(self, centerPoint: XYZPosition):
        self._centerXCOM.Value = centerPoint.X
        self._centerYCOM.Value = centerPoint.Y
        self._centerZCOM.Value = centerPoint.Z

    @property
    def Gamma(self) -> float:
        """Defines the angle gamma in degree"""
        return self._gammaCOM.Value

    @Gamma.setter
    def Gamma(self, gamma: float):
        self._gammaCOM.Value = gamma

    @property
    def IntegrationTime(self) -> float:
        """Defines the integration time in seconds"""
        return self._integrationTimeCOM.Value

    @IntegrationTime.setter
    def IntegrationTime(self, integrationTime: float):
        self._integrationTimeCOM.Value = integrationTime

    def Start(self):
        """Starts the Large Area Scan"""
        self._startCOM.ExecuteTrigger()


class LargeAreaScan62(LargeAreaScan):
    """Extension of the LargeAreaScan class for version 6.2 and higher"""

    def __init__(self, aGetParameter: Callable):
        super().__init__(aGetParameter)
        self._accumulationsCOM: COMIntParameter = aGetParameter(parampath + "NrOfAccumulations")

    @property
    def NumberOfAccumulations(self) -> int:
        """Defines the number of accumulations (only for Stepwise raster)"""
        return self._accumulationsCOM.Value
    
    @NumberOfAccumulations.setter
    def NumberOfAccumulations(self, value: int):
        self._accumulationsCOM.Value = value
