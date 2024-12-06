from WITecSDK import WITecSDKClass
import sys

def printerr(input):
    sys.stderr.write(str(input) + "\n")

def iterateObj(testobj, prefix: str):
    attributes = [attr for attr in dir(testobj) if not callable(getattr(testobj, attr)) and not attr.startswith('_')]
    for item in attributes:
        itemobj = getattr(testobj, item)
        if itemobj is None or isinstance(itemobj, (bool, int, float, str, tuple, list)):
            print(prefix + item + ': ' + str(itemobj))
        else:
            print(prefix + item + ': ' + str(type(itemobj)))
            iterateObj(itemobj, prefix + item + '.')

def testmodule(methodpointer):
    print('')
    print('Testing: ' + str(methodpointer))
    try:
        testmod = methodpointer()
        print(type(testmod))
        iterateObj(testmod, '')

    except Exception as exc:
        printerr(type(exc))
        printerr(exc)

WITec = WITecSDKClass()

createmethods = [getattr(WITec, func) for func in dir(WITec) if callable(getattr(WITec, func)) and func.startswith("Create")]

for cmethod in createmethods:
    testmodule(cmethod)