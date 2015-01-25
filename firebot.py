#!/usr/bin/env python

"""
img-ascii is a simple command-line utility that converts images to ASCII art images.
For more information visit https://github.com/PacoHobi/img-ascii
"""

__title__ = "firebot"
__version__ = "1.0"
__author__ = "Paco Hobi"


import irc, sys, os, CommandProcessor, Caps, Poll, Giveaway, TwitchAPI
from time import strftime
from json import load as json_load
from thread import start_new_thread

# read config file
def load_config(f):
	with open(f) as file:
		return json_load(file)

# initiliaze user info in the users dictionary
def init_user(user):
	if user not in users.keys():
		users[user] = {'user':user,'follower':False,'subscriber':False,'turbo':False,'mod':False,'owner':False,'color':'default','emoteset':'[]'}
		if user == config['channel']:
			users[user]['owner'] = True

# process message from the server
def process_message(message):
	split = message.split(' ', 2)
	user = split[0][1:].split('!', 1)[0]
	command = split[1]
	msg = split[2].strip(' \t\n\r').split(' :', 1)
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
	elif command == 'NOTICE' and msg in ['Error logging in', 'Login unsuccessful']:
		echo('Error logging in, check that the bot_user option is correct. If error persist get a new OAuth token', c=1, b=1)
		exit()

# system message event
def system_message(message):
	msg = message.split()
	cmd = msg[0]
	if len(msg) > 1:
		user = msg[1]
	else:
		print "\033[31m%s\033[m" %(' '.join(msg))
		return
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
		print "\033[31m%s\033[m" %(message)

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
	if config['log_chat']:
		log("[%s] %s: %s\n" %(strftime("%H:%M:%S"), user, msg), logfile)
	# commands
	split = msg.split()
	if split[0].lower() in ['!poll','!vote'] and config['polls']['enabled']:
		poll.process(users[user], msg)
	elif split[0].lower() in ['!giveaway','!enter'] and config['giveaways']['enabled']:
		giveaway.process(users[user], msg)
	elif split[0].lower() in commands.commands['basic'].keys() and config['commands']:
		commands.process_basic(users[user], msg)
	elif split[0].lower() in commands.commands['custom'].keys() and config['commands']:
		commands.process_custom(users[user], msg)
	# check caps
	if config['caps']['enabled']:
		caps.check(users[user], msg)

# user subscription event
def user_subscribed(user, months):
	print '\033[33;1mNew subscriber: %s [%s]\033[m' %(user, months)

# add mod event
def add_mod(user):
	init_user(user)
	users[user]['mod'] = True

# remove mod event
def remove_mod(user):
	init_user(user)
	users[user]['mod'] = False

# print to console
def echo(message, c=4, b=False, i=False, u=False):
	opts = []
	if c is not False and c in range(8):
		opts.append(str(30 + c))
	if b is not False:
		opts.append('1')
	if i is not False:
		opts.append('3')
	if u is not False:
		opts.append('4')
	print '\033[%sm%s\033[m' %(';'.join(opts), message)


# log message to file
def log(m, f):
	f.write(m)
	f.flush()

# exit firebot
def exit():
	os._exit(1)


base_dir = os.path.dirname(os.path.realpath(__file__)) # directory of the script
conn = irc.IRC() # irc object
echo('Loading config ...')
config = load_config(base_dir + '/config') # config dictionary
commands = CommandProcessor.CommandProcessor(conn, config, base_dir + '/commands')
caps = Caps.Caps(conn, config)
poll = Poll.Poll(conn, config)
giveaway = Giveaway.Giveaway(conn, config)
users = {} # users dictionary

if len(sys.argv) > 1: # if channel specified as an argument we ignore the channel in config
	config['channel'] = sys.argv[1].lower()
else:
	config['channel'] = config['channel'].lower()
echo('Connecting to Twitch IRC server ...')
try:
	conn.connect('irc.twitch.tv') # connect to the server
except:
	echo('Error connecting to the server', c=1, b=1)
	exit()
echo('Logging in as %s...' %config['bot_user'])
conn.login(config['bot_user'], config['bot_password']) # login the bot
echo('Joining channel %s...' %config['channel'])
conn.join('#'+config['channel']) # join the channel
conn.send('TWITCHCLIENT 3') # to receive user info (usermode, color, emotesets) and twitchnotify (user subscriptions)
echo('Firebot is up and ready!', b=1)
#open file for log chat
if (config['log_chat']):
	if not os.path.exists(base_dir + '/logs'):
		os.makedirs(base_dir + '/logs')
	logfile = open(base_dir + '/logs/'+config['channel']+'-'+strftime("%Y-%m-%d-%H-%M-%S")+'.log', 'w+')
try:
	start_new_thread(conn.receive, (process_message,)) # listen for messages from the server
except:
	echo('Error: unable to start thread', c=1, b=1)
	exit()


# manage user input
while True:
	s=raw_input()
	# conn.send_channel(s)
	twitch.request(twitch.links['channel'])