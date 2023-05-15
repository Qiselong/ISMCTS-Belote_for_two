IMPORTANT: executions are done from the /src folder
The two executions you may want to do are for files:
    - tutorial.py (recommended)
    - main.py

Notes: 
    - you need to have python working on your computer. you can find it here: https://www.python.org/downloads/
    - the programm should work fine for linux, windows & mac. However, if you have any problem on your windows or mac, please mail me as soon as possible so I can fix it in time.
    - the deadline for sending the logs is 25th of May, please don't forget about it ! Also, when sending the logs, tell me if you want to be credited in the final report.

You can find the rules in the file tutorial.txt; alternatively I suggest you run tutorial.py to play a test-game against a random opponent.

The game is played by running main.py. When it is your turn to play, the program suggest to you playable cards. You then enter the corresponding number then enter.

A game tipycally lasts 2 to 6 minutes depending on how much thinking you give it. I do not require from you a minimum number of game to be played, just send me the results when you are done with it. 
At the end of each game, the logs are automatically stored in logs.txt. When you are done participating in the experiment, please send this file to me at thomas.boudier@gssi.it. 
In STA.pdf you can find a complete description on how the AI works as well as reference under the form of a research report.

Some tips:
    - your opponent cannot infer what is in your hand from your previous moves, but you can.
    - your opponent never does "exploration" moves, aka sacrificing a card to get informations about the cards in hand; but you can.
    - cards in hand have more values than cards visible to all. The more cards you have in hands, the less enlightened will be the decisions of your opponent.
    - the less information are hidden to your opponent, the better he will become as his prediction will be more accurate.
