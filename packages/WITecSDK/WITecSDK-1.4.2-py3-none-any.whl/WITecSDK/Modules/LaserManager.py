from typing import Callable
from WITecSDK.Parameters import COMIntParameter, COMTriggerParameter, COMFloatParameter, COMBoolParameter
from WITecSDK.Modules.HelperStructs import microscopecontrol

parampath = microscopecontrol + "Laser|"

class LaserInformation:
    """Class holding the information for one laser source"""
    def __init__(self, aPower: float, aWavelength: float, aHasShutter: bool, aHasFilter: bool):
        self.Power: float = aPower
        self.Wavelength: float = aWavelength
        self.HasShutter: bool = aHasShutter
        self.HasFilter: bool = aHasFilter


class LaserManager:
    """Gives access to the laser control"""

    def __init__(self, aGetParameter: Callable):
        self._numberOfLasersCOM: COMIntParameter = aGetParameter(parampath + "NumberOfLasers")
        self._selectNoLaserCOM: COMTriggerParameter = aGetParameter(parampath + "SelectNoLaser")
        self._laserPowerCOM: COMFloatParameter = aGetParameter(parampath + "Selected|Power")
        self._waveLengthCOM: COMFloatParameter = aGetParameter(parampath + "Selected|Wavelength")
        self._filterCOM: COMBoolParameter = aGetParameter(parampath + "Selected|Filter")
        self._shutterCOM: COMBoolParameter = aGetParameter(parampath + "Selected|Shutter")
        
        self.availableLasers: list[Laser] = []
        for i in range(self.NumberOfLasers):
            self.availableLasers.append(Laser(aGetParameter, i))

    def SelectLaser(self, LaserNo: int):
        """Switches to the laser defined by the Laser number"""
        if self.NumberOfLasers == 0:
            raise NoLaserAvailableException("No lasers available.")
        if LaserNo < 0 or LaserNo >= self.NumberOfLasers:
            raise LaserNotExistingException(f"Available lasers: {self.NumberOfLasers}, indexing 0 to {self.NumberOfLasers - 1}.")
        self.availableLasers[LaserNo].Select()

    def SelectNoLaser(self):
        """Selects no laser"""
        self._selectNoLaserCOM.ExecuteTrigger()

    @property
    def SelectedLaserInfo(self) -> LaserInformation:
        """Retrieves the information of the slected laser as LaserInformation class"""
        laserPower = self.SelectedLaserPower
        waveLength = self._waveLengthCOM.Value
        return LaserInformation(laserPower, waveLength, None, None)

    @property
    def SelectedLaserPower(self) -> float:
        """Defines the current laser power of the selected laser"""
        return self._laserPowerCOM.Value

    @SelectedLaserPower.setter
    def SelectedLaserPower(self, laserPower: float):
        self._laserPowerCOM.Value = laserPower

    @property
    def SelectedLaserShutterOpen(self) -> bool:
        """Defines the shutter status of the selected laser"""
        return self._shutterCOM.Value

    @SelectedLaserShutterOpen.setter
    def SelectedLaserShutterOpen(self, state: bool):
        self._shutterCOM.Value = state

    @property
    def SelectedLaserFilterIn(self) -> bool:
        """Defines the laser filter position of the selected laser (applies only to older input couplers)"""
        return self._filterCOM.Value

    @SelectedLaserFilterIn.setter
    def SelectedLaserFilterIn(self, state: bool):
        self._filterCOM.Value = state
    
    @property
    def NumberOfLasers(self) -> int:
        """Retrieves the number of lasers"""
        return self._numberOfLasersCOM.Value


class Laser:
    """Internal class used for each laser stored in the availableLasers list"""
    def __init__(self, aGetParameter, laserNo: int):
        self._laserSelectCOM: COMTriggerParameter = aGetParameter("MultiComm|MicroscopeControl|Laser|SelectLaser" + str(laserNo));

    def Select(self):
        """Selects the laser of this class instance"""
        self._laserSelectCOM.ExecuteTrigger()


class LaserManager52(LaserManager):
    """Extension of the LaserManager class for version 5.2 and higher"""

    def __init__(self, aGetParameter: Callable):
        super().__init__(aGetParameter)
        self._hasShutterCOM: COMBoolParameter = aGetParameter(parampath + "Selected|HasShutter")
        self._hasFilterCOM: COMBoolParameter = aGetParameter(parampath + "Selected|HasFilter")

    @property
    def SelectedLaserInfo(self) -> LaserInformation:
        """Retrieves the information of the slected laser as LaserInformation class"""
        laserinfo = super().SelectedLaserInfo
        laserinfo.HasShutter = self._hasShutterCOM.Value
        laserinfo.HasFilter = self._hasFilterCOM.Value
        return laserinfo


class LaserManager61(LaserManager52):
    """Extension of the LaserManager class for version 6.1 and higher"""

    def __init__(self, aGetParameter: Callable):
        super().__init__(aGetParameter)
        self._correctionFactorCOM: COMFloatParameter = aGetParameter(parampath + "Selected|PowerCorrectionFactor")

    @property
    def SelectedLaserPowerInFiber(self):
        """Defines the current laser power of the selected laser measured out of fiber (by deviding by the correction factor)"""
        correctionFactor = self._correctionFactorCOM.Value
        return super().SelectedLaserPower / correctionFactor
    
    @SelectedLaserPowerInFiber.setter
    def SelectedLaserPowerUncorrected(self, laserPower: float):
        correctionFactor = self._correctionFactorCOM.Value
        super().SelectedLaserPower = laserPower * correctionFactor


class NoLaserAvailableException(IndexError):
    pass

class LaserNotExistingException(IndexError):
    pass