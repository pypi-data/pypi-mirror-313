from typing import Callable
from WITecSDK.Modules.HelperStructs import userparam, datachannelpath
from WITecSDK.Parameters import COMFloatParameter, COMTriggerParameter, COMFloatStatusParameter

parampath = userparam + "SequencerTipApproach|"
parampathPI = userparam + "PIController|"

class AFM:
    """Gives access to AFM functions"""
    
    def __init__(self, aGetParameter: Callable):
        
        self._startCOM: COMTriggerParameter = aGetParameter(parampath + "Start")
        self._retractTipCOM: COMTriggerParameter = aGetParameter(parampath + "RetractTip")
        self._retractDistanceCOM: COMFloatParameter = aGetParameter(parampath + "RetractDistance")

        self._setpointCOM: COMFloatParameter = aGetParameter(parampathPI + "Setpoint")
        self._pGainCOM: COMFloatParameter = aGetParameter(parampathPI + "PGain")
        self._iGainCOM: COMFloatParameter = aGetParameter(parampathPI + "IGain")
        
        self._drivingAmpCOM: COMFloatParameter = aGetParameter(userparam + "LockInPrimary|ExcitationAmplitude")
        self._drivingFreqCOM: COMFloatParameter = aGetParameter(userparam + "LockInPrimary|ExcitationFrequency")
        self._autoResonanceCOM: COMTriggerParameter = aGetParameter(userparam + "SequencerAutoResonance|Start")

        self._dcSumCOM: COMFloatStatusParameter = aGetParameter(datachannelpath + "SumSignal")
        self._dcTMBCOM: COMFloatStatusParameter = aGetParameter(datachannelpath + "TopMinusBottom")
        self._dcLMRCOM: COMFloatStatusParameter = aGetParameter(datachannelpath + "LeftMinusRight")
        self._dcAmplCOM: COMFloatStatusParameter = aGetParameter(datachannelpath + "AmplitudePrimary")
        self._dcPhaseCOM: COMFloatStatusParameter = aGetParameter(datachannelpath + "PhasePrimary")

    @property
    def RetractDistance(self) -> float:
        return self._retractDistanceCOM.Value

    @RetractDistance.setter
    def RetractDistance(self, value: float):
        self._retractDistanceCOM.Value = value

    def StartApproach(self):
        self._startCOM.ExecuteTrigger()

    def RetractTip(self):
        self._retractTipCOM.ExecuteTrigger()

    @property
    def Setpoint(self) -> float:
        return self._setpointCOM.Value

    @Setpoint.setter
    def Setpoint(self, value: float):
        self._setpointCOM.Value = value

    @property
    def PGain(self) -> float:
        return self._pGainCOM.Value

    @PGain.setter
    def PGain(self, value: float):
        self._pGainCOM.Value = value
    
    @property
    def IGain(self) -> float:
        return self._iGainCOM.Value

    @IGain.setter
    def IGain(self, value: float):
        self._iGainCOM.Value = value

    @property
    def DrivingAmplitude(self) -> float:
        return self._drivingAmpCOM.Value

    @DrivingAmplitude.setter
    def DrivingAmplitude(self, value: float):
        self._drivingAmpCOM.Value = value

    @property
    def DrivingFrequency(self) -> float:
        return self._drivingFreqCOM.Value

    @DrivingFrequency.setter
    def DrivingFrequency(self, value: float):
        self._drivingFreqCOM.Value = value

    def AutoResonance(self):
        self._autoResonanceCOM.ExecuteTrigger()

    @property
    def SumSignal(self) -> float:
        return self._dcSumCOM.Value
    
    @property
    def TopMinusBottom(self) -> float:
        return self._dcTMBCOM.Value
    
    @property
    def LeftMinusRight(self) -> float:
        return self._dcLMRCOM.Value
    
    @property
    def Amplitude(self) -> float:
        return self._dcAmplCOM.Value
    
    @property
    def Phase(self) -> float:
        return self._dcPhaseCOM.Value