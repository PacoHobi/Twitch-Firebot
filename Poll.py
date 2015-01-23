#!/usr/bin/env python

class Poll():
	# init poll object
	def __init__(self, conn, config):
		self.conn = conn
		self.config = config
		self.started = False
		self.options = {}
		self.voters = []
		
	# process command
	def process(self, user, message):
		msg = message.split(' ', 2)
		if len(msg) == 1:
			return
		msg[0] = msg[0].lower()
		msg[1] = msg[1].lower()
		if msg[0] == '!poll':
			sub = msg[1]
			if sub == 'start':
				self.start_command(user, msg)
			elif sub == 'end' and self.started:
				self.end_command(user, msg)
			elif sub == 'restart' and self.started:
				self.restart_command(user, msg)
			elif sub == 'stats' and self.started:
				self.stats_command(user, msg)
		elif msg[0] == '!vote' and self.started:
			self.vote_command(user, msg)
			

	# process start command
	def start_command(self, user, msg):
		if self.started:
			self.conn.send_channel(self.config['polls']['start_error'])
			return
		if len(msg) < 3:
			return
		self.started = True
		for i, opt in enumerate(o.strip() for o in msg[2].split('|')):
			self.options[str(i+1)] = {'option':opt, 'votes':0}
		optList = ', '.join('%s: %s' %(key, self.options[key]['option']) for key in sorted(key for key in self.options))
		response = self.config['polls']['start'].replace('$options$', optList)
		self.conn.send_channel(response)

	# process end command
	def end_command(self, user, msg):
		resList = ', '.join('%s (%d)' %(option,votes) for (votes,option) in reversed(sorted((self.options[key]['votes'], self.options[key]['option']) for key in self.options.keys())))
		response = self.config['polls']['end'].replace('$options$', resList)
		self.conn.send_channel(response)
		self.started = False
		self.options = {}
		self.voters = []

	# process restart command
	def restart_command(self, user, msg):
		if self.started:
			optList = ', '.join('%s: %s' %(key, self.options[key]['option']) for key in sorted(key for key in self.options))
			response = self.config['polls']['restart'].replace('$options$', optList)
			self.conn.send_channel(response)
			for key in self.options.keys():
				self.options[key]['votes'] = 0
			self.voters = []

	# process stats command
	def stats_command(self, user, msg):
		resList = ', '.join('%s (%d)' %(option,votes) for (votes,option) in reversed(sorted((self.options[key]['votes'], self.options[key]['option']) for key in self.options.keys())))
		response = self.config['polls']['stats'].replace('$options$', resList)
		self.conn.send_channel(response)

	# process vote command
	def vote_command(self, user, msg):
		opt = msg[1]
		if user['user'] not in self.voters and opt in self.options.keys():
			self.options[opt]['votes'] += 1
			self.voters.append(user['user'])