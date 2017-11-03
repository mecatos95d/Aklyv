#-*- coding: utf-8 -*-

from modules import Crew
from util import *

import socket
import time
import sys

import argparse # Arguments parsing
import configparser # Config reading
import logging # Logger. (Not fully applied)

# Config reading.
def init():
	try: # Initializing
		irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Defines the socket
		logging.basicConfig(format='%(asctime)s | %(message)s', datefmt='%Y%m%d %H:%M:%S') # Logging setting

		config_raw = configparser.ConfigParser() # Wrong argument will cause KeyError
		config_raw.read("setting")
		parser = argparse.ArgumentParser()
		parser.add_argument("-d", "--debug", help="boot with debug mode", action="store_true") # Use alt-setting
		parser.add_argument("-p", "--print", help="boot with print mode", action="store_true") # Print with detailed options.
		parser.add_argument("-t", "--test", help="test before boot", action="store_true") # Execute test before booting. Currently not implemented.
		arg = parser.parse_args()
		if arg.test:
			logging.warning("Testing is currently unimplemented. Skip test execution.")

		if arg.debug: # When debug mode is running
			if config_raw.has_section("alt"):
				option = config_raw["alt"]
				# TODO : Missed option should automatically filled from "bot" section.
			else:
				logging.warning('No alt setting. Boot with default setting.')
		else:
			option = config_raw["bot"]

		irc.connect((option['server'], int(option['port']))) # Connects to the server
		send_raw(irc, "USER " + option['name'] + " " + option['name'] + " " + option['name'] + " :" + option['description'] + "\n") # User authentication
		send_raw(irc, "NICK " + option['nick'] +"\n") # Nick setting
		# send_raw(irc, "PRIVMSG nickserv :iNOOPE\r\n") # Auth maybe...
		for channel in parse_config_list(option['channels']):
			send_raw(irc, "JOIN #" + channel + "\n") # Join channel

		if parser.parse_args().print: # When print mode is running
			pass
	except Exception as ex:
		logging.error("Booting failed. Check config file.")
		if arg.print:
			logging.exception("Error caused by : " + str(ex))
		sys.exit(0)

	return irc

def run():
	note = []
	expCalc = Crew.ExpCalc()

	joined = False
	lasttime = time.time()
	timeout = 200

	irc = init()

	while True: # In a loop
		if (time.time() - lasttime) > timeout: # Current problem : While-phrase runs if message came in.
			#print("TIMEOUT : " + str(time.time() - lasttime) + "s elapsed without message")
			break # Time elapsed more than (timeout) sec after last message given.
		text = message(irc)
		msgSet = parse_msg(text)
		if len(text) != 0:
			if text.find('PING') != -1: # REPLY FIRST PING
				ping_msg = text[5:]
				send_raw(irc, "PONG " + ping_msg + "\n")

			print("DELAY| " + '{:.3f}'.format(time.time() - lasttime) + "s")
			lasttime = time.time()
			if text.find("*QUIT") != -1:
				send_raw(irc, "QUIT\n") # QUIT MSG TEST
				break # Temporary Quit Code
			if text.find('Closing link') != -1:
				sys.exit(0)

			if 0 < len(msgSet): # Invite-response
				if 2 < len(msgSet[0]): # Invite = 3 args
					if 'INVITE' == msgSet[0][1]:
						send_raw(irc, "JOIN " + msgSet[1] + "\n")
				# if 3 < len(msgSet[0]): # Kick = 4 args
				# 	if 'KICK' == msgSet[0][1] and nick == msgSet[0][3]:
				# 		print("RESPONDING KICK")
				# 		send_raw(irc, "JOIN " + msgSet[0][2] + "\n")
				# 		send_msg(irc, msgSet[0][2], "제 기능이 더 필요하지 않으시다면, *leave 를 사용해주세요.")

			chat = [] # Parsed Data. Original Chat can be checked by "msgSet[1]"
			if len(msgSet) > 1:
				chat = msgSet[1].strip().split(' ')
			
			if len(chat) != 0:
				print("PARSE| " + str(chat) + "\n")
				if chat[0] == '*핑' or chat[0] == "*ping":
					send_msg(irc, msgSet[0][2], get_nick(msgSet) + ", 퐁\n")

				if chat[0] == '*leave':
					send_raw(irc, "LEAVE " + msgSet[1] + "\n")
				
				if chat[0] == '*노트':
					if len(chat) == 1:
						send_msg(irc, msgSet[0][2], "노트 명령입니다. *노트 <내용>으로 저장을, *노트 <번호>로 호출이 가능합니다. 봇이 종료 시 데이터는 자동적으로 삭제됩니다.")
					else:
						if is_int_str(chat[1]):
							num = int(chat[1])
							if num < 0 or num >= len(note):
								send_msg(irc, msgSet[0][2], "노트 번호가 잘못되었습니다! 입력 > " + chat[1])
							else:
								print(note[num])
								send_msg(irc, msgSet[0][2], "노트 #" + chat[1] + " > " + note[num])
						else:
							rmlen = 4 # remove "*노트 "
							note.append(msgSet[1].strip()[rmlen:])
							print(str(note))
							send_msg(irc, msgSet[0][2], "노트 #" + str(len(note)-1) + "가 등록되었습니다. | " + note[-1])

				if chat[0] in ["*경험치", "*경", "*exp", "*e"]:
					if len(chat) < 3:
						send_msg(irc, msgSet[0][2], "월탱 승무원 경험치 명령입니다. *경험치 <시작%> <최종%> [<잔여경험치>] 로 계산이 가능합니다.")
					else:
						if is_int_str(chat[1]) and is_int_str(chat[2]):
							exp_start = int(chat[1])
							exp_end = int(chat[2])
							exp_left = 0
							if len(chat) >= 4:
								if is_int_str(chat[3]):
									exp_left = int(chat[3])
									if exp_left < 0:
										exp_left = 0

							if exp_start < 50 or exp_start > 500:
								send_msg(irc, msgSet[0][2], "경험치 입력 범위(50~500)를 벗어났습니다! 입력 > " + str(exp_start))
							elif exp_end < 50 or exp_end > 500:
								send_msg(irc, msgSet[0][2], "경험치 입력 범위(50~500)를 벗어났습니다! 입력 > " + str(exp_end))
							else:
								result = expCalc.run(exp_start, exp_end, exp_left)
								send_msg(irc, msgSet[0][2], result)
						else:
							send_msg(irc, msgSet[0][2], "입력이 잘못되었습니다! 입력 > " + chat[1] + " / " + chat[2])

			
			

run()