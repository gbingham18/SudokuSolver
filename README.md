# SudokuSolver.  

This is a python program that uses several hueristics to solve any valid Sudoku input.  

Includes a GUI built with the pygame library that shows the solving process of the puzzle.  

To run the program, enter . to represent a blank square, and 0 - 9 to set a square to a number.  

Here is an example of a valid input:  

2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3  

Columns are filled from top to bottom, left most column is filled first, like so:  

2 . . | . 3 . | . . .  
. . . | . . . | 4 . .  
. . 1 | 6 . . | . 5 . 
_____________________  
. . . | . . 6 | . 2 .  
. . . | . 9 . | . . .  
. 6 . | 8 . . | . . . 
_____________________    
. 2 . | . . 4 | 8 . .  
. . 7 | . . . | . . .  
. . . | . 7 . | . . 3   


