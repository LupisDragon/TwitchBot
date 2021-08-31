# TwitchBot
A special bot I created for my twitch channel. Plays the GT guessing game on my command.

The "fakesettings.py" file would need to be re-named to "settings.py" for the code to work.
Also, the first three lines in "fakesettings.py" need to be changed. The lines are for example only.

Commands:
* As user:
  * !gt - Start standard GT guessing game
  * !gt mc - Start GT guessing game, where maps/compasses are shuffled
  * !gt mcs - Start GT guessing game, where maps/compasses/small keys are shuffled
  * !end - Will lock the guessing game, so no more bets can be taken
  * !win ## - Declare winners on that check
* As anyone (including user):
  * !bet ## - Bet which position is the winner. (NOTE: Only works while the guessing game is active)
  * !reminder - Show a reminder of how to bet
