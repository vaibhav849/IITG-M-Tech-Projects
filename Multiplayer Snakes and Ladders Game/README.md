# 1. Multiplayer Snakes and Ladders Game
## Introduction
The main objective of this project is to create a Multiplayer Snakes and Ladders Game that creates multiple players  and implement Inter-Process Communication among them with the help of Pipes. In this game players works as child processes and board game is the parent process and communication between players and board game is happening through pipes. 
## How to run?
The folder Multiplayer Snakes and Ladders Game contains snakes_ladders.c which can be executed as:

```gcc snakes_ladders.c N P input.txt```

Where,
N is size of grid.
P is number of players.
input.txt is the input file which contains information about positions of snakes and ladders for example,

```S 45 3```

means there is a snake from 45 to 3.

```L 16 72```

means there is a ladder from 16 to 72.