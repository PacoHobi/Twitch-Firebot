#!/usr/bin/env python

"""
img-ascii is a simple command-line utility that converts images to ASCII art images.
For more information visit https://github.com/PacoHobi/img-ascii
"""

__title__ = "firebot"
__version__ = "1.0"
__author__ = "Paco Hobi"


import irc, sys, os
from time import strftime
from json import load as json_load
from thread import start_new_thread

# read preferences file
def load_pref(f):
	with open(f) as file:
		return json_load(file)

# initiliaze user info in the users dictionary
def init_user(user):
	if user not in users.keys():
		users[user] = {'follower':False,'subscriber':False,'turbo':False,'mod':False,'color':'default','emoteset':'[]'}

# process message from the server
def process_message(message):
	split = message.split(' ', 2)
	user = split[0][1:].split('!', 1)[0]
	command = split[1]
	msg = split[2].split(' :', 1)
	if len(msg) > 1:
		msg = msg[1]
	else:
		msg = msg[0]
	if command == 'PRIVMSG':
		if user == 'jtv':
			system_message(msg)
		elif user == 'twitchnotify':
			months = '1'
			split = msg.split()
			if len(split) > 3:
				months = split[3]
			user_subscribed(split[0], months)
		else:
			user_message(user, msg)
	elif command == 'MODE':
		msg = msg.split()
		if msg[1] == '+o':
			add_mod(msg[2])
		elif msg[1] == '-o':
			remove_mod(msg[2])
	else:
		pass
		# print "\033[31m%s\033[m" %(message)

# system message event
def system_message(msg):
	msg = msg.split()
	cmd = msg[0]
	user = msg[1]
	if len(msg) > 2:
		value = msg[2]
	init_user(user)
	if cmd == 'SPECIALUSER':
		users[user][value] = True
	elif cmd == 'USERCOLOR':
		users[user]['color'] = value
	elif cmd == 'EMOTESET':
		users[user]['emoteset'] = value
	elif cmd == 'CLEARCHAT':
		pass
	else:
		print "\033[31m%s\033[m" %(' '.join(msg))

# user message event
def user_message(user, msg):
	init_user(user)
	flags = ''
	if users[user]['subscriber']:
		flags += 'S'
	else:
		flags += ' '
	if users[user]['follower']:
		flags += 'F'
	else:
		flags += ' '
	if users[user]['turbo']:
		flags += 'T'
	else:
		flags += ' '
	if users[user]['mod']:
		print "[%s][%s] \033[32;1m%s\033[m: %s" %(flags, users[user]['color'], user, msg)
	else:
		print "[%s][%s] \033[1m%s\033[m: %s" %(flags, users[user]['color'], user, msg)
	if preferences['log_chat']:
		log("[%s] %s: %s\n" %(strftime("%H:%M:%S"), user, msg), logfile)

# user subscription event
def user_subscribed(user, months):
	print "\033[33;1mNew subscriber: %s [%s]\033[m" %(user, months)

# add mod event
def add_mod(user):
	init_user(user)
	users[user]['mod'] = True

# remove mod event
def remove_mod(user):
	init_user(user)
	users[user]['mod'] = False

# log message to file
def log(m, f):
	f.write(m)
	f.flush()

conn = irc.IRC() # irc object
preferences = load_pref('preferences') # preferences dictionary
users = {} # users dictionary

channel = preferences['channel'] # channel from preferences
if len(sys.argv) > 1: # if channel specified as an argument we ignore the channel in preferences
	channel = sys.argv[1]
conn.connect('irc.twitch.tv') # connect to the server
conn.login(preferences['bot_user'], preferences['bot_password']) # login the bot
conn.join('#'+channel) # join the channel
conn.send("TWITCHCLIENT 3") # to receive user info (usermode, color, emotesets) and twitchnotify (user subscriptions)
#open file for log chat
if (preferences['log_chat']):
	if not os.path.exists('logs'):
		os.makedirs('logs')
	logfile = open('logs/'+channel+'-'+strftime("%Y-%m-%d-%H-%M-%S")+'.log', 'w+')
try:
	start_new_thread(conn.receive, (process_message,)) # listen for messages from the server
except:
	print "Error: unable to start thread"
	exit()


# manage user input
while True:
	s=raw_input()
	print 
	print users.keys()
	print 