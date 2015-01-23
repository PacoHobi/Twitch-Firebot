#!/usr/bin/env python

import utils
from json import load as json_load
from time import strftime

class Caps():
	# load the commands from file f
	def __init__(self, conn, config):
		self.conn = conn
		self.config = config
		
	# check caps
	def check(self, user, message):
		if len(message) > self.config['caps']['min_length']:
			count = sum(1 for c in message if c.isupper())
			percentage = 100. * count / len(message)
			limit = 100. - .6 * len(message)
			limit = max(min(limit, self.config['caps']['upper_limit']), self.config['caps']['lower_limit'])
			if percentage > limit:
				# warning
				if self.config['caps']['warn']:
					warning = utils.format_message(user, self.config['caps']['warning'])
					self.conn.send_channel(warning)
				# timeout
				if self.config['caps']['timeout']:
					self.conn.send_channel('.timeout %s %d' %(user['user'], self.config['caps']['timeout_time']))
