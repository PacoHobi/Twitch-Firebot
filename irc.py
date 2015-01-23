#!/usr/bin/env python

import socket

class IRC():
	# open a socket to handle the connection
	def __init__(self):
		self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.channel = ''

	# connect to a server
	def connect(self, server, port=6667):
		self.conn.connect((server, port))

	# send command to the server
	def send(self, command):
		self.conn.send(command + '\n')

	# send message to channel
	def send_channel(self, msg):
		self.send("PRIVMSG %s :%s" %(self.channel, msg))

	# join a channel
	def join(self, channel):
		self.channel = channel
		self.send("JOIN %s" % channel)

	# send login data
	def login(self, nickname, password):
		self.send("PASS " + password)
		self.send("NICK " + nickname)

	# receive messages from server
	def receive(self, callback):
		buffer = ''
		while True:
			buffer += self.conn.recv(1024)
			if buffer[-2:]!='\r\n': # if not end of message receive more
				continue
			for line in buffer.split('\n')[:-1]: # send each message to the callback function
				if line[0:4] == 'PING':
					self.send("PONG %s" % line.split()[1]) # respond to PING with PONG
				else:
					callback(line)
			buffer = ''