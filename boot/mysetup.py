#mysetup.py
from distutils.core import setup
import py2exe

#setup(console=["Main.py"], options={"py2exe": {"dll_excludes": ["MSVCP90.dll"]}})
#setup(windows=["Main.py"], options={"py2exe": {"dll_excludes": ["MSVCP90.dll"]}})
setup(windows=["Main.py"])