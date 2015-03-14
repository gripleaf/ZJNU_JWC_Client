__author__ = 'glcsnz123'
#_*_encoding:utf-8_*_
import wx
import thread, threading, CET
import sys, time

global runmt


class RunMulThreads(wx.Frame, threading.Thread):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, id=-1, title="CET4|6 ShowScore", size=(400, 400),
                          style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
        threading.Thread.__init__(self)
        self.SetIcon(wx.Icon('..\\var\\sys_logo\\CETGUI.ico', wx.BITMAP_TYPE_ICO))
        self.InitPanel()
        self.AddElement0()
        self.AddElement1()
        self.AddBind()
        self.curnow = 0
        self.anslist = []

        #create the Gauge

    def InitPanel(self):
        self.panel = wx.Panel(self, id=-1)
        self.panel.img = wx.Image("..\\var\\CETGUI\\cet_bg.jpg", wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
        self.panel.bmp = wx.StaticBitmap(self.panel, id=-1, bitmap=self.panel.img)
        self.panel.SetPosition((self.GetSize()[0], self.GetSize()[1]))
        self.panel.SetSize((self.GetSize()[0], self.GetSize()[1]))
        #self.panel.SetBackgroundColour("white")

        #两个panel的分界线

        self.panel_show = wx.Panel(self, id=-1)
        self.panel_show.img = wx.Image("..\\var\\CETGUI\\cet_pbg.jpg", wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
        self.panel_show.bmp = wx.StaticBitmap(self.panel_show, id=-1, bitmap=self.panel_show.img)
        self.panel_show.SetPosition((0, 0))
        self.panel_show.SetSize((self.GetSize()[0], self.GetSize()[1]))
        #self.panel_show.SetBackgroundColour("yellow")

    def AddElement0(self):
        self.cetrb = wx.RadioBox(self.panel_show.bmp, id=-1, label="CET Level", name="radiobox",
                                 choices=['CET4', 'CET6'], pos=(137, 160))
        self.cetrb.SetForegroundColour("purple")
        self.cetbut = wx.Button(self.panel_show.bmp, -1, label=u"确定", pos=(152, 300))
        self.cetkch = wx.Button(self.panel_show.bmp, -1, label=u"默认考场上限200，座位号上限30，如需更改，请点击此处", size=(400, 28))
        self.kchlimit = 200
        self.zwhlimit = 30
        self.cetlev = 4
        name = open(r"..\etc\UserName.conf").read()


    def AddBind(self):#create the bind
        #panel_show
        self.Bind(wx.EVT_BUTTON, self.SetKZLimit, self.cetkch)
        self.Bind(wx.EVT_BUTTON, self.NextPanel, self.cetbut)

        #panel
        self.Bind(wx.EVT_BUTTON, self.PreResult, self.cetprebut)
        self.Bind(wx.EVT_BUTTON, self.NextResult, self.cetnextbut)
        self.Bind(wx.EVT_CLOSE, self.ErrorLog)

    def AddElement1(self):
        self.cetGua = wx.Gauge(self.panel.bmp, -1, 100, name="gauge", pos=(50, 90), size=(300, 20))
        self.cetGua.Show(False)
        #create the staicText
        self.cetShowSt = wx.StaticText(self.panel.bmp, -1, "", pos=(120, 25))
        self.cetShowSt.SetBackgroundColour((155, 178, 196))

        #create the staticText
        self.cetRes = wx.StaticText(self.panel.bmp, -1, u"you can't see me!", pos=(120, 130))
        self.cetRes.Show(False)

        #create the button
        self.cetprebut = wx.Button(self.panel.bmp, -1, label=u"上一个", pos=(100, 300))
        self.cetnextbut = wx.Button(self.panel.bmp, -1, label=u"下一个", pos=(200, 300))
        self.cetprebut.Show(False)
        self.cetnextbut.Show(False)

    def ErrorLog(self, event):
        self.Destroy()

    def SetKZLimit(self, event):
        ted = wx.TextEntryDialog(self, u"输入两个整数分别表示考场号和座位号上限（用英文状态下输入的“逗号”隔开）", style=wx.OK | wx.CANCEL)
        if ted.ShowModal() == wx.ID_OK:
            try:
                self.kchlimit, self.zwhlimit = map(int, ted.GetValue().split(","))
            except Exception, e:
                self.kchlimit, self.zwhlimit = 200, 30

    def NextPanel(self, event):
        if self.cetrb.GetSelection() == 0:
            self.cetlev = '1'
        else:
            self.cetlev = '2'
        t = self.panel.GetPosition()
        self.panel.SetPosition(self.panel_show.GetPosition())
        self.panel_show.SetPosition(t)
        thread.start_new_thread(CET.CreateMultiCheck, (self.cetlev, 60, (1, self.kchlimit), (1, self.zwhlimit)))
        self.start()


    def PreResult(self, event):
        self.curnow -= 1
        self.curnow %= len(self.anslist)
        self.cetRes.SetLabel(self.anslist[self.curnow])

    def NextResult(self, event):
        self.curnow += 1
        self.curnow %= len(self.anslist)
        self.cetRes.SetLabel(self.anslist[self.curnow])

    def run(self):
        self.ShowTable = u"    正在努力创建60个线程 ... "
        self.cetShowSt.SetLabel(self.ShowTable)
        while True:
            if CET.Rating > 0:
                self.cetShowSt.SetLabel(self.ShowTable + u"\n\n创建完成！O(∩_∩)O~ 开始查找 ...")
                break
            time.sleep(1)
        time.sleep(0.5)
        self.cetGua.Show(True)
        while True:
            self.cetGua.SetValue(CET.Rating)
            time.sleep(5)
            if CET.Rating >= 99.9:
                self.cetGua.SetValue(100)
                break
        self.cetRes.SetLabel(u"      努力处理数据中...")
        self.cetRes.Show(True)
        self.anslist = CET.CreateScore(True)
        time.sleep(2)
        self.curnow = 0
        if len(self.anslist) > 0:
            self.cetRes.SetLabel(self.anslist[self.curnow])
            self.cetprebut.Show(True)
            self.cetnextbut.Show(True)
        else:
            self.cetRes.SetPosition((100, 130))
            self.cetRes.SetLabel(u"              查找失败~~~~~~\n\n对不起，是我们的程序太差劲了T T")


def RunMulGUI():#图形界面开始处
    app = wx.App();
    runmt = RunMulThreads()
    runmt.Centre()
    runmt.Show(True)
    app.MainLoop();
    #thread.start_new_thread(CET.CreateMultiCheck, ())


def RunMulConsle(tlimit, kchlimit, zwhlimit=(1, 50)):#控制台界面启动处
    CET.CreateMultiCheck(tlimit, kchlimit, zwhlimit)
    CET.CreateScore(False)


if __name__ == '__main__':#main function
    if len(sys.argv) <= 1 or sys.argv[1] == 0:
        RunMulGUI()
    else:
        print "create the console ... "
        if len(sys.argv) == 5:
            kchlimit = map(int, sys.argv[3].split(','))
            zwhlimit = map(int, sys.argv[4].split(','))
            RunMulConsle(sys.argv[1], int(sys.argv[2]), kchlimit, zwhlimit)
        elif len(sys.argv) == 4:
            kchlimit = map(int, sys.argv[3].split(','))
            RunMulConsle(sys.argv[1], int(sys.argv[2]), kchlimit)
        else:
            print "[ERROR] args error~"



