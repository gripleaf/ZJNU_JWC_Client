__author__ = 'glcsnz123'
#_*_encoding:utf-8_*_
import pickle, time


def DumpObject(Object, path=r"..\tmp\default.obj"):
    try:
        objfile = open(path, 'w')
        pickle.dump(Object, objfile)
    finally:
        objfile.close()


def LoadObject(path=r"..\tmp\default.obj"):#return back a object
    try:
        objfile = open(path, "r")
        obj = pickle.load(objfile)
    finally:
        objfile.close()
    return obj


if __name__ == '__main__':
    obj = [123213, 13123123, 13123, 12, 3, 12, 312]
    DumpObject(obj)
    obj = "fdsadfads"
    DumpObject(obj)
    obj = (1, 231, 21, 312, 312)
    DumpObject(obj)
    time.sleep(1)
    t = LoadObject()
    print t
    t = LoadObject()
    print t
    t = LoadObject()
    print t




