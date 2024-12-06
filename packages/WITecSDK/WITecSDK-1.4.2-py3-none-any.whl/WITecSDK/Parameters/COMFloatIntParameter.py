from WITecSDK.Parameters.COMParameterBase import COMBoolStringIntFloatParameter
from WITecSDK.Parameters.COMClient import IUnknown, IBUCSFloat, IBUCSInt, IBUCSFloatMinMaxValues, IBUCSIntMinMaxValues, IBUCSSingleValueHasLimits, CheckConnection

class COMFloatIntParameter(COMBoolStringIntFloatParameter):

    hasLimits = None
    rangevals = None

    def __init__(self):
        self.hasLimits = self.modifier.QueryInterface(IBUCSSingleValueHasLimits)
        self.limits = self.HasLimits
        super().__init__()

    def _SetValue(self, aValue: float|int):
        range = self.Range
        if self.limits[0] and range[0] > aValue:
            raise ValueOutOfRangeException(f'Value {aValue} is smaller than {self.Range[0]}')
        if self.limits[1] and range[1] < aValue:
            raise ValueOutOfRangeException(f'Value {aValue} is bigger than {self.Range[1]}')
        super()._SetValue(aValue)

    @property
    @CheckConnection
    def Range(self) -> tuple[float|int, float|int]:
        minval = self.rangevals.GetMinimum()
        maxval = self.rangevals.GetMaximum()
        return minval, maxval
    
    @property
    @CheckConnection
    def HasLimits(self) -> tuple[bool, bool]:
        minlim = self.hasLimits.HasMinimum()
        maxlim = self.hasLimits.HasMaximum()
        return minlim, maxlim
        
    def __del__(self):
        if self.hasLimits is not None:
            self.hasLimits.Release()
            self.rangevals.Release()
        super().__del__()


class COMFloatParameter(COMFloatIntParameter):

    def __init__(self, aDefaultInterface: IUnknown):
        self.modifier = aDefaultInterface.QueryInterface(IBUCSFloat)
        self.rangevals = self.modifier.QueryInterface(IBUCSFloatMinMaxValues)
        super().__init__()

    @property
    def Value(self) -> float:
        return super().Value

    @Value.setter
    def Value(self, aValue: float):
        super()._SetValue(aValue)

    @property
    def Range(self) -> tuple[float, float]:
        return super().Range


class COMIntParameter(COMFloatIntParameter):
    
    def __init__(self, aDefaultInterface: IUnknown):
        self.modifier = aDefaultInterface.QueryInterface(IBUCSInt)
        self.rangevals = self.modifier.QueryInterface(IBUCSIntMinMaxValues)
        super().__init__()

    @property
    def Value(self) -> int:
        return super().Value

    @Value.setter
    def Value(self, aValue: int):
        super()._SetValue(aValue)

    @property
    def Range(self) -> tuple[int, int]:
        return super().Range
    

class ValueOutOfRangeException(Exception):
    pass