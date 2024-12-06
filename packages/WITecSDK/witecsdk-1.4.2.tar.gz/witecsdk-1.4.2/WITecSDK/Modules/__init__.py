"""Modules containing classes for different measurement modes or
hardware control."""

from WITecSDK.Modules.ActiveSequencer import ActiveSequencer, ActiveSequencer60, ActiveSequencer62
from WITecSDK.Modules.AFM import AFM
from WITecSDK.Modules.ApertureFieldStop import ApertureFieldStop
from WITecSDK.Modules.ApplicationControl import ApplicationControl
from WITecSDK.Modules.AutoFocus import AutoFocus61, AutoFocus
from WITecSDK.Modules.BeamPath import BeamPath, BeamPath51, CalibrationCoupler, CalibrationCoupler62
from WITecSDK.Modules.ConfigurationLoader import ConfigurationLoader
from WITecSDK.Modules.DetectorOutput import DetectorOutput
from WITecSDK.Modules.DistanceCurve import DistanceCurve
from WITecSDK.Modules.EFMControl import EFMControl
from WITecSDK.Modules.FastTimeSeries import FastTimeSeries
from WITecSDK.Modules.Heating import Heating
from WITecSDK.Modules.Illumination import TopIllumination, BottomIllumination
from WITecSDK.Modules.ImageScan import ImageScan
from WITecSDK.Modules.ImageScanMultipass import ImageScanMultipass
from WITecSDK.Modules.LargeAreaScan import LargeAreaScan,LargeAreaScan62
from WITecSDK.Modules.LaserManager import LaserManager61, LaserManager52, LaserManager, LaserInformation
from WITecSDK.Modules.LaserPowerSeries import LaserPowerSeries
from WITecSDK.Modules.LineScan import LineScan, LineScan62
from WITecSDK.Modules.ManualTopography import ManualTopography
from WITecSDK.Modules.ObjectiveTurret import ObjectiveTurret
from WITecSDK.Modules.ParameterNameGetter import ParameterNameGetter
from WITecSDK.Modules.Polarization import Polarization
from WITecSDK.Modules.ProjectCreatorSaver import ProjectCreatorSaver
from WITecSDK.Modules.SampleName import SampleName
from WITecSDK.Modules.SamplePositioner import SamplePositioner, SamplePositioner51
from WITecSDK.Modules.ScanTable import ScanTable
from WITecSDK.Modules.SilentSpectrum import SilentSpectrum
from WITecSDK.Modules.SingleSpectrum import SingleSpectrum
from WITecSDK.Modules.SlowTimeSeriesManual import SlowTimeSeriesManual
from WITecSDK.Modules.SlowTimeSeriesTimed import SlowTimeSeriesTimed
from WITecSDK.Modules.SpectralAutofocus import SpectralAutofocus53, SpectralAutofocus51, SpectralAutofocus
from WITecSDK.Modules.SpectralStitching import SpectralStitching
from WITecSDK.Modules.Spectrograph import Spectrograph
from WITecSDK.Modules.StateManager import StateManager
from WITecSDK.Modules.TrueSurface import TrueSurface62, TrueSurface
from WITecSDK.Modules.VideoControl import VideoControl61, VideoControl51, VideoControl50
from WITecSDK.Modules.WITecControlVersionTester import WITecControlVersionTester
from WITecSDK.Modules.XYAxes import XYAxes
from WITecSDK.Modules.ZAxis import ZAxis, ZStepper
from WITecSDK.Modules.HelperStructs import (AutofocusSettings, DataChannelDescription, SamplePositionerPosition, XYZPosition, LargeAreaSettings)


class WITecModules:
    """Base class of the main class for creating the module classes."""
    
    _activeSequencer = None
    _afm = None
    _apertureFieldStop = None
    _applicationControl = None
    _autofocus = None
    _beamPath = None
    _configurationLoader = None
    _detectorOutput = None
    _distanceCurve = None
    _efmControl = None
    _fastTimeSeries = None
    _heating = None
    _topIllumination = None
    _bottomIllumination = None
    _imageScan = None
    _imageScanMP = None
    _largeAreaScan = None
    _laserManager = None
    _laserPowerSeries = None
    _lineScan = None
    _manualTopography = None
    _objectiveTurret = None
    _parameterNameGetter = None
    _polarization = None
    _projectCreatorSaver = None
    _sampleName = None
    _scanTable = None
    _silentSpectrum = None
    _singleSpectrum = None
    _slowTimeSeriesManual = None
    _slowTimeSeriesTimed = None
    _spectralAutofocus = None
    _spectralStitching = None
    _spectrograph1 = None
    _spectrograph2 = None
    _spectrograph3 = None
    _stateManager = None
    _trueSurface = None
    _videoControl = None
    _versionTester = None
    _samplePositioner = None
    _xyAxes = None
    _zAxis = None
    _zStepper = None
    
    def __init__(self):
        self._versionTester = WITecControlVersionTester(self.comParameters.GetParameter)

    def CreateActiveSequencer(self) -> ActiveSequencer|ActiveSequencer60:
        """Creates a class instance to query and stop the active sequencer."""

        if self._activeSequencer is None:
            if self._versionTester.IsVersionGreater62:
                self._activeSequencer = ActiveSequencer62(self.comParameters.GetParameter)
            elif self._versionTester.IsVersionGreater60:
                self._activeSequencer = ActiveSequencer60(self.comParameters.GetParameter)
            else:
                self._activeSequencer = ActiveSequencer(self.comParameters.GetParameter)
        return self._activeSequencer
    
    def CreateAFM(self) -> AFM:
        """Creates a class instance to control AFM basic functions and to read its datachannels"""

        if self._afm is None:
            self._afm = AFM(self.comParameters.GetParameter)
        return self._afm
    
    def CreateApertureFieldStop(self) -> ApertureFieldStop:
        """Creates a class instance to control Aperture and field stop.
        Throws an ParameterNotAvailableException if hardware is not available."""

        if self._apertureFieldStop is None:
            self._apertureFieldStop = ApertureFieldStop(self.comParameters.GetParameter)
        return self._apertureFieldStop
    
    def CreateApplicationControl(self) -> ApplicationControl:
        """Creates a class instance of Application Control"""

        if self._applicationControl is None:
            self._applicationControl = ApplicationControl(self.comParameters.GetParameter)    
        return self._applicationControl

    def CreateAutoFocus(self) -> AutoFocus61|AutoFocus:
        """Creates a class instance to control the video autofocus.
        Throws an ParameterNotAvailableException if hardware is not available."""

        if self._autofocus is None:
            if self._versionTester.IsVersionGreater61:
                self._autofocus = AutoFocus61(self.comParameters.GetParameter)
            else:
                self._autofocus = AutoFocus(self.comParameters.GetParameter)
        return self._autofocus
        
    def CreateBeamPath(self) -> BeamPath|BeamPath51:
        """Creates a class instance to control the beampath."""

        if self._beamPath is None:
            if self._versionTester.IsVersionGreater51:
                self._beamPath = BeamPath51(self.comParameters.GetParameter)
            else:
                self._beamPath = BeamPath(self.comParameters.GetParameter)
            if self._versionTester.IsVersionGreater62:
                self._beamPath.CalibrationLamp = CalibrationCoupler62(self.comParameters.GetParameter)
            else:
                self._beamPath.CalibrationLamp = CalibrationCoupler(self.comParameters.GetParameter)
        return self._beamPath
    
    def CreateConfigurationLoader(self) -> ConfigurationLoader:
        """Creates a class instance to change the configuration."""

        if self._configurationLoader is None:
            self._configurationLoader = ConfigurationLoader(self.comParameters.GetParameter)
        return self._configurationLoader
    
    # Only for internal use, use ConfigurationLoader instead to change the output
    def CreateDetectorOutput(self) -> DetectorOutput:
        """Creates a class instance to control the detector output.
        Throws an ParameterNotAvailableException if hardware is not available.
        Only for internal use."""

        if self._detectorOutput is None:
            self._detectorOutput = DetectorOutput(self.comParameters.GetParameter)
        return self._detectorOutput
    
    def CreateDistanceCurve(self) -> DistanceCurve:
        """Creates a class instance for a distance curve."""

        if self._distanceCurve is None:
            self._distanceCurve = DistanceCurve(self.comParameters.GetParameter)
        return self._distanceCurve
    
    def CreateEFMControl(self) -> EFMControl:
        """Creates a class instance for the EFM Control."""

        if self._efmControl is None:
            self._efmControl = EFMControl(self.comParameters.GetParameter)
        return self._efmControl
    
    def CreateFastTimeSeries(self) -> FastTimeSeries:
        """Creates a class instance for a fast time series."""

        if self._fastTimeSeries is None:
            self._fastTimeSeries = FastTimeSeries(self.comParameters.GetParameter)
        return self._fastTimeSeries
    
    def CreateHeating(self) -> Heating:
        """Creates a class instance to control the heating stage.
        Throws an ParameterNotAvailableException if hardware is not available."""

        if self._heating is None:
            self._heating = Heating(self.comParameters.GetParameter)
        return self._heating
    
    def CreateBottomIllumination(self) -> BottomIllumination:
        """Creates a class instance to control the top illumination.
        Throws an ParameterNotAvailableException if hardware is not available."""

        if self._bottomIllumination is None:
            self._bottomIllumination = BottomIllumination(self.comParameters.GetParameter)
        return self._bottomIllumination
    
    def CreateTopIllumination(self) -> TopIllumination:
        """Creates a class instance to control the top illumination.
        Throws an ParameterNotAvailableException if hardware is not available."""

        if self._topIllumination is None:
            self._topIllumination = TopIllumination(self.comParameters.GetParameter)
        return self._topIllumination

    def CreateImageScan(self) -> ImageScan:
        """Creates a class instance for an image scan."""

        if self._imageScan is None:
            self._imageScan = ImageScan(self.comParameters.GetParameter)
        return self._imageScan
    
    def CreateImageScanMultipass(self) -> ImageScanMultipass:
        """Creates a class instance for an image scan multipass."""

        if self._imageScanMP is None:
            self._imageScanMP = ImageScanMultipass(self.comParameters.GetParameter)
        return self._imageScanMP

    def CreateLargeAreaScan(self) -> LargeAreaScan|LargeAreaScan62:
        """Creates a class instance for a large area series."""

        if self._largeAreaScan is None:
            if self._versionTester.IsVersionGreater62:
                self._largeAreaScan = LargeAreaScan62(self.comParameters.GetParameter)
            else:
                self._largeAreaScan = LargeAreaScan(self.comParameters.GetParameter)
        return self._largeAreaScan
    
    def CreateLaserManager(self) -> LaserManager61|LaserManager52|LaserManager:
        """Creates a class instance to control the lasers."""

        if self._laserManager is None:
            if self._versionTester.IsVersionGreater61:
                self._laserManager = LaserManager61(self.comParameters.GetParameter)
            elif self._versionTester.IsVersionGreater52:
                self._laserManager = LaserManager52(self.comParameters.GetParameter)
            else:
                self._laserManager = LaserManager(self.comParameters.GetParameter)
        return self._laserManager
    
    def CreateLaserPowerSeries(self) -> LaserPowerSeries:
        """Creates a class instance for a Laser Power series.
        Only available for version >= 5.1"""

        if self._laserPowerSeries is None:
            if self._versionTester.IsVersionGreater51:
                self._laserPowerSeries = LaserPowerSeries(self.comParameters.GetParameter)
        return self._laserPowerSeries

    def CreateLineScan(self) -> LineScan|LineScan62:
        """Creates a class instance for a line scan."""

        if self._lineScan is None:
            if self._versionTester.IsVersionGreater62:
                self._lineScan = LineScan62(self.comParameters.GetParameter)
            else:
                self._lineScan = LineScan(self.comParameters.GetParameter)
        return self._lineScan
    
    def CreateManualTopography(self) -> ManualTopography:
        """Creates a class instance to control the manual topography correction.
        Throws an ParameterNotAvailableException if function is not available.
        Only useful in combination XYAxes and ZAxis class starting in 6.1."""

        if self._versionTester.IsVersionGreater61:
            if self._manualTopography is None:
                self._manualTopography = ManualTopography(self.comParameters.GetParameter, self.CreateXYAxes(), self.CreateZAxis(),
                                                           self.CreateSpectralAutofocus(), self.CreateActiveSequencer())
            return self._manualTopography

    def CreateObjectiveTurret(self) -> ObjectiveTurret|None:
        """Creates a class instance to control the objective turret.
        Throws an ParameterNotAvailableException if hardware is not available.
        Only available for version >= 6.1"""

        if self._objectiveTurret is None:
            if self._versionTester.IsVersionGreater61:
                self._objectiveTurret = ObjectiveTurret(self.comParameters.GetParameter)
        return self._objectiveTurret
    
    def CreateParameterNameGetter(self) -> ParameterNameGetter:
        """Creates a class instance to read available parameters."""

        if self._parameterNameGetter is None:
            self._parameterNameGetter = ParameterNameGetter(self.comParameters.AllParams)
        return self._parameterNameGetter
    
    def CreatePolarization(self) -> Polarization|None:
        """Creates a class instance to control polarizer and analyzer.
        Throws an ParameterNotAvailableException if hardware is not available.
        Only available for version >= 5.1"""

        if self._polarization is None:
            if self._versionTester.IsVersionGreater51:
                self._polarization = Polarization(self.comParameters.GetParameter)
        return self._polarization
    
    def CreateProjectCreatorSaver(self) -> ProjectCreatorSaver:
        """Creates a class instance to save and load projects."""
        
        if self._projectCreatorSaver is None:
            self._projectCreatorSaver = ProjectCreatorSaver(self.comParameters.GetParameter)
        return self._projectCreatorSaver 

    def CreateSampleName(self) -> SampleName:
        """Creates a class instance for setting the sample name.
        Only available for version >= 5.2"""

        if self._sampleName is None:
            if self._versionTester.IsVersionGreater52:
                self._sampleName = SampleName(self.comParameters.GetParameter)
        return self._sampleName
    
    # Depricated, will be removed in future versions, use XYAxes
    def CreateSamplePositioner(self) -> SamplePositioner|SamplePositioner51:
        """Creates a class instance to control the motorized xy stage.
        Throws an ParameterNotAvailableException if hardware is not available.
        Depricated, will be removed in future versions, use CreateXYAxes"""

        if self._samplePositioner is None:
            if self._versionTester.IsVersionGreater51:
                self._samplePositioner = SamplePositioner51(self.comParameters.GetParameter)
            else:
                self._samplePositioner = SamplePositioner(self.comParameters.GetParameter)
        return self._samplePositioner
        
    def CreateScanTable(self) -> ScanTable:
        """Creates a class instance to control the piezo stage.
        Throws an ParameterNotAvailableException if hardware is not available."""

        if self._scanTable is None:
            self._scanTable = ScanTable(self.comParameters.GetParameter)
        return self._scanTable
    
    def CreateSilentSpectrum(self) -> SilentSpectrum:
        """Creates a class instance for a silent spectrum which returns the spectrum
        as ASCII.
        Only available for version >= 5.2"""

        if self._silentSpectrum is None:
            if self._versionTester.IsVersionGreater52:
                self._silentSpectrum = SilentSpectrum(self.comParameters.GetParameter, self.CreateBeamPath())
        return self._silentSpectrum
    
    def CreateSingleSpectrum(self) -> SingleSpectrum:
        """Creates a class instance for a single spectrum."""

        if self._singleSpectrum is None:
            self._singleSpectrum = SingleSpectrum(self.comParameters.GetParameter)
        return self._singleSpectrum

    def CreateSlowTimeSeriesManual(self) -> SlowTimeSeriesManual:
        """Creates a class instance for software-triggered slow series."""

        if self._slowTimeSeriesManual is None:
            self._slowTimeSeriesManual = SlowTimeSeriesManual(self.comParameters.GetParameter, self.CreateActiveSequencer())
        return self._slowTimeSeriesManual

    def CreateSlowTimeSeriesTimed(self) -> SlowTimeSeriesTimed:
        """Creates a class instance for a slow time series."""

        if self._slowTimeSeriesTimed is None:
            self._slowTimeSeriesTimed = SlowTimeSeriesTimed(self.comParameters.GetParameter)
        return self._slowTimeSeriesTimed

    def CreateSpectralAutofocus(self) -> SpectralAutofocus53|SpectralAutofocus51|SpectralAutofocus:
        """Creates a class instance to control the spectral autofocus.
        Throws an ParameterNotAvailableException if hardware is not available."""

        if self._spectralAutofocus is None:
            if self._versionTester.IsVersionGreater53:
                self._spectralAutofocus = SpectralAutofocus53(self.comParameters.GetParameter)
            elif self._versionTester.IsVersionGreater51:
                self._spectralAutofocus = SpectralAutofocus51(self.comParameters.GetParameter)
            else:
                self._spectralAutofocus = SpectralAutofocus(self.comParameters.GetParameter)
        return self._spectralAutofocus
    
    def CreateSpectralStitching(self) -> SpectralStitching:
        """Creates a class instance for spectral stitching"""

        if self._spectralStitching is None:
            self._spectralStitching = SpectralStitching(self.comParameters.GetParameter)
        return self._spectralStitching

    def CreateSpectrograph1(self) -> Spectrograph:
        """Creates a class instance to control spectrograph 1.
        Throws an ParameterNotAvailableException if hardware is not available."""

        if self._spectrograph1 is None:
            self._spectrograph1 = Spectrograph(self.comParameters.GetParameter, 1)
        return self._spectrograph1

    def CreateSpectrograph2(self) -> Spectrograph:
        """Creates a class instance to control spectrograph 2.
        Throws an ParameterNotAvailableException if hardware is not available."""

        if self._spectrograph2 is None:
            self._spectrograph2 = Spectrograph(self.comParameters.GetParameter, 2)
        return self._spectrograph2

    def CreateSpectrograph3(self) -> Spectrograph:
        """Creates a class instance to control spectrograph 3.
        Throws an ParameterNotAvailableException if hardware is not available."""

        if self._spectrograph3 is None:
            self._spectrograph3 = Spectrograph(self.comParameters.GetParameter, 3)
        return self._spectrograph3

    def CreateStateManager(self) -> StateManager|None:
        """Creates a class instance for setting the state manager.
        Only available for version >= 6.2"""

        if self._stateManager is None:
            if self._versionTester.IsVersionGreater62:
                self._stateManager = StateManager(self.comParameters.GetParameter)
        return self._stateManager
    
    def CreateTrueSurface(self) -> TrueSurface|TrueSurface62:
        """Creates a class instance to control TrueSurface (Mk3).
        Throws an ParameterNotAvailableException if hardware is not available.
        Only available for version >= 6.1"""

        if self._trueSurface is None:
            if self._versionTester.IsVersionGreater62:
                self._trueSurface = TrueSurface62(self.comParameters.GetParameter)
            elif self._versionTester.IsVersionGreater60:
                self._trueSurface = TrueSurface(self.comParameters.GetParameter)
        return self._trueSurface
    
    def CreateVideoControl(self) -> VideoControl61|VideoControl51|VideoControl50:
        """Creates a class instance to control the video image."""

        if self._videoControl is None:
            if self._versionTester.IsVersionGreater61:
                self._videoControl = VideoControl61(self.comParameters.GetParameter)
            elif self._versionTester.IsVersionGreater51:
                self._videoControl = VideoControl51(self.comParameters.GetParameter)
            else:
                self._videoControl = VideoControl50(self.comParameters.GetParameter)
        return self._videoControl
    
    def CreateWITecControlVersionTester(self) -> WITecControlVersionTester:
        """Creates a class instance to check the WITec Control version."""
        
        return self._versionTester
        
    def CreateXYAxes(self) -> XYAxes|SamplePositioner:
        """Creates a class instance to control the motorized xy stage.
        Throws an ParameterNotAvailableException if hardware is not available.
        For versions before 6.1 the SamplePositioner class is returned
        instead of the XYAxes class."""

        if self._versionTester.IsVersionGreater61:
            if self._xyAxes is None:
                self._xyAxes = XYAxes(self.comParameters.GetParameter)
            return self._xyAxes
        else:
            return self.CreateSamplePositioner()
        
    def CreateZAxis(self) -> ZAxis|ZStepper:
        """Creates a class instance to control the motorized z stage.
        Throws an ParameterNotAvailableException if hardware is not available.
        For versions before 6.1 the ZStepper class is returned
        instead of the ZAxis class."""

        if self._versionTester.IsVersionGreater61:
            if self._zAxis is None:
                self._zAxis = ZAxis(self.comParameters.GetParameter)
            return self._zAxis
        else:
            return self.CreateZStepper()

    # Depricated, will be removed in future versions, use ZAxis
    def CreateZStepper(self) -> ZStepper:
        """Creates a class instance to control the motorized z stage.
        Throws an ParameterNotAvailableException if hardware is not available.
        Depricated, will be removed in future versions, use CreateZAxis"""

        if self._zStepper is None:
            self._zStepper = ZStepper(self.comParameters.GetParameter)
        return self._zStepper