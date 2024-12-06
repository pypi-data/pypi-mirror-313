#For internal use only, can be removed or changed in future versions
from typing import Callable
from WITecSDK.Parameters import COMStringParameter, COMBoolParameter, COMTriggerParameter
from WITecSDK.Modules.BeamPath import BeamPath
from asyncio import sleep
from time import sleep as tsleep

parampath = "MultiComm|SequencerSingleSpectrum|"

class SilentSpectrum:

    def __init__(self, aGetParameter: Callable, aBeamPath: BeamPath):
        self._beamPath = aBeamPath
        self._acquisitionParameterCOM: COMStringParameter = aGetParameter(parampath + "SilentSpectrumAcquisitionParameter")
        self._acquisitionInformationCOM: COMStringParameter = aGetParameter(parampath + "SilentSpectrumAcquisitionInformation")
        self._sequenceDoneCOM: COMBoolParameter = aGetParameter(parampath + "SilentSpectrumSequenceDone")
        self._spectrumAsTextCOM: COMStringParameter = aGetParameter(parampath + "SilentSpectrumAsText")
        self._errorCOM: COMStringParameter = aGetParameter(parampath + "SilentSpectrumError")
        self._startSilentSpectrumCOM: COMTriggerParameter = aGetParameter(parampath + "StartSilentSpectrumAcquisition")

    def SetParameters(self, numberOfAccumulations: int, integrationTime: float):
        parameterString = f"IntegrationTime {integrationTime}\n NumberOfAccumulations {numberOfAccumulations}\n"
        self._acquisitionParameterCOM.Value = parameterString

    def GetacquisitionInformation(self) -> str:
        return self._acquisitionInformationCOM.Value

    def GetSpectrumAsText(self) -> str:
        return self._spectrumAsTextCOM.Value

    def IsSequenceDone(self) -> bool:
        return self._sequenceDoneCOM.Value

    def ResetSequenceDone(self):
        self._sequenceDoneCOM.Value = False

    def GetError(self) -> str:
        return self._errorCOM.Value

    def Start(self):
        self._startSilentSpectrumCOM.ExecuteTrigger()

    async def AwaitSilentSpectrumAvailableBeamPath(self) -> str:
        self._beamPath.SetRaman()
        sleep(4)
        result = await self.AwaitSilentSpectrumAvailable()
        return result

    async def AwaitSilentSpectrumAvailable(self) -> str:
        # Returns when spectrum is available, sequence maybe not completed, check with ActiveSequencer
        self.ResetSequenceDone()
        self.Start()
        await self.waitUntilFinished()
        self.throwIfError()
        return self.GetSpectrumAsText()

    async def waitUntilFinished(self):
        while True:
            val = self.IsSequenceDone()
            if val:
                break
            await sleep(0.1)

    def throwIfError(self):
        result = self.GetError()
        if result != "Ok":
            raise SilentSpectrumNoSuccessException(result)


class SilentSpectrumNoSuccessException(Exception):
    def __init__(self, errormsg: str):
        super().__init__("Silent spectrum ended with error: " + errormsg)
