"""This COM client uses comtypes to communicate with the COM server (WITec Control)"""

from comtypes.client import GetModule, CreateObject
from _ctypes import COMError

class LibraryNotFoundException (Exception):
    pass

bucstlb_id = '{E84FEF4C-DD2F-4B8D-9C2F-D016FEBB01F4}'
try:
    GetModule((bucstlb_id, 1, 0))
except OSError as e:
    if e.winerror == -2147319779:
        #OSError: [WinError -2147319779] Library not registered
        raise LibraryNotFoundException("BasicUniversalCOMServerLib not found. Install COM Add-On")
    else:
        raise e
except Exception as e:
    raise e

from comtypes.gen.BasicUniversalCOMServerLib import (IUnknown, CBUCSCore, IBUCSCore, IBUCSAccess, IBUCSSubSystemsList, IBUCSStatusContainer, IBUCSTrigger,
                                                     IBUCSSingleValueHasLimits, IBUCSBool, IBUCSEnum, IBUCSFillStatus, IBUCSFloat, IBUCSFloatMinMaxValues,
                                                     IBUCSInt, IBUCSIntMinMaxValues, IBUCSString, IBUCSSubSystemInfo, IBUCSSingleValue)

from WITecSDK.Parameters.COMSubSystemsList import COMSubSystemsList


def CheckConnection(func):
    
    def wrapper(self, *args):
        try:
            return func(self, *args)
        except COMError as e:
            serverName = ""
            if isinstance(self, COMCoreInterface):
                serverName = self.ServerName
            if e.hresult == -2147023174 or e.hresult == -2147023170:
                #The RPC server is unavailable or The remote procedure call failed.
                raise ConnectionLostException(serverName, "Connection to WITec Control lost")
            elif e.hresult == -2147467259 and e.details[0].startswith("No callback function pointer registered"):
                #No callback function pointer registered for getting the default interface for a Sub-System Name
                raise ConnectionLostException(serverName, "WITec Control disconnects")
            else:
                raise e
        except Exception as e:
            raise e
    
    return wrapper


class COMAccessInterface:
    """This class implements the IBUCSAccess interface"""
    
    _accessInterface: IBUCSAccess = None
    
    def __init__(self, modifier):
        self._accessInterface = modifier.QueryInterface(IBUCSAccess)

    @property
    @CheckConnection
    def ReadAccess(self) -> bool:
        """Checks for read access over IBUCSAccess"""

        return self._accessInterface.HasReadAccess()
    
    @property
    @CheckConnection
    def WriteAccess(self) -> bool:
        """Checks/Requests write access over IBUCSAccess"""

        return self._accessInterface.HasWriteAccess()
    
    @WriteAccess.setter
    @CheckConnection
    def WriteAccess(self, value: bool):
        if self.WriteAccess != value:
            self._accessInterface.RequestWriteAccess(value)
            if self.WriteAccess:
                print("WITec COM Client write access granted")
            elif not value:
                print("WITec COM Client write access released")


class COMCoreInterface(COMAccessInterface):
    """This class implements the IBUCSCore interface"""
    
    _wcCoreInterface: IBUCSCore = None
    
    def __init__(self, aServerName: str):
        """Accepts a server name of a remote PC in case WITec Control
        doesn't run on the same computer (refer to help)"""

        self.ServerName = aServerName

        try:
            self._wcCoreInterface = CreateObject(CBUCSCore, interface = IBUCSCore, machine = self.ServerName)
        except OSError as e:
            if e.winerror == -2147023174:
                #OSError: [WinError -2147023174] The RPC server is unavailable
                raise COMClientException(self.ServerName, "The remote server is not avilable.")
            elif e.winerror == -2147221164 or e.winerror == -2147024891:
                #OSError: [WinError -2147221164] Class not registered
                #PermissionError: [WinError -2147024891] Access is denied
                raise COMClientException(self.ServerName, "WITec Control is not running.")
            else:
                raise e
        except Exception as e:
            raise COMClientException(self.ServerName, "Could not instantiate an Object of the Core Interface class.") from  e
        
        if self._wcCoreInterface is None:
            raise COMClientException(self.ServerName, "Create Object of IBUCSCore returned null")
        
        print("WITec COM Client connected")
        super().__init__(self._wcCoreInterface)
        
    @CheckConnection
    def GetSubSystemsList(self, aName: str|None, aSubSystemsDepth: int) -> COMSubSystemsList:
        """Implements GetSubSystemsList of IBUCSCore interface"""

        return COMSubSystemsList(self._wcCoreInterface.GetSubSystemsList(aName, aSubSystemsDepth))
    
    @CheckConnection
    def GetSubSystemDefaultInterface(self, aParameter: str):
        """Implements GetSubSystemDefaultInterface of IBUCSCore interface"""
        
        try:
            return self._wcCoreInterface.GetSubSystemDefaultInterface(aParameter)
        except COMError as e:
            if e.hresult == -2147467259 and e.details[1].startswith("Invalid Class-ID"):
                #Invalid Class-ID (GUID_NULL) for Sub-System
                raise InvalidSubSystemException(self.ServerName, "SubSystem not found: " + aParameter)
            else:
                raise e
        except Exception as e:
            raise e
    
    def __del__(self):
        if self._wcCoreInterface is not None:
            try:
                self.WriteAccess = False
            except ConnectionLostException:
                pass
            except Exception as e:
                raise e
            
            self._accessInterface.Release()
            self._wcCoreInterface.Release()
            print("WITec COM Client disconnected")


class COMClientException(Exception):

    def __init__(self, serverName: str, message: str):
        super().__init__(serverName + ": " + message)

class ConnectionLostException(COMClientException):
    pass

class InvalidSubSystemException(COMClientException):
    pass

"""self._wcCoreInterface.GetSubSystemDefaultInterface(aParameter)

_ctypes.COMError: (-2147467259, 'Unspecified error', ('No callback function pointer registered for getting the default interface for a Sub-System Name', 'WITec.COMAutomation', None, 0, None))

_ctypes.COMError: (-2147467259, 'Unspecified error', ('Invalid Class-ID (GUID_NULL) for Sub-System with name: UserParameters|Naming', 'WITec.COMAutomation', None, 0, None))

_ctypes.COMError: (-2147023174, 'The RPC server is unavailable.', (None, None, None, 0, None))

_ctypes.COMError: (-2147023170, 'The remote procedure call failed.', (None, None, None, 0, None))"""