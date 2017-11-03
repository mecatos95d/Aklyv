#-*- coding: utf-8 -*-

# Utility functions are defined here.

def send_raw(sock, msg):
	print("SEND : " + msg)
	sock.send(msg.encode('utf-8'))

def send_msg(sock, target, msg):
	send_raw(sock, "PRIVMSG " + target + " " + msg + "\n");

def message(sock):
	return sock.recv(4096).decode('utf-8') # Receive the text

def parse_msg(msg):
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

def get_nick(msgSet):
	return msgSet[0][0].split('!')[0]

def is_int_str(s): # Came From http://stackoverflow.com/questions/1265665/python-check-if-a-string-represents-an-int-without-using-try-except
	try:
		int(s)
		return True
	except ValueError:
		return False

def parse_config_list(config_str):
	sep = [' ', '.', ',', ':', ';', '/', '\n']
	config_list = []
	cursor = 0
	while len(config_str) > cursor:
		if config_str[cursor] in sep:
			if 0 != cursor:
				scrap = config_str[:cursor].strip()
				if 0 != len(scrap):
					config_list.append(scrap)
			config_str = config_str[cursor+1:]
			cursor = 0
		else:
			cursor += 1
	if 0 != len(config_str):
		config_list.append(config_str)
	return config_list