#!/usr/bin/env python

from time import strftime

# formats a string wirh our custom variables
def format_message(user, message):
	message = message.replace('$user', user['user'])
	message = message.replace('$time', strftime("%I:%M:%S %p"))
	return message