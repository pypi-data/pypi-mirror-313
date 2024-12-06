from WITecSDK.Parameters.COMParameterBase import COMParameterBase
from WITecSDK.Parameters.COMClient import IUnknown, IBUCSStatusContainer, CheckConnection

def update(GetFunc):
    
    def wrapper(self: "COMStatusParameter"):
        self.Update()
        *args, res = GetFunc(self)
        if not res:
            raise Exception('Reading status parameter ' + self.GetName() + ' was not successful. Result: ' + str(res))
        if len(args) == 1:
            return args[0]
        else:
            return (*args,)
    
    return wrapper


class COMStatusParameter(COMParameterBase):

    def __init__(self, aDefaultInterface: IUnknown):
        self.modifier = aDefaultInterface.QueryInterface(IBUCSStatusContainer)
        super().__init__()

    @CheckConnection
    def Update(self):
        self.modifier.Update()
    
    @property
    @update
    @CheckConnection
    def StatusProperties(self) -> tuple[str, str]:
        # returns caption, unit
        return self.modifier.GetStatusProperties()


class COMStringStatusParameter(COMStatusParameter):

    @property
    @update
    @CheckConnection
    def Value(self) -> str:
        return self.modifier.GetSingleValueAsString()


class COMIntStatusParameter(COMStatusParameter):

    @property
    @update
    @CheckConnection
    def Value(self) -> int:
        return self.modifier.GetSingleValueAsInt()


class COMFloatStatusParameter(COMStatusParameter):
    
    @property
    @update
    @CheckConnection
    def Value(self) -> float:
        return self.modifier.GetSingleValueAsDouble()


class COMBoolStatusParameter(COMIntStatusParameter):
    
    @property
    def Value(self) -> bool:
        return super().Value != 0


class COMArrayStatusParameter(COMStatusParameter):
    
    @property
    @update
    @CheckConnection
    def Value(self) -> tuple[int, tuple[int,...]|None, tuple]:
        return self.modifier.GetStatusArray()