#Firebot

##Overview
Firebot is a command-line utility that connects to a [Twitch.tv](http://www.twitch.tv) channel chat and outputs the chat messages. Firebot detects users name color, if they are subscribers and if they are Turbo users. Firebot will also anounce new subscribers in real-time.


##Requirements
To run Firebot you will need:
+ [Python 2.7](https://www.python.org/downloads/)


##Usage
By default Firebot will connect to the channel specified in the config. If you want to quickly connect to another channel you can specify the channel when launching Firebot.
```
python firebot.py [channel]
```

##Config
Firebot will use the options values in the `config` file if no other values are specified when launching Firebot.

Option         | Type      | Description
-------------- | --------- | -----------
`bot_user`     | *string*  | Username of the account with which Firebot will connect to the channel
`bot_password` | *string*  | The password should be an OAuth token. You can get your OAuth token [here](http://www.twitchapps.com/tmi/)
`channel`      | *string*  | The channel Firebot will connect to
`commands`     | *boolean* | If set to `true` Firebot will process user commands as specified in the file `commands`<br>If set to `false` Firebot will not process user commands 
`log_chat`     | *boolean* |If set to `true` Firebot will log all chat messages to a file called `channel-yyyy-mm-dd-hh-mm-ss.log` in the `logs` folder<br>If set to `false` Firebot will not log any messages


##Commands
All commands are defined in the `commands` file in JSON format. All commands must have all their options specified to prevents errors.

###Response commands
Option         | Type      | Description
-------------- | --------- | -----------
`mod`          | *boolean* | If set to `true` Firebot will **not** respond to users who are not moderatos<br>If set to `false` Firebot will respond to users who are not moderators
`subscriber`   | *boolean* | If set to `true` Firebot will **not** respond to users who are not subscribers<br>If set to `false` Firebot will respond to users who are not subscribers
`response`     | *string*  | Message Firebot will respond to this command<br>[Variables](#variables) can be used
####Example
```json
"!firebot" : {
	"mod": false,
	"subscriber": false,
	"response": "To find more about Firebot visit http://github.com/PacoHobi/Firebot"
}
```

###Variables
This variables can be used in any command response and will be replaced by the apropiate value.

Variable | Value
-------- | -------
`$user`  | Username of the user who sent the command
`$time`  | Current time of the machine where Firebot is running, with format `hh:mm:ss AM/PM`
