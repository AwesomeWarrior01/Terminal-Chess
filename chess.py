import pygame
import stockfish
import csv

# note to self: board will be indexed 1-8.
# board is index by (column, row). This means that (0,0) refers to the piece in the upper-left hand corner.

# TODO: Instead of checking if a move is legal after the fact, I'm going to make it so that all legal moves are calculated and shown when you click a piece.
    # the king will be an exception to this. It will still only show its legal moves when it has been clicked, but it will also calculate its legal moves in the background.
        #This will occur at the start of each player's turn.
    # This will involve changing the following functions:
        #'move_check' will become 'getLegal_general', and it will return the pieces possible moves if there were no other pieces on the board, based on its current position.
        #'kingCheck_check' will become 'getLegal_pin'. It will only look at pieces that could be pinned to the king.
        #'move_check_limited' will become 'getLegal_limited', and it will remain relatively the same.
    # Another method also needs to be implemented that checks for obstacles (pieces that are your own color, or any squares past an opponent's piece).
    # Pieces cannot move to or past obstacles (note that knights do not have obstacles).
        #This method could be called 'getLegal_obstacle' 

# TODO: There are 4 types of illegal moves. They are:

# 1. Moving a piece in a direction it cannot normally go (i.e. moving a king as if it were a queen).
# 2. Moving through pieces as with the pawn, bishop, rook, or queen.
# 3. Moving your own king into check.
# 4. Moving your own piece that would put your own king into check

# So far, only #1 and #4 has been taken care of. However, #2 and #3 still need to be done.

# TODO: I'm currently at a dilemna when it comes to recording general piece legality: Do I append every position one-by-one to a csv file, or do I create a list and append to that?
# Also, to make things easier, should I get rid of the child classes and just have one piece class with if statements?
# I think I will do this since I want all pieces to share one legalMoves variable. Also, I don't think there's much merit in having child classes since
# Also, I don't think there's much merit in having child classes since each child class (except for pawns) only has like one thing in it.
class Board:
    def __init__(self) -> None:
        with open('chess.csv', 'w') as board:
            #This just creates the stating position by adding a whole bunch of rows to csv file
            writer = csv.writer(board)
            writer.writerow(['r','n','b','q','k','b','n','r'])
            writer.writerow(['p','p','p','p','r','p','p','p'])
            writer.writerow(['q','o','o','n','o','n','o','b'])
            writer.writerow(['q','o','n','p','r','p','n','b'])
            writer.writerow(['q','o','o','r','K','r','o','b'])
            writer.writerow(['o','q','n','p','r','p','n','o'])
            writer.writerow(['P','P','o','n','P','n','n','P'])
            writer.writerow(['R','N','r','Q','K','q','N','R'])
    # This method will update piece positions in csv file
    def update(self, oldPos, newPos, specialMove, white):
        piece = Piece.get_piece(self, oldPos)
        
             # This is the default case that works for any normal move or capture.
        if specialMove == 0:
            pass
        # This will be for Kingside Castling
        elif specialMove == 1:
            pass
        # Queenside Castling
        elif specialMove == 2:
            pass
        # Queen Promotion
        elif specialMove == 3:
            pass
        # Rook Promotion
        elif specialMove == 4:
            pass
        # Knight promotion
        elif specialMove == 5:
            pass
        # Bishop promotion
        elif specialMove == 6:
            pass
        else:
            print("Bruh what kinda goofy-ahh move did you just make??")

        Board.move(self, oldPos, newPos, piece)

    def move(self, oldPos, newPos, piece):
        with open('chess.csv', 'r') as board:
            reader = csv.reader(board, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            print("this is the reader" + str(reader))
            layout = list(reader)
            print(piece)
        with open('chess.csv', 'w') as board:
            layout[oldPos[0]][oldPos[1]] = 'o'
            print("this is oldpos:" + str(oldPos))
            layout[newPos[0]][newPos[1]] = piece

            writer = csv.writer(board)
            for row in layout:
                writer.writerow(row)
            print(layout)

    def show_legal_moves(self, oldPos, piece):
        # This method will take the inputted position and piece and update a csv file of its legal moves.
        # By default, the file will be filled with 'X's (illegal moves).
        # When a piece is clicked, it will update its legal moves to be shown with 'O's
        # The formula for calculating legal moves is as follows:
        # Legal Moves = (Normal Moves) - (Obstacle Moves) - !(Pinned Moves) + (Special Moves)
        pass
        
class Piece:
    def __init__(self):
        self.legalMoves = [None] * 8
        for i in range(8):    
            self.legalMoves[i] = ['X','X','X','X','X','X','X','X']
        print(self.legalMoves)
        with open('piece.csv', 'w') as writer:
            # This just creates the default legal moves by adding a whole bunch of rows to a csv file
            #self.legalMoves[0][1] = 'O'
            writerRow = csv.writer(writer)
            for row in self.legalMoves:
                writerRow.writerow(row)
    # This function will get the name of a piece on a given square,
    def get_piece(self, position):
        #print(str(position) + "hiiiiiiiiiiiiii")
        csv_position = tuple([position[0], position[1]])
        #print(csv_position)
        with open('chess.csv', 'r') as board:
            reader = csv.reader(board)
            for column, row in enumerate(reader):
                if column == csv_position[0]:
                    #print(row[csv_position[1]])
                    piece = row[csv_position[1]]
                    return piece

     # This functon checks legality for bishop, rook, and queen (pieces that have unlimited move distance)
    def getLegal(self, oldPos, piece):
         with open('piece.csv', 'w') as writer:
            # This just creates the default legal moves by adding a whole bunch of rows to a csv file
            writerRow = csv.writer(writer)
            self.legalMoves_general = [None] * 8
            for i in range(8):    
                self.legalMoves_general[i] = ['X','X','X','X','X','X','X','X']
            loop = False
            if piece == 'q' or piece == 'Q':
                #self.delta_range = [(1,1), (-1,1), (-1,-1), (1,-1), (1,0), (0,1), (-1,0), (0,-1)]
                loop = True
            while True:
                if piece == 'b' or piece == 'B' or piece == 'q' or piece == 'Q':
                    self.delta_range = [(1,1), (-1,1), (-1,-1), (1,-1)]
                    print("hi")
                if piece == 'r' or piece == 'R' or loop == True:
                    self.delta_range = [(1,0), (0,1), (-1,0), (0,-1)]
                    print("hi")
                # If the piece turns out to be any of these pieces, use this function instead.
                if piece == 'n' or piece == 'N' or piece == 'k' or piece == 'K':
                    self.getLegal_limited(oldPos, piece)
                    break
                
                for i in range(4):
                    self.range = [None]*8

                    for j in range(8):
                        
                        # Here, delta_range is sent from the child class
                        self.range[j] = tuple([(j+1)*x for x in self.delta_range[i]])
                        result = tuple(map(lambda x,y: x + y, oldPos, self.range[j]))
                        
                        if -1 < result[0] < 8 and -1 < result[1] < 8:
                            self.legalMoves_general[result[0]][result[1]] = 'O'

                print(self.legalMoves_general)
                if loop == False:
                    break
                else:
                    loop = False
                    
            for row in self.legalMoves_general:
                writerRow.writerow(row)
    
    # This function checks gets general legality for king and knight (pieces that have limited move distance except pawns)
    def getLegal_limited(self, oldPos, piece):
        # TODO: remove king from this function. Use 'getLegal_king' instead
        if piece == 'n' or piece == 'N':
            self.range = [(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]
        elif piece == 'k' or piece == 'K':
            self.range = [(1,1), (-1,1), (-1,-1), (1,-1), (1,0), (0,1), (-1,0), (0,-1)]

        for i in range(8):
            result = tuple(map(lambda x,y: x + y, oldPos, self.range[i]))
            print(result)
            if result and -1 < result[0] < 8 and -1 < result[1] < 8:
                self.legalMoves_general[result[0]][result[1]] = 'O'
    
    # This will check to see if the move made puts one's own king in check (another type of illegal move)
    def getLegal_pin(self, white, piece_oldPos, kingPos, specialMove):
        
        delta_range_diag = [(1,1), (-1,1), (-1,-1), (1,-1)]
        delta_range_rowcol = [(1,0), (0,1), (-1,0), (0,-1)]
        vector = None
        range_temp = [None]*8
        sus_rowcol = False
        sus_diag = False
        super_break = False
        legal = False
        # These two vectors will contain the coords for pins on either rows or columns.
        # diag list varies in size because diagonals vary in number of spaces (from 3 to 8)
        self.pinVector_diag = []
        self.pinVector_rowcol = [None] * 8


    # This will check to see if the piece that moved was actually pinned to the king
        for i in range(4):
            for j in range(8):
                range_temp[j] = tuple([(j+1)*x for x in delta_range_diag[i]])
                #print(self.range[j])
                diag_result = tuple(map(lambda x,y: x + y, kingPos, range_temp[j]))
                if piece_oldPos == diag_result:

                    sus_diag = True
                    print("piece move may have put king in check on diagonal")
                    # This will set the vector to the diagonal unit vector that the piece was moved on
                    vector = delta_range_diag[i]
                    # So here's the thing: the vector here is currently the opposite reciprical of what it should
                    # be, since I'm going off of chess board coordinates but csv files have a different coord system.
                    # because of this, I have to do a bit of jank to fix it.
                    # new_vector = tuple([-vector[1], -vector[0]])
                    new_vector = vector
                    print("diag vector: " + str(new_vector))

                    # This gets the entire 1st-3rd quadrant diag vector.
                    if vector == (-1,1) or vector == (1,-1):  
                        l = 1   
                        for k in range(8):
                            testPos = (-k + kingPos[0], k + kingPos[1]) 
                            if -1 < testPos[0] < 8 and -1 < testPos[1] < 8:
                                self.pinVector_diag.append(testPos)
                            else:
                                testPos = (l + kingPos[0], -l + kingPos[1])
                                if -1 < testPos[0] < 8 and -1 < testPos[1] < 8:
                                    self.pinVector_diag.append(testPos)
                                    l += 1
                                else:
                                    print("no more diagVector tuples!")
                                    break
                                
                    # Gets the entire 2nd-4th quadrant diag vector.
                    else:
                        l = 1
                        for k in range(8):
                            testPos = (k + kingPos[0], k + kingPos[1]) 
                            if -1 < testPos[0] < 8 and -1 < testPos[1] < 8:
                                self.pinVector_diag.append(testPos)
                            else:
                                testPos = (-l + kingPos[0], -l + kingPos[1])
                                if -1 < testPos[0] < 8 and -1 < testPos[1] < 8:
                                    self.pinVector_diag.append(testPos)
                                    l += 1
                                else:
                                    print("no more diagVector tuples!")
                                    break
                    # Now the possible moves of the piece is limited by this vector!     
                    
                    super_break = True
                    print("diag pinvector: " + str(self.pinVector_diag))
                    break
                else:
                    test_piece = self.get_piece(diag_result)
                    if test_piece != 'o':
                        print("moved piece was not pinned on diag vector :)")
                        break
            if super_break == True:
                break

        range_temp = [None]*8
        if super_break == False:
            for i in range(4):
                for j in range(8):
                    range_temp[j] = tuple([(j+1)*x for x in delta_range_rowcol[i]])
                    print(range_temp[j])
                    rowcol_result = tuple(map(lambda x,y: x + y, kingPos, range_temp[j]))
                    print(rowcol_result)
                    # This compares piece positions. If a piece is in the same unit vector direction from the king, and has only 'o' in-between, it could be pinned
                    if piece_oldPos == rowcol_result:
                        vector = delta_range_rowcol[i]
                        print("vector:" + str(vector))
                        sus_rowcol = True
                        print("piece move may have put king in check on vertical or horizontal")
                        # This gets the entire column if the pieces are aligned vertically.
                        if vector == (-1,0) or vector == (1,0):     
                            for k in range(8):
                                self.pinVector_rowcol[k] = (k, kingPos[1],)
                        # Otherwise, pieces are aligned horizontally.
                        else:
                            for k in range(8):
                                self.pinVector_rowcol[k] = (kingPos[0], k)
                        # Now the possible moves of the piece is limited by this vector!   
                        # TODO: Create this same thing, but for the diag!     
                        print(self.pinVector_rowcol)
                        break
                        
                    #T his only continues checking if there is a 'o' on the square.
                    else:
                        test_piece = self.get_piece(rowcol_result)
                        if test_piece != 'o':
                            print("moved piece not pinned on rowcol vector :)")
                            break
                    # If the piece is an enemy piece, it is either not pinned or it is an illegal move. Therefore it can't be pinned!
                        
            # now if sus is True, we need to see if there was an enemy piece along the diagnal or rowcol that can put the king in check. 
        if sus_diag == True or sus_rowcol == True:
            # If the piece could be pinned on the rowcol
            if sus_rowcol == True:
                if white == True:
                    condition1 = 'r'
                    condition2 = 'q'
                else:
                    condition1 = 'R'
                    condition2 = 'Q'
                print(condition2)
                print(condition1)
                test_rowcol_temp = [None]*8
                test_rowcol = [None]*8
                for j in range(8):
                    test_rowcol_temp[j] = tuple([(j+1)*x for x in vector])
                    print(test_rowcol_temp)
                    test_rowcol[j] = tuple(map(lambda x,y: x + y, piece_oldPos, test_rowcol_temp[j]))
                    #print(test_rowcol[j])
                    if (-1 < test_rowcol[j][0] < 8 and -1 < test_rowcol[j][1] < 8):
                        piece = self.get_piece(test_rowcol[j])
                        print(piece)
                        # If one of the problematic pieces exist in the direction of the vector, the move is illegal!
                        if  piece == condition1 or piece ==  condition2:
                            legal = False
                            print("you sussy baka. there is something pinning that piece to your king along the rowcol!")
                            break
                        elif piece == 'o':
                            continue
                        else:
                            print("closest piece is not problematic. Legal is True!")
                            break
                    else:
                        print("projected coord outside board range! returing legal")
                        break    
            # If the pinned piece is on the diagonal.
            elif sus_diag == True:

                if white == True: 
                    condition1 = 'b'
                    condition2 = 'q'
                else:
                    condition1 = 'B'
                    condition2 = 'Q'
                print(condition2)
                print(condition1)
                test_diag_temp = [None]*8
                test_diag = [None]*8
                for j in range(8):
                    test_diag_temp[j] = tuple([(j+1)*x for x in new_vector])
                    print(test_diag_temp)
                    test_diag[j] = tuple(map(lambda x,y: x + y, piece_oldPos, test_diag_temp[j]))
                    print(test_diag[j])
                    # This check is makes sure that the coordinate actually exists on the chess board. If not,
                    # the loop will break
                    if (-1 < test_diag[j][0] < 8 and -1 < test_diag[j][1] < 8):
                        piece = self.get_piece(test_diag[j])
                        print(piece)
                        if  piece == condition1 or piece ==  condition2:
                            legal = False
                            print("you sussy baka. there is something pinning that piece to your king along the diagonal!")
                            break
                        elif piece == 'o':
                            continue
                        else:
                            print("closest piece is not problematic. Legal is True!")
                            break
                    else:
                        print("projected coord outside board range! returing legal")
                        break             
        return legal
    
    # This function will tell me if there are any pieces blocking the path of rook, bishop, or queen.
    def getLegal_obstacle(self):
        pass
    
    # When the king moves, check for knight, pawn, enemy king, queen, bishop, and rook covering intended move square.
    def getLegal_king(self, oldPos):
        pass
    # This function will return 3 possible values: your king is not in check, your king is in check,
    # or the king is in double check.
    def getLegal_inCheck(self, kingPos, white):
        inCheck = 0
        self.TotalDeltaRange = [(1,1),(-1,1),(-1,-1),(1,-1),(1,0),(0,1),(-1,0),(0,-1)]
        self.enemyKnightRange = [(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]
        if white == True:
            self.enemyPawnRange = [(-1,-1),(-1,1)]
        else:
            self.enemyPawnRange = [(1,-1),(1,1)]
        # for bishops, rooks, and queens.   
        for i in range(8):
            for j in range(8):
                # This is exact same code in 'getLegal_pin'. Maybe I can optimize?
                range_temp = tuple([(j+1)*x for x in self.TotalDeltaRange[i]])
                result = tuple(map(lambda x,y: x + y, kingPos, range_temp))

                piece = self.get_piece(result)
                # matches checks for white pieces
                if white == True:
                    if piece == 'q' or (piece == 'b' and -1<i<4) or (piece == 'r' and 3<i<8):
                        inCheck += 1
                        break
                    elif piece == 'o':
                        continue
                    else:
                        #print("no check along this vector")
                        break
                # matches checks for black pieces
                else:
                    if piece == 'Q' or (piece == 'B' and -1<i<4) or (piece == 'R' and 3<i<8):
                        inCheck += 1
                        break
                    elif piece == 'o':
                        continue
                    else:
                        #print("no check along this vector")
                        break
        # for knights
        for k in range(8):
            result = tuple(map(lambda x,y: x + y, kingPos, self.enemyKnightRange[k]))
            #print(result)
            piece = self.get_piece(result)
            if (white == True and piece == 'n') or (white == False and piece == 'N'):
                inCheck += 1
        # for pawns
        for l in range(2):
            result = tuple(map(lambda x,y: x + y, kingPos, self.enemyPawnRange[l]))
            piece = self.get_piece(result)
            if (white == True and piece == 'p') or (white == False and piece == 'P'):
                inCheck += 1
        return inCheck

#TODO: get rid of this subclass!
class Pawn(Piece):
    def __init__(self):
        self.whiteRange = [(-1,0)]
        self.blackRange = [(1,0)]
        self.firstMove = [None] * 8 
        
        self.blackPieces = ['p','n','b','r','q']
        self.whitePieces = ['P','N','B','R','Q']

    def move_check(self, oldPos, newPos, white, firstMove, specialMove): 
        # This needs to be fixed so that pawns moving forward do not capture pieces. (AKA they need to move onto 
        # empty squares)
        if white == True:
            if firstMove == True:
                self.whiteRange += [(-2,0)]

            print(tuple([oldPos[0]-1, oldPos[1]-1]))
            temp = tuple([oldPos[0]-1, oldPos[1]-1])
            capture1 = self.get_piece(temp)
            for i in self.blackPieces:
                # print(i)
                # print(capture1)
                if capture1 == i:      
                    self.whiteRange += [(-1,-1)]
            print(tuple([oldPos[0]-1, oldPos[1]+1]))
            capture2 = self.get_piece(tuple([oldPos[0]-1, oldPos[1]+1]))
            # print(capture2)
            for i in self.blackPieces:
                if capture2 == i:
                    self.whiteRange += [(1,-1)]
            print(self.whiteRange)
        if white == False:
            self.range = self.blackRange
            if firstMove == True:
                self.blackRange += [(2,0)]
            capture1 = self.get_piece(tuple([oldPos[0]-1, oldPos[1]+1]))
            for i in self.whitePieces:
                if capture1 == i:
                    self.blackRange += [(-1,-1)]
            capture2 = self.get_piece(tuple([oldPos[0]+1, oldPos[1]+1]))
            for i in self.whitePieces:
                if capture2 == i:
                    self.blackRange += [(1,-1)]
        print(self.blackRange)

# Testing

board = Board()

oldPosTest = (1,1)
newPosTest = (1,1)

pawnOldPos = (6,3)
pawnNewPos = (5,0)

specialMove = False
piece = Piece()
#knight = Knight()
#bishop = Bishop()
#rook = Rook()
#king = King()
#pawn = Pawn()
#test_bishop = piece.getLegal(oldPosTest, 'Q')
test_knight = piece.getLegal(oldPosTest, 'n')
#test_rook = piece.getLegal(oldPosTest, 'R')

#print(test_knight)
#print(test_bishop)
#print(test_rook)

white = True

knight = "knight"

kingPos = (7,4)
king2Pos = (6,5)
king3Pos = (4,4)
knight_oldPos = (5,6)
knight2_oldPos = (5,4)

queen_oldPos = (7,3)
bishop_oldPos = (7,5)

pin_test1 = piece.getLegal_pin(white, knight_oldPos, king2Pos, specialMove)
print(pin_test1)
pin_test2 = piece.getLegal_pin(white, knight2_oldPos, kingPos, specialMove)
print(pin_test2)
pin_test3 = piece.getLegal_pin(white, queen_oldPos, kingPos, specialMove)
print(pin_test3)
inCheck_test1 = piece.getLegal_inCheck(king3Pos, white) 
print("Number of Checks on king: " + str(inCheck_test1))
#king.get_piece((5,1))
#name = input('what is your name?')
#print(name)
pawn = Pawn()
pawn = pawn.move_check(pawnOldPos, pawnNewPos, white=True, firstMove=True, specialMove=False)

#board.update(oldPosTest, newPosTest, specialMove=0)

