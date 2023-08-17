# Goofy-ahh-Chess
Right now, This seeks to be a fully coded game of chess that acounts for all standard chess rules as a fun personal python project. Eventually, I will add my own spin on the game.

## Progress thus far
Most of the work will be commited to 'Pre-release-main', and will be mostly back-end stuff. Right now, the entirety of the game is being tested through a coupld of csv files. my original plan was to eventually utilize a gui library like pygame. However, for the time being I have set up a couple of bash scripts to continuously display the updated csv files in tmux and To be honest, I kind of like how it looks. For this reason, I renamed the project to 'Terminal Chess'. 

## Project organization
The bulk of this project includes the two python files that I have, main.py and legal.py. Main.py is the main event loop for my program and contains the logic for terminal input to control the pieces To move the pieces or do anything of that sort, leggal.py is called. In it, there are two classes: 'Board' and 'Piece'. What they do is as follows:

### Board
This function is used to move the pieces. It also contains some misc. methods.
#### Methods
* update: Decides how to call the move function, and how many times in the case of a special move being presented.
* move: Takes a piece from its old position and moves it to its new position, replacing the old position with an empty square.
* letterNum_to_coords: This misc. method takes user input as traditional chess coords (letter, number) and converts it to a tuple of csv row and column number.


### Piece
The pieces have quite a few functions that determine the legality of moving a piece. The way this project is designed, the user will select their designated piece, and then there is a display that shows all available legal moves. The user makes a move, or selects a different piece, and then it is the opponent's turn.

The specific formula for how a legal move is calculated is as follows:

legalMoves_final=((legalMoves_general + specialMoves) | legalMoves_inCheck) * legalMoves_pin

Basically, I first account for the general moves where I assume that the king is not on the board. If there are any special moves, I add it to this list. Then I see if the king is in check. If it is, pieces are limited to a certain square, vector, or they are not able to move at all (especially if there is more than one check. If the piece is pinned, I convolute the matrix of legal moves for the piece with the vector that the piece is pinned to (since a piece can't move to put own king in check).

There are some other things to check though. At the start of each turn, the king's position must be checked to see if it is in check. If it is, see if there are any pieces that can block the check or capture the piece that is giving the check. If not, the king must move. If the king cant move, then it is checkmate and the opponent wins.

A similar method also applies to stalemate, but this is more complicated. Stalemate occurs when one player doesn't have any legal moves. This would involve checking every single piece for its legal moves. I have yet to implement this.

In specific, here are the names of all the methods in thi class and what they do:
#### Methods
* getPiece: This reads the piece from a specified position of the 'chess.csv' file.
* getLegal: This gets the all possible positions that a piece could move assuming that there are no other pieces on the board.
* getLegal_limited: this is a subfunction of getLegal that only applies to knights and kings.
* getLegal_special: If the piece selected has special moves (castling, en-passant, or promotions) then this function will see if they are legal and add them to legalMoves_general.
* 
* getLegal_pin: Basically, it will return if a piece is pinned your king or not, as well as the new legal moves list for the piece.
* getLegal_mate: Checks to see if the king is checkmated or not. This is dependent on 'getLegal_pieceControl'
* getLegal_piecControl: returns how many times own king is in check (assuming total legality, it is either 0, 1 or 2) However, with some other arguements, this method can also be configured to see if how many pieces (either yours or your opponent's) controls a certain square.

Right now, this project still isn't fully complete. For the time being, i have yet to fix some bugs with castling and add promotions.
