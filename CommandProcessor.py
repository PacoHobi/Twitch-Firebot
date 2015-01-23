#!/usr/bin/env python

from json import load as json_load
import utils

class CommandProcessor():
	# load the commands from file f
	def __init__(self, conn, config, f):
		self.conn = conn
		self.config = config
		with open(f, 'r') as file:
			self.commands = json_load(file)
		
	# process command
	def process(self, user, msg):
		msg = msg.split()
		cmd = msg[0]
		if cmd.lower() in self.commands.keys(): # command recognized
			command = self.commands[cmd.lower()]
			# check if userlevel requirements are met
			if (command['mod'] and user['mod']) or (command['subscriber'] and user['subscriber']) or (not command['mod'] and not command['subscriber']):
					self.response_command(user, command)
		else: # command not recognized
			pass
			# self.conn.send("PRIVMSG #%s :Command %s not recognized" %(self.config['channel'], cmd))

	# response command event
	def response_command(self, user, command):
		response = utils.format_message(user, command['response'])
		print "> " + response
		self.conn.send_channel(response)
