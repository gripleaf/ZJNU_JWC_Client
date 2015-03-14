__author__ = 'glcsnz123'
#_*_encoding:utf-8_*_
import urllib, urllib2, cookielib, hashlib, time, socket, os
import Jwc_InfoCollect, threading, thread, sys, random
#todo: here we create the args
HOST = open("..\\etc\\sysconfig\\mshost.conf", 'r').read()
HBEAT = "/HeartBeat.php"

AskFVC = "/AskforVerifyCode.php"

LOGINDict = {"StuName": "", "StudentID": 1, "password": 1, "zzzaskdicturl": "/VerifyRegister.php",
             "zzzcodenumber": "utf-8"}
DJKSDict = {"Rating_Cate": "0", "Rating_Name": "0", "Rating_Score": "0", "zzzaskdicturl": "/upload/rank.php",
            "zzzcodenumber": "utf-8"}
SCOREDict = {"CourseName": "0", "CourseCredit": "0", "GPoint": 0.0, "Score": "0", "TermID": "0",
             "zzzaskdicturl": "/upload/score.php", "zzzcodenumber": "utf-8"}
CINFODict = {"CourseCredit": "0", "CourseName": "0", "CourseTime": "0", "Location": "0",
             "Teacher": "0", "TermID": "0", "zzzaskdicturl": "/upload/courseinfo.php", "zzzcodenumber": "utf-8"}
SELECTIONDict = {"CourseName": "0", "StudentID": "0", "TermID": "0", "zzzaskdicturl": "/upload/selection.php",
                 "zzzcodenumber": "utf-8"}
EXAMINFODict = {"CourseName": "0", "ExamLocation": "0", "ExamTime": "0", "TermID": "0",
                "zzzaskdicturl": "/upload/examinfo.php", "zzzcodenumber": "utf-8"}

#here view the information
MTERMSDict = {"TermID": "20131", "zzzaskdicturl": "/ViewInfo/VTermScore.php", "zzzcodenumber": "utf-8"}
MTOTALSDict = {"zzzaskdicturl": "/ViewInfo/VTotalScore.php", "zzzcodenumber": "utf-8"}
MRANKSDict = {"zzzaskdicturl": "/ViewInfo/VRankScore.php", "zzzcodenumber": "utf-8"}
MUSERINFODict = {"zzzaskdicturl": "/ViewInfo/VUserInfo.php", "zzzcodenumber": "utf-8"}
MCOURSEDict = {"zzzaskdicturl": "/ViewInfo/VTermClass.php", "zzzcodenumber": "utf-8"}

#here is auto task infomation
AUTOSDict = {"zzzaskdicturl": "/HeartBeat.php", "zzzuploadurl": "/upload/mark_examinfo.php", "zzzcodenumber": "utf-8"}

HEADERS = [('User-agent',
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31'),
           ("Cache-Control", "max-age=0"), ("Host", "localhost"),
           ("Connection", "keep-alive"), ("Content-Type", "application/x-www-form-urlencoded "),
           ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")]
TRANSLATEDict = {"LOGIN": "Murshroom_Login", "DJKS": "UpLoadUserInfo", "SCORE": "UpLoadUserInfo",
                 "CINFO": "UpLoadUserInfo", "SELECTION": "UpLoadUserInfo", "EXAMINFO": "UpLoadUserInfo",
                 "MTERMS": "GetServerInfo", "MTOTALS": "GetServerInfo", "MUSERINFO": "GetServerInfo",
                 "MCOURSE": "GetServerInfo", "MRANKS": "GetServerInfo", "AUTOS": "TaskAUTOS", "START": "StartRUN"}

#un todo
class MurshroomServerArgs():
    def __init__(self):
        self.Init()

    def Init(self):#此处需要备份上述的参数列表
        self.HOST = HOST
        self.LOGINDict = LOGINDict
        self.DJKSDict = DJKSDict
        self.SCOREDict = SCOREDict
        self.CINFODict = CINFODict
        self.SELECTIONDict = SELECTIONDict
        self.EXAMINFODict = EXAMINFODict
        self.MTERMSDict = MTERMSDict
        self.MTOTALSDict = MTOTALSDict
        self.AUTOSDict = AUTOSDict
        self.HEADERS = HEADERS
        self.MUSERINFODict = MUSERINFODict
        self.MRANKSDict = MRANKSDict
        self.MCOURSEDict = MCOURSEDict


class MurshroomServer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.InitCookie(HEADERS)
        self.msargs = MurshroomServerArgs()
        self.runFlag = True
        self.StartFlag = False
        self.sys_name = "MurshroomServer"

    def InitCookie(self, HEADERS):
        self.ACCESS = False
        self.cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        self.opener.addheaders = HEADERS
        urllib2.install_opener(self.opener)
        urllib2.socket.setdefaulttimeout(10)

    def AskForVerifyCode(self):
        #print HOST + AskFVC
        vcode = urllib2.urlopen(HOST + AskFVC).read()
        m = hashlib.md5()
        m.update(vcode)
        return m.hexdigest()

    #murshroom server 统一的接口
    def ClientAPI(self, func, args=[]):
        try:
            askdict = getattr(self.msargs, func + 'Dict', {})
            askkey = askdict.keys()
            askkey.sort()
            tmpstr = ""
            for i in range(0, len(args)):
                askdict[askkey[i]] = args[i]
                if func == "LOGIN": continue
                tmpstr = tmpstr + askkey[i] + " : " + args[i] + "|"
            print tmpstr
            func = getattr(self, TRANSLATEDict[func], self.Error)
            return func(askdict)
        except IOError, e:
            return e

    def Error(self):
        return 'wrong function name'

    def Murshroom_Login(self, askdict={}):
        self.ACCESS = False
        if len(askdict.keys()) == 0:
            askdict = self.msargs.LOGINDict
            if os.path.isfile("..\\etc\sysconfig\\shadow"):
                account, password = open("..\\etc\sysconfig\\shadow", 'r').read().split(',')
                askdict['StudentID'] = account
                askdict['password'] = password
        vcode = self.AskForVerifyCode()
        askdict['code_md5'] = vcode
        pst_data = urllib.urlencode(askdict)
        req = urllib2.Request(HOST + askdict['zzzaskdicturl'], pst_data)
        html = urllib2.urlopen(req).read().decode(askdict['zzzcodenumber'])
        if html.count("success") > 0:
            self.msargs.LOGINDict = askdict;
            self.ACCESS = True
        return html

    def HeartBeat(self, expe=True):
        try:
            html = urllib2.urlopen(HOST + HBEAT).read()
        except Exception, ex:
            print self.Murshroom_Login() + ' again 106'
            return self.HeartBeat(False)
        return html

    def TaskAUTOS(self, asktask):
        print "auto run task" + asktask
        frequency = int(asktask.split(',')[1])
        jwc = Jwc_InfoCollect.JWC_SYS()
        year, tid = GetPreTermID()
        while True:
            jwc.CilentAPI("LOGIN",
                          [0, self.msargs.LOGINDict['password'], "student", self.msargs.LOGINDict['StudentID']])
            asklist = jwc.CilentAPI("VTERMS", [tid, year])
            for cask in asklist:
                #print "SCORE:", UnionString(map(FormatEncode, cask))
                print "SCORE:", UnionString(map(FormatEncode, [cask[1], cask[2], cask[-1], cask[3], year + tid]))
                reply = self.ClientAPI("SCORE",
                                       map(FormatEncode, [cask[1], cask[2], cask[-1], cask[3], year + tid])), '117'
                #此处要求弹出消息提醒框
                if reply[0].count("success") > 0:
                    mesg = cask[1] + u"更新了!\n绩点： " + cask[-1] + u"   成绩： " + cask[3] + "\n"
                    print mesg
                    mesg = self.CreateRandomFile(mesg)
                    self.MSSocketAPI(mesg)
                else:
                    print reply
            time.sleep(frequency)

    def GetServerInfo(self, askdict):
        html = self.GetUserInfo(askdict)
        result = html.split('|')
        reslist = []
        for item in result:
            tmplist = item.split(',')
            reslist.append(tuple(tmplist))
        return reslist

    def GetUserInfo(self, askdict, expe=True):
        vcode = self.AskForVerifyCode()
        askdict['code_md5'] = vcode
        pst_data = urllib.urlencode(askdict)
        req = urllib2.Request(HOST + askdict['zzzaskdicturl'], pst_data)
        try:
            html = urllib2.urlopen(req).read().decode(askdict['zzzcodenumber'])
            if html.count("login") > 0 or html.count('ask for code') > 0:
                if expe == False:
                    return ''
                print self.Murshroom_Login(), 'again in GetUserInfo'
                html = self.GetUserInfo(askdict)
                return html
            return html
        except Exception, ex:
            if expe:
                print "[ERROR] try to restart the murshroom server...", ex
                self.InitCookie(HEADERS)
                self.Murshroom_Login()
                print "start ok! redo the task..."
                return self.UpLoadUserInfo(askdict, expe=False)
            else:
                return "[ERROR] fail to restart the task in getuserinfo....leaving..."

    def UpLoadUserInfo(self, askdict, expe=True):
        vcode = self.AskForVerifyCode()
        askdict['code_md5'] = vcode
        pst_data = urllib.urlencode(askdict)
        req = urllib2.Request(HOST + askdict['zzzaskdicturl'], pst_data)
        try:
            html = urllib2.urlopen(req, timeout=10).read().decode(askdict['zzzcodenumber'])
            if html.count("login") > 0:
                if expe == False:
                    return ''
                print self.Murshroom_Login(), 'again in UpLoadUserInfo'
                html = self.UpLoadUserInfo(askdict, False)
                return html
            return html
        except Exception, ex:
            if expe:
                print 'try to restart the murshroom server...'
                self.InitCookie(HEADERS)
                self.Murshroom_Login()
                print "start ok! redo the task..."
                return self.UpLoadUserInfo(askdict, expe=False)
            else:
                return "fail to restart the task in uploaduserinfo"

    #murshroom server 的socket接口，用于给非系统调用相应的函数
    def CreateRandomFile(self, mesg):
        filename = ''
        for i in range(16):
            filename += str(random.randint(0, 10))
        if type(mesg) == type([0, 1]):
            data = ''
            for line in mesg:
                if type(line) == type((1, 2, 3)):
                    stu = ''
                    for item in line:
                        stu += item + ','
                    stu = stu[0:-1:1]
                    stu += '\n'
                    print stu
                    data += stu
                else:
                    data += line
            print type(data)
            open('..\\tmp\\' + filename, 'w').write(data.encode('utf-8'))
        else:
            open("..\\tmp\\" + filename, 'w').write(mesg.encode('utf-8'))
        return filename

    def MSSocketAPI(self, commond):
        msconn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = '127.0.0.1'
        port = int(open("..\\etc\\sysconfig\\Notif_socketport", 'r').read())
        try:
            msconn.connect((host, port))
        except Exception, e:
            print "connect to Notification server failed.", e
            return
        print "connect Notification server cilent..."
        msconn.sendall(commond)
        msconn.close()

    def MurshroomServerSocket(self):
        socket.setdefaulttimeout(144000)
        socport = open("..\\etc\\sysconfig\\socket_port", 'r').read()
        mssocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print "[murshroom]socket is created."
        try:
            mssocket.bind(("127.0.0.1", int(socport)))
        except socket.error, msg:
            print "[ms ERROR]:Bind failed.Error Code:", msg[0], 'message:', msg[1]
            sys.exit()
        print "[murshroom]socket bind complete."
        mssocket.listen(3)
        while self.runFlag:
            try:
                conn, addr = mssocket.accept()    #此处定义数据接收规范
            except Exception, e:
                print "[murshroom]timeout..."
            if addr[0] != '127.0.0.1':
                conn.sendall('[murshroom]error connection')
                break
            data = conn.recv(4096)
            if not data or data.count('|') != 1:
                break
            func, args = data.split('|')
            if args == '':
                args = []
            else:
                args = list(args.split(','))
            mesg = self.ClientAPI(func, args)
            #mesg = [(u"数据结构", "0-010203 4-060708"), (u"线性代数", "3-030405"), (u"高等数学", "0-0607 2-101112"),
            #(u"体育", "1-030405")]
            #mesg = [(u"算法与程序设计", '3', '99', '4.5'), (u"数据结构", '3', '99', '4.5'), (u"数据结构", '3', '99', '4.5'), (u"数据结构", '3', '99', '4.5')]
            #mesg = [(u"大学外语", u'国家外语六级', '477', u'合格'), (u"大学外语", u'国家外语六级', '477', u'合格'),
            #(u"大学外语", u'国家外语六级', '477', u'合格'), (u"大学外语", u'国家外语六级', '477', u'合格')]
            print mesg
            if mesg is not None and mesg != '':
                conn.sendall(self.CreateRandomFile(mesg))
        conn.close()
        mssocket.close()

    def StartRUN(self, askdict):
        if self.StartFlag:
            self.StartFlag = False
            self.Stop()
        else:
            print "StartRun"
            self.StartFlag = True
            self.start()

    def run(self):#此处启动murshroom server cilent的所有服务
        frequency = 10
        print "create multi-thread"
        while self.runFlag and self.StartFlag:
            asktask = self.HeartBeat()
            if asktask == '~0~' or asktask == '~~':
                print "restart the server ", asktask
                print self.Murshroom_Login() + ' again 152'
                continue
            if len(asktask) > 4:
                thread.start_new_thread(getattr(self, TRANSLATEDict[asktask.split(',')[0]]), (asktask,))
            time.sleep(frequency)

    def Stop(self):
        self.StartFlag = False


def FormatEncode(x):
    return (x.strip()).encode('utf-8')


def GetPreTermID():
    tid = GetNowTermID()
    year = tid[0:4]
    tid = tid[-1]
    if str(tid) == '1':
        year = int(year) - 1
        tid = '2'
    else:
        tid = '1'
    return str(year), tid


def GetNowTermID():
    date = time.localtime(time.time())
    year = int(str(date[0]))
    if date[1] >= 6 and date[1] < 12:
        return str(year) + '1'
    elif date[1] < 3:
        return str(year - 1) + '2'
    else:
        return str(year) + '2'

#这里，我写出了这个系统中最最最最最丑陋的代码，没有之一- -||长得跟我一样奇葩。。。 实在是看不下去了 = =||

class NoneOfBussiness():
    def __init__(self):
        pass


def InfoUploadScore(account='10600106', passwd='10600106', INFOGUA=NoneOfBussiness):
    #do the rating
    #thread.start_new_thread(RunGua, ())
    #time.sleep(1.5)
    INFOGUA.bar.SetValue(0.1)     #todo: init the gua
    time.sleep(1)
    print type(INFOGUA)
    jwc = Jwc_InfoCollect.JWC_SYS()
    jwc.CilentAPI("LOGIN", [0, passwd, 'student', account])
    if jwc.ACCESS == False:
        print "can't connect jwc"
        return
    INFOGUA.bar.SetValue(5)#todo
    name = jwc.GetNameInfo()
    #we need get the information first
    examlist = jwc.CilentAPI("VEXAM", [])
    INFOGUA.bar.SetValue(10)#todo
    examlist[-1] = GetNowTermID()
    djkslist = jwc.CilentAPI('DJKS', [])
    INFOGUA.bar.SetValue(15)#todo
    scorelist = jwc.CilentAPI("VTOTALS", [])
    INFOGUA.bar.SetValue(20) #todo
    courselist = []
    termid = []
    for i in range(int(account[0:2]), int(examlist[-1][2:4]) + 1):
        for j in range(1, 3):
            print ['20%02d' % int(i + 1), j, '20%02d' % int(i)]
            clist = jwc.CilentAPI("SCOURSE", ['20%02d' % int(i + 1), j, '20%02d' % int(i)])
            if len(clist) > 0:
                courselist.append(clist)
                termid.append('20%02d%d' % (int(i), int(j)))
            if '20' + str(i) + '' + str(j) == examlist[-1]: break
            #then do the insert operator
    INFOGUA.bar.SetValue(45) #todo
    print "create the murshroom server..."
    #test the result is ok?
    if False:
        for iexam in examlist:#导入考试信息
            if len(iexam) <= 5: break
            year, tid = GetPreTermID()
            print "EXAMINFO: ", UnionString(
                map(FormatEncode, [iexam[1], iexam[6], iexam[4] + ' ' + iexam[5], year + tid]))
        for idjks in djkslist:#导入等级考试信息
            if len(idjks) != 3: break
            print "DJKS:", UnionString(map(FormatEncode, idjks))
        for i in range(len(courselist)):#导入课程信息
            clist = courselist[i]
            tid = termid[i]
            for icourse in clist:
                if len(icourse) < 6: break
                #print icourse[-3], icourse[2], jwc.CourseDateAnalyse(icourse[-6]), icourse[-1], icourse[3], tid
                print "CINFO:", UnionString(map(FormatEncode, icourse))
            if i == len(courselist) - 1:
                for icourse in clist:
                    if len(icourse) < 6: break
                    print "SELECTION:", UnionString(map(FormatEncode, [icourse[2], account, tid]))
        for iscore in scorelist:#导入成绩信息
            if len(iscore) <= 4: break
            print "SCORE:", UnionString(map(FormatEncode, [iscore[2], iscore[3], iscore[-1], iscore[4], iscore[0]]))
        return
    ms = MurshroomServer()
    callback = ms.ClientAPI("LOGIN", [name.encode('utf-8'), account, passwd])
    INFOGUA.bar.SetValue(50) #todo
    if ms.ACCESS == False:
        print "can not connect murshroom server"
        return
    print callback
    for iexam in examlist:#导入考试信息
        if len(iexam) <= 5: break
        year, tid = GetPreTermID()
        print "EXAMINFO:", UnionString(map(FormatEncode, [iexam[1], iexam[6], iexam[4] + ' ' + iexam[5], year + tid]))
        print ms.ClientAPI("EXAMINFO", map(FormatEncode, [iexam[1], iexam[6], iexam[4] + ' ' + iexam[5], year + tid]))
    INFOGUA.bar.SetValue(60) #todo
    for idjks in djkslist:#导入等级考试信息
        if len(idjks) != 3: break
        print "DJKS:", UnionString(map(FormatEncode, idjks))
        print ms.ClientAPI("DJKS", map(FormatEncode, idjks))
    INFOGUA.bar.SetValue(65) #todo
    for i in range(len(courselist)):#导入课程信息
        clist = courselist[i]
        tid = termid[i]
        for icourse in clist:
            if len(icourse) < 6: break
            if len(icourse) == 10:
                print "CINFO:", UnionString(
                    map(FormatEncode, [icourse[-3], icourse[2], icourse[-6], icourse[-1], icourse[3], tid]))
                print ms.ClientAPI("CINFO", map(FormatEncode,
                                                [icourse[-3], icourse[2], jwc.CourseDateAnalyse(icourse[-6]),
                                                 icourse[-1], icourse[3], tid]))
            else:
                print "CINFO:", UnionString(
                    map(FormatEncode, [icourse[-2], icourse[2], icourse[-5], icourse[-1], icourse[3], tid]))
                print ms.ClientAPI("CINFO", map(FormatEncode,
                                                [icourse[-2], icourse[2], jwc.CourseDateAnalyse(icourse[-5]),
                                                 icourse[-1], icourse[3], tid]))
        if i == len(courselist) - 1:
            for icourse in clist:
                if len(icourse) < 6: break
                print "SELECTION:", UnionString(map(FormatEncode, [icourse[2], account, tid]))
                print ms.ClientAPI("SELECTION", map(FormatEncode, [icourse[2], account, tid]))
    INFOGUA.bar.SetValue(80) #todo
    for iscore in scorelist:#导入成绩信息
        if len(iscore) <= 4: break
        print "SCORE:", UnionString(map(FormatEncode, [iscore[3], iscore[2], iscore[-1], iscore[4], iscore[0]]))
        print ms.ClientAPI("SCORE", map(FormatEncode, [iscore[3], iscore[2], iscore[-1], iscore[4], iscore[0]]))
    INFOGUA.bar.SetValue(100) #todo
    INFOGUA.stext.Show(True)
    time.sleep(3)
    INFOGUA.Show(False)
    INFOGUA.Destroy()
    print "end of create~"


def One(account='', passwd=''):#none of business
    jwc = Jwc_InfoCollect.JWC_SYS()
    jwc.CilentAPI("LOGIN", [0, passwd, 'student', account])
    while True:
        print jwc.GetNameInfo()
        time.sleep(2)


def Two(account='10600140', passwd='96201'):#none of business
    ms = MurshroomServer()
    print ms.ClientAPI("LOGIN", [u'钟浙云'.encode('utf-8'), account, passwd])
    while True:
        print ms.ClientAPI("DJKS", map(FormatEncode, ['1', '2', '3']))
        time.sleep(2)


def UnionString(slist):
    st = ""
    for item in slist:
        st += item + " "
    return st


def Test():
    ms = MurshroomServer()
    print ms.ClientAPI("LOGIN", ["", "10600140", "96201"])
    #print ms.ClientAPI("MCOURSE", [])
    #print ms.ClientAPI("MTERMS", ['20121'])
    ms.MurshroomServerSocket()
    #exit()


if __name__ == '__main__':
    pass


