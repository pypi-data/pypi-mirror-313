"""Handles the different parameter types used by WITec Control"""

from typing import Callable
from WITecSDK.Parameters.COMClient import COMCoreInterface, IUnknown
from WITecSDK.Parameters.COMParameter import COMBoolParameter, COMStringParameter, COMTriggerParameter
from WITecSDK.Parameters.COMEnumParameter import COMEnumParameter
from WITecSDK.Parameters.COMFloatIntParameter import COMFloatParameter, COMIntParameter
from WITecSDK.Parameters.COMStatusParameter import (COMIntStatusParameter, COMBoolStatusParameter, COMFloatStatusParameter,
                                                    COMStringStatusParameter, COMArrayStatusParameter, COMStatusParameter)
from WITecSDK.Parameters.COMFillStatusParameter import COMStringFillStatusParameter, COMFloatFillStatusParameter

IIDToParamClass = {
    "EFAE9411-A8E0-461D-A5F4-4887595AA830":COMIntParameter,
    "08862E7F-BE29-4DCF-B2FC-55A3DFAE33F7":COMBoolParameter,
    "3EBB7227-74F9-4A0D-9AC9-7E3327AB5221":COMFloatParameter,
    "923FC802-04D3-4BEE-AE63-A349051FE2E8":COMTriggerParameter,
    "90C0EA65-0483-46BB-80FD-B1B536D73FC4":COMStringParameter,
    "CC1BD98A-2D74-4242-B5F9-0288FC58E339":COMEnumParameter,
    "5CAF623C-976F-46DC-9624-2F685B00D293":COMStatusParameter
}

TypeToStatusParamClass = {
    "int":COMIntStatusParameter,
    "bool":COMBoolStatusParameter,
    "float":COMFloatStatusParameter,
    "string":COMStringStatusParameter,
    "uint[2]":COMArrayStatusParameter
}

TypeToFillStatusParamClass = {
    "float":COMFloatFillStatusParameter,
    "string":COMStringFillStatusParameter
}

class SubSys():
    """Stores information about one SubSystem"""
    IID: str
    Type: str
    Path: str
    ParamClass = None
    _instance = None

    def __init__(self, aGetDefI: Callable, aIID: str, aParamDescription: str):
        """Extracts the type of the SubSystem"""
        self.GetDefaultInterface = aGetDefI
        self.IID = aIID
        self.Type, self.Path = aParamDescription.split(':', 1)
        self.ParamClass = IIDToParamClass.get(self.IID)
        if self.ParamClass is COMStatusParameter:
            if self.Path.startswith("Status|Software|Sequencers|SequencerTimeSeriesSlow|"):
                self.ParamClass = TypeToFillStatusParamClass.get(self.Type.lower())
            else:
                self.ParamClass = TypeToStatusParamClass.get(self.Type.lower())

    @property
    def Instance(self):
        """Creates and gives back an instance of the parameter"""
        if self._instance is None:
            try:
                defInterface: IUnknown = self.GetDefaultInterface(self.Path)
            except Exception as e:
                raise ParameterNotAvailableException("Parameter Not Available: " + self.Path) from e
            self._instance = self.ParamClass(defInterface)
        return self._instance


class COMParameters(COMCoreInterface):
    """Creates the different parameter types and checks type and existence
    by using IBUCSSubSystemsList"""

    AllParams: dict[str,SubSys] = {}

    def __init__(self, aServerName: str):
        """Creates and stores a dictonary with all available parameters"""
        
        super().__init__(aServerName)
        self.GetAllParameters()

    def GetAllParameters(self):
        """Creates a dictonary with all available parameters"""

        subSystemsList = self.GetSubSystemsList(None,5) #unsorted
        for parameterDescription, IID in subSystemsList.SubSystemsNameAndIIdList:
            if not IID.startswith("000"):
                subSys = SubSys(self.GetSubSystemDefaultInterface, IID, parameterDescription)
                self.AllParams[subSys.Path] = subSys

    def GetParameter(self, aParameter: str) -> (COMTriggerParameter|COMBoolParameter|COMIntParameter|
                                                COMFloatParameter|COMStringParameter|COMEnumParameter|
                                                COMBoolStatusParameter|COMIntStatusParameter|COMFloatStatusParameter|
                                                COMFloatFillStatusParameter|COMStringFillStatusParameter):
        """Creates a parameter or status parameter of the regarding type"""

        param = self.AllParams.get(aParameter)
        if param is None:
            raise ParameterNotAvailableException(f"The COM-Parameter {aParameter} is not available.")
        return param.Instance


class ParameterNotAvailableException(Exception):
    pass