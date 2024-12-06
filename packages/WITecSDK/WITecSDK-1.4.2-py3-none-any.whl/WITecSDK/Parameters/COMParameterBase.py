from WITecSDK.Parameters.COMClient import COMAccessInterface, IBUCSSubSystemInfo, IBUCSSingleValue, IUnknown, CheckConnection

class COMParameterBase(COMAccessInterface):

    modifier = None
    subsysinfo = None

    def __init__(self):
        self.subsysinfo: IBUCSSubSystemInfo = self.modifier.QueryInterface(IBUCSSubSystemInfo)
        super().__init__(self.modifier)

    @property
    @CheckConnection
    def Name(self) -> str:
        return self.subsysinfo.GetName()

    @property
    @CheckConnection
    def Enabled(self) -> bool:
        return self.subsysinfo.GetEnabled()       
    
    def _throwExceptionIfNoWriteAccess(self):
        if not self.Enabled:
            raise ParameterDisabledException('Parameter ' + self.Name + ' is disabled.')
        if not self.WriteAccess:
            raise NoWriteAccessException('No write access granted to perform an action on parameter ' + self.Name + '.')
    
    def __del__(self):
        if self.modifier is not None:
            self.modifier.Release()
            self.subsysinfo.Release()


class COMSingleValueParameter(COMParameterBase):

    singleval = None

    def __init__(self):
        self.singleval = self.modifier.QueryInterface(IBUCSSingleValue)
        super().__init__()

    @property
    @CheckConnection
    def DisplayName(self) -> str:
        return self.singleval.GetDisplayName()

    def __del__(self):
        if self.singleval is not None:
            self.singleval.Release()
        super().__del__()


class COMBoolStringIntFloatParameter(COMSingleValueParameter):

    @property
    @CheckConnection
    def Value(self) -> bool|str|int|float:
        return self.modifier.GetValue()
    
    @CheckConnection
    def _SetValue(self, aValue: bool|str|int|float):
        self._throwExceptionIfNoWriteAccess()
        self.modifier.SetValue(aValue)


class NoWriteAccessException(Exception):
    pass

class ParameterDisabledException(Exception):
    pass
