#-*- coding: utf-8 -*-

### This program try to connect, and connect, and ping timeout-rejects.

import socket
import time
import sys

# Initial Settings
server = "irc.ozinger.org"
channels = ["TOZ", "XGC"]
botName = "HiyukiBot"
botDescription = "HiyukiBot: Bot Mk.3 by TOZ57"
botNick = "Hiyuki"

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
        if len(msgSet) > 1 and msgSet[1][:2] == '*핑':
            sendMsg(msgSet[0][2], getNick(msgSet) + ", 퐁\n")
        if text.find('PING') != -1: # REPLY FIRST PING
            ping_msg = text[5:]
            send("PONG " + ping_msg + "\n")
            if not init:
                for channel in channels:
                    send("JOIN #" + channel +"\n") #join the chan
                init = True
