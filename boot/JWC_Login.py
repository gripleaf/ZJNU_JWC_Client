__author__ = 'guoaway'
#_*_encoding:utf-8_*_

import wx, Jwc_InfoCollect, MurshroomServer, FileDownload
import random, os

PASSWDPATH = r'..\etc\passwd'
SERVER = None
UINFO = {}
IconPath = "..\\var\\sys_logo\\murshroom.ico"


class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, id=-1, title=u'校园蘑菇登录界面', pos=(100, 100), size=(380, 320),
                          style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
        self.SetIcon(wx.Icon(IconPath, wx.BITMAP_TYPE_ICO))
        self.InitBegin()
        self.AddElement()
        self.AddBind()
        self.InitEnd()
        self.CheckSystemUpdate()

    def CheckSystemUpdate(self):
        if FileDownload.IfHasNewVersion():
            ted = wx.MessageDialog(self, u"检测到新的校园蘑菇版本，是否需要更新？更新是为了修复原有的错误，并提供最新的服务！", caption=u"更新提醒",
                                   style=wx.YES | wx.NO)
            if ted.ShowModal() == wx.ID_YES:
                FileDownload.AutoCheckUpdate()


    def InitEnd(self):
        if os.path.isfile(PASSWDPATH):
            self.jizhu.SetValue(True)
            try:
                accout, passwd = open(PASSWDPATH, 'r').read().split(',')
                self.account.SetValue(accout)
                self.password.SetValue(passwd)
            except Exception, ex:
                pass
        else:
            self.jizhu.SetValue(False)

    def InitBegin(self):
        imglist = os.listdir("..\\var\\jwc_login\\login_bp")
        for i in imglist:
            if i.startswith("main"):
                self.img1 = wx.Image("..\\var\\jwc_login\\login_bp\\" + i, wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
        else:
            self.img1 = wx.Image("..\\var\\jwc_login\\login_bp\\" + imglist[random.randint(0, len(imglist) - 1)],
                                 wx.BITMAP_TYPE_JPEG).ConvertToBitmap()


    def AddElement(self):
        self.panel = wx.Panel(self, -1)
        self.bmp = wx.StaticBitmap(parent=self.panel, bitmap=self.img1)
        self.account = wx.TextCtrl(self.bmp, -1, value=u"请输入账号", pos=(100, 105), size=(180, 25))
        self.password = wx.TextCtrl(self.bmp, -1, pos=(100, 142), size=(180, 25), style=wx.TE_PASSWORD)
        self.but = wx.Button(self.bmp, id=-1, label=u"登  录", pos=(140, 220), size=(100, 30))
        self.jizhu = wx.CheckBox(self.bmp, id=-1, label=u"记住密码", pos=(200, 190), size=(70, 20), style=0,
                                 name="checkBox")
        self.jwc_login = wx.CheckBox(self.bmp, id=-1, label=u"首次登录", pos=(120, 190), size=(70, 20), style=0,
                                     name="checkBox1")
        self.login_label = wx.StaticText(self.bmp, -1, label=u"", pos=(145, 170), size=(85, 20))
        self.login_label.Show(False)


    def SetTextStytel(self, tex):
        tex.SetForegroundColour('0')
        tex.SetBackgroundColour('0')
        font = wx.Font(15, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        tex.SetFont(font)

    def AddBind(self):
        self.account.Bind(wx.EVT_LEFT_DOWN, self.ClickLogin)
        self.password.Bind(wx.EVT_LEFT_DOWN, self.ClickPassword)
        self.Bind(wx.EVT_BUTTON, self.Jwc_LogIn, self.but)


    def ExitTheFrame(self):#exit the GUI, go to the main GUI
        print "exit jwc_login frame..."
        open("..\\etc\\sysconfig\\shadow", 'w').write(self.account.GetValue() + ',' + self.password.GetValue())
        if self.jizhu.GetValue():
            try:
                f = open(PASSWDPATH, 'w')
                f.write(self.account.GetValue() + ',' + self.password.GetValue())
            finally:
                f.close()
        else:
            if os.path.isfile(PASSWDPATH):
                os.remove(PASSWDPATH)
        self.Destroy()

    def Jwc_LogIn(self, event):
        global SERVER
        but = event.GetEventObject()
        if but.GetLabel() == u"登  录":
            but.SetLabel(u"正在登录")
        else:
            print "don't touch it"
            return
        try:
            print  self.password.GetValue() + " " + self.account.GetValue()
            UINFO['StudentID'] = self.account.GetValue()
            UINFO['password'] = self.password.GetValue()
            try:
                int(UINFO['StudentID'])
            except Exception, ex:
                self.login_label.SetLabel(u"账号格式错误")
                return
            if UINFO['password'].count("'") > 0 or UINFO['password'].count("&"):
                self.login_label.SetLabel(u"密码含'或&等非法字符")
                return
                #todo here we should judge if we need login first in jwc or murshroom server?
            if self.jwc_login.GetValue():
                SERVER = Jwc_InfoCollect.JWC_SYS()
                try:
                    SERVER.CilentAPI("LOGIN", ['0', UINFO['password'], "student", UINFO['StudentID']])
                except Exception, ex:
                    self.login_label.SetLabel(u"无法连接上教务处服务器")
                    #print JWC.GetNameInfo()
                if SERVER.ACCESS:
                    print "login success in jwc server"
                    name = SERVER.GetNameInfo()
                    try:
                        open(r'..\etc\UserName.conf', 'w').write(name.encode("utf-8"))
                    except IOError, ioer:
                        print ioer
                    print "welcome to use murshroom,", name
                    #self.login_label.SetLabel(u"welcome!")
                    self.ExitTheFrame()
                else:
                    print "login failed in jwc server"
                    self.login_label.SetLabel(u"账号或密码错误")
            else:

                SERVER = MurshroomServer.MurshroomServer()
                try:
                    SERVER.ClientAPI("LOGIN", ["", UINFO['StudentID'], UINFO['password']])
                except Exception, ex:
                    self.login_label.SetLabel(u"无法连接上蘑菇服务器")
                if SERVER.ACCESS:
                    print "login success in murshroom server"
                    name = SERVER.ClientAPI("MUSERINFO", [])
                    name = name[0][1]
                    try:
                        open(r"..\etc\UserName.conf", 'w').write(name.encode("utf-8"))
                    except IOError, ioer:
                        print ioer
                    print "welcome to use murshroom,", name
                    #self.login_label.SetLabel(u"welcome!")
                    self.ExitTheFrame()
                else:
                    print "login failed in murshroom server"
                    self.login_label.SetLabel(u"账号或密码错误")
        except IOError, ec:
            print "[ERROR] login failed", ec
        finally:
            self.login_label.Show(True)
            but.SetLabel(u"登  录")


    def ClickLogin(self, event):
        self.account.SetValue("")
        event.Skip();

    def ClickPassword(self, event):
        self.password.SetValue("")
        event.Skip();


#self.Bind(wx.EVT_BUTTON, self.OnButtonClick, self.button)
#self.button.Bind(wx.EVT_ENTER_WINDOW, self.OnEnterWindow)
#self.button.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)
#self.button.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)

class App(wx.App):
    def OnInit(self):
        self.frame = Frame()
        self.frame.Centre()
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True


def InitLogin():
    global SERVER
    app = wx.PySimpleApp()
    frame = Frame()
    frame.Centre()
    frame.Show(True)
    app.SetTopWindow(frame)
    app.MainLoop()
    return SERVER


if __name__ == '__main__':
    InitLogin()


