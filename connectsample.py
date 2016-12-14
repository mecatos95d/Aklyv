#-*- coding: utf-8 -*-

### This program try to connect, and connect, and ping timeout-rejects.

import socket
import sys

# Initial Settings
server = "irc.ozinger.org"
channel = "#XGC"
botName = "HiyukiBot"
botDescription = "HiyukiBot"
botNick = "Hiyuki"

global irc
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #defines the socket

def send(msg):
   irc.send(msg.encode('utf-8'))

irc.connect((server, 6667)) #connects to the server
send("USER " + botName +" " + botName +" " + botName +" :" + botDescription + "\n") #user authentication
send("NICK " + botNick +"\n") #sets nick
send("PRIVMSG nickserv :iNOOPE\r\n") #auth

while True: # In a loop
    text=irc.recv(2040).decode('utf-8') #receive the text
    if len(text) != 0:
        print(text) #print text to console
        if text.find("QUIT") != -1:
            send("QUIT\n") # QUIT MSG TEST
            break # Temporary Quit Code
        if text.find('Closing link') != -1:
            break
        if text.find('PING') != -1: # REPLY FIRST PING
            ping_msg = text[5:]
            send("PONG " + ping_msg + "\n")
            send("JOIN " + channel +"\n") #join the chan
