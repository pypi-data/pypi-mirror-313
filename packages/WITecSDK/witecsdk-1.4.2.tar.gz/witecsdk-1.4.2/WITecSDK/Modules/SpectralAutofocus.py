from typing import Callable
from WITecSDK.Parameters import COMTriggerParameter, COMFloatParameter, COMEnumParameter, COMStringParameter
from WITecSDK.Modules.HelperStructs import AutofocusSettings, userparam

parampath = userparam + "SequencerAutoFocus|"

class SpectralAutofocus:

    def __init__(self, aGetParameter: Callable):
        self._startAutoFocusCOM: COMTriggerParameter = aGetParameter(parampath + "Start")
        self._maximumRangeCOM: COMFloatParameter = aGetParameter(parampath + "MaximumRange")
        self._minimalIntegrationTimeCOM: COMFloatParameter = aGetParameter(parampath + "MinimalIntegrationTime")
        self._postFocusMoveCOM: COMFloatParameter = aGetParameter(parampath + "PostAutoFocusMovement")

    def PerformAutofocus(self, autofocusSettings: AutofocusSettings = None):
        if autofocusSettings is not None:
            self.Initialize(autofocusSettings)
            
        self.Start()
    
    def Initialize(self, settings: AutofocusSettings):
        self.MaxRange = settings.MaximumRange
        self.MinIntegrationTime = settings.MinimalIntegrationTime

    @property
    def MinIntegrationTime(self) -> float:
        return self._minimalIntegrationTimeCOM.Value
    
    @MinIntegrationTime.setter
    def MinIntegrationTime(self, integrationTime: float):
        self._minimalIntegrationTimeCOM.Value = integrationTime

    @property
    def MaxRange(self) -> float:
        return self._maximumRangeCOM.Value
    
    @MaxRange.setter
    def MaxRange(self, range: float):
        self._maximumRangeCOM.Value = range

    @property
    def PostFocusMove(self) -> float:
        return self._postFocusMoveCOM.Value
    
    @PostFocusMove.setter
    def PostFocusMove(self, range: float):
        self._postFocusMoveCOM.Value = range
    
    def Start(self):
        self._startAutoFocusCOM.ExecuteTrigger()


class SpectralAutofocus51(SpectralAutofocus):

    def __init__(self, aGetParameter: Callable):
        super().__init__(aGetParameter)
        self._centerCOM: COMFloatParameter = aGetParameter(parampath + "Center")
        self._stepSizeMultiplierCOM: COMFloatParameter = aGetParameter(parampath + "StepSizeMultiplier")
        self._autoFocusModeCOM: COMEnumParameter = aGetParameter(parampath + "AutoFocusMode")

    def PerformAutofocus(self, autofocusSettings: AutofocusSettings = None):
        if autofocusSettings is not None:
            self.InitializeFindRaman(autofocusSettings)
            
        self.Start()

    def Initialize(self, settings: AutofocusSettings):
        super().Initialize(settings)
        self.Center = settings.Center
        
    def InitializeFindRaman(self, settings: AutofocusSettings):
        self.Initialize(settings)
        self.SetModeFindRaman()
        self.StepsizeMultiplier = settings.StepSizeMultiplier

    def InitializeFindPeak(self, settings: AutofocusSettings):
        self.Initialize(settings)
        self.SetModeFindPeak()

    def SetModeFindPeak(self):
        self._autoFocusModeCOM.Value = 0

    def SetModeFindRaman(self):
        self._autoFocusModeCOM.Value = 1

    @property
    def Center(self) -> float:
        return self._centerCOM.Value
    
    @Center.setter
    def Center(self, center: float):
        self._centerCOM.Value = center

    @property
    def StepsizeMultiplier(self) -> float:
        return self._stepSizeMultiplierCOM.Value
    
    @StepsizeMultiplier.setter
    def StepsizeMultiplier(self, stepsize: float):
        self._stepSizeMultiplierCOM.Value = stepsize


class SpectralAutofocus53(SpectralAutofocus51):

    def __init__(self, aGetParameter: Callable):
        super().__init__(aGetParameter)
        self._spectralMaskCOM: COMStringParameter = aGetParameter("UserParameters|SpectralDataAnalysis|Mask")

    def Initialize(self, settings: AutofocusSettings):
        super().Initialize(settings)
        self.Mask = settings.Mask

    def setSpectralMask(self, mask: str = "100;3600"):
        self._spectralMaskCOM.Value = mask

    @property
    def SpectralMask(self) -> str:
        return self._spectralMaskCOM.Value
    
    @SpectralMask.setter
    def SpectralMask(self, mask: str):
        self._spectralMaskCOM.Value = mask
