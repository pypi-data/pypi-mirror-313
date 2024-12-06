from typing import Callable
from _ctypes import COMError
from WITecSDK.Parameters import COMTriggerParameter, COMStringParameter, COMIntParameter,COMEnumParameter, COMStringStatusParameter
from datetime import date

parampath = "UserParameters|AutoSaveProject|"

def CatchException(func):
    
    def wrapper(arg):
        val = None
        try:
            val = func(arg)
        except COMError as e:
            # Throws an exception, if project is not saved yet. 
            if e.hresult != -2147467263: #NotImplemented
                raise e
        except Exception as e:
            raise e
        return val
    return wrapper

class ProjectCreatorSaver:

    def __init__(self, aGetParameter: Callable):
        self._storeProjectCOM: COMTriggerParameter = aGetParameter(parampath + "StoreProject")
        self._startDirectoryCOM: COMStringParameter = aGetParameter(parampath + "StartDirectory")
        self._extraDirectoryCOM: COMStringParameter = aGetParameter(parampath + "ExtraDirectory")
        self._fileNameCOM: COMStringParameter = aGetParameter(parampath + "FileName")
        self._fileNumberCOM: COMStringParameter = aGetParameter(parampath + "FileNumber")
        self._directoryModeCOM:COMEnumParameter = aGetParameter(parampath + "DirectoryMode")
        self._storeModeCOM: COMEnumParameter = aGetParameter(parampath + "StoreMode")
        self._overwriteModeCOM: COMEnumParameter = aGetParameter(parampath + "OverwriteMode")
        self._newProjectCOM: COMTriggerParameter = aGetParameter("ApplicationControl|NewProject")
        self._appendProjectCOM: COMStringParameter = aGetParameter("ApplicationControl|FileNameToAppendToProject")
        self._currentProjectNameCOM: COMStringStatusParameter = aGetParameter("Status|Software|Application|CurrentFileName")

    #Saves project in the start directory

    def SaveProject(self, fileName: str, directory: str|None = None):
        fileparts = fileName.split('\\')
        if len(fileparts) > 1:
            directory = '\\'.join(fileparts[:-1] + [''])
            fileName = fileparts[-1]

        if fileName[-4:] == '.wip':
            fileName = fileName[:-4]

        if fileName == '':
            raise Exception('An empty fileName is not allowed.')

        if directory is not None:
            initialDirectoryMode = self._directoryModeCOM.Value
            initialStartDirectory = self.StartDirectory

            self.StartDirectory = directory
            self._directoryModeCOM.Value = 0
        
        self.ClearAfterStore = True
        self.OverwriteExisting = False
        self.FileName = fileName
        self.AutoSave()
        
        if directory is not None:
            self.StartDirectory = initialStartDirectory
            self._directoryModeCOM.Value = initialDirectoryMode

    def AppendProject(self, fileName: str):
        self._appendProjectCOM.Value = fileName

    def CreateNewProject(self):
        self._newProjectCOM.ExecuteTrigger()

    def AutoSave(self):
        self._storeProjectCOM.ExecuteTrigger()

    @property
    @CatchException
    def CurrentProjectName(self) -> str:
        return self._currentProjectNameCOM.Value
    
    @property
    def StartDirectory(self) -> str:
        return self._startDirectoryCOM.Value

    @StartDirectory.setter
    def StartDirectory(self, value: str):
        self._startDirectoryCOM.Value = value
        
    @property
    def SubDirectory(self) -> str:
        dirmode = self._directoryModeCOM.Value
        extradir = self._extraDirectoryCOM.Value
        datestr = date.today().strftime("%Y%m%d")
        if dirmode == 0:
            return ""
        elif dirmode == 1:
            return extradir
        elif dirmode == 2:
            return datestr
        elif dirmode == 3:
            return extradir + "\\" + datestr
        elif dirmode == 4:
            return datestr + "\\" + extradir

    def DefineSubDirectory(self, value: str, useDate: bool = False, putDateFirst: bool = False):
        if value is None or value == "":
            if useDate:
                self._directoryModeCOM.Value = 2
            else:
                self._directoryModeCOM.Value = 0
        else:
            self._extraDirectoryCOM.Value = value
            if useDate:
                if putDateFirst:
                    self._directoryModeCOM.Value = 4
                else:
                    self._directoryModeCOM.Value = 3
            else:
                self._directoryModeCOM.Value = 1
        
    @property
    def FileName(self) -> str:
        return self._fileNameCOM.Value

    @FileName.setter
    def FileName(self, value: str):
        self._fileNameCOM.Value = value
        
    @property
    def FileNumber(self) -> int:
        return self._fileNumberCOM.Value

    @FileNumber.setter
    def FileNumber(self, value: int):
        self._fileNumberCOM.Value = value

    @property
    def ClearAfterStore(self) -> bool:
        return bool(self._storeModeCOM.Value)

    @ClearAfterStore.setter
    def ClearAfterStore(self, value: bool):
        self._storeModeCOM.Value = int(value)
        
    @property
    def OverwriteExisting(self) -> bool:
        return bool(self._overwriteModeCOM.Value)

    @OverwriteExisting.setter
    def OverwriteExisting(self, value: bool):
        self._overwriteModeCOM.Value = int(value)