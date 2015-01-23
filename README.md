#Firebot

##Overview
Firebot is a command-line utility that connects to a [Twitch.tv](http://www.twitch.tv) channel chat and outputs the chat messages. Firebot detects users name color, if they are subscribers and if they are Turbo users. Firebot will also anounce new subscribers in real-time.

***

##Requirements
To run Firebot you will need:
+ [Python 2.7](https://www.python.org/downloads/)

***

##Usage
By default Firebot will connect to the channel specified in the config. If you want to quickly connect to another channel you can specify the channel when launching Firebot.
```
python firebot.py [channel]
```

***

##Config
Firebot will use the options values in the `config` file if no other values are specified when launching Firebot.

###General options
Option         | Type      | Description
-------------- | --------- | -----------
`bot_user`     | *string*  | Username of the account with which Firebot will connect to the channel.
`bot_password` | *string*  | The password should be an OAuth token. You can get your OAuth token [here](http://www.twitchapps.com/tmi/).
`channel`      | *string*  | The channel Firebot will connect to.
`commands`     | *boolean* | If set to `true` Firebot will process user commands as specified in the file `commands`.<br>If set to `false` Firebot will **not** process user commands.
`log_chat`     | *boolean* |If set to `true` Firebot will log all chat messages to a file called `channel-yyyy-mm-dd-hh-mm-ss.log` in the `logs` folder.<br>If set to `false` Firebot will **not** log any messages.

###Caps options
Option         | Type      | Description
-------------- | --------- | -----------
`enabled`      | *boolean* | If set to `true` Firebot will monitor the chat for excessive caps.<br>If set to `false` Firebot will **not** monitor the chat for excessive caps.
`min_length`   | *integer* | Minimum number of characters in a message for Firebot to check caps.
`lower_limit`  | *integer* | Lower limit to which the maximum percentage of caps will be bound.
`upper_limit`  | *integer* | Upper limit to which the maximum percentage of caps will be bound.
`warn`         | *boolean* | If set to `true` Firebot will send a warning message when excessive caps are used.<br>If set to `false` Firebot will **not** send a warning message when excessive caps are used.
`warning`      | *string*  | Warning message Firebot will send if `warn` is set to `true`.
`timeout`      | *boolean* | If set to `true` Firebot will timeout users who use excessive caps.<br>If set to `false` Firebot will **not** timeout users who use excessive caps.
`timeout_time` | *integer* | Duration of the timeout in seconds.

###Polls options
Option         | Type      | Description
-------------- | --------- | -----------
`enabled`      | *boolean* | If set to `true` Firebot will respond to poll commands.<br>If set to `false` Firebot will **not** respond to poll commands.
`start`        | *string*  | Message Firebot will send when a poll is started.
`start_error`  | *string*  | Message Firebot will send when trying to start a poll while a poll is already running.
`end`          | *string*  | Message Firebot will send when a poll is ended.
`restart`      | *string*  | Message Firebot will send when a poll is restarted.
`stats`        | *string*  | Message Firebot will send when the poll stats are requested.

***

##Commands
All commands must have all their options specified to prevents errors.

###Response commands
Response commands are defined in the `commands` file in JSON format.

####Options
Option         | Type      | Description
-------------- | --------- | -----------
`mod`          | *boolean* | If set to `true` Firebot will **not** respond to users who are not moderatos.<br>If set to `false` Firebot will respond to users who are not moderators.
`subscriber`   | *boolean* | If set to `true` Firebot will **not** respond to users who are not subscribers.<br>If set to `false` Firebot will respond to users who are not subscribers.
`response`     | *string*  | Message Firebot will respond to this command.<br>[Variables](#variables) can be used.

####Variables
This variables can be used in any response command response and will be replaced by the apropiate value.

Variable | Value
-------- | -------
`$user`  | Username of the user who sent the command.
`$time`  | Current time of the machine where Firebot is running, with format `hh:mm:ss AM/PM`.

####Example
```json
"!firebot" : {
	"mod": false,
	"subscriber": false,
	"response": "To find more about Firebot visit http://github.com/PacoHobi/Twitch-Firebot"
}
```
###Poll commands
Command                                   | Description
----------------------------------------- | -----------
`!poll start option1 | option2 | option3` | Starts a poll with options option1, option2, option3. More (or less) options can de declared.
`!poll end`                               | Ends the current poll.
`!poll restart`                           | Restarts the votes of the current poll.
`!poll stats`                             | Firebot will respond with the current poll results.
`!vote [OptionNumber]`                    | Votes for the `[OptionValue]` option of the current poll.