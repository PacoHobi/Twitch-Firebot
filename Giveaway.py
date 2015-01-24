#!/usr/bin/env python

from random import choice as random_choice

class Giveaway():
	# init poll object
	def __init__(self, conn, config):
		self.conn = conn
		self.config = config
		self.started = False
		self.keyword = ''
		self.users = []
		
	# process command
	def process(self, user, message):
		msg = message.split(' ', 2)
		if len(msg) == 1:
			return
		msg[0] = msg[0].lower()
		msg[1] = msg[1].lower()
		if msg[0] == '!giveaway':
			sub = msg[1]
			if sub == 'start':
				self.start_command(user, msg)
			elif sub == 'end' and self.started:
				self.end_command(user, msg)
			elif sub == 'restart' and self.started:
				self.restart_command(user, msg)
			elif sub == 'stats' and self.started:
				self.stats_command(user, msg)
			elif sub == 'draw' and self.started:
				self.draw_command(user, msg)
		elif msg[0] == '!enter' and self.started:
			self.enter_command(user, msg)
			

	# process start command
	def start_command(self, user, msg):
		if self.started:
			self.conn.send_channel(self.config['giveaways']['start_error'])
			return
		if len(msg) < 3:
			return
		self.started = True
		self.keyword = msg[2]
		response = self.config['giveaways']['start'].replace('$keyword$', self.keyword)
		self.conn.send_channel(response)

	# process end command
	def end_command(self, user, msg):
		self.started = False
		self.keyword = ''
		self.users = []
		self.conn.send_channel(self.config['giveaways']['end'])
	
	# process restart command
	def restart_command(self, user, msg):
		self.users = []
		response = self.config['giveaways']['restart'].replace('$keyword$', self.keyword)
		self.conn.send_channel(response)

	# process stats command
	def stats_command(self, user, msg):
		response = self.config['giveaways']['stats'].replace('$n$', str(len(self.users)))
		self.conn.send_channel(response)

	# process draw command
	def draw_command(self, user, msg):
		if len(self.users) > 0:
			response = self.config['giveaways']['draw'].replace('$winner$', random_choice(self.users))
			self.conn.send_channel(response)

	# process enter command
	def enter_command(self, user, msg):
		if msg[1] == self.keyword and user['user'] not in self.users:
			self.users.append(user['user'])