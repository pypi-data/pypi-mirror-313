from typing import Callable
from WITecSDK.Parameters import COMBoolParameter, COMFloatParameter, COMEnumParameter, COMTriggerParameter, COMIntParameter
from WITecSDK.Modules.BeamPath import BaseDevice, AutomatedCoupler
from WITecSDK.Modules.SlowTimeSeriesBase import SlowSeriesBase
from WITecSDK.Modules.HelperStructs import microscopecontrol

parampath = microscopecontrol + "OpticControl|"

class Polarization:
    """Implements the polarization features as five subclasses"""

    def __init__(self, aGetParameter: Callable):
        self.Polarizer = Polarizer(aGetParameter)
        self.Analyzer = Analyzer(aGetParameter)
        self.Syncron = Syncron(aGetParameter)
        self.Lambda4 = Lambda4(aGetParameter)
        self.Series = PolarizationSeries(aGetParameter)


class Polarizer(BaseDevice):
    """Gives access to the motorized polarizer"""

    _defparam: str = parampath + "Selected|Polarizer"
            
    def __init__(self, aGetParameter: Callable):
        self._polarizerCOM: COMFloatParameter = self._initCOM
        self._isPolarizerSelectedCOM: COMBoolParameter = aGetParameter(parampath + "Selected|IsPolarizerSelected")
        
    @property
    def Angle(self) -> float:
        """Defines the polarizer angle"""
        return self._polarizerCOM.Value

    @Angle.setter
    def Angle(self, value: float):
        self._polarizerCOM.Value = value

    @property
    def IsSelected(self) -> bool:
        """True if current selected laser has an polarizer"""
        return self._isPolarizerSelectedCOM.Value


class Analyzer(BaseDevice):
    """Gives access to the motorized analyzer"""

    _defparam: str = parampath + "Analyzer"
            
    def __init__(self, aGetParameter: Callable):
        self._analyzerCOM: COMFloatParameter = self._initCOM
        self.AnalyzerCoupler = AutomatedCoupler(aGetParameter, parampath + "AnalyzerCoupler")

    @property
    def Angle(self) -> float:
        """Defines the analyzer angle"""
        return self._analyzerCOM.Value

    @Angle.setter
    def Angle(self, value: float):
        self._analyzerCOM.Value = value


class Syncron(BaseDevice):
    """Gives access to the synchronized angle"""

    _defparam: str = parampath + "AnalyzerPolarizerMovingSynchron"
            
    def __init__(self, aGetParameter: Callable):
        self._anaPolSynchronCOM: COMBoolParameter = self._initCOM
        self._anaPolAngleDifferenceCOM: COMFloatParameter = aGetParameter(parampath + "AnalyzerPolarizerAngleDifference")

    @property
    def Enabled(self) -> bool:
        """Enables the synchronized angle between polarizer and analyzer"""
        return self._anaPolSynchronCOM.Value

    @Enabled.setter
    def Enabled(self, value: bool):
        self._anaPolSynchronCOM.Value = value

    @property
    def AngleDifference(self) -> float:
        """Defines the angle difference between polarizer and analyzer"""
        return self._anaPolAngleDifferenceCOM.Value

    @AngleDifference.setter
    def AngleDifference(self, value: float):
        self._anaPolAngleDifferenceCOM.Value = value


class Lambda4(BaseDevice):
    """Gives access to the Lamda/4 control"""

    _defparam: str = parampath + "Selected|PolarizerIsLambda4Coupled"
            
    def __init__(self, aGetParameter: Callable):
        self._isPolarizerLambda4COM: COMBoolParameter = self._initCOM
        self._polarizerLambda4ModeCOM: COMEnumParameter = aGetParameter(parampath + "Selected|PolarizerLambda4Mode")
    
    @property
    def Enabled(self) -> bool:
        """Enables the use of the Lambda/4 feature"""
        return self._isPolarizerLambda4COM.Value
    
    @property
    def Mode(self) -> int:
        """Defines the mode of the Lambda/4"""
        return self._polarizerLambda4ModeCOM.Value

    @Mode.setter
    def Mode(self, unit: int):
        self._polarizerLambda4ModeCOM.Value = unit

    def GetModes(self) -> dict:
        """Returns all available modes"""
        return self._polarizerLambda4ModeCOM.AvailableValues


class PolarizationSeries(SlowSeriesBase):
    """Implements the polarization series"""

    def __init__(self, aGetParameter: Callable):
        super().__init__(aGetParameter)
        self._numberOfPolarizerValuesCOM: COMIntParameter = aGetParameter(self._parampath + "PolarizerSeries|NumberOfPolarizerValues")
        self._startPolarizerSeriesCOM: COMTriggerParameter = aGetParameter(self._parampath + "PolarizerSeries|StartPolarizerSeries")
        self._numberOfAnalyzerValuesCOM: COMIntParameter = aGetParameter(self._parampath + "AnalyzerSeries|NumberOfAnalyzerValues")
        self._startAnalyzerSeriesCOM: COMTriggerParameter = aGetParameter(self._parampath + "AnalyzerSeries|StartAnalyzerSeries")

    @property
    def StepsPolarizerSeries(self) -> int:
        """Defines the number of steps for 360 ° rotation for the polarizer series"""
        return self._numberOfPolarizerValuesCOM.Value

    @StepsPolarizerSeries.setter
    def StepsPolarizerSeries(self, value: int):
        self._numberOfPolarizerValuesCOM.Value = value

    @property
    def StepsAnalyzerSeries(self) -> int:
        """Defines the number of steps for 360 ° rotation for the analyzer series"""
        return self._numberOfAnalyzerValuesCOM.Value

    @StepsAnalyzerSeries.setter
    def StepsAnalyzerSeries(self, value: int):
        self._numberOfAnalyzerValuesCOM.Value = value

    def StartPolarizerSeries(self):
        """Starts the polarizer series"""
        self._startPolarizerSeriesCOM.ExecuteTrigger()

    def StartAnalyzerSeries(self):
        """Starts the analyzer series"""
        self._startAnalyzerSeriesCOM.ExecuteTrigger()