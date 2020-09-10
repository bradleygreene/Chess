# Chess
## Table Of Contents
* [General Information](#general-information)
* [Setup](#setup)
* [Updates](#updates)
## General Information
Chess is ran with:
- Python 2.7.17
- Pygame 1.9.6

This game was coded with python. It has all the rules for for chest including 
pawn promotion, en passant, and castling. The white pieces start first. A player 
wins by getting checkmate on the other's king. Stalemates are also included. 
Chess notation for each pieced move is printed to the console.
### Controls
- To move a piece, simply click on the piece you want to move and the 
location you want it to go. The piece you select will be highlighted, 
as well as the possible locations for that piece to move
- To undo a move, press `Z`
- To reset the game at any time, press `R`
## Setup
You can run the program by either :
1. Command line
   - `$ python ChessMain.py`
2. PyCharm
   - running ChessMain.py
## Updates
| Version | Description |
| ----: | :---------------------- |
| 0.1 | Initial setup on Github |
| 0.2 | Drawing board with pieces |
| 0.3 | Piece movement and 'undo' functionality |
| 0.4 | Valid piece movement and check/checkmate validation |
| 0.5 | Pawn promotion, en passant, and castling |
| 1.0 | UI features - highlighting/move animation/reset game |