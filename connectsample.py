#-*- coding: utf-8 -*-

### This program try to connect, and connect, and ping timeout-rejects.

import 'modules/ping'
import socket
import time
import sys

# Initial Settings
server = "irc.ozinger.org"
channels = ["TOZ", "Chaser", "XGC"]
botName = "AklyvBot"
botDescription = "Aklyv: Bot Mk.3 by TOZ57"
botNick = "Aklyv"

global irc
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #defines the socket

def send(msg):
    print("SEND : " + msg)
    irc.send(msg.encode('utf-8'))

def sendMsg(target, msg):
    send("PRIVMSG " + target + " " + msg + "\n");

def message():
    return irc.recv(2050).decode('utf-8') #receive the text

def parseMsg(msg):
    # Parse to [[Who, Order, Channel], Msg]
    data = msg.split(':',2)[1:]
    print("ORIG | " + msg.strip())
    if len(data) == 1: # MSG EXAMPLE -> :^^!ozinger@ika.ozinger.org MODE #TOZ +vo Hiyuki Hiyuki
        print("RECV | " + data[0].strip())
    else:
        data[0] = data[0].split(' ')[:-1]
        print("FROM | " + str(data[0]))
        print("RECV | " + data[1].strip())
        if len(data) != 2:
            print("ERROR: PARSE LENGTH IS NOT 2")
    return data

def getNick(msgSet):
    return msgSet[0][0].split('!')[0]

def isIntStr(s): # Came From http://stackoverflow.com/questions/1265665/python-check-if-a-string-represents-an-int-without-using-try-except
    try:
        int(s)
        return True
    except ValueError:
        return False

note = []

irc.connect((server, 6667)) #connects to the server
send("USER " + botName +" " + botName +" " + botName +" :" + botDescription + "\n") #user authentication
send("NICK " + botNick +"\n") #sets nick
send("PRIVMSG nickserv :iNOOPE\r\n") #auth

init = False
lasttime = time.time()
timeout = 200

while True: # In a loop
    if (time.time() - lasttime) > timeout: # Current problem : While-phrase runs if message came in.
        #print("TIMEOUT : " + str(time.time() - lasttime) + "s elapsed without message")
        break # Time elapsed more than (timeout) sec after last message given.
    text = message()
    msgSet = parseMsg(text)
    if len(text) != 0:
        print("DELAY| " + '{:.3f}'.format(time.time() - lasttime) + "s\n")
        lasttime = time.time()
        if text.find("QUIT") != -1:
            send("QUIT\n") # QUIT MSG TEST
            break # Temporary Quit Code
        if text.find('Closing link') != -1:
            break
        
        chat = [] # Parsed Data. Original Chat can be checked by "msgSet[1]"
        if len(msgSet) > 1:
            chat = msgSet[1].strip().split(' ')
        
        if len(chat) != 0:
            print("PARSE| " + str(chat))
            if chat[0] == '*핑':
                sendMsg(msgSet[0][2], getNick(msgSet) + ", 퐁\n")
            
            if chat[0] == '*노트':
                if len(chat) == 1:
                    sendMsg(msgSet[0][2], "노트 명령입니다. *노트 <내용>으로 저장을, *노트 <번호>로 호출이 가능합니다. 봇이 종료 시 데이터는 자동적으로 삭제됩니다.")
                else:
                    if isIntStr(chat[1]):
                        num = int(chat[1])
                        if num < 0 or num >= len(note):
                            sendMsg(msgSet[0][2], "노트 번호가 잘못되었습니다! 입력 > " + chat[1])
                        else:
                            print(note[num])
                            sendMsg(msgSet[0][2], "노트 #" + chat[1] + " > " + note[num])
                    else:
                        rmlen = 4 # remove "*노트 "
                        note.append(msgSet[1].strip()[rmlen:])
                        print(str(note))
                        sendMsg(msgSet[0][2], "노트 #" + str(len(note)-1) + "가 등록되었습니다. | " + note[-1])

        
        
        if text.find('PING') != -1: # REPLY FIRST PING
            ping_msg = text[5:]
            send("PONG " + ping_msg + "\n")
            if not init:
                for channel in channels:
                    send("JOIN #" + channel +"\n") #join the chan
                init = True
