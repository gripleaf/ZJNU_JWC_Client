__author__ = 'guoaway'
#_*_encoding:utf-8_*_
import wx, socket, sys, os, time, threading, thread

MESSAGE = ""


class Frame(wx.Frame, threading.Thread):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, id=-1, title=u'消息框', size=(250, 180),
                          style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.STAY_ON_TOP)
        threading.Thread.__init__(self)
        self.message = self.GetMessage()
        width, height = wx.DisplaySize()
        self.SetPosition((width - self.GetSize()[0], height - self.GetSize()[1] - 45))
        mesg = self.GetString(1)
        self.panel1 = wx.Panel(self, id=-1, pos=(0, 0), size=(250, 80))
        self.panel2 = wx.Panel(self, id=-1, pos=(0, 80), size=(250, 70))
        self.t = wx.StaticText(self.panel1, id=-1, label="", pos=(10, 35), size=(250, 30),
                               style=wx.TE_LINEWRAP | wx.TE_MULTILINE)
        self.t.SetLabel(mesg)
        self.SetTextStytel(self.t)
        self.but = wx.Button(self.panel2, id=-1, label=u"查看详情", pos=(75, 30), size=(100, 30))
        self.Bind(wx.EVT_BUTTON, self.Click, self.but)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.runFlag = False
        self.start()

    def run(self):
        time.sleep(3)
        if self.runFlag == False:
            self.Destroy()

    def OnClose(self, event):
        self.runFlag = False
        self.Destroy()

    def Click(self, event):
        self.runFlag = True
        self.SetSize((500, 300))
        self.SetPosition((500, 300))
        self.panel1.Destroy()
        self.panel2.Destroy()
        self.BuildNewPanel()

    def BuildNewPanel(self):
        self.panel = wx.Panel(self, id=-1, size=(500, 300), pos=(0, 0))
        self.txt = wx.TextCtrl(self.panel, id=-1, value=self.GetString(2), pos=(0, 0), size=(500, 300),
                               style=wx.TE_LINEWRAP | wx.TE_MULTILINE | wx.TE_READONLY)
        self.SetTextStytel(self.txt)

    def GetMessage(self):
        global MESSAGE
        return MESSAGE

    def GetString(self, num):
        x = self.message
        if num == 1:
            r = len(x)
            if r > 10:
                r = 10
            return x[0:r] + "...."
        if num == 2:
            return x

    def SetTextStytel(self, tex):
        tex.SetForegroundColour('0')
        tex.SetBackgroundColour('0')
        font = wx.Font(10, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        tex.SetFont(font)


def RunApp():
    app = wx.PySimpleApp()
    frame = Frame()
    frame.Show(True)
    app.SetTopWindow(frame)
    app.MainLoop()


def RunWork():
    RunApp()


def CheckPort():
    sport = int(open("..\\etc\\sysconfig\\socket_port", 'r').read())
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sk.settimeout(2)
        sk.bind(('127.0.0.1', sport))
        sk.close()
    except Exception, ex:
        #print "murshroom is alive.", ex
        return True
        #print "murshroom is dead."
    return False


def NotificationScoketListen():
    socket.setdefaulttimeout(144000)
    global MESSAGE
    sockport = open("..\\etc\\sysconfig\\Notif_socketport", 'r').read()
    nosocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "[notification]socket is created."
    try:
        nosocket.bind(("127.0.0.1", int(sockport)))
    except socket.error, msg:
        print "[no ERROR]:Bind failed.Error Code:", msg[0], 'message:', msg[1]
        sys.exit()
    print "[notification]socket bind complete."
    nosocket.listen(3)
    socketFlag = True
    while True:
        try:
            print "we are listen"
            conn, addr = nosocket.accept()    #此处定义数据接收规范
            print "get the connect"
        except Exception, e:
            print "[notification]timeout..."
        if addr[0] != '127.0.0.1':
            conn.sendall('[notification]error connection')
            break
        print "recive data"
        data = conn.recv(4096)
        print data
        if len(data) < 30 and os.path.isfile("..\\tmp\\" + data):
            MESSAGE = open("..\\tmp\\" + data).read()
        else:
            MESSAGE = data
        thread.start_new_thread(RunApp, ())
    conn.close()
    nosocket.close()


def NotificationMainWork():
    thread.start_new_thread(NotificationScoketListen, ())
    while True:
        time.sleep(10)


if __name__ == '__main__':
    NotificationMainWork()
    #RunWork()


