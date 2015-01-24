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
	


	# process custom command
	def process_custom(self, user, msg):
		msg = msg.split()
		cmd = msg[0]
		if cmd.lower() in self.commands['custom'].keys(): # command recognized
			command = self.commands['custom'][cmd.lower()]
			# check if userlevel requirements are met
			if utils.check_permissions(user, command):
				self.response_command(user, command)

	# response command event
	def response_command(self, user, command):
		response = utils.format_message(user, command['response'])
		self.conn.send_channel(response)

	# process basic command
	def process_basic(self, user, msg):
		msg = msg.split()
		cmd = msg[0]
		# check if userlevel requirements are met
		if cmd.lower() in self.commands['basic'].keys():
			command = self.commands['basic'][cmd.lower()]
			if not utils.check_permissions(user, command):
				return
		if cmd == '!timeout':
			self.timeout_command(user, msg)
		elif cmd == '!ban':
			self.ban_command(user, msg)
		elif cmd == '!unban':
			self.unban_command(user, msg)
		elif cmd == '!title':
			self.title_command(user, msg)
		elif cmd == '!game':
			self.game_command(user, msg)
		elif cmd == '!ad':
			self.ad_command(user, msg)
		elif cmd == '!cancelad':
			self.cancelad_command(user, msg)
		elif cmd == '!silence':
			self.silence_command(user, msg)

	# process timeout command
	def timeout_command(self, user, msg):
		if len(msg) >= 2 and self.commands['basic']['!timeout']['enabled']:
			target = msg[1]
			time = str(self.commands['basic']['!timeout']['time'])
			if len(msg) > 2 and utils.is_int(msg[2]):
				time = msg[2]
			self.conn.send_channel('.timeout %s %s' %(target, time))
			if self.commands['basic']['!timeout']['respond']:
				message = utils.format_message(user, self.commands['basic']['!timeout']['response'], target=target)
				self.conn.send_channel(message)

	# process ban command
	def ban_command(self, user, msg):
		if len(msg) >= 2 and self.commands['basic']['!ban']['enabled']:
			self.conn.send_channel('.ban %s' %(msg[1]))
			if self.commands['basic']['!ban']['respond']:
				message = utils.format_message(user, self.commands['basic']['!ban']['response'], target=msg[1])
				self.conn.send_channel(message)

	# process unban command
	def unban_command(self, user, msg):
		if len(msg) >= 2 and self.commands['basic']['!unban']['enabled']:
			self.conn.send_channel('.unban %s' %(msg[1]))
			if self.commands['basic']['!unban']['respond']:
				message = utils.format_message(user, self.commands['basic']['!unban']['response'], target=msg[1])
				self.conn.send_channel(message)

	# process title command
	def title_command(self, user, msg):
		if len(msg) >= 2 and self.commands['basic']['!title']['enabled']:
			pass # TODO
			if self.commands['basic']['!title']['respond']:
				message = utils.format_message(user, self.commands['basic']['!title']['response'])
				self.conn.send_channel(message)

	# process game command
	def game_command(self, user, msg):
		if len(msg) >= 2 and self.commands['basic']['!game']['enabled']:
			pass # TODO
			if self.commands['basic']['!game']['respond']:
				message = utils.format_message(user, self.commands['basic']['!game']['response'])
				self.conn.send_channel(message)

	# process ad command
	def ad_command(self, user, msg):
		if len(msg) >= 2 and self.commands['basic']['!ad']['enabled']:
			pass # TODO
			if self.commands['basic']['!ad']['respond']:
				message = utils.format_message(user, self.commands['basic']['!ad']['response'])
				self.conn.send_channel(message)

	# process cancelad command
	def cancelad_command(self, user, msg):
		if len(msg) >= 2 and self.commands['basic']['!cancelad']['enabled']:
			pass # TODO
			if self.commands['basic']['!cancelad']['respond']:
				message = utils.format_message(user, self.commands['basic']['!cancelad']['response'])
				self.conn.send_channel(message)

	# process silence command
	def silence_command(self, user, msg):
		if len(msg) >= 2 and self.commands['basic']['!silence']['enabled']:
			if msg[1] == 'on':
				if self.commands['basic']['!silence']['respond']:
					message = utils.format_message(user, self.commands['basic']['!silence']['response_on'])
					self.conn.send_channel(message)
				self.conn.silent = True
			elif msg[1] == 'off':
				self.conn.silent = False
				if self.commands['basic']['!silence']['respond']:
					message = utils.format_message(user, self.commands['basic']['!silence']['response_off'])
					self.conn.send_channel(message)


		
























