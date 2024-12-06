from typing import Callable
from WITecSDK.Parameters import COMFloatParameter,   COMStringParameter,  COMTriggerParameter,  COMEnumParameter
from WITecSDK.Modules.BeamPath import AutomatedCoupler
from WITecSDK.Modules.HelperStructs import microscopecontrol
from asyncio import sleep
import tempfile

videopath = microscopecontrol + "Video|"
objectivepath = microscopecontrol + "Objective|"
whitelightpath = microscopecontrol + "WhiteLight|"

class ObjectiveInformation:
    def __init__(self, aFocusDepth: float, aMagnification: float, aInformation: str):
        self.FocusDepth = aFocusDepth
        self.Magnification = aMagnification
        self.Information = aInformation
        
class CalibrationData:
    def __init__(self, aWidth: float, aHeight: float, aRotation: float):
        self.Width = aWidth
        self.Height = aHeight
        self.Rotation = aRotation

class VideoControlBase:

    _tempImagePath = tempfile.gettempdir() + "\\WITec\\temp.png"
    _videoImageFileNameCOM: COMFloatParameter = None
    _saveVideoImageToFileCOM: COMTriggerParameter = None
    _acquireVideoImageCOM: COMTriggerParameter = None
    VideoCameraCoupler = None

    def __init__(self, aGetParameter: Callable):
        self._rotationDegreesCOM: COMFloatParameter = aGetParameter(videopath + "Calibration|RotationDegrees")
        self._imageWidthMicronsCOM: COMFloatParameter = aGetParameter(videopath + "Calibration|ImageWidthMicrons")
        self._imageHeightMicronsCOM: COMFloatParameter = aGetParameter(videopath + "Calibration|ImageHeightMicrons")
        self._focusDepthCOM: COMFloatParameter = aGetParameter(objectivepath + "SelectedTop|FocusDepth")
        self._informationCOM: COMStringParameter = aGetParameter(objectivepath + "SelectedTop|Information")
        self._magnificationCOM: COMFloatParameter = aGetParameter(objectivepath + "SelectedTop|Magnification")
        self._probePositionXCOM: COMFloatParameter = aGetParameter(videopath + "ProbePosition|RelativeX")
        self._probePositionYCOM: COMFloatParameter = aGetParameter(videopath + "ProbePosition|RelativeY")
        self._executeAutoBrightnessCOM: COMTriggerParameter = aGetParameter(videopath + "AutoBrightness|Execute")
        self._selectedCameraCOM: COMStringParameter = aGetParameter(videopath + "SelectedCameraName")
        self._selectTopCameraCOM: COMTriggerParameter = aGetParameter(videopath + "SelectTopCamera")
        self.VideoCameraCoupler = AutomatedCoupler(aGetParameter, videopath + "VideoCameraCoupler")
            
    async def ExecuteAutoBrightness(self) -> bool:
        self._executeAutoBrightnessCOM.ExecuteTrigger()  
        return await self._waitForAutoBrightness()
        
    async def _waitForAutoBrightness(self) -> bool:
        await sleep(1)
        return True
        
    async def AcquireVideoImageToFile(self, imagepath: str = None) -> str:
        if imagepath is None:
            imagepath = self._tempImagePath
        self._videoImageFileNameCOM.Value = imagepath
        self._saveVideoImageToFileCOM.ExecuteTrigger()
        await sleep(1)
        return imagepath

    async def AcquireVideoImage(self):
        self._acquireVideoImageCOM.ExecuteTrigger()
        await sleep(1)
        return

    @property
    def SelectedCameraName(self) -> str:
        return self._selectedCameraCOM.Value
    
    @SelectedCameraName.setter
    def SelectedCameraName(self, name: str):
        self._selectedCameraCOM.Value = name

    def SelectTopCamera(self):
        self._selectTopCameraCOM.ExecuteTrigger()

    def GetCalibrationData(self) -> CalibrationData:
        rotation = self._rotationDegreesCOM.Value
        width = self._imageWidthMicronsCOM.Value
        height = self._imageHeightMicronsCOM.Value
        return CalibrationData(width, height, rotation)

    def GetObjectiveInformation(self) -> ObjectiveInformation:
        focusDepth = self._focusDepthCOM.Value
        magnification = self._magnificationCOM.Value
        information = self._informationCOM.Value
        return ObjectiveInformation(focusDepth, magnification, information)
    
    @property
    def ProbePosition(self) -> tuple[float,float]:
        probeX = self._probePositionXCOM.Value
        probeY = self._probePositionYCOM.Value
        return (probeX, probeY)


class VideoControl50(VideoControlBase):
    
    def __init__(self, aGetParameter: Callable):
        multicom = "MultiComm|MultiCommVideoSystem|"
        super().__init__(aGetParameter)
        self._videoImageFileNameCOM: COMStringParameter = aGetParameter(multicom + "BitmapFileName")
        self._saveVideoImageToFileCOM: COMTriggerParameter = aGetParameter(multicom + "SaveColorBitmapToFile")
        self._acquireVideoImageCOM: COMTriggerParameter = aGetParameter("UserParameters|VideoSystem|Start")


class VideoControl51(VideoControlBase):
    
    def __init__(self, aGetParameter: Callable):
        super().__init__(aGetParameter)
        self._videoImageFileNameCOM: COMStringParameter = aGetParameter(videopath + "VideoImageFileName")
        self._saveVideoImageToFileCOM: COMTriggerParameter = aGetParameter(videopath + "AcquireVideoImageToFile")
        self._acquireVideoImageCOM: COMTriggerParameter = aGetParameter(videopath + "AcquireVideoImage")


class VideoControl61(VideoControl51):
    
    def __init__(self, aGetParameter: Callable):
        super().__init__(aGetParameter)
        self._smartBrightnessFactorCOM: COMFloatParameter = aGetParameter(whitelightpath + "SmartBrightnessFactor")
        self._smartBrightnessFactorMaxCOM: COMFloatParameter = aGetParameter(whitelightpath + "SmartBrightnessFactorMax")
        self._smartBrightnessPercentageCOM: COMFloatParameter = aGetParameter(whitelightpath + "SmartBrightnessPercentage")
        self._statusAutoBrightnessCOM: COMEnumParameter = aGetParameter(videopath + "AutoBrightness|Status")

    @property
    def SmartBrightnessFactor(self) -> float:
        return self._smartBrightnessFactorCOM.Value
    
    @SmartBrightnessFactor.setter
    def SmartBrightnessFactor(self, value: float):
        self._smartBrightnessFactorCOM.Value = value

    @property
    def SmartBrightnessFactorMax(self) -> float:
        return self._smartBrightnessFactorMaxCOM.Value

    @property
    def SmartBrightnessPercentage(self) -> float:
        return self._smartBrightnessPercentageCOM.Value
    
    @SmartBrightnessPercentage.setter
    def SmartBrightnessPercentage(self, value: float):
        self._smartBrightnessPercentageCOM.Value = value
    
    async def _waitForAutoBrightness(self) -> bool:
        abstate: int = 0
        while abstate == 0:
            await sleep(0.1)
            abstate = self._statusAutoBrightnessCOM.Value
            #"Running", "LastSucceeded", "LastFailed"
        return abstate == 1
