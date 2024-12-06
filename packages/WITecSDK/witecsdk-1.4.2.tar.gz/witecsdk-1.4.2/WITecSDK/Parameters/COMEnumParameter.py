from WITecSDK.Parameters.COMParameterBase import COMSingleValueParameter
from WITecSDK.Parameters.COMClient import IUnknown, IBUCSEnum, CheckConnection

class COMEnumParameter(COMSingleValueParameter):

    def __init__(self, aDefaultInterface: IUnknown):
        self.modifier = aDefaultInterface.QueryInterface(IBUCSEnum)
        super().__init__()

    @property
    @CheckConnection
    def EnumValue(self) -> tuple[str, int]:
        value = self.modifier.GetValue()
        return value
    
    @property
    def Value(self) -> int:
        value = self.EnumValue
        return value[1]
    
    @Value.setter
    @CheckConnection
    def Value(self, aEnumIndex: int):
        self._throwExceptionIfNoWriteAccess()
        self.modifier.SetValueNumeric(aEnumIndex)
    
    @property
    def StringValue(self) -> str:
        value = self.EnumValue
        return value[0]

    @property
    @CheckConnection
    def AvailableValues(self) -> dict[int, str] | None:
        index, strings, numValues = self.modifier.GetAvailableValues()
        
        if index is None or strings is None:
            return None

        enumValues = {}
        for i in range(numValues):
            enumValues[index[i]] = strings[i]

        return enumValues
