__author__ = 'glcsnz123'
#_*_encoding:utf-8_*_
import urllib, urllib2, cookielib
import ImageProcessing, re, threading, time
#todo: static arguments begin


HOST = open("..\\etc\\sysconfig\\jwchost.conf", 'r').read()

#login the jwc system
#args: GetCode  ->   pwd   ->  userId
LOGINDict = {"GetCode": "", "pwd": "", "userId": "", "radioUserType": "student", "zzzaskdicturl": "/login.asp",
             "zzzcodenumber": "gbk"}
#see all the score
VTOTALSDict = {"zzzaskdicturl": "/studentWeb/ViewScore/ViewTotalScore.asp", "zzzcodenumber": 'gbk',
               "zzzregexp": r'<tr bordercolor="#99CCFF" bgcolor="#FFFFFF">[^,]{0,700}</tr>',
               "zzzchildregexp": r'&nbsp;[\S]*</div></td>', 'zzzchilds': 6, 'zzzchilde': -11}
#see cet and so on
DJKSDict = {"zzzaskdicturl": "/studentWeb/ViewDJKSScore/ViewTotalDJKSScore.asp", 'zzzcodenumber': 'gbk',
            "zzzregexp": r'<tr bordercolor="#99CCFF" bgcolor="#FFFFFF">[^,]{0,700}</tr>',
            "zzzchildregexp": r'&nbsp;[\S]*</div></td>', 'zzzchilds': 6, 'zzzchilde': -11};
#see some term score
#args: SelectTerm   ->  textYear
VTERMSDict = {"SelectTerm": 1, "textYear": 2011, "zzzaskdicturl": "/studentWeb/ViewScore/ViewTermScore.asp",
              'zzzcodenumber': 'gbk', "zzzregexp": r'<tr bordercolor="#99CCFF" bgcolor="#FFFFFF">[^,]{0,800}</tr>',
              "zzzchildregexp": r'&nbsp;[\S]*</div></td>', 'zzzchilds': 6, 'zzzchilde': -11
}
#see exam time
VEXAMDict = {"zzzaskdicturl": "/studentWeb/Examination/ViewExam1.asp", "zzzcodenumber": 'gbk',
             "zzzregexp": r'<td height="24">[^,]{0,700}</tr>',
             "zzzchildregexp": r'&nbsp;[\S]*</div></td>', 'zzzchilds': 6, 'zzzchilde': -11}
#see select course list
#args:  nouse   ->   select    ->  year
SCOURSEDict = {"nouse": 2013, "select": 1, "year": 2013, "zzzaskdicturl": "/studentWeb/SelectCourse/displayhistory.asp",
               "zzzcodenumber": 'gbk', "zzzregexp": r"<tr>[^~]{100,1200}</tr>",
               "zzzchildregexp": r">\S+</td>|>\S+</div|>\S+[\t ]{3,}</td>", 'zzzchilds': 1, 'zzzchilde': -5,
               "zzzspecialquest": ">\S+</td>|>\S+</div|>\S+[\t 0-9]{2,}</td>|>[0-9][\s0-9]</td>"}
#see your name
NAMEDict = {"zzzaskdicturl": "/studentWeb/leftframe.asp", "zzzcodenumber": "gbk",
            "zzzregexp": r'<font color="#[a-zA-Z0-9]+">&nbsp[\S]+&nbsp</font>', "zzzchildregexp": r"&nbsp[\S]+&nbsp"}

HEADERS = [('User-agent',
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31'),
           ("Cache-Control", "max-age=0"), ("Host", "10.1.74.16"),
           ("Connection", "keep-alive"), ("Content-Type", "application/x-www-form-urlencoded "),
           ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")]
TRANSLATEDict = {"VTOTALS": "GetClassScore", "DJKS": "GetClassScore", "VTERMS": "GetClassScore",
                 "VEXAM": "GetClassExam", "SCOURSE": "GetClassScore", "NAME": "GetNameInfo",
                 "LOGIN": "Jwc_Login"}
#<tr bordercolor="#99CCFF" bgcolor="#FFFFFF">infomations</tr>
#<td height="24"><div align="center">information</div></td>
#<font color="#0000FF">&nbsp information &nbsp</font>
#

class JWCArgs():
    def __init__(self):
        self.Init()

    def Init(self):
        self.HOST = HOST
        self.LOGINDict = LOGINDict
        self.VTOTALSDict = VTOTALSDict
        self.DJKSDict = DJKSDict
        self.NAMEDict = NAMEDict
        self.VTERMSDict = VTERMSDict
        self.VEXAMDict = VEXAMDict
        self.HEADERS = HEADERS
        self.SCOURSEDict = SCOURSEDict

#todo: static arguments end

class JWC_SYS(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.InitCookie(HEADERS)
        self.jwcargs = JWCArgs()
        self.preScoreTuple = set()
        self.runFlag = True
        self.WeekDate = {u"一": 0, u"二": 1, u"三": 2, u"四": 3, u"五": 4, u"六": 5, u"七": 6}
        self.sys_name = 'JWC_SYS'

    def CilentAPI(self, func, args=[], excp=False):
        try:
            askdict = getattr(self.jwcargs, func + 'Dict')
            askkey = askdict.keys()
            askkey.sort()
            for i in range(len(args)):
                askdict[askkey[i]] = args[i]
            func = getattr(self, TRANSLATEDict[func])
            if excp:
                return func(askdict, excp)
            else:
                return func(askdict)
        except IOError, e:
            return self.Error()


    def Error(self):
        return 'wrong function name'

    def InitCookie(self, HEADERS):
        self.ACCESS = False
        self.cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        self.opener.addheaders = HEADERS
        urllib2.install_opener(self.opener)

    def Jwc_Login(self, askdict):
        self.ACCESS = False
        if askdict["GetCode"] == "" or askdict["GetCode"] is None or len(str(askdict["GetCode"])) != 4:
            askdict["GetCode"] = ImageProcessing.Get_jwc_Code(HOST)
        pst_data = urllib.urlencode(askdict)
        req = urllib2.Request(HOST + askdict['zzzaskdicturl'], pst_data)
        html = urllib2.urlopen(req).read().decode(askdict['zzzcodenumber'])
        if html.count(u"用户失效") == 0:
            self.ACCESS = True
        return html

    def AskForData(self, askdict):
        if askdict.has_key('zzzchildregexp'):
            tmp_zzzchildregexp = askdict['zzzchildregexp']
            askdict['zzzchildregexp'] = 0
        pst_data = urllib.urlencode(askdict)
        if askdict.has_key('zzzchildregexp'):
            askdict['zzzchildregexp'] = tmp_zzzchildregexp
        if askdict.has_key('zzzspecialquest'):
            return urllib2.urlopen(HOST + askdict['zzzaskdicturl'] + '?' + pst_data).read().decode(
                askdict['zzzcodenumber'])
        req = urllib2.Request(HOST + askdict['zzzaskdicturl'], pst_data)
        return urllib2.urlopen(req).read().decode(askdict['zzzcodenumber'])


    def GetNameInfo(self):#NAMEDict
        html = self.AskForData(NAMEDict)
        #print html
        regexp = re.compile(NAMEDict['zzzregexp'])
        result = regexp.findall(html)
        regexp = re.compile(NAMEDict['zzzchildregexp'])
        return regexp.findall(result[0])[0][5:-5:1]

    def GetClassExam(self, askdict):
        html = self.AskForData(askdict)
        html = html.replace('\n', '')
        regexp = re.compile(askdict['zzzregexp'])
        result = regexp.findall(html)
        reslist = []
        for item in result:
            #print item
            regexp = re.compile(askdict['zzzchildregexp'])
            chres = regexp.findall(item)
            chlst = []
            for citem in chres:
                chlst.append(citem[askdict['zzzchilds']:askdict['zzzchilde']:1])
            reslist.append(tuple(chlst))
            #todo exception re
        regexp = re.compile(r'\[[0-9]{5,5}\]')
        result = regexp.findall(html)
        reslist.append(result[0][1:-1:1])
        return reslist

    def GetClassScore(self, askdict, exp=False):
        html = self.AskForData(askdict)
        #print html
        html = html.replace('\n', '')
        regexp = re.compile(askdict['zzzregexp'])
        result = regexp.findall(html)
        reslist = []
        #print len(result)
        for item in result:
            #print item
            regexp = re.compile(askdict['zzzchildregexp'])
            chres = regexp.findall(item)
            chlst = []
            for citem in chres:
                chlst.append(citem[askdict['zzzchilds']:askdict['zzzchilde']:1])
            reslist.append(tuple(chlst))
        if exp:
            tmp = self.GetExceptionInfo(html=html)
            return reslist, tmp
        else:
            if askdict.has_key("zzzspecialquest"):
                return reslist[1:]
            return reslist

    def GetExceptionInfo(self, regexp=r'<font color="#FF0000">\S+</font>', html=""):
        regexp = re.compile(regexp)
        result = regexp.findall(html)
        return (result[0][22:-7:1], result[1][22:-7:1])

    def AutoGetTheScore(self, askdict):
        curList, score = self.GetClassScore(askdict, True)
        curSet = set(curList)
        tmpSet = curSet - self.preScoreTuple
        self.preScoreTuple = curSet
        return tmpSet

    def run(self, func, askdict, frequency=60):#auto get the information
        while self.runFlag:
            func(askdict)
            time.sleep(frequency)

    def CourseDateAnalyse(self, codate):
        reslist = ""
        for i in range(len(codate)):
            if self.WeekDate.has_key(codate[i]):
                tmplist = str(self.WeekDate[codate[i]]) + '-'
                st = ""
                for j in range(i + 1, len(codate)):
                    if self.WeekDate.has_key(codate[j]):
                        break
                    elif codate[j] == ',' or j == len(codate) - 1:
                        tmplist += "%02d" % int(st)
                        st = ""
                    else:
                        st += codate[j]
                reslist += " " + tmplist
        return reslist.lstrip()


if __name__ == '__main__':
    jwc = JWC_SYS()
    #print jwc.CourseDateAnalyse(u"二4,5,四1,2,3,")
    #if True: exit()
    jwc.CilentAPI("LOGIN", [0, '853753836', "student", 11170331])
    #asklist = jwc.CilentAPI("SCOURSE", ['2013', '2', '2012'])
    asklist = jwc.CilentAPI("SCOURSE", [])
    #print asklist
    for i in asklist:
        st = ''
        for j in i:
            st += j.rstrip() + "|"
        print st.replace('\t', '')




