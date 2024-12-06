from typing import Callable
from WITecSDK.Parameters import COMStringStatusParameter

class WITecControlVersionTester:

    def __init__(self, aGetParameter: Callable):
        self._programVersionCOM: COMStringStatusParameter = aGetParameter("Status|Software|Application|ProgramVersion")
        # Could be i.e. "WITec Control, 6.2 Develop, Build: 6.02.3.4"
        self.Version: float = float(self.StringVersion.split(", ")[1].split(" ")[0])
        # Create IsVersionGreater... attributes
        versions: list[float,...] = [5.1, 5.2, 5.3, 6.0, 6.1, 6.2, 7.0, 7.1]
        isversions: list[bool,...] = [(str(int(ver * 10)), self.Version >= ver) for ver in versions]
        for verstr, isver in isversions:
            setattr(self, 'IsVersionGreater' + verstr, isver)
    
    @property
    def StringVersion(self) -> str:
        return self._programVersionCOM.Value