__author__ = 'glcsnz123'
#_*_encoding:utf-8_*_
import urllib, urllib2, thread, time

mylock = thread.allocate_lock()
ScoreList = []
anslist = []
cefy = []
Prefix = ""
UserName = ""
Rating = 0.0


def Check(hole, stid="330382121208311", name="李莎"):
    #print stid, name
    if not isinstance(stid, unicode):
        stid = stid.decode("ascii")
    if not isinstance(name, unicode):
        name = name.decode("utf-8")
    post_data = urllib.urlencode({"id": stid.encode("gbk"), "name": name.encode("gbk")});
    #print post_data
    HEADERS = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", \
               "Accept-Charset": "GBK,utf-8;q=0.7,*;q=0.3", "Accept-Encoding": "gzip,deflate,sdch", \
               "Accept-Language": "zh-CN,zh;q=0.8", "Cache-Control": "max-age=0",
               "Content-Type": "application/x-www-form-urlencoded", \
               "Cookie": "cnzz_a30023677=4; sin30023677=; rtime30023677=5; ltime30023677=1356177904700; cnzz_eid30023677=19927958-1318821986-http%3A//www.baidu.com/s%3Fwd%3D99%25CB%25DE%25C9%25E1%26rsv_bp%3D0%26rsv_spt%3D3%26oq%3D9; searchtime=1356177913"
        ,
               "Host": "cet.99sushe.com", "Origin": "http://cet.99sushe.com", "Referer": "http://cet.99sushe.com/", \
               "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.20 (KHTML, like Gecko) Chrome/25.0.1337.0 Safari/537.20"
    };

    pst = urllib2.Request("http://cet.99sushe.com/s", headers=HEADERS);
    try:
        pst = urllib2.urlopen(pst, post_data)
    except Exception, e:
        try:
            mylock.acquire()
            hole.append(stid[-5::1])
            #print stid
        finally:
            mylock.release()
        return "w"
    html = pst.read()
    return html.decode("gbk")


def LoopOne(prefix, name, hole, async=True): #check the query in loop
    while True:
        try:
            if async:
                mylock.acquire()
            if len(hole) <= 0:
                break
            i = hole[0]
            del hole[0]
        finally:
            if async:
                mylock.release()
        result = Check(hole, prefix + i, name)
        if len(result) >= 10:
            print result
            try:
                mylock.acquire()
                anslist.append(result.split(','))
                cefy.append(prefix + i)
            finally:
                mylock.release()


def GetLocalNum():
    return "330020"
    #return raw_input("请输入准考证号的前六位：")


def GetName():
    return open(r"..\etc\UserName.conf", 'r').read()
    #return raw_input(u"请输入你的姓名：")


def GetLevel():
    cetlv = raw_input("CET?");
    if cetlv == '4':
        return '1'
    return '2'


def GetYear():
    date = time.localtime(time.time())
    year = int(str(date[0])[2:])
    if date[1] < 8:
        year -= 1
    if int(date[1]) >= 8 or int(date[1]) < 2:
        year = str(year) + '1'
    else:
        year = str(year) + '2'
    return str(year)


def InitCheck(cetlev):
    global Prefix, UserName
    Prefix = GetLocalNum() + GetYear()
    if cetlev == '':
        Prefix += GetLevel()
    else:
        Prefix += cetlev
    UserName = GetName()


def CreateMultiCheck(cetlev='', tlimit=60, kchlimit=(1, 200), zwhlimit=(1, 50)):
    global Rating
    total = (kchlimit[1] - kchlimit[0] + 1) * (zwhlimit[1] - zwhlimit[0] + 1)
    up = total / tlimit + 1
    t = 0
    global Prefix, UserName
    if len(Prefix) != 9 or len(UserName) <= 1:
        InitCheck(cetlev)
    print Prefix, UserName
    hole = []
    preh = []
    tmp = []
    for i in range(kchlimit[0], kchlimit[1]):
        for j in range(zwhlimit[0], zwhlimit[1]):
            tmp.append("%03d%02d" % (i, j))
            t += 1
            if t == up:
                preh.append(t)
                hole.append(tmp)
                tmp = []
                t = 0
    hole.append(tmp)
    preh.append(t)
    while len(hole) != tlimit:
        hole.append([])
        preh.append(0)
    print "I will create", tlimit, "threads..."

    for i in range(0, tlimit):
        thread.start_new_thread(LoopOne, (Prefix, UserName, hole[i], False))
        #time.sleep(0.1)

    print "create is over"
    sum = total
    while sum != 0:
        time.sleep(5)
        sum = 0
        dying = 0
        for i in range(0, tlimit):
            tcg = len(hole[i])
            if tcg == preh[i] and tcg != 0:
                thread.start_new_thread(LoopOne, (Prefix, UserName, hole[i], False))
                dying += 1
            else:
                preh[i] = tcg
            sum += tcg
            #print sum
        Rating = (1.0 - sum * 1.0 / total) * 100.0
        print "%.4f %% finished~ " % (Rating)
        print "there is ", dying, "threads died"


def CreateScore(expe=True):
    print "deal with the data...."
    global ScoreList
    ScoreList = []
    for i in range(len(anslist)):
        tmp = anslist[i]
        scors = u"姓名： " + tmp[-1]
        scors += u"\n准考证号： " + cefy[i]
        scors += u"\n学校： " + tmp[-2]
        scors += u"\n总分： " + tmp[-3]
        scors += u"\n听力： " + tmp[1]
        scors += u"\n阅读： " + tmp[2]
        scors += u"\n综合： " + tmp[3]
        scors += u"\n写作： " + tmp[4]
        if expe:
            open(r'..\tmp\cet' + str(cefy[i]), 'w').write(scors.encode('utf-8'))
        print scors + "\n"
        if len(tmp[-1]) * 3 == len(UserName):
            ScoreList.append(scors)
    return ScoreList


if __name__ == '__main__':
    CreateMultiCheck()

    #CreateScore()




