__author__ = 'guoaway'
#_*_encoding:utf-8_*_
import wx, os, thread, socket
import time, MurshroomServer, FileDownload, SoftList, Pro_Gua

butList = []
taskList = []
if not os.path.isfile("..\\etc\cilentsoft.list"):
    open("..\\etc\\cilentsoft.list", 'w').write("")
dirlist = open("..\\etc\\cilentsoft.list", 'r').read()
dirlist = dirlist.split('\n')
for softname in dirlist:
    ###直接把第一行略过了，到时候删掉吧
    print "<" + softname + ">"
    if len(softname) <= 2: continue
    butList.append("..\\var\\soft_logo\\" + softname + ".gif")
    taskList.append("..\\bin\\" + softname + ".bat")
butList.append("..\\var\\sys_logo\\addItem.gif")

sum = len(butList)
x = sum / 12
if sum % 12:
    x = x + 1
panelNum = x
clickNum = 0
FTPHOST = open("..\\etc\\sysconfig\\ftphost.conf", 'r').read()
IconPath = "..\\var\\sys_logo\\murshroom.ico"


class TaskBarIcon(wx.TaskBarIcon):
    ID_Minshow = wx.NewId()
    ID_Maxshow = wx.NewId()
    ID_Closeshow = wx.NewId()

    def __init__(self, frame):
        wx.TaskBarIcon.__init__(self)
        self.frame = frame
        self.SetIcon(wx.Icon(name=IconPath, type=wx.BITMAP_TYPE_ICO), u"校园蘑菇")  #wx.ico为ico图标文件
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.OnTaskBarLeftDClick) #定义左键双击
        self.Bind(wx.EVT_MENU, self.OnMinshow, id=self.ID_Minshow)
        self.Bind(wx.EVT_MENU, self.OnMaxshow, id=self.ID_Maxshow)
        self.Bind(wx.EVT_MENU, self.OnCloseshow, id=self.ID_Closeshow)

    def OnTaskBarLeftDClick(self, event=None):
        if self.frame.IsIconized():
            self.frame.Iconize(False)
        if not self.frame.IsShown():
            self.frame.Show(True)
        self.frame.Raise()
        if event is not None:
            self.OnMaxshow()


    def OnMinshow(self, event):
        self.frame.Iconize(True)


    def OnMaxshow(self, event=None):
        if self.frame.IsIconized():
            self.frame.Iconize(False)
        if not self.frame.IsShown():
            self.frame.Show(True)
        self.frame.Raise()
        if event is not None:
            self.OnTaskBarLeftDClick()

            #self.frame.Maximize(True) #最大化显示

    def OnCloseshow(self, event):
        self.frame.Close(True)

    # 右键菜单
    def CreatePopupMenu(self):
        menu = wx.Menu()
        menu.Append(self.ID_Minshow, u'最小化到托盘')
        menu.Append(self.ID_Maxshow, u"显示窗口")
        menu.Append(self.ID_Closeshow, u'退出')
        return menu


class Panel(wx.Panel):
    def __init__(self, parent, num, frame=None):
        wx.Panel.__init__(self, parent=parent, id=-1, size=(800, 600))
        if num != 0:
            self.SetPosition((800, 600))
        self.frame = frame
        self.img = wx.Image("..\\var\\jwc_login\\mainGUI_background.jpg", wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
        self.bmp = wx.StaticBitmap(self, id=-1, bitmap=self.img)
        self.x = num * 12
        self.y = self.x + 12
        self.num = num
        if self.y > butList.__len__():
            self.y = butList.__len__()
        self.AddButton()

    def AddButton(self):
        if self.num != 0:
            self.but1 = wx.Button(self.bmp, id=-1, label=u"上一页", pos=(250, 500), size=(100, 50))
            self.Bind(wx.EVT_BUTTON, self.ButtonClick, self.but1)
        if self.num != panelNum - 1:
            self.but2 = wx.Button(self.bmp, id=-1, label=u"下一页", pos=(400, 500), size=(100, 50))
            self.Bind(wx.EVT_BUTTON, self.ButtonClick1, self.but2)
        s = 100
        h = 50
        for i in range(self.x, self.y):
            print "use the image |" + butList[i] + "|"
            self.bimg = wx.Image(butList[i], wx.BITMAP_TYPE_GIF).ConvertToBitmap()
            bitname = wx.BitmapButton(self.bmp, -1, self.bimg, pos=(s, h), size=(100, 100), name=str(i))
            self.Bind(wx.EVT_BUTTON, self.TaskDeal, bitname)
            s += 150
            if (i + 1) % 4 == 0:
                s = 100
                h += 150


    def DoCommon(self, cmd):
        os.system(cmd)

    def TaskDeal(self, event):
        object = event.GetEventObject()
        name = object.GetName()
        x = int(name)
        print x
        self.frame.OnIconfiy("hh")
        if x == len(butList) - 1:
            sframe = SoftList.Frame(self)
            sframe.Show(True)
            return
        thread.start_new_thread(self.DoCommon, (taskList[x],))   #开启程序
        time.sleep(1)
        #thread.start_new_thread(self.DoCommon, (r"..\bin\.Cet46.bat",))   # 关闭程序


    def ButtonClick(self, event):
        global clickNum
        clickNum = clickNum - 1
        self.name = getattr(self.Parent, "panel" + str(clickNum))
        self.SetPosition((800, 600))
        self.name.SetPosition((0, 0))

    def ButtonClick1(self, event):
        global clickNum
        clickNum = clickNum + 1
        self.name = getattr(self.Parent, "panel" + str(clickNum))
        self.SetPosition((800, 600))
        self.name.SetPosition((0, 0))


class ChildFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent=parent, id=-1, pos=(450, 230), size=(600, 400))
        self.panel = wx.Panel(self, id=-1)
        self.panel.img = wx.Image("..\\var\\jwc_login\\upload.jpg", wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
        self.panel.bmp = wx.StaticBitmap(self.panel, id=-1, bitmap=self.panel.img)
        #self.textFont = wx.Font(10, family=wx.SCRIPT, style=wx.NORMAL, weight=wx.BOLD)
        self.DirText = wx.StaticText(self.panel.bmp, id=-1, pos=(90, 60), size=(320, 30))
        self.DirText.SetLabel(u"【注意】请选择全英文的文件名及路径上传！")
        self.textFont = self.DirText.GetFont()
        self.DirText.SetForegroundColour('white')
        self.DirText.SetBackgroundColour((28, 95, 64))
        self.DirText.SetFont(self.textFont)
        #self.DirText.SetBackgroundColour("gray")
        self.but = wx.Button(self.panel.bmp, id=-1, label=u"浏 览", pos=(430, 40), size=(100, 30))
        self.but.SetBackgroundColour((28, 95, 64))
        self.but.SetForegroundColour('white')
        self.but.SetFont(self.textFont)
        self.ftpGua = wx.Gauge(self.panel.bmp, -1, 100, name="gauge", pos=(48, 130), size=(480, 30))
        self.ftpGua.Show(False)
        self.Bind(wx.EVT_BUTTON, self.OpenFileDialog, self.but)
        self.but1 = wx.Button(self.panel.bmp, id=-1, label=u"上 传", pos=(430, 80), size=(100, 30))
        self.but1.SetBackgroundColour((28, 95, 64))
        self.but1.SetForegroundColour('white')
        self.but1.SetFont(self.textFont)
        self.Bind(wx.EVT_BUTTON, self.IWantToUpload, self.but1)
        self.tongzhi = wx.StaticText(self.panel.bmp, id=-1, pos=(110, 160))
        self.tongzhi.SetLabel(u'具体上传方式以及上传软件所需符合的规范,\n      请参见帮助菜单栏下的用户文档。')
        tx, ty = self.tongzhi.GetSize()
        self.tongzhi.SetPosition((300-tx / 2, 160))
        self.tongzhi.SetBackgroundColour((28, 95, 64))
        self.tongzhi.SetForegroundColour("white")
        self.closebut = wx.Button(self.panel.bmp, id=-1, label=u'关  闭', pos=(250, 275), size=(90, 40))
        self.closebut.SetBackgroundColour((28, 95, 64))
        self.closebut.SetForegroundColour('white')
        self.closebut.SetFont(self.textFont)
        self.closebut.Show(False)
        self.closetext = wx.StaticText(self.panel.bmp, id=-1, pos=(240, 250))
        self.closetext.SetBackgroundColour((28, 95, 64))
        self.closetext.SetForegroundColour('white')
        self.closetext.SetFont(self.textFont)
        self.Bind(wx.EVT_BUTTON, self.CloseFrame, self.closebut)
        self.paths = ""

    def CloseFrame(self, event):
        self.Destroy()

    def OpenFileDialog(self, event):
        dlg = wx.FileDialog(
            self, message=u"选择所要上传的文件",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard="",
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
        )
        if dlg.ShowModal() == wx.ID_OK:
            self.paths = dlg.GetPath()
            if len(self.paths) > 40:
                self.DirText.SetLabel('%s\n' % self.paths[-39::1])
            else:
                self.DirText.SetLabel("%s\n" % self.paths)
        dlg.Destroy()

    #这里我们要创建对文件进行上传。
    #接下去的就是要做一个界面，用来选择文件上传的对话框界面
    def HowManyIUpload(self):#暂时未被使用
        self.ftpGua.Show(True)
        tsize = os.path.getsize(self.paths)
        print tsize
        fsize = 0
        usingtime = 0
        while True:
            if self.flagGua == True:
                self.ftpGua.SetValue(100)
                self.closebut.Show(True)
                self.closetext.SetLabel(u"恭喜您！上传成功了~")
                return
            if fsize > tsize:
                fsize = tsize - 1024
                if fsize < 0:
                    fsize = 0
            self.ftpGua.SetValue(fsize * 100.0 / tsize)
            if usingtime > 180:
                if tsize >= 1024.0 * 1024 * 15:
                    self.closetext.SetLabel(u"文件有点大~，请稍等...")
                else:
                    self.closetext.SetLabel(u"网速不给力啊！！！")
            time.sleep(2)
            fsize += 1024 * 100 * 2
            usingtime += 2


    def IWantToUpload(self, event):
        #设置一个进度条
        if os.path.isfile(self.paths):
            self.flagGua = False
            #thread.start_new_thread(self.HowManyIUpload, ())
            self.closetext.SetLabel(u"上传文件期间，系统会有点卡~")
            FileDownload.UpLoadFTPFile(FTPHOST, self.paths)
            self.closetext.SetLabel(u"恭喜您！上传成功了~")
            self.closebut.Show(True)
        else:
            self.closetext.SetLabel(u"请选择一个文件上传!")


class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, id=-1, title=u"校园蘑菇主界面", pos=(100, 100), size=(800, 600),
                          style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
        self.Init()
        self.AddMenu()
        self.AddBind()

    def Init(self):
        for i in range(0, panelNum):
            setattr(self, "panel" + str(i), Panel(self, i, self))
            self.name = getattr(self, "panel" + str(i))
            #self.name.Hide()
            #self.name=getattr(self, "panel0")

        self.SetIcon(wx.Icon(IconPath, wx.BITMAP_TYPE_ICO))
        self.taskBarIcon = TaskBarIcon(self)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_ICONIZE, self.OnIconfiy)

    def OnClose(self, event):
        self.taskBarIcon.Destroy()
        self.Destroy()

    def OnIconfiy(self, event):
        self.Hide()
        try:
            event.Skip()
        except Exception, ex:
            pass

    def AddBind(self):
        #self.Bind(wx.EVT_BUTTON, self.OnButtonClick, self.button)
        self.Bind(wx.EVT_MENU, self.UploadUserInfo, self.mbut1)
        self.Bind(wx.EVT_MENU, self.UploadSoftInfo, self.mbut2)
        self.Bind(wx.EVT_MENU, self.StartMS, self.mbut3)
        self.Bind(wx.EVT_MENU, self.About_Us, self.mbut4)
        self.Bind(wx.EVT_MENU, self.About_Our_Soft, self.mbut5)
        self.Bind(wx.EVT_MENU, self.Soft_help, self.mbut6)

    def StartMS(self, event):
        if self.mbut3.GetLabel() == u"自动成绩更新":
            self.mbut3.SetItemLabel(u"关闭自动成绩更新")
        else:
            self.mbut3.SetItemLabel(u"自动成绩更新")
        msconn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = '127.0.0.1'
        port = int(open("..\\etc\\sysconfig\\socket_port", 'r').read())
        try:
            msconn.connect((host, port))
        except Exception, e:
            print "connect to server failed.", e
            return
        print "connect murshroom server cilent..."
        msconn.sendall("START|")
        time.sleep(1)
        msconn.close()

    def UploadSoftInfo(self, event):
        self.childframe = ChildFrame(self)
        self.childframe.Show(True)

    def UploadUserInfo(self, event):
        if self.mbut1.GetLabel() != u'一键导入成绩': return
        print "create the thread to load your information"
        if os.path.isfile("..\\etc\\sysconfig\\shadow"):
            account, password = open('..\\etc\\sysconfig\\shadow', 'r').read().split(',')
        self.INFOGUA = Pro_Gua.Frame(self)
        self.INFOGUA.Show(True)
        time.sleep(1)
        MurshroomServer.InfoUploadScore(account, password, self.INFOGUA)
        self.mbut1.SetItemLabel(u"成绩已导入")

    def About_Us(self, event):
        self.childframe = wx.Frame(self, id=-1, title=u"关于我们", size=(610, 430), pos=(420, 220))
        self.childframe.Show(True)
        self.img = wx.Image("..\\var\\sys_logo\\about_us.jpg", wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
        self.bmp = wx.StaticBitmap(parent=self.childframe, bitmap=self.img, size=(600, 400))

    def About_Our_Soft(self, event):
        self.childframe = wx.Frame(self, id=-1, title=u"关于我们", size=(610, 430), pos=(420, 220))
        self.childframe.Show(True)
        self.img = wx.Image("..\\var\\sys_logo\\about_our_soft.jpg", wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
        self.bmp = wx.StaticBitmap(parent=self.childframe, bitmap=self.img, size=(600, 400))

    def Soft_help(self, event):
        self.childDialog = wx.FileDialog(self, message=u"下载到", defaultDir=os.getcwd(), defaultFile=u"用户手册.pdf",
                                         wildcard="", style=wx.SAVE | wx.OVERWRITE_PROMPT | wx.CHANGE_DIR,
                                         pos=((360, 180)))
        self.paths = ""
        if self.childDialog.ShowModal() == wx.ID_OK:
            self.paths = self.childDialog.GetPath()
            print self.paths
            try:
                FileDownload.DownLoadSingleFile("ftp://upload@" + FTPHOST + "/murshroom_manual.pdf",
                                                os.path.dirname(self.paths) + "\\", os.path.basename(self.paths))
            except Exception, ex:
                print "[ERROR]MainGUI in download file."


    def AddMenu(self):
        menuBar = wx.MenuBar()
        menu1 = wx.Menu()
        menu2 = wx.Menu()
        menuBar.Append(menu1, u"内置功能")
        menuBar.Append(menu2, u"帮助")
        self.mbut1 = menu1.Append(-1, u"一键导入成绩")
        self.mbut2 = menu1.Append(-1, u"共享我的软件")
        self.mbut3 = menu1.Append(-1, u"自动成绩更新")
        self.mbut4 = menu2.Append(-1, u"关于我们")
        self.mbut5 = menu2.Append(-1, u"关于校园蘑菇")
        self.mbut6 = menu2.Append(-1, u"用户文档下载")
        self.SetMenuBar(menuBar)

    def SetTextStytel(self, txt):
        txt.SetForegroundColour('0')
        txt.SetBackgroundColour('0')
        font = wx.Font(13, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        txt.SetFont(font)


def TestFrame():
    app = wx.PySimpleApp()
    frame = Frame()
    frame.Centre()
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    TestFrame()




