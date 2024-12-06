This package enables control of WITec microscopes over its COM interface (additonal license required).

- Gives access to data acquisition functions
- Implements all classes of WITec's COM interface
- Offers ready-to-use classes for main measurement modes (Large Area Scan, Line Scan, Slow Series)
- Has classes for hardware control (motorized xy and z stage, spectrograph, laser, TrueSurface, polarization, turret)
- Gives access to video system (image acquisition, autofocus)
- Enables to save and create projects
- Can be extended by directly accessing needed parameters
- All classes are tested with versions down to WITec Control 5.0 (can be used even for older version but not all classes might work)

# Documentation and examples

Basic information can be found using the Python's built-in help function.

## Quickstart

```
from WITecSDK import WITecSDKClass
WITec = WITecSDKClass()
```

All other classes are created by the instance of the main class using the respective method.

## Examples

Documented examples are delivered with WITec Control. Further information can be found in it's help. If you use an older version of WITec Control please contact the [WITec support team](https://raman.oxinst.com/contact).

# Contribution, feature requests and bug reports

If you want to share your own extensions or have feature wishes or bug reports please contact the [WITec support team](https://raman.oxinst.com/contact).

# Changelog

## Changes in 1.4.2

- module for EFMControl added
- ScanMode implemented for LineScan class
- version information in prompt when connecting
- Typo PGain corrected in AFM class
- correct range output in ValueOutOfRangeException

## Changes in 1.4.1

- Support for AFM added
- new modules AFM, DistanceCurve and ImageScanMultiPass
- new method in WITecSDKClass: WaitForWriteAccess
- bug in property Beta of ImagesScan fixed

## Changes in 1.4.0

- Support for pywin32 removed
- COM parameter classes now use properties
- COMParameters.GetParameter always returns the correct class
- COM operations will produce a ConnectionLostException in case WITec Control is not available
- AwaitSilentSpectrumAvailableBeamPath() in SilentSpectrum now waits 4 seconds for beampath change
- XYAxes has AwaitMoveToSoftwarePosBacklashComp which moves with Backlash compensation
- Wrong calculation of Laser power in combination with correction factor fixed, new property SelectedLaserPowerInFiber in LaserManager module

## Changes in 1.3.1

- Mask property for SpectralAutofocus
- setSpectralMask is deprecated and will be removed in the future
- Mask added to AutofocusSettings

## Changes in 1.3.0

- Image scan added
- Scan table (piezo stage) added

## Changes in 1.2.5

- Bug in Autofocus fixed
- Bug in WITecControlVersionTester fixed

## Changes in 1.2.4

- Spectral Stitching added
- WITecControlVersionTester reworked

## Changes in 1.2.3

- Bug in Polarization.py and Beampath.py fixed

## Changes in 1.2.2

- Readme fixed

## Changes in 1.2.1

- Bug in Polarization.py fixed

## Changes in 1.2.0

- New WITec Control 6.2 features implemented (for LineScan, LargeAreaScan, ActiveSequencer, TrueSurface)
- docstrings added
- compatibility down to WITec Control 5.0 added
- New class LaserPowerSeries
- New structure for Polarization class
- CalibrationLamp and AdjustmentSampleCoupler added to BeamPath
- LineScan has own Integration time and Accumulation property
- LaserManager gives the corrected laser power by default (old property removed)
- New property Unit for Spectrograph

## Changes in 1.1.2

- New property HideViewers for the ActiveSequencer
- New property WriteAccess in the COMClient replacing old implemantation
- New property ReadAccess for the COMClient and HasReadAccess for the main class
- Improved error handling in __del__ of COMClient

## Changes in 1.1.1

- Bug in ProjectCreatorSaver module corrected
- property ExtraDirectory renamed to SubDirectory (read-only) and method DefineSubDirectory()

## Changes in 1.1.0

- New class AutomatedCoupler attached to TopIllumination and VideoControl, if automated
- New classes inheriting from its main class to implement versiongreater61 features
- New class DetectorOutput for internal use
- __del__ removed from all modules