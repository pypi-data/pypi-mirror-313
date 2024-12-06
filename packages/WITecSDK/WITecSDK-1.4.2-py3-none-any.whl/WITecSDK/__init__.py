"""This package simplifies to access the COM interface of WITec Control.

It is downwards compatible with WITec Control versions older than the
current release. Ready-to-use classes are offered for most common
measurement modes.

Typical usage example:
    
    from WITecSDK import WITecSDKClass
    WITec = WITecSDKClass()
"""

from WITecSDK.Parameters import COMParameters
from WITecSDK.Modules import (WITecModules, LaserInformation, AutofocusSettings, DataChannelDescription,
                              SamplePositionerPosition, XYZPosition, LargeAreaSettings)
from socket import gethostname
from asyncio import sleep
from importlib.metadata import version

__version__: str = version('WITecSDK')

class WITecSDKClass(WITecModules):
    """Main class that connects to WITec Control and could create
    classes for the measurement modes."""

    def __init__(self, aServerName: str = gethostname()):
        """Initializes an instance of the class and allows to connect to WITec
        Control running on a remote computer. By default the localhost is used."""

        print(f"WITecSDK {__version__} connects to {aServerName} from {gethostname()}")
        self.comParameters = COMParameters(aServerName)
        super().__init__()
        print(self._versionTester.StringVersion)
    
    def RequestWriteAccess(self) -> bool:
        """Requests write access from WITec Control and returns success as boolean.
        Precondition:
            WITec Control must allow Remote Write Access
            (Control-Form, Parameter: COM Automation -> Allow Remote Access)"""

        self.comParameters.WriteAccess = True
        return self.comParameters.WriteAccess

    def ReleaseWriteAccess(self):
        """Returns write access to WITec Control."""

        self.comParameters.WriteAccess = False

    @property
    def HasReadAccess(self) -> bool:
        """Checks for read access."""

        return self.comParameters.ReadAccess
    
    @property
    def HasWriteAccess(self) -> bool:
        """Checks for write access."""

        return self.comParameters.WriteAccess

    async def WaitForWriteAccess(self):
        """Waits until COM Automation button in WITec Control is pressed"""
        print('Requesting write access')
        while not self.RequestWriteAccess():
            sleep(0.5)