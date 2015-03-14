from distutils.core import setup
import py2exe

#setup(console=["CETGUI.py"], options={"py2exe": {"dll_excludes": ["MSVCP90.dll"]}})
setup(windows=["AchievementReport.py"], options={"py2exe": {"dll_excludes": ["MSVCP90.dll"]}})
