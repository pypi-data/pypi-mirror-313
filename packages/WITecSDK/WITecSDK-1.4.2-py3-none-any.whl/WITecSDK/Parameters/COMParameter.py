from WITecSDK.Parameters.COMParameterBase import COMParameterBase, COMBoolStringIntFloatParameter, CheckConnection
from WITecSDK.Parameters.COMClient import IUnknown, IBUCSBool, IBUCSString, IBUCSTrigger

class COMBoolParameter(COMBoolStringIntFloatParameter):

    def __init__(self, aDefaultInterface: IUnknown):
        self.modifier = aDefaultInterface.QueryInterface(IBUCSBool)
        super().__init__()

    @property
    def Value(self) -> bool:
        return super().Value

    @Value.setter
    def Value(self, aValue: bool):
        super()._SetValue(aValue)


class COMStringParameter(COMBoolStringIntFloatParameter):
    
    def __init__(self, aDefaultInterface: IUnknown):
        self.modifier = aDefaultInterface.QueryInterface(IBUCSString)
        super().__init__()

    @property
    def Value(self) -> str:
        return super().Value

    @Value.setter
    def Value(self, aValue: str):
        super()._SetValue(aValue)


class COMTriggerParameter(COMParameterBase):

    def __init__(self, aDefaultInterface: IUnknown):
        self.modifier = aDefaultInterface.QueryInterface(IBUCSTrigger)
        super().__init__()

    @CheckConnection
    def ExecuteTrigger(self):
        self._throwExceptionIfNoWriteAccess()
        self.modifier.OperateTrigger()