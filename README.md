# IITG-M-Tech-Projects
## 1. SAT Solver
### Introduction
The main objective of this project is to implement a sat solver which takes cnf files in DIMACS format as input and assign boolean value to each variable if the given cnf is SATISFIABLE otherwise it produces UNSATISFIABLE as output.  For more info check here-
https://github.com/vaibhav849/IITG-M-Tech-Projects/blob/master/SAT_Solver/Report.pdf
### How to run?
To run code use jupyter notebooks the ipynb file and input file should be in same folder. While running cells in jupyter notebook it will ask for name of input file and output file from user. After entering input and output file code will complete execution and load ouput of code in output file.
To run python file use this command :

```python3 Solver.py```

```Enter Input File: sat3.cnf```

```Enter Output File: sat3_output.txt```

## 2. Multiplayer Snakes and Ladders Game
### Introduction
The main objective of this project is to create a Multiplayer Snakes and Ladders Game that creates multiple players  and implement Inter-Process Communication among them with the help of Pipes. In this game players works as child processes and board game is the parent process and communication between players and board game is happening through pipes. 
### How to run?
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
## 3. Linux Shell Simulation

