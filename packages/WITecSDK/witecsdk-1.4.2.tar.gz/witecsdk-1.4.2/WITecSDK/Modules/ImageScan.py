from typing import Callable
from WITecSDK.Modules.HelperStructs import XYZPosition, LargeAreaSettings, specchannelpath, userparam
from WITecSDK.Parameters import COMEnumParameter, COMFloatParameter, COMIntParameter, COMTriggerParameter, COMBoolParameter, ParameterNotAvailableException

parampath = userparam + "SequencerScanImage|"

class ImageScan:
    
    def __init__(self, aGetParameter: Callable):
        
        self._scanMethodCOM: COMEnumParameter = aGetParameter(parampath + "ConsecutiveMode")
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
        self._alphaCOM: COMFloatParameter = aGetParameter(parampath + "Geometry|Alpha")
        self._betaCOM: COMFloatParameter = aGetParameter(parampath + "Geometry|Beta")
        self._startCOM: COMTriggerParameter = aGetParameter(parampath + "Start")
        self._integrationTimeCOM: COMFloatParameter = aGetParameter(parampath + "TraceIntegrationTime")
        self._FilterManager1 = None
        self._FilterManager1R = None
        self._FilterManager2 = None
        self._FilterManager2R = None
        self._FilterManager3 = None
        self._FilterManager3R = None
        try:
            self._FilterManager1: COMBoolParameter = aGetParameter(specchannelpath + "SpectralCamera1Data|ScanImage|CreateFilterManagerTrace")
            self._FilterManager1R: COMBoolParameter = aGetParameter(specchannelpath + "SpectralCamera1Data|ScanImage|CreateFilterManagerRetrace")
            self._FilterManager2: COMBoolParameter = aGetParameter(specchannelpath + "SpectralCamera2Data|ScanImage|CreateFilterManagerTrace")
            self._FilterManager2R: COMBoolParameter = aGetParameter(specchannelpath + "SpectralCamera2Data|ScanImage|CreateFilterManagerRetrace")
            self._FilterManager3: COMBoolParameter = aGetParameter(specchannelpath + "SpectralCamera3Data|ScanImage|CreateFilterManagerTrace")
            self._FilterManager3R: COMBoolParameter = aGetParameter(specchannelpath + "SpectralCamera3Data|ScanImage|CreateFilterManagerRetrace")
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
        self._initialize(points, lines, width, integrationTime, center, gamma)
        self.setScanMethodToArea()
        self._heightCOM.Value = height

    def InitializeDepth(self, points: int, lines: int, width: float, depth: float, integrationTime: float, center: XYZPosition = None, gamma: float = 0):
        self._initialize(points, lines, width, integrationTime, center, gamma)
        self.setScanMethodToDepth()
        self._depthCOM.Value = depth

    def InitializeStack(self, points: int, lines: int, layers: int, width: float, height: float, depth: float, integrationTime: float, center: XYZPosition = None, gamma: float = 0):
        self._initialize(points, lines, width, integrationTime, center, gamma)
        self.setScanMethodToStack()
        self._layersPerScanCOM.Value = layers
        self._heightCOM.Value = height
        self._depthCOM.Value = depth

    def GetAllParameters(self) -> LargeAreaSettings:
        return LargeAreaSettings(self._scanMethodCOM.Value, self._pointsPerLineCOM.Value, self._linesPerImageCOM.Value,
                                 self._layersPerScanCOM.Value, self._widthCOM.Value, self._heightCOM.Value,
                                 self._depthCOM.Value, self.IntegrationTime, self.Center, self.Gamma)

    def SetAllParameters(self, LAStruct: LargeAreaSettings):
        if LAStruct.Mode == 0 or LAStruct.Mode == 1:
            self.InitializeArea(LAStruct.Points, LAStruct.Lines, LAStruct.Width, LAStruct.Height,
                                LAStruct.IntegrationTime, LAStruct.Center, LAStruct.Gamma)
        elif LAStruct.Mode == 2 or LAStruct.Mode == 3:
            self.InitializeDepth(LAStruct.Points, LAStruct.Lines, LAStruct.Width, LAStruct.Depth,
                                 LAStruct.IntegrationTime, LAStruct.Center, LAStruct.Gamma)
        elif LAStruct.Mode == 4:
            self.InitializeStack(LAStruct.Points, LAStruct.Lines, LAStruct.Layers ,LAStruct.Width,
                                 LAStruct.Height, LAStruct.Depth, LAStruct.IntegrationTime, LAStruct.Center, LAStruct.Gamma)
        else:
            raise Exception('Mode is not supported')

    def setScanMethodToArea(self):
        self._scanMethodCOM.Value = 0

    def setScanMethodToAreaLoop(self):
        self._scanMethodCOM.Value = 1

    def setScanMethodToDepth(self):
        self._scanMethodCOM.Value = 2

    def setScanMethodToDepthLoop(self):
        self._scanMethodCOM.Value = 3
        
    def setScanMethodToStack(self):
        self._scanMethodCOM.Value = 4

    def centerAtCurrenPos(self):
        self._centerAtCurrentPosCOM.ExecuteTrigger()

    def DeactivateFilterViewer(self):
        if self._FilterManager1 is not None:
            self._FilterManager1.Value = False
            self._FilterManager1R.Value = False
        if self._FilterManager2 is not None:
            self._FilterManager2.Value = False
            self._FilterManager2R.Value = False
        if self._FilterManager3 is not None:
            self._FilterManager3.Value = False
            self._FilterManager3R.Value = False

    @property
    def Center(self) -> XYZPosition:
        return XYZPosition(self._centerXCOM.Value, self._centerYCOM.Value, self._centerZCOM.Value)
    
    @Center.setter
    def Center(self, centerPoint: XYZPosition):
        self._centerXCOM.Value = centerPoint.X
        self._centerYCOM.Value = centerPoint.Y
        self._centerZCOM.Value = centerPoint.Z

    @property
    def Gamma(self) -> float:
        return self._gammaCOM.Value

    @Gamma.setter
    def Gamma(self, gamma: float):
        self._gammaCOM.Value = gamma

    @property
    def Alpha(self) -> float:
        return self._alphaCOM.Value

    @Alpha.setter
    def Alpha(self, alpha: float):
        self._alphaCOM.Value = alpha

    @property
    def Beta(self) -> float:
        return self._betaCOM.Value

    @Beta.setter
    def Beta(self, beta: float):
        self._betaCOM.Value = beta

    @property
    def IntegrationTime(self) -> float:
        return self._integrationTimeCOM.Value

    @IntegrationTime.setter
    def IntegrationTime(self, integrationTime: float):
        self._integrationTimeCOM.Value = integrationTime

    def Start(self):
        self._startCOM.ExecuteTrigger()