from WITecSDK.Parameters import SubSys
from WITecSDK.Modules.HelperStructs import datachannelpath

class ParameterNameGetter:
    """This class lists all available parameter on the system"""

    def __init__(self, aAllParams: dict[str,SubSys]):
        self._parameters: dict[str, SubSys] = aAllParams

    def GetNamesOfAvailableParameters(self, startstr: str = "") -> list[str]:
        """Returns all available parameters as list
        The optional string filters for all parameters starting with it"""
        parameterNames = []
        for key, value in self._parameters.items():
            if key.startswith(startstr):
                parameterNames.append(value.Type + ':' + key)
        return parameterNames
    
    def GetNamesOfAvailableDataChannels(self) -> list[str]:
        """Returns only data channels as list"""
        return self.GetNamesOfAvailableParameters(datachannelpath)

    def WriteParameterNamesToFile(self, filePath: str, startstr: str = ""):
        """Write all available parameters to the file defined by filePath
        The optional string filters for all parameters starting with it"""
        self._writeListToFile(filePath, self.GetNamesOfAvailableParameters(startstr))
    
    def WriteDataChannelsToFile(self, filePath: str):
        """Write only data channels to the file defined by filePath"""
        self._writeListToFile(filePath, self.GetNamesOfAvailableDataChannels())

    @staticmethod
    def _writeListToFile(filePath: str, paramlist: list[str]):
        with open(filePath, 'w') as f:
            f.write('\n'.join(x for x in paramlist))
