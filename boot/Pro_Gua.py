__author__ = 'guoaway'
#_*_encoding:utf-8_*_
import wx, threading, time, thread

IconPath = "..\\var\\sys_logo\\murshroom.ico"


class Frame(wx.Frame):
    def __init__(self, parent=None):
        wx.Frame.__init__(self, parent=parent, id=-1, title=u'上传进度', pos=(500, 300), size=(400, 110),
                          style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
        self.SetIcon(wx.Icon(IconPath, wx.BITMAP_TYPE_ICO))
        self.panel = wx.Panel(self, id=-1, size=wx.DefaultSize, pos=wx.DefaultPosition)
        self.txt = wx.StaticText(self.panel, id=-1, label=u"正在上传……", pos=(150, 10), size=wx.DefaultSize)
        self.txt.Show(True)
        self.bar = wx.Gauge(self.panel, id=-1, range=100, pos=(25, 30), size=(350, 20), name="gauge")
        self.stext = wx.StaticText(self.panel, id=-1, label=u"3秒后自动关闭", pos=(150, 60))
        self.stext.Show(False)
        self.rating = 0


class App(wx.App):
    def OnInit(self):
        self.frame = Frame()
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True


app = None


def TestT():
    global app
    app = App()
    app.MainLoop()


if __name__ == '__main__':
    thread.start_new_thread(TestT, ())
    time.sleep(1)
    global app
    app.frame.start()
    for i in range(0, 11):
        app.frame.rating = i * 10
        time.sleep(1)
