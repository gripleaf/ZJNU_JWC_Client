__author__ = 'glcsnz123'
#_*_encoding:utf-8_*_
import urllib, time, thread, sys
import urlparse, httplib
import os, ftplib, socket, subprocess


def CheckFileName(filename):
    unaclist = ['\r', '\n', '\t', '?']
    for uncode in unaclist:
        filename = filename.replace(uncode, '')
    return filename


def DownLoadSingleFile(url, ptah="F:\\Users\\glcsnz123\\Desktop\\", filename="default"):
    if filename == 'default' or filename == '':
        filename = url.split('/')[-1]
    filename = CheckFileName(filename)
    print ptah, filename
    if not os.path.isdir(ptah):
        os.makedirs(ptah)
    urllib.urlretrieve(url, filename=ptah + filename)
    print "download over"


def CalcSize(url):# here we use the httplib to get the size of the file we download.
    parsedurl = urlparse.urlparse(url)
    httpConn = httplib.HTTPConnection(parsedurl[1])
    httpConn.request('GET', parsedurl[2])
    response = httpConn.getresponse()
    size = response.getheader('Content-Length')
    return int(size)


def DownloadSche(url, ptah="F:\\Users\\glcsnz123\\Desktop\\", filename="default"):
    if filename == 'default' or filename == '':
        filename = url.split('/')[-1]
    fsize = CalcSize(url)
    download_v = 0.0
    now = -1
    print ptah + filename
    while True:
        try:
            pre = os.path.getsize(ptah + filename)
            download_v = (pre - now) / 1024.0 / 2.0
            print download_v, "Kb/s", ' ', pre / 1024, '/', fsize / 1024
            if pre == now:
                print "over too"
                break
            now = pre
        except Exception, ex:
            print "a oh"
            break
        time.sleep(2)

#上传文件到ftp，两个参数分别是ftp的地址，所要上传文件的绝对地址
def GetRemoteFileSize(ftpfile, filename):
    try:
        fsize = ftpfile.size(filename)
    except Exception, ex:
        return 0
    return fsize


def UpLoadFTPFile(HOST='10.7.18.40', localfile=u'F:\\Users\\glcsnz123\\Desktop\\abc.doc'):
    try:#connect to the ftp server
        ftpfile = ftplib.FTP(HOST)
    except (socket.error, socket.gaierror), e:
        print 'ERROR:cannot reach "%s"' % HOST
        return
    print '***connected to host "%s"' % HOST
    try:#login
        ftpfile.login(user='upload', passwd='')
    except ftplib.error_perm:
        print 'ERROR:cannot login anonymously'
        ftpfile.quit()
        return
    print 'welcome:', ftpfile.getwelcome()
    fd = open(localfile, 'rb')
    try:
        ftpfile.storbinary('STOR %s' % os.path.basename(localfile), fd)
    except ftplib.error_perm:
        print "[ERROR]:can not upload."
    fd.close()
    ftpfile.quit()
    print "task is over.\nquit the ftp server."


def DoDownLoad(url="http://localhost/downloadfile/abc.doc"):
    t = time.clock()
    dargs = (url,)
    thread.start_new_thread(DownLoadSingleFile, dargs)
    DownloadSche(dargs)
    #DownLoadSingleFile("http://acm.zjnu.edu.cn/download/360sd3.0.exe")
    print time.clock() - t

#完成对比下载的功能
MSHOST = open("..\\etc\\sysconfig\\mshost.conf").read()   #测试阶段是http://localhost


def IfHasNewVersion():
    version = open('..\\etc\\version', 'r').read()    #获取本地版本号
    try:
        fversion = urllib.urlopen(MSHOST + '/downloadfile/version').read()    #获取服务器端版本号
    except Exception, e:
        print "[ERROR]:can not connect the HOST-" + MSHOST
    print fversion, version + '|'
    if fversion == version:  #对比版本号，如果版本号不同，则进行更新
        print "no need to update"
        return False
    if fversion.split('.')[0] == version.split('.')[0]:
        AutoCheckUpdate()
        return False
    return True


def AutoCheckUpdate():
    version = open('..\\etc\\version', 'r').read()    #获取本地版本号
    try:
        fversion = urllib.urlopen(MSHOST + '/downloadfile/version').read()    #获取服务器端版本号
    except Exception, e:
        print "[ERROR]:can not connect the HOST-" + MSHOST
    sys_version, soft_version = fversion.split('.')
    lsys_version, lsoft_version = version.split('.')
    filelist = urllib.urlopen(MSHOST + '/downloadfile/filelist.v' + fversion).read().split('\n')
    if sys_version == lsys_version:#small update   系统版本号一样，所以下载最新的软件列表
        print "update the soft list..."
        for lines in filelist:
            if len(lines) < 2: continue
            if lines.startswith("var\\soft_logo") or lines.startswith("var\\soft_info"):
                print "Download the |" + lines + "|..."
                ptah = os.path.dirname("..\\" + lines) + '\\'
                filename = os.path.basename(lines)
                #if os.path.isfile(ptah + filename): continue
                DownLoadSingleFile(MSHOST + '/downloadfile/' + lines.replace('\\', '/'), ptah, filename)
        open('..\\etc\\version', 'w').write(fversion)    #更新版本号

    else:#system update    系统版本号都不一样，所以要下载最新系统版本，但是首先要进行的是系统软件文件下载，完了在放到对应的目录中去
        try:
            fout = open("..\\tmp\\tmpfile", 'w')
            for lines in filelist:
                if lines.startwith("boot\\") or lines.startwith("boot\\sysconfig"):
                    fout.write(lines)
                    #here we should create a process to move the file to the right way!
        except Exception, ex:
            print "[ERROR]:Update system failed."
            return
        finally:
            fout.close()
        open("..\\etc\\version", 'w').write(sys_version + '.' + lsoft_version)
        subprocess.call("..\\tmp\\updatefile\\UpdateFile.exe")
        sys.exit()


def InstallNewSoft(name='default'):
    if name == 'default':
        return
    filelist = urllib.urlopen(MSHOST + '/' + 'downloadfile/soft_list/' + name + ".list").read().split('\n')
    for lines in filelist:
        if len(lines) < 2: continue
        ptah = os.path.dirname("..\\" + lines) + '\\'
        filename = os.path.basename(lines)
        if os.path.isfile(ptah + filename):
            continue
        DownLoadSingleFile(MSHOST + '/downloadfile/' + lines.replace('\\', '/'), ptah, filename)

    #此处需要更新客户端已有软件列表
    open("..\\etc\\cilentsoft.list", 'a').write(name + '\n')


if __name__ == '__main__':
    AutoCheckUpdate()



