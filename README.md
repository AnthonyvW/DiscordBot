# DiscordBot

This is a bot meant to roll dice. It allows for placing a message when rolling dice, exploding dice both on a 1 and on the max, adding to the result, adding to every dice rolled, and showing what dice were rolled.

```
python -m venv venv
venv\Scripts\activate.bat
pip install discord.py
```

Go to https://discord.com/developers/docs/intro

click Applications

click New Application in top right corner

go to OAuth, change Authorization method to be in app authorization

select bot as scope
select administrator as its permissions

go to Oauth URL generator
select bot as scope
select administrator in the area that appears

Go to Bot
Enable all 3 privileged intents

A URL will appear that you can use to invite a bot
