'''
This program was created by Ian Schwartz
What it does:
    * Connect to twitch using IRC
    * Joins my channel
    * Keeps connection active
    * Run special functions as needed (Like GT guessing game)

Helpful links:
https://www.techbeamers.com/create-python-irc-bot/
https://dev.twitch.tv/docs/irc/guide

GT Guide:
Standard - 20
MC - 22
MCS - 26
Full - 27 - GT Key will most likely be outside of the tower, so can't check # of pulls.
'''

from settings import *
from irc_class import *
import os
import random

irc = IRC()
irc.connect(server, port, channel, botnick, botpass)

gtactive = False
enterednames = [] #this may not be necessary, but just for safety....
killbot = False #added this so I can close the bot on command
chatfile = open("lastchat.txt","wt")

while not killbot:
    text = irc.get_response()
    print(text)

    #text will look like this:
    #:lupisdragon!lupisdragon@lupisdragon.tmi.twitch.tv PRIVMSG #lupisdragon :testing
    #:nightbot!nightbot@nightbot.tmi.twitch.tv PRIVMSG #lupisdragon :@LupisDragon -> Current Stream Title: Finding motivation

    if "PRIVMSG" in text:
        text = text[1:]
        nameend = text.index("!")
        name = text[0:nameend] #gets the name of the sender
        msgindex = text.index(":") + 1
        msg = text[msgindex:] #grab the rest of the message (the part we actually want)

        chatfile.write(name + ": " + msg")
        
        if (name in gtapproved) and (not gtactive) and (msg.startswith("!gt")): #init the guessing game
            print("Setting up GT guessing game.\n")
            enterednames = [] #a list of the names that have guessed
            checks = [] #initialize the empty list of the checks
            if (msg[4:7] == "mc\r"):
                numchecks = 22
            elif (msg[4:7] == "mcs"):
                numchecks = 26
            else:
                numchecks = 20
            print("Number of checks: " + str(numchecks))
            x = 0
            while x < numchecks:
                checks.append([])
                x += 1
            gtactive = True
            print("Set up complete.")
            irc.send(channel, "All right chat, get your guesses into chat as to where the big key is! Type '!bet ##' (1 - " + str(numchecks) + ") to get your guess in!")
        elif (name in gtapproved) and (gtactive) and (msg.startswith("!end")): #end the guessing game
            gtactive = False
            print("Guessing game ended")
            irc.send(channel, "Ok chat, guesses are locked in, and there's no more guessing for now! Good luck to all the entrants!")
        elif (name in gtapproved) and (not gtactive) and (msg.startswith("!win")): #declare winners
            try:
                correct = int(msg[5:7]) - 1
                print("Winning position (value-1): " + str(correct))
                if (correct >= 0) and (correct < numchecks):
                    print("Check list: \n" + str(checks))
                    if (checks[correct] != []): #ie, there are people who guessed correctly
                        irc.send(channel,"All right chat, lets give a big hand to the winners of the guessing game!")
                        irc.send(channel,"Winners are:")
                        print("Winners this run:")
                        while (checks[correct] != []):
                            winner = checks[correct].pop()
                            irc.send(channel, "@" + winner)
                            print(winner)
                    else:
                        irc.send(channel, "No one guessed correctly. Better luck next time!")
                        print("No winners this run.")
                else:
                    irc.send(channel, name + " goofed, and entered something out of range. One moment while we figure this out!")
                    print("NUMBER OUT OF RANGE! CHECK CODE IF CORRECT USAGE!")
            except:
                irc.send(channel,"Oops. something went wrong with the bot command. Give us a moment to figure it out!")
                print("TRY BRANCH THREW EXCEPTION. CHECK CODE IF CORRECT USAGE!")
        elif (gtactive) and (msg.startswith("!bet")) and (name not in enterednames): #someone is betting for the first time
            try:
                enter = int(msg[5:7]) - 1
                if (enter >= 0) and (enter < numchecks): #the bet is within range
                    checks[enter].append(name)
                    enterednames.append(name)
                    irc.send(channel, "@" + name + "! Your bet has been entered! Good Luck!")
                else:
                    irc.send(channel, "@" + name + ": Your bet was outside the scope. Please enter a number between 1 and " + str(numchecks) + ".")
            except: #not a valid bet
                irc.send(channel, "Sorry, @" + name + ", your entry was invalid. correct format is !bet ## (1 - " + str(numchecks) + ")")
                
        elif (gtactive) and (msg.startswith("!bet")) and (name in enterednames): #someone tried betting again
            irc.send(channel, "@" + name + ", you have already bet correctly. Please wait for the results. Thanks, and good luck!")
        elif (gtactive) and (msg.startswith("!reminder")): #anyone wants a reminder
            irc.send(channel, "Reminder chat! You can get in on the GT guessing game! Just type '!bet ##' (1 - " + str(numchecks) + ") to get your guess in! It'll close when I enter GT, so get those guesses in!")
        elif (name == botnick) and (msg[0:8] == '!killbot'):
            killbot = True
chatfile.close()
