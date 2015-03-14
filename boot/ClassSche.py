__author__ = 'guoaway'
#_*_encoding:utf-8_*_
import wx, socket, codecs, os

#courseList = [(u"数据结构", "0-010203 4-060708"), (u"线性代数", "3-030405"), (u"高等数学", "0-0607 2-101112"), (u"体育", "1-030405")]
courseList = []
colourList = []


class SampleWindow(wx.PyWindow):
    """
    A simple window that is used as sizer items in the tests below to
    show how the various sizers work.
    """

    def __init__(self, parent, text, colour, pos=wx.DefaultPosition, size=wx.DefaultSize):
        wx.PyWindow.__init__(self, parent, -1,
                             #style=wx.RAISED_BORDER
                             #style=wx.SUNKEN_BORDER
                             style=wx.SIMPLE_BORDER
        )
        self.SetBackgroundColour(colour)
        self.text = text
        if size != wx.DefaultSize:
            self.bestsize = size
        else:
            self.bestsize = (80, 25)
        self.SetSize(self.GetBestSize())

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        #self.Bind(wx.EVT_LEFT_UP, self.OnCloseParent)


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


def makeGrid1(win, coursename, colournum):
    gs = wx.GridSizer(13, 8, 4, 2)  # rows, cols, vgap, hgap
    colour1 = wx.Colour(235, 118, 4)
    colour2 = wx.Colour(83, 163, 195)
    colour = wx.Colour(255, 255, 255)
    colourList.append(colour)
    r = 230
    g = 255
    b = 0
    for i in range(len(courseList)):
        colour = wx.Colour(r, g, b)
        b += 50
        g -= 50
        if b>255:
            b=20
        if g<0:
            g=235
        colourList.append(colour)

    list = [(SampleWindow(win, '', colourList[0]), 0, wx.EXPAND),
            (SampleWindow(win, 'Mon', colour1), 0, wx.EXPAND),
            (SampleWindow(win, 'Tue', colour1), 0, wx.EXPAND),
            (SampleWindow(win, 'Wed', colour1), 0, wx.EXPAND),
            (SampleWindow(win, 'Thu', colour1), 0, wx.EXPAND),
            (SampleWindow(win, 'Fri', colour1), 0, wx.EXPAND),
            (SampleWindow(win, 'Sat', colour1), 0, wx.EXPAND),
            (SampleWindow(win, 'Sun', colour1), 0, wx.EXPAND)]
    for i in range(1, 13):
        for j in range(0, 8):
            if j == 0:
                list.append((SampleWindow(win, str(i), colour2), 0, wx.EXPAND))
            else:
                list.append((SampleWindow(win, coursename[i][j], colourList[colournum[i][j]]), 0, wx.EXPAND))
    gs.AddMany(list)
    return gs


class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, title=u"课程表", id=-1)
        self.SetIcon(wx.Icon('..\\var\\sys_logo\\ClassSche.ico', wx.BITMAP_TYPE_ICO))
        p = wx.Panel(self, -1)
        self.coursename = self.init()
        self.colournum = self.init1()
        self.sizer = makeGrid1(p, self.coursename, self.colournum)
        self.CreateStatusBar()
        self.SetStatusText("Resize this frame to see how the sizers respond...")
        p.SetSizer(self.sizer)
        self.sizer.Fit(p)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Fit()

        #这里在对courseList进行取值

    def TupleSmallFormat(self, strtuple):#将(1,2,3)这样的字符串变成类似输出的tuple
        return tuple(strtuple.split(','))

    def GetCourseList(self):
        filename = self.MurshroomServerAPI("MCOURSE|")
        if filename == '':
            return []
        reslist = codecs.open('..\\tmp\\' + filename, 'r', 'utf-8').read().split('\n')
        os.remove("..\\tmp\\" + filename)
        reslist = map(self.TupleSmallFormat, reslist)
        glist = []
        for line in reslist:
            if len(line) < 2: continue
            print line
            glist.append(line)
        return glist

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

    def OnCloseWindow(self, event):
        self.MakeModal(False)
        self.Destroy()

    def init(self):
        global courseList
        a = [["", "", "", "", "", "", "", ""], ["", "", "", "", "", "", "", ""], ["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""], ["", "", "", "", "", "", "", ""], ["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""], ["", "", "", "", "", "", "", ""], ["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""], ["", "", "", "", "", "", "", ""], ["", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", ""], ["", "", "", "", "", "", "", ""]]
        courseList = self.GetCourseList()
        for course in courseList:
            name = course[0]
            timelist = course[1].split(" ")
            for tim in timelist:
                t = tim.split("-")
                if len(t) <= 1: continue

                y = int(t[0]) + 1
                tmp = ""
                for i in range(len(t[1])):
                    tmp = tmp + t[1][i]
                    if i % 2 == 1:
                        x = int(tmp)
                        tmp = ""
                        a[x][y] = name
        return a

    def init1(self):
        a = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
        sum = 0
        for course in courseList:
            sum = sum + 1
            timelist = course[1].split(" ")
            for tim in timelist:
                t = tim.split("-")
                if len(t) <= 1: continue
                y = int(t[0]) + 1
                tmp = ""
                for i in range(len(t[1])):
                    tmp = tmp + t[1][i]
                    if i % 2 == 1:
                        x = int(tmp)
                        tmp = ""
                        a[x][y] = sum
        return a


class App(wx.App):
    def OnInit(self):
        win = Frame()
        win.CentreOnParent(wx.BOTH)
        win.Show(True)
        return True


def Test():
    app = wx.PySimpleApp()
    frame = Frame()
    frame.CenterOnParent(wx.BOTH)
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    Test()




