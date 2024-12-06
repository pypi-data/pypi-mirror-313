from typing import Callable
from WITecSDK.Parameters import COMStringParameter

class ConfigurationLoader:
    """Gives access to the configuration of WITec Control"""

    def __init__(self, aGetParameter: Callable):
        self._loadConfigurationCOM: COMStringParameter = aGetParameter("ApplicationControl|LoadConfiguration")

    @property
    def Configuration(self) -> str:
        """Retrieves and sets the configuration of WITec Control"""
        return self._loadConfigurationCOM.Value

    @Configuration.setter
    def Configuration(self, configurationName):
        self._loadConfigurationCOM.Value = configurationName