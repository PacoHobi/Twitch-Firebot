#!/usr/bin/env python

from time import strftime

# formats a string wirh our custom variables
def format_message(user, message, target=''):
	message = message.replace('$user$', user['user'])
	message = message.replace('$target$', target)
	message = message.replace('$time$', strftime("%I:%M:%S %p"))
	return message

# returns true if the input is an integer
def is_int(s):
	try: 
		int(s)
		return True
	except ValueError:
		return False

# check if a user has the permissions for a command
def check_permissions(user, command):
	if (command['mod'] and user['mod']) or (command['subscriber'] and user['subscriber']) or (command['owner'] and user['owner']) or (not command['mod'] and not command['subscriber'] and not command['owner']):
		return True
	else:
		return False