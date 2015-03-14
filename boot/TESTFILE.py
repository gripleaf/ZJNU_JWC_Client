__author__ = 'glcsnz123'

if __name__ == '__main__':
    import socket, time

    while True:
        msconn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        msconn.connect(('127.0.0.1', 9999))
        mesg = raw_input("input your message:")
        if mesg == 'exit' or mesg == '': break
        msconn.sendall(mesg)
        time.sleep(1)
        msconn.close()




