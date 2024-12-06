from WITecSDK.Parameters.COMStatusParameter import COMStatusParameter
from WITecSDK.Parameters.COMClient import IUnknown, IBUCSFillStatus, CheckConnection
from comtypes.automation import BSTR, VARIANT, VT_ARRAY, _SysAllocStringLen, _VariantClear, _midlSAFEARRAY
from ctypes import c_float, memmove, byref, cast, sizeof, _SimpleCData

def ConvertToVARIANT(value: list, atype: type(_SimpleCData)) -> VARIANT:
    """Creates SAFEARRAY of a certain type in comtypes"""

    varobj = VARIANT()
    _VariantClear(varobj)
    obj = _midlSAFEARRAY(atype).create(value)
    memmove(byref(varobj._), byref(obj), sizeof(obj))
    varobj.vt = VT_ARRAY | obj._vartype_
    return varobj

class COMFillStatusParameter(COMStatusParameter):

    fillvals = None
    
    def __init__(self, aDefaultInterface: IUnknown):
        super().__init__(aDefaultInterface)
        self.fillvals = self.modifier.QueryInterface(IBUCSFillStatus)

    @CheckConnection
    def fillDataArray(self, dataarray: VARIANT):
        self._throwExceptionIfNoWriteAccess()
        self.fillvals.FillDataArray(dataarray)

    def __del__(self):
        if self.fillvals is not None:
            self.fillvals.Release()
        super().__del__()

class COMStringFillStatusParameter(COMFillStatusParameter):

    def WriteArray(self, datalist: list[str]):
        isstr = [isinstance(x,str) for x in datalist]
        if not False in isstr:
            datalist = [cast(_SysAllocStringLen(item, len(item)), BSTR) for item in datalist]
            self.fillDataArray(ConvertToVARIANT(datalist, BSTR))
        else:
            raise Exception("Non-matching datatypes for IBUCSFillStatus")
        
class COMFloatFillStatusParameter(COMFillStatusParameter):

    def WriteArray(self, datalist: list[float]):
        isnum = [isinstance(x,(int,float)) for x in datalist]
        if not False in isnum:
            self.fillDataArray(ConvertToVARIANT(datalist, c_float))
        else:
            raise Exception("Non-matching datatypes for IBUCSFillStatus")
