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

Option         | Description
-------------- | -----------
`bot_user`     | Username of the account with which Firebot will connect to the channel
`bot_password` | The password should be an OAuth token. You can get your OAuth token [here](http://www.twitchapps.com/tmi/)
`channel`      | The channel Firebot will connect to
`log_chat`     | If set to `true` Firebot will log all chat messages to a file called `channel-yyy-mm-dd-hh-mm-ss.log`<br>If set to `false` Firebot will not log any messages
