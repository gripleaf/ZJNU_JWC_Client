__author__ = 'guoaway'
#_*_encoding:utf-8_*_

import wx, os, FileDownload


infolist = []
LOGOPath = "..\\var\\soft_logo\\"    #软件logo的路径
INFOPath = '..\\var\\soft_info\\'    #软件对应信息的路径
CILEPath = '..\\etc\\cilentsoft.list'   #已经安装的软件路径
LogoList = []          #全局变量来记录未安装软件的logo列表
choicenum = -1         #选择了未安装的软件列表中的软件编号
InfoList = []          #未安装软件的信息列表
IconPath = "..\\var\\sys_logo\\additem.ico"


class ListCtrl(wx.ListCtrl):
    def __init__(self, parent):
        self.list = wx.ListCtrl.__init__(self, parent, pos=(0, 0), size=(700, 500),
                                         style=wx.LC_SMALL_ICON | wx.LC_AUTOARRANGE)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.list)
        self.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.NORMAL, wx.NORMAL, False, u'宋体'))
        il = wx.ImageList(100, 100, True)
        tmpList = os.listdir(LOGOPath)
        self.logoList = []
        self.dirList = []
        global infolist
        infolist = []
        for sname in tmpList:
            if self.IsSoftExit(sname.split('.')[0]): continue
            print sname
            self.logoList.append(sname)
            bmp = wx.Bitmap(LOGOPath + sname, wx.BITMAP_TYPE_GIF)
            self.dirList.append(INFOPath + sname.split('.')[0] + ".info")
            data = open(INFOPath + sname[:-4:1] + ".info").read().decode("UTF_8")
            litinfo = ""
            for x in data:
                if len(litinfo) == 35:
                    break
                litinfo += x
            if len(litinfo) < 35:
                litinfo = litinfo + ' ' * (35 - len(litinfo))
            litinfo = litinfo + "..."
            infolist.append(litinfo)
            il_max = il.Add(bmp)
        self.AssignImageList(il, wx.IMAGE_LIST_SMALL)
        for x in range(len(infolist)):
            self.InsertImageStringItem(x, infolist[x], x)
        global InfoList, LogoList
        InfoList = self.dirList
        LogoList = self.logoList

    def IsSoftExit(self, sname):
        #if True: return False
        soft_list = open(CILEPath, 'r').read().split('\n')
        for item in soft_list:
            if sname == item:
                return True
        return False

    def OnItemSelected(self, event):
        global choicenum
        choicenum = event.GetIndex()


class Frame(wx.Frame):
    def __init__(self, parent=None):
        wx.Frame.__init__(self, parent=parent, id=-1, title=u'软件列表', pos=(50, 20), size=(700, 600),
                          style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
        self.SetIcon(wx.Icon(name=IconPath, type=wx.BITMAP_TYPE_ICO))
        self.InitFrame()
        self.AddElment()

    def InitFrame(self):
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnClose(self, event):
        self.Destroy()

    def IsSoftExit(self, sname):
        print sname
        #if True: return False
        soft_list = open(CILEPath, 'r').read().split('\n')
        for item in soft_list:
            if sname == item:
                return True
        return False

    def AddElment(self):
        self.panel = wx.Panel(self, id=-1, pos=(0, 0), size=(700, 500))
        self.list = ListCtrl(self.panel)
        self.panel1 = wx.Panel(self, id=-1, pos=(0, 500), size=(700, 200))
        self.but = wx.Button(self.panel1, id=-1, label=u"查看详情", pos=(220, 20), size=(100, 30))
        self.Bind(wx.EVT_BUTTON, self.ShowInfo, self.but)
        self.but2 = wx.Button(self.panel1, id=-1, label=u"直接安装", pos=(370, 20), size=(100, 30))
        self.Bind(wx.EVT_BUTTON, self.SetupSoft, self.but2)

    def ShowInfo(self, event):
        global choicenum
        if choicenum != -1:
            self.infoframe = wx.Frame(self, id=-1, title=u"软件信息详情", size=(600, 600),
                                      style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
            self.infoframe.Show(True)
            self.infopanel = wx.Panel(self.infoframe, id=-1, pos=(0, 0), size=(600, 150))
            self.img = wx.Bitmap(LOGOPath + LogoList[choicenum], wx.BITMAP_TYPE_GIF)
            wx.StaticBitmap(parent=self.infopanel, bitmap=self.img, pos=(250, 0), size=(100, 100))
            self.but3 = wx.Button(self.infoframe, id=-1, label=u"安装", pos=(250, 530), size=(100, 30))
            self.Bind(wx.EVT_BUTTON, self.SetupSoft, self.but3)
            self.SetTextStytel(self.infoframe)
            data = open(InfoList[choicenum]).read().decode("UTF_8")
            i = 0
            v = ""
            for x in data:
                if x != '\n':
                    v = v + x
            wx.TextCtrl(self.infoframe, id=-1, value=v, pos=(0, 100), size=(600, 400),
                        style=wx.TE_LINEWRAP | wx.TE_MULTILINE | wx.TE_READONLY)


    def SetupSoft(self, event):
        if choicenum < 0 or choicenum >= len(LogoList):
            return
        objbut = event.GetEventObject()
        if objbut.GetLabel() == u"直接安装" or objbut.GetLabel() == u"安装":
            objbut.SetLabel(u"正在安装")
            filename, lazy = LogoList[choicenum].split('.')
            FileDownload.InstallNewSoft(filename)
            objbut.SetLabel(u"安装完成")
        else:
            pass
            #filename = filename + '.list'
            #filelist = urllib.urlopen(MSHOST + "/downloadfile/soft_list/" + filename).split('\n')

    def SetTextStytel(self, tex):
        tex.SetForegroundColour('0')
        tex.SetBackgroundColour('0')
        font = wx.Font(13, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        tex.SetFont(font)


class App(wx.App):
    def OnInit(self):
        self.frame = Frame()
        self.frame.Show(True)
        self.frame.Centre()
        self.SetTopWindow(self.frame)
        return True


if __name__ == '__main__':
    app = App()
    app.MainLoop()




