__author__ = 'guoaway'
#_*_encoding:utf-8_*_

import wx, socket, os, codecs

data = open("..\\etc\\passwd").read().decode("UTF_8")
x = (int)("20" + data[:2])
list1 = []
for i in range(x, x + 4):
    a = str(i)
    list1.append(a)
list2 = [u"第一学期", u"第二学期"]
scoreList = []
rankList = []
TermList = []


def makeGrid1(win, sum, scoreList):
    gs = wx.GridSizer(sum + 1, 4, 0, 0)  # rows, cols, vgap, hgap
    list = [(SampleWindow(win, u'课程名', 1), 0, wx.EXPAND),
            (SampleWindow(win, u'学分', 1), 0, wx.EXPAND),
            (SampleWindow(win, u'成绩', 1), 0, wx.EXPAND),
            (SampleWindow(win, u'绩点', 1), 0, wx.EXPAND)]
    for i in range(0, sum):
        for j in range(0, 4):
            list.append((SampleWindow(win, scoreList[i][j], 0), 0, wx.EXPAND))
    gs.AddMany(list)
    return gs


def makeGrid2(win, sum):
    global rankList
    gs = wx.GridSizer(sum + 1, 3, 0, 0)  # rows, cols, vgap, hgap
    list = [(SampleWindow(win, u'等级大类', 1), 0, wx.EXPAND),
            (SampleWindow(win, u'等级名称', 1), 0, wx.EXPAND),
            (SampleWindow(win, u'成绩', 0), 1, wx.EXPAND)]

    for i in range(0, sum):
        for j in range(0, 3):
            list.append((SampleWindow(win, rankList[i][j], 0), 0, wx.EXPAND))
    gs.AddMany(list)
    return gs


class SampleWindow(wx.PyWindow):
    """
    A simple window that is used as sizer items in the tests below to
    show how the various sizers work.
    """

    def __init__(self, parent, text, flag):
        wx.PyWindow.__init__(self, parent, -1,
                             #style=wx.RAISED_BORDER
                             #style=wx.SUNKEN_BORDER
                             style=wx.SIMPLE_BORDER
        )
        colour = wx.Colour(0, 255, 255)
        if flag == 1:
            self.SetBackgroundColour("yellow")
        self.text = text
        self.SetTextStytel()
        self.bestsize = (160, 20)
        self.SetSize(self.bestsize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        #self.Bind(wx.EVT_LEFT_UP, self.OnCloseParent)

    def SetTextStytel(self):
        self.SetForegroundColour('0')
        self.SetBackgroundColour('0')
        font = wx.Font(10, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        self.SetFont(font)


    def OnPaint(self, evt):
        sz = self.GetSize()
        dc = wx.PaintDC(self)
        w, h = dc.GetTextExtent(self.text)
        dc.Clear()
        dc.DrawText(self.text, (sz.width - w) / 2, (sz.height - h) / 2)

    def OnSize(self, evt):
        self.Refresh()

    def OnCloseParent(self, evt):
        p = wx.GetTopLevelParent(self)
        if p:
            p.Close()

    def DoGetBestSize(self):
        return self.bestsize


class Panel(wx.Panel):
    def __init__(self, parent, num):
        wx.Panel.__init__(self, parent=parent, id=-1, size=(800, 600))
        self.p = wx.Panel(self, id=-1, size=(0, 0))
        if num == 2:
            self.txt = wx.StaticText(self, id=-1, pos=(300, 4), label=u"学期成绩查询")
            self.SetTitleTextStytel(self.txt)
            self.YearChoice = wx.Choice(self, id=-1, pos=(150, 50), size=(150, 50), choices=list1, style=0,
                                        validator=wx.DefaultValidator, name="YearChoice")
            self.TermChoice = wx.Choice(self, id=-1, pos=(350, 50), size=(150, 50), choices=list2, style=0,
                                        validator=wx.DefaultValidator, name="TermChoice")
            self.Searchbut = wx.Button(self, id=-1, pos=(550, 50), size=(100, 30), label=u"查询", name="but")
            self.txt1 = wx.StaticText(self, id=-1, pos=(1000, 1000))
            self.txt2 = wx.StaticText(self, id=-1, pos=(1000, 10000))
            self.SetTextStytel(self.YearChoice)
            self.SetTextStytel(self.TermChoice)

            self.Bind(wx.EVT_BUTTON, self.AddReport, self.Searchbut)

        if num == 1:
            self.txt = wx.StaticText(self, id=-1, pos=(300, 4), label=u"等级考试查询")
            self.SetTitleTextStytel(self.txt)
            self.SetPosition((800, 800))
            self.AddReport1()

        if num == 3:
            self.txt = wx.StaticText(self, id=-1, pos=(300, 4), label=u"历史成绩查询")
            self.SetTitleTextStytel(self.txt)
            self.SetPosition((800, 800))
            self.AddReport2()

    def MurshroomServerAPI(self, commond):#这里输入commod就可以通过murshroom server获取信息
        achconn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = '127.0.0.1'
        port = int(open("..\\etc\\sysconfig\\socket_port", 'r').read())
        try:
            achconn.connect((host, port))
        except Exception, e:
            print "connect to server failed."
            return
        print "connect murshroom server cilent..."
        achconn.sendall(commond)
        mesg = achconn.recv(4096)
        print mesg
        achconn.close()
        return mesg

    def SetTextStytel(self, tex):
        tex.SetForegroundColour('0')
        tex.SetBackgroundColour('0')
        font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        tex.SetFont(font)

    def SetTitleTextStytel(self, tex):
        tex.SetForegroundColour('0')
        tex.SetBackgroundColour('0')
        font = wx.Font(25, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        tex.SetFont(font)

    def TupleSmallFormat(self, strtuple):#将(1,2,3)这样的字符串变成类似输出的tuple
        return tuple(strtuple.split(','))

    def GetTermList(self):
        filename = self.MurshroomServerAPI("MTERMS|" + str(self.YearChoice.GetStringSelection()) + str(
            int(int(self.TermChoice.GetCurrentSelection()) + 1)))
        if filename == '':
            return []
        reslist = codecs.open('..\\tmp\\' + filename, 'r', 'utf-8').read()
        reslist = reslist.split('\n')
        os.remove('..\\tmp\\' + filename)
        reslist = map(self.TupleSmallFormat, reslist)
        glist = []
        for line in reslist:
            if len(line) < 4: continue
            glist.append(line)
        return glist


    def GetRankList(self):
        filename = self.MurshroomServerAPI("MRANKS|")
        if filename == '':
            return []
        reslist = codecs.open('..\\tmp\\' + filename, 'r', 'utf-8').read()
        reslist = reslist.split('\n')
        os.remove('..\\tmp\\' + filename)
        reslist = map(self.TupleSmallFormat, reslist)
        glist = []
        for line in reslist:
            if len(line) < 3: continue
            glist.append(line)
        return glist

    def GetScoreList(self):
        filename = self.MurshroomServerAPI("MTOTALS|")
        if filename == '':
            return []
        reslist = codecs.open('..\\tmp\\' + filename, 'r', 'utf-8').read().split('\n')
        os.remove("..\\tmp\\" + filename)
        reslist = map(self.TupleSmallFormat, reslist)
        glist = []
        for line in reslist:
            if len(line) < 4: continue
            glist.append(line)
        return glist

    def AddReport(self, event):
        global TermList
        TermList = self.GetTermList()
        sum = len(TermList)
        x = sum * 20 + 130
        sum1 = 0
        sum2 = 0.0
        for i in range(0, sum):
            sum1 = sum1 + int(TermList[i][1])
            sum2 = sum2 + int(TermList[i][1]) * float(TermList[i][3])
        try:
            sum2 = sum2 / sum1
        except ZeroDivisionError, ex:
            sum2 = 0
        self.txt1.Destroy()
        self.txt2.Destroy()
        self.txt1 = wx.StaticText(self, id=-1, pos=(1000, 1000))
        self.txt2 = wx.StaticText(self, id=-1, pos=(1000, 1000))
        self.txt1.SetPosition((250, x))
        self.txt1.SetLabel(u"所得学分数：" + str(sum1))
        self.txt2.SetPosition((400, x))
        self.txt2.SetLabel(u"平均学分绩点：%.2f" % (sum2))
        self.p.Destroy()
        self.p = wx.Panel(self, id=-1, size=(800, 600), pos=(100, 100))
        self.p.sizer = makeGrid1(self.p, sum, TermList)
        self.p.SetSizer(self.p.sizer)
        self.p.sizer.Fit(self.p)
        self.p.Fit()


    def AddReport1(self):
        global rankList
        rankList = self.GetRankList()
        sum = len(rankList)
        self.p.Destroy()
        self.p = wx.Panel(self, id=-1, size=(800, 600), pos=(150, 50))
        self.p.sizer = makeGrid2(self.p, sum)
        self.p.SetSizer(self.p.sizer)
        self.p.sizer.Fit(self.p)
        self.p.Fit()

    def AddReport2(self):
        global scoreList
        scoreList = self.GetScoreList()
        sum = len(scoreList)
        #self.p = wx.Panel(self, id=-1, size=(800, 600), pos=(100, 50))
        x = sum * 20 + 80
        self.p.Destroy()
        self.p = wx.ScrolledWindow(self, id=-1, pos=(100, 50), size=(650, 400))
        self.p.SetVirtualSize((800, 3000))
        self.p.SetScrollRate(0, 20)
        self.p.sizer = makeGrid1(self.p, sum, scoreList)
        self.p.SetSizer(self.p.sizer)
        self.p.sizer.Fit(self.p)
        self.p.Fit()
        sum1 = 0
        sum2 = 0.0
        for i in range(0, sum):
            sum1 = sum1 + int(scoreList[i][1])
            sum2 = sum2 + int(scoreList[i][1]) * float(scoreList[i][3])
        try:
            sum2 = sum2 / sum1
        except ZeroDivisionError, ex:
            sum2 = 0
        self.txt1 = wx.StaticText(self, id=-1, pos=(250, 480), label=u"所得学分数：" + str(sum1))
        self.txt2 = wx.StaticText(self, id=-1, pos=(400, 480), label=u"平均学分绩点：%.2f" % (sum2))


class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, id=-1, title=u"成绩单", size=(800, 600), pos=(320, 150),
                          style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
        self.SetIcon(wx.Icon('..\\var\\sys_logo\\AchievementReport.ico', wx.BITMAP_TYPE_ICO))
        self.AddElement()
        self.AddMenu()

    def AddMenu(self):
        menuBar = wx.MenuBar()
        menu1 = wx.Menu()
        menuBar.Append(menu1, u"选项")
        self.Menu_Rank = menu1.Append(-1, u"等级考试查询")
        self.Menu_Term = menu1.Append(-1, u"学期成绩查询")
        self.Menu_All = menu1.Append(-1, u"历年成绩查询")
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.ChangePanel1, self.Menu_Rank)
        self.Bind(wx.EVT_MENU, self.ChangePanel2, self.Menu_Term)
        self.Bind(wx.EVT_MENU, self.ChangePanel3, self.Menu_All)

    def ChangePanel1(self, event):
        self.panel1.SetPosition((0, 0))
        self.panel2.SetPosition((600, 800))
        #self.panel2.Show(False)
        self.panel3.SetPosition((600, 800))
        #self.panel3.Show(False)

    def ChangePanel2(self, event):
        self.panel2.SetPosition((0, 0))
        self.panel1.SetPosition((600, 800))
        #self.panel1.Show(False)
        self.panel3.SetPosition((600, 800))
        # self.panel3.Show(False)

    def ChangePanel3(self, event):
        self.panel3.SetPosition((0, 0))
        self.panel2.SetPosition((600, 800))
        #self.panel2.Show(False)
        self.panel1.SetPosition((600, 800))
        # self.panel1.Show(False)

    def AddElement(self):
        self.panel1 = Panel(self, 1)
        self.panel2 = Panel(self, 2)
        self.panel3 = Panel(self, 3)


class App(wx.App):
    def OnInit(self):
        self.frame = Frame()
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True


def TestA():
    app = App()
    app.MainLoop()


if __name__ == '__main__':
    TestA()





