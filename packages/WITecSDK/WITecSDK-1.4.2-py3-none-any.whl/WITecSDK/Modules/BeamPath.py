from typing import Callable
from WITecSDK.Parameters import COMStringParameter, COMTriggerParameter, COMBoolParameter, COMEnumParameter, ParameterNotAvailableException
from WITecSDK.Parameters.COMParameterBase import NoWriteAccessException
from WITecSDK.Modules.HelperStructs import userparam, microscopecontrol

class BeamPath:
    """Gives access to the beampath control"""
    
    _preventIdleState = False
    _parampath = microscopecontrol + "BeamPath|"
    CalibrationLamp = None
    
    def __init__(self, aGetParameter: Callable):
        self._stateCOM: COMStringParameter = aGetParameter(self._parampath + "State")
        self._setStateAllOffCOM: COMTriggerParameter = aGetParameter(self._parampath + "SetStateAllOff")
        self._setStateVideoCOM: COMTriggerParameter = aGetParameter(self._parampath + "SetStateVideo")
        self._setStateRamanCOM: COMTriggerParameter = aGetParameter(self._parampath + "SetStateRaman")
        self._stateOnIdleCOM: COMStringParameter = aGetParameter(userparam + "MicroscopeStateOnIdle")
        self.AdjustmentSampleCoupler = AutomatedCoupler(aGetParameter, microscopecontrol + "AdjustmentSampleCoupler|State")
        self._initialIdleState = self._stateOnIdleCOM.Value

    @property
    def State(self) -> str:
        """Retrieves the current beampath state"""
        return self._stateCOM.Value

    def SetAllOff(self):
        """Takes everything out of the beampath"""
        self._setStateAllOffCOM.ExecuteTrigger()

    def SetVideo(self):
        """Configures the beampath for getting the video image"""
        self._setStateVideoCOM.ExecuteTrigger()

    def SetRaman(self):
        """Configures the beampath for doing Raman measurements"""
        self._setStateRamanCOM.ExecuteTrigger()

    @property
    def PreventIdleState(self) -> bool:
        """Removes the idle state entry
        Is valid until the configuration is reloaded"""
        return self._preventIdleState

    @PreventIdleState.setter
    def PreventIdleState(self, value: bool):
        if value:
            self._stateOnIdleCOM.Value = ""
        else:
            self._stateOnIdleCOM.Value = self._initialIdleState
        self._preventIdleState = value

    def __del__(self):
        try:
            if self.PreventIdleState:
                self.PreventIdleState = False
        except NoWriteAccessException:
            print("Not possible to restore initial Idle State. Reload configuration to fix.")


class BeamPath51(BeamPath):
    """Extension of the BeamPath class for version 5.1 and higher"""
    
    def __init__(self, aGetParameter: Callable):
        super().__init__(aGetParameter)
        self._setStateWhiteLightMeasurementCOM: COMTriggerParameter  = aGetParameter(self._parampath + "SetStateWhiteLightMeasurement")


    def SetWhiteLightMeasurement(self):
        """Configures the beampath for doing whitelight spectroscopy"""
        self._setStateWhiteLightMeasurementCOM.ExecuteTrigger()


class BaseDevice:
    """Base class for automated couplers"""

    _defparam: str

    def __new__(cls, aCreateParam: callable):
        try:
            initCOM = aCreateParam(cls._defparam)
        except ParameterNotAvailableException:
            return None
        except Exception as e:
            raise e
        else:
            devInstance = super().__new__(cls)
            devInstance._initCOM = initCOM
            return devInstance


class AutomatedCoupler(BaseDevice):
    """Controls an automated coupler"""

    _defparam: str

    def __new__(cls, aGetParameter: Callable, aCouplerPath: str):
        cls._defparam = aCouplerPath
        return super().__new__(cls, aGetParameter)
    
    def __init__(self, aGetParameter: Callable, aCouplerPath: str):
        self._CouplerCOM: COMBoolParameter = self._initCOM

    @property
    def Coupled(self) -> bool:
        """State of the coupler, True if coupled in"""
        return self._CouplerCOM.Value
    
    @Coupled.setter
    def Coupled(self, state: bool):
        self._CouplerCOM.Value = state


class CalibrationCoupler(BaseDevice):
    """Class for an automated calibration coupler"""

    _defparam: str = "MultiComm|MicroscopeControl|CalibrationLamp|State"

    def __init__(self, aGetParameter: Callable):
        self._StateCOM: COMEnumParameter = self._initCOM

    @property
    def State(self) -> int:
        """State of the coupler"""
        return self._StateCOM.Value

    @property
    def StateValues(self) -> dict:
        return self._StateCOM.AvailableValues


class CalibrationCoupler62(CalibrationCoupler):
    """Extension of the CalibrationCoupler class for version 6.2 and higher"""

    def __init__(self, aGetParameter: Callable):
        super().__init__(aGetParameter)
        self._isPermanentlyOnCOM: COMBoolParameter = aGetParameter("MultiComm|MicroscopeControl|CalibrationLamp|IsPermanentlyOn")

    @property
    def IsPermanentlyOn(self) -> bool:
        """If True the calibration coupler is coupled independend from the beampath state"""
        return self._isPermanentlyOnCOM.Value
    
    @IsPermanentlyOn.setter
    def IsPermanentlyOn(self, value: bool):
        self._isPermanentlyOnCOM.Value = value