__author__ = 'glcsnz123'
#_*_encoding:utf-8_*_
import JWC_Login, MainGUI, MurshroomServer, sys
import thread, Notification, codecs


def InitMainGUI():
    MainGUI.TestFrame()


def InitServer():
    Notification.NotificationMainWork()


if __name__ == '__main__':
    server = JWC_Login.InitLogin()
    if not server is None and server.ACCESS:
        if server.sys_name == 'MurshroomServer':
            #server.start()
            pass
        else:
            server = MurshroomServer.MurshroomServer()
            username = codecs.open("..\\etc\\UserName.conf", 'r', 'utf-8').read()
            account, passwd = codecs.open("..\\etc\sysconfig\\shadow", 'r', 'utf-8').read().split(',')
            print type(username), type(account), type(passwd)
            server.ClientAPI("LOGIN", [username.encode("utf-8"), account, passwd])
            #server.start()
        thread.start_new_thread(server.MurshroomServerSocket, ())#启动socket接口服务
        thread.start_new_thread(InitServer, ())
        InitMainGUI()
        #server.Stop()
        print "goodbye", codecs.open("..\\etc\UserName.conf", 'r', 'utf-8').read()
        sys.exit()



