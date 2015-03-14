from distutils.core import setup
import py2exe

#setup(console=["CETGUI.py"], options={"py2exe": {"dll_excludes": ["MSVCP90.dll"]}})
setup(windows=["CETGUI.py"], options={"py2exe": {"dll_excludes": ["MSVCP90.dll"]}})
