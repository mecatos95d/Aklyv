import socket
import sys

server = "irc.ozinger.org"       #settings
channel = "#XGC"
botnick = "Hiyuki"

global irc
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #defines the socket

def send(msg):
   irc.send(msg.encode())

print("connecting to:", server)
irc.connect((server, 6667)) #connects to the serverx
send("USER "+ botnick +" "+ botnick +" "+ botnick +" :This is a fun bot!\n") #user authentication
send("NICK "+ botnick +"\n")                            #sets nick
send("PRIVMSG nickserv :iNOOPE\r\n")    #auth
send("JOIN "+ channel +"\n")        #join the chan

while True:    #puts it in a loop
   text=irc.recv(2040)  #receive the text
   if len(text) != 0:
      print(text)   #print text to console

   #if text.find('PING') != -1:                          #check if 'PING' is found
   #   irc.send('PONG ' + text.split() [1] + '\r\n') #returnes 'PONG' back to the server (prevents pinging out!)

input('Press ENTER to exit')

### This program try to connect, and connect, and ping timeout-rejects.