import csv

# TODO: Create promotion in getLegal_special

# note to self: board will be indexed 0-7.
# board is index by (column, row). This means that (0,0) refers to the piece in the upper-left hand corner.

# Instead of checking if a move is legal after the fact, I'm going to make it so that all legal moves are calculated and shown when you click a piece.
    # the king will be an exception to this. It will still only show its legal moves when it has been clicked, but it will also calculate its legal moves in the background.
        #This will occur at the start of each player's turn.
    # This will involve changing the following functions:
        #'move_check' will become 'getLegal_general', and it will return the pieces possible moves if there were no other pieces on the board, based on its current position.
        #'kingCheck_check' will become 'getLegal_pin'. It will only look at pieces that could be pinned to the king.
        #'move_check_limited' will become 'getLegal_limited', and it will remain relatively the same.
    # Another method also needs to be implemented that checks for obstacles (pieces that are your own color, or any squares past an opponent's piece).
    # Pieces cannot move to or past obstacles (note that knights do not have obstacles).
        #This method could be called 'getLegal_obstacle' 

# There are 4 types of illegal moves. They are:

# 1. Moving a piece in a direction it cannot normally go (i.e. moving a king as if it were a queen).
# 2. Moving through pieces as with the pawn, bishop, rook, or queen.
# 3. Moving your own king into check.
# 4. Moving your own piece that would put your own king into check

# I'm currently at a dilemna when it comes to recording general piece legality: Do I append every position one-by-one to a csv file, or do I create a list and append to that?
# Also, to make things easier, should I get rid of the child classes and just have one piece class with if statements?
# I think I will do this since I want all pieces to share one legalMoves variable. Also, I don't think there's much merit in having child classes since
# Also, I don't think there's much merit in having child classes since each child class (except for pawns) only has like one thing in it.


class Board:
    def __init__(self) -> None:
        with open('chess.csv', 'w') as board:
            #This just creates the starting position by adding a whole bunch of rows to csv file
            self.whiteKing_pos = (7,4)
            self.blackKing_pos = (0,4)
            
            # variables indicating if kings or rooks moved from start.
            self.whiteKing1stMove = True
            self.blackKing1stMove = True    
            self.whiteRookLeft1stMove = True
            self.whiteRookRight1stMove = True 
            self.blackRookLeft1stMove = True
            self.blackRookRight1stMove = True

            writer = csv.writer(board)
            writer.writerow(['r','o','o','o','k','o','o','r'])
            writer.writerow(['p','P','p','p','p','p','p','p'])
            writer.writerow(['b','o','o','o','o','o','o','o'])
            writer.writerow(['b','P','o','o','o','o','o','o'])
            writer.writerow(['o','p','o','o','o','o','o','o'])
            writer.writerow(['o','o','o','o','o','o','o','o'])
            writer.writerow(['P','P','P','P','P','o','p','P'])
            writer.writerow(['R','o','o','o','K','o','o','o'])

            '''writer.writerow(['r','o','o','o','q','r','o','o'])
            writer.writerow(['o','o','o','o','p','o','k','o'])
            writer.writerow(['n','o','p','o','n','o','P','o'])
            writer.writerow(['p','p','o','p','P','o','Q','o'])
            writer.writerow(['o','o','o','P','o','o','o','P'])
            writer.writerow(['P','o','o','P','o','P','o','o'])
            writer.writerow(['o','P','o','o','N','o','o','o'])
            writer.writerow(['R','o','o','o','K','o','o','R'])'''

            '''writer.writerow(['o','o','o','o','r','k','o','k'])
            writer.writerow(['q','P','q','o','o','p','b','p'])
            writer.writerow(['o','P','P','P','o','o','P','o'])
            writer.writerow(['p','o','n','p','o','o','o','o'])
            writer.writerow(['P','o','P','o','P','P','q','o'])
            writer.writerow(['o','r','o','o','o','o','R','o'])
            writer.writerow(['q','o','o','o','R','o','K','r'])
            writer.writerow(['B','R','o','Q','o','o','o','o'])'''
            
    # This method will update piece positions in csv file
    # 'specialMovePiece' is only for promotions. (By default it will be passed in as '0')
    def update(self, oldPos, newPos, newPiece, white):
        # This is the default case that works for any normal move or capture.
        specialMove = piece.legalMoves_special[newPos[0]][newPos[1]]
        specialMove = int(specialMove)
        # For normal moves
        if specialMove == 0:
            print("hi")
            self.move(oldPos, newPos, newPiece)
            if newPiece == 'K': self.whiteKing1stMove = False
            elif newPiece == 'k': self.blackKing1stMove = False
            # It's worth mentioning that the rook piece and position must both be accounted for, since 
            # there are cases where you could have a non-rook piece on the rook starting square, which would 
            # accidentally enable castling!
            elif newPiece == 'R' and newPos == (7,0): self.whiteRookLeft1stMove = False
            elif newPiece == 'R' and newPos == (7,7): self.whiteRookLeft1stMove = False
            elif newPiece == 'r' and newPos == (0,0): self.blackRookLeft1stMove = False
            elif newPiece == 'r' and newPos == (0,7): self.blackRookLeft1stMove = False

        # This will be for Kingside Castling
        elif specialMove == 1:
            self.move(oldPos, newPos, newPiece)
            if white == True:
                # NOTE: This is hardcoded for now. If I wanted to do FischerRandom, I would have to change this.
                self.move((7,7), (7,5), 'R')
            else:
                self.move((0,7), (0,5), 'r')
  
        # Queenside Castling
        elif specialMove == 2:
            self.move(oldPos, newPos, newPiece)
            if white == True:
                self.move((7,0), (7,3), 'R')
            else:
                self.move((0,0), (0,3), 'r')
        # En Passant
        elif specialMove == 3:
            self.move(oldPos, newPos, newPiece)
            # This is a very hacky way of doing the piece capture.
            if white == True:
                self.move((newPos[0]+1,newPos[1]), newPos, 'P')
            else:
                self.move((newPos[0]-1,newPos[1]), newPos, 'p')
        # Promotions
        elif specialMove == 4:
            print("Now promoting to: " + str(newPiece))
            self.move(oldPos, newPos, newPiece)
        else:
            print("Bruh what kinda goofy-ahh move did you just make??")

    # When called, this method actually moves the piece to the new position
    # and replaces the old position with 'o'.
    def move(self, oldPos, newPos, piece):
        with open('chess.csv', 'r') as board:
            reader = csv.reader(board, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            layout = list(reader)
            #print(piece)
        with open('chess.csv', 'w') as board:
            layout[oldPos[0]][oldPos[1]] = 'o'
            #print("this is oldpos:" + str(oldPos))
            layout[newPos[0]][newPos[1]] = piece

            writer = csv.writer(board)
            for row in layout:
                writer.writerow(row)
    # The user will enter standard chess coordinates (i.e. a4, b4, h7) which will be
    # converted to list indexes.
    def letterNum_to_coords(self, letterNum):
        letters = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
        index = 0
        for character in letterNum:
            if index == 0:
                x = letters[character]
            elif index == 1:
                y = 8 - int(character)
            index+=1 
        result = (y,x)
        print(result)
        return result
        
class Piece:
    def __init__(self):

        self.blackPieces = ['p','n','b','r','q','k']
        self.whitePieces = ['P','N','B','R','Q','K']
        
        self.legalMoves = [None] * 8
        self.legalMoves_special = [None] * 8
        for i in range(8):    
            self.legalMoves[i] = ['X','X','X','X','X','X','X','X']
            self.legalMoves_special[i] = [0,0,0,0,0,0,0,0]
        with open('piece.csv', 'w') as writer:
            # This just creates the default legal moves by adding a whole bunch of rows to a csv file
            #self.legalMoves[0][1] = 'O'
            writerRow = csv.writer(writer)
            for row in self.legalMoves:
                writerRow.writerow(row)
    # This function will get the name of a piece on a given square,
    def get_piece(self, position):
        csv_position = tuple([position[0], position[1]])
        with open('chess.csv', 'r') as board:
            reader = csv.reader(board)
            for column, row in enumerate(reader):
                if column == csv_position[0]:
                    piece = row[csv_position[1]]
                    return piece

     # This functon checks legality for bishop, rook, and queen (pieces that have unlimited move distance)
    def getLegal(self, pos, kingPos, piece, white):
        
        with open('piece.csv', 'w') as writer:
            # This just creates the default legal moves by adding a whole bunch of rows to a csv file
            writerRow = csv.writer(writer)
            self.legalMoves_general = [None] * 8
            for i in range(8):    
                self.legalMoves_general[i] = ['X','X','X','X','X','X','X','X']
            loop = False
            if piece == 'q' or piece == 'Q':
                loop = True
            # Done init. Now selecting delta range.
            while True:
                # kings, knights, and pawns are sent to other functions since they have different moves.
                if piece == 'b' or piece == 'B' or piece == 'q' or piece == 'Q':
                    self.delta_range = [(1,1),(-1,1),(-1,-1),(1,-1)]
                if piece == 'r' or piece == 'R' or loop == True:
                    self.delta_range = [(1,0),(0,1),(-1,0),(0,-1)]
                # If the piece turns out to be any of these pieces, use this function instead.
                if piece == 'n' or piece == 'N' or piece == 'k' or piece == 'K':
                    self.getLegal_limited(pos, kingPos, piece, white)
                    break
                if piece == 'p' or piece == 'P':
                    self.getLegal_pawn(pos,white)
                    break
                # Use select delta range in each direction.
                for i in range(4):
                    self.range = [None]*8
                    #print("starting new direction")
                    superbreak = False
                    for j in range(8):
                        
                        self.range[j] = tuple([(j+1)*x for x in self.delta_range[i]])
                        result = tuple(map(lambda x,y: x + y, pos, self.range[j]))
                        #print(result)
                        
                        if -1 < result[0] < 8 and -1 < result[1] < 8:
                            newPiece = self.get_piece(result)
                            #print(newPiece)
                            if newPiece == 'o':
                                self.legalMoves_general[result[0]][result[1]] = 'O'
                                # Test

                            elif white == True:
                                for k in range(6):
                                    if newPiece == self.whitePieces[k]:
                                        #print("cannot capture same color piece, break.")  
                                        superbreak = True 
                                        break
                                    elif newPiece == self.blackPieces[k]:
                                        #print("can capture piece, but will go no farther.")
                                        self.legalMoves_general[result[0]][result[1]] = 'O'
                                        # Test
                                        superbreak = True 
                                        break
                                    else:
                                        pass
                                        #print("no piece matches white")
                                    
                            elif white == False:
                                for l in range(6):
                                    if newPiece == self.blackPieces[l]:
                                        #print("cannot capture same color piece, break.") 
                                        superbreak = True   
                                        break
                                    elif newPiece == self.whitePieces[l]:
                                        #print("can capture piece, but will go no farther.")
                                        self.legalMoves_general[result[0]][result[1]] = 'O'
                                        # Test
                                        superbreak = True 
                                        break
                                    else:
                                        pass
                                        #print("no piece matches black")
                            if superbreak == True:
                                break       
                        else:
                            #print("out of range! break")
                            break

                #print(self.legalMoves_general)
                if loop == False:
                    break
                else:
                    loop = False
            # Write to piece.csv
            #print("hi")        
            for row in self.legalMoves_general:
                writerRow.writerow(row)
    
    # This function checks gets general legality for king and knight (pieces that have limited move distance except pawns)
    def getLegal_limited(self, pos, kingPos, piece, white):
        self.enemyControlledSquare = 0
        
        if piece == 'n' or piece == 'N':
            self.range = [(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]
        elif piece == 'k' or piece == 'K':
            self.range = [(1,1),(-1,1),(-1,-1),(1,-1),(1,0),(0,1),(-1,0),(0,-1)]

        for i in range(8):
            result = tuple(map(lambda x,y: x + y, pos, self.range[i]))
            #print(result)
            if -1 < result[0] < 8 and -1 < result[1] < 8:
                # I could actually edit this to cond between knight and king.
                if piece == 'k' or piece == 'K':
                    self.enemyControlledSquare = self.getLegal_pieceControl(result, kingPos, white, True, True)

                # Makes sure the pos isnt controlled by enemy if piece == king
                if self.enemyControlledSquare == 0:
                    
                    for k in range(6):
                        newPiece = self.get_piece(result)
                        if newPiece == self.whitePieces[k] and white == False:
                            #print("cannot capture same color piece, break.")  
                            self.legalMoves_general[result[0]][result[1]] = 'O'
                            break
                        elif newPiece == self.blackPieces[k] and white == True:
                            #print("can capture piece, but will go no farther.")
                            self.legalMoves_general[result[0]][result[1]] = 'O'
                            # Test
                            break
                        elif newPiece == 'o':
                            self.legalMoves_general[result[0]][result[1]] = 'O'
                            break
                    #print(self.legalMoves_general)

    # This method will add in the legal moves that come from castling, en-passant, and promotion.
    # These moves will be added to self.legalMoves_general, but the type of special move
    # will also go into its own double list called legalMoves_special.
    def getLegal_special(self, pos, kingPos, myPiece, lastEnemyPawnMove, numChecks):
        # We don't technically need to pass 'white' since we can go by the
        # specific piece alone.

        for i in range(8):
            self.legalMoves_special[i] = ['0','0','0','0','0','0','0','0']

        # I don't need to check if out of board range here since the moves
        # would be impossible to make.
        posRight = (pos[0], pos[1]+1)
        posLeft = (pos[0], pos[1]-1)
        if myPiece == 'P':
            print(lastEnemyPawnMove)
            print(pos)
            # White promotion
            if pos[0] == 0:
                pass
            # White en-passant
            elif lastEnemyPawnMove[0] == pos[0] and (lastEnemyPawnMove[1] == posRight[1]\
            or lastEnemyPawnMove[1] == posLeft[1]):
                newPos = (lastEnemyPawnMove[0]-1, lastEnemyPawnMove[1])
                self.legalMoves_general[newPos[0]][newPos[1]] = 'O'
                self.legalMoves_special[newPos[0]][newPos[1]] = 3
                print(self.legalMoves_general)
        elif myPiece == 'p':
            # Black promotion
            if pos[0] == 7:
                pass
            # Black en-passant
            elif lastEnemyPawnMove[0] == pos[0] and (lastEnemyPawnMove[1] == posRight[1]\
            or lastEnemyPawnMove[1] == posLeft[1]):
                newPos = (lastEnemyPawnMove[0]+1, lastEnemyPawnMove[1])
                self.legalMoves_general[newPos[0]][newPos[1]] = 'O'
                self.legalMoves_special[newPos[0]][newPos[1]] = 3
        
        elif myPiece == 'K' and numChecks == 0:
            if board.whiteKing1stMove == True:
                # kingside castling
                if board.whiteRookRight1stMove == True:
                    # We can call this method along the path the king must move when castling.
                    # I'm to lazy to make it a vector to account for all possible cases, so this is hard-coded for now.
                    inCheck1 = piece.getLegal_pieceControl((7,5), kingPos, True, True, True)
                    inCheck2 = piece.getLegal_pieceControl((7,6), kingPos, True, True, True)
                    piece1 = piece.get_piece((7,5))
                    piece2 = piece.get_piece((7,6))
                    if (inCheck1 == inCheck2 == 0) and (piece1 == piece2 == 'o'):
                        newPos = (7,6)
                        self.legalMoves_general[newPos[0]][newPos[1]] = 'O'
                        self.legalMoves_special[newPos[0]][newPos[1]] = 1
                # queenside castling
                if board.whiteRookLeft1stMove == True:
                    inCheck1 = piece.getLegal_pieceControl((7,3), kingPos, True, True, True)
                    inCheck2 = piece.getLegal_pieceControl((7,2), kingPos, True, True, True)
                    piece1 = piece.get_piece((7,3))
                    piece2 = piece.get_piece((7,2))
                    piece3 = piece.get_piece((7,1))
                    if (inCheck1 == inCheck2 == 0) and (piece1 == piece2 == piece3 == 'o'):
                        newPos = (7,2)
                        self.legalMoves_general[newPos[0]][newPos[1]] = 'O'
                        self.legalMoves_special[newPos[0]][newPos[1]] = 2

        elif myPiece == 'k' and numChecks == 0:
            if board.blackKing1stMove == True:
                # kingside castling
                if board.blackRookRight1stMove == True:
                    inCheck1 = piece.getLegal_pieceControl((0,5), kingPos, False, True, True)
                    inCheck2 = piece.getLegal_pieceControl((0,6), kingPos, False, True, True)
                    piece1 = piece.get_piece((0,5))
                    piece2 = piece.get_piece((0,6))    

                    if (inCheck1 == inCheck2 == 0) and (piece1 == piece2 == 'o'):
                        newPos = (0,6)
                        self.legalMoves_general[newPos[0]][newPos[1]] = 'O'
                        self.legalMoves_special[newPos[0]][newPos[1]] = 1
                # queenside castling
                if board.blackRookLeft1stMove == True:
                    inCheck1 = piece.getLegal_pieceControl((0,3), kingPos, False, True, True)
                    inCheck2 = piece.getLegal_pieceControl((0,2), kingPos, False, True, True)
                    piece1 = piece.get_piece((0,3))
                    piece2 = piece.get_piece((0,2))
                    piece3 = piece.get_piece((0,1))

                    if (inCheck1 == inCheck2 == 0) and (piece1 == piece2 == piece3 == 'o'):
                        newPos = (0,2)
                        self.legalMoves_general[newPos[0]][newPos[1]] = 'O'
                        self.legalMoves_special[newPos[0]][newPos[1]] = 2
        else:
            print("No special moves for chosen piece!")
                
    # This will check to see if the move made puts one's own king in check (another type of illegal move)
    def getLegal_pin(self, white, piece_oldPos, kingPos):
        
        delta_range_diag = [(1,1),(-1,1),(-1,-1),(1,-1)]
        delta_range_rowcol = [(1,0),(0,1),(-1,0),(0,-1)]
        vector = None
        range_temp = [None]*8
        sus_rowcol = False
        sus_diag = False
        super_break = False
        legalVector = []
        legal = True
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
                #print(diag_result)
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
                    #print("diag vector: " + str(new_vector))

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
                                    #print("no more diagVector tuples!")
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
                                    #print("no more diagVector tuples!")
                                    break
                    # Now the possible moves of the piece is limited by this vector!     
                    
                    super_break = True
                    #print("diag pinvector: " + str(self.pinVector_diag))
                    break
                elif -1<diag_result[0]<8 and -1<diag_result[1]<8:
                    test_piece = self.get_piece(diag_result)
                    if test_piece != 'o':
                        #print("moved piece was not pinned on diag vector :)")
                        break
                else:
                    break
            if super_break == True:
                break

        range_temp = [None]*8
        if super_break == False:
            for i in range(4):
                for j in range(8):
                    range_temp[j] = tuple([(j+1)*x for x in delta_range_rowcol[i]])
                    #print(range_temp[j])
                    rowcol_result = tuple(map(lambda x,y: x + y, kingPos, range_temp[j]))
                    #print(rowcol_result)
                    # This compares piece positions. If a piece is in the same unit vector direction from the king, and has only 'o' in-between, it could be pinned
                    if piece_oldPos == rowcol_result:
                        vector = delta_range_rowcol[i]
                        #print("vector:" + str(vector))
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
                        #print(self.pinVector_rowcol)
                        break
                        
                    #This only continues checking if there is a 'o' on the square.
                    elif -1<rowcol_result[0]<8 and -1<rowcol_result[1]<8:
                        test_piece = self.get_piece(rowcol_result)
                        if test_piece != 'o':
                            #print("moved piece not pinned on rowcol vector :)")
                            break
                    else:
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
                #print(condition2)
                #print(condition1)
                test_rowcol_temp = [None]*8
                test_rowcol = [None]*8
                for j in range(8):
                    test_rowcol_temp[j] = tuple([(j+1)*x for x in vector])
                    #print(test_rowcol_temp)
                    test_rowcol[j] = tuple(map(lambda x,y: x + y, piece_oldPos, test_rowcol_temp[j]))
                    #print(test_rowcol[j])
                    if (-1 < test_rowcol[j][0] < 8 and -1 < test_rowcol[j][1] < 8):
                        piece = self.get_piece(test_rowcol[j])
                        #print(piece)
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
                #print(condition2)
                #print(condition1)
                test_diag_temp = [None]*8
                test_diag = [None]*8
                for j in range(8):
                    test_diag_temp[j] = tuple([(j+1)*x for x in new_vector])
                    #print(test_diag_temp)
                    test_diag[j] = tuple(map(lambda x,y: x + y, piece_oldPos, test_diag_temp[j]))
                    #print(test_diag[j])
                    # This check is makes sure that the coordinate actually exists on the chess board. If not,
                    # the loop will break
                    if (-1 < test_diag[j][0] < 8 and -1 < test_diag[j][1] < 8):
                        piece = self.get_piece(test_diag[j])
                        #print(piece)
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
        if sus_diag == True and legal == False:
            legalVector = self.pinVector_diag
        elif sus_rowcol == True and legal == False:
            legalVector = self.pinVector_rowcol  
        #If legal is true, the legal vector is determined as a blank vector.          
        return legalVector
 
    # For whichever number of checks the king is in, determine the amount of legal moves. If there are no checks, this isn't taken into account.
    # This method will also detect if checkmate or stalemate has been achieved.
    def getLegal_mate(self, kingPos, numChecks, white, pieceVectorTemp):
        # For clarification, the checkPiece will be the piece that moves and delivers the check, or rather the first check given.
        print("starting getLegal_mate...")
        self.kingOnly = False
        pawnCapture = False # See 'getLegal_pieceControl'
        enemyPawn = False # The pawns we will be checking occupancy for are own color.
        # the class variable changes when getLegal_pieceControl is called again, so I'm saving it here.
        self.checkVectorPermanent = piece.checkVector 

        # I need to differentiate between which king is being tested here.
        if white == True:
            king = 'K'
            print("it is white's turn.")
        else:
            king = 'k'
            print("it is black's turn.")

        if numChecks == 1:
            
            if white == True:
                #Note: checkPos is the position of checking piece.
                numMoves = 0
                for a in pieceVectorTemp:
                    #check to see if last item in list, since it contains checking piece coords.
                    print(a)
                    if a == pieceVectorTemp[-1]:
                        pawnCapture = True
                    numMoves += self.getLegal_pieceControl(a, kingPos, (not white), enemyPawn, pawnCapture)
                    print("number of legal moves: " + str(numMoves))
            else:
                numMoves = 0
                for b in pieceVectorTemp:
                    print(b)
                    if b == pieceVectorTemp[-1]:
                        pawnCapture = True
                    numMoves += self.getLegal_pieceControl(b, kingPos, (not white), enemyPawn, pawnCapture)
                    print("number of legal moves: " + str(numMoves))

            if numMoves == 0:
                self.kingOnly = True
        elif numChecks >= 2:
            # Need to make it so that only king moves are legal here.
            print("multiple checks!")
            self.kingOnly = True
            
        else:
            # This will be for numChecks == 0, or some non-numeric value.
            print("no checks here!")

        # If only king moves are possible, but the king can't make any moves,
        # then it is checkmate!

        # If the king cant make any moves but it is not in check, then we need
        # to test for stalemate.
        self.getLegal(kingPos, kingPos, king, white)
        legalKingMoves = 0
        
        for i in range(8):
            # Ok, so this is a really bad fix but this set of tuples never changes.
            result =  tuple(map(lambda x,y: x + y, kingPos, self.totalDeltaRange[i]))
            if -1<result[0]<8 and -1<result[1]<8:
                if self.legalMoves_general[result[0]][result[1]] == 'O':
                    legalKingMoves += 1
        print("KingMoves = " + str(legalKingMoves))
        
        #TODO: There will then be a section of code that determines if the king is mated or stalemated or not.

        if legalKingMoves == 0:
            if self.kingOnly == True:
                print("king has been checkmated!")
            elif numChecks == 0:
                print("king may be stalemated. Need to investigate further.")
            else:
                print("King is in check, but not checkmated or stalemated :)")
                print(self.checkVectorPermanent)


    def getLegal_pieceControl(self, pos, kingPos, white, enemyPawn, pawnCapture):
        # This function determines how many pieces control a certain square.
        # It also determines how many checks your king is currently in.
        # This represents the number of pieces that control a certain square.

        # Note about the boolean 'pawnCapture': if true, the pawn can only capture pieces
        # on the sqare. If false, the pawn can only move to that square. This is because a pawn
        # cannot capture to an empty square, and must cannot just simply move normally to
        # an occupied square.
        self.checkVector = []
        inCheck = 0
        self.totalDeltaRange = [(1,1),(-1,1),(-1,-1),(1,-1),(1,0),(0,1),(-1,0),(0,-1)]
        self.enemyKnightRange = [(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]
        if white == True and enemyPawn == True:
            self.enemyPawnRange = [(-1,-1),(-1,1)]
        elif white == False and enemyPawn == True:
            self.enemyPawnRange = [(1,-1),(1,1)]
        # For below,This is if checking for own pawns.
        # NOTE: in ths section when 'white == True' we are actually talking in respect to black here.
        # This is because in order to check same side piece occupancy, I'm treating white as black.
        # This is a very bad hack but I wanted to minimize my code.
        elif white == True and pawnCapture == True and enemyPawn == False:
            self.enemyPawnRange = [(-1,-1),(-1,1)]
        elif white == True and pawnCapture == False and enemyPawn == False:
            self.enemyPawnRange = [(-1,0),(-2,0)]
        elif white == False and pawnCapture == True and enemyPawn == False:
            self.enemyPawnRange = [(1,-1),(1,1)]
        else:
            self.enemyPawnRange = [(1,0),(2,0)]
        # NOTE: keep in mind that the pawncapture==false second pawnrange element only
        # exists if it is the first pawn move. If the pawn is not in its starting position,
        # then the loop iteration is skipped.

        # for bishops, rooks, and queens.   
        for i in range(8):
            checkVector = []
            for j in range(8):
                # This is exact same code in 'getLegal_pin'. Maybe I can optimize?
                range_temp = tuple([(j+1)*x for x in self.totalDeltaRange[i]])
                result = tuple(map(lambda x,y: x + y, pos, range_temp))
                
                #print(result)
                if -1<result[0]<8 and -1<result[1]<8:
                    piece = self.get_piece(result)
                    # Yes I know I can optimize this but I personally like it for code readability.
                    checkVector.append(result)
                else:
                    checkVector = []
                    break
                # matches checks for white pieces
                if white == True:
                    if piece == 'q' or (piece == 'b' and -1<i<4) or (piece == 'r' and 3<i<8):
                        pinnedState = self.getLegal_pin((not white), result, kingPos)    
                        if pinnedState == [] or enemyPawn == True:
                            if inCheck == 0:
                                # This will lock the vector for the first check that is detected.
                                self.checkVector = checkVector
                            inCheck += 1
                            print("adding B/R/Q move for white")
                            break
                        elif pinnedState != []:
                            print("abandoning vector!")
                            break
                    # This will make it so that checks can pass through your own king.
                    # This prevents a bug where the king hasn't fully moved yet, so moving along
                    # the check vector away from the check will count as a legal move.
                    elif piece == 'o' or piece == 'K':
                        continue
                    else:
                        #print("no check along this vector")
                        break
                # matches checks for black pieces
                else:
                    if piece == 'Q' or (piece == 'B' and -1<i<4) or (piece == 'R' and 3<i<8):
                        pinnedState = self.getLegal_pin((not white), result, kingPos)    
                        if pinnedState == [] or enemyPawn == True:
                            if inCheck == 0:
                                self.checkVector = checkVector
                            inCheck += 1
                            print("adding B/R/Q move for black")
                            break
                        elif pinnedState != []:
                            print("abandoning vector!")
                            break
                    elif piece == 'o' or piece == 'k':
                        continue
                    else:
                        #print("no check along this vector")
                        break
        #print(self.checkVector)
        # for knights
        for k in range(8):
            
            result = tuple(map(lambda x,y: x + y, pos, self.enemyKnightRange[k]))
            if -1<result[0]<8 and -1<result[1]<8:
                #print(result)
                piece = self.get_piece(result)
            else:
                continue
            if (white == True and piece == 'n') or (white == False and piece == 'N'):
                pinnedState = self.getLegal_pin((not white), result, kingPos)    
                if pinnedState == [] or enemyPawn == True:
                    if inCheck == 0:
                        self.checkVector = [result]
                        print("knight vector thing:" + str(result))
                    inCheck += 1
                    print("adding legal N move")
        # For pawns
        blocking2Move = 'o'
        for l in range(2):
            result = tuple(map(lambda x,y: x + y, pos, self.enemyPawnRange[l]))
            #print("pawnPos: " + str(result))
            if -1<result[0]<8 and -1<result[1]<8:
                # This will ignore second noncapture enemyPawnRange element if it isn't in its starting position.
                # This will also ignore if there is a piece inbetween this position and a blocking position along checkVector
                if l == 1 and (((result[0] != 1 and white == True) or (result[0] != 6 and white == False)\
                or blocking2Move != 'o') and pawnCapture == False):
                    break
                piece = self.get_piece(result)
                # Basically, if this piece does not equal 'o', that means the pawn can't move two squares.
                blocking2Move = piece
                #print("blocking2Move: " + str(blocking2Move))
                #print("Test piece:" + str(result) + str(piece))
                #print("pawnCapture:" + str(pawnCapture))
            else:
                #print("king check test: out of range!")
                continue
            if (white == True and piece == 'p') or (white == False and piece == 'P') or ((piece == 'P' and white == True and enemyPawn == False) or \
                (piece == 'p' and white == False and enemyPawn == False)):
                pinnedState = self.getLegal_pin((not white), result, kingPos)    
                if pinnedState == [] or enemyPawn == True:    
                    inCheck += 1
                    print("adding legal pawn move")
        # For enemy king
        for m in range(8):
            result = tuple(map(lambda x,y: x + y, pos, self.totalDeltaRange[m]))
            if -1<result[0]<8 and -1<result[1]<8:
                piece = self.get_piece(result)
                if white == True and piece == 'k' and enemyPawn == True:
                    inCheck += 1
                    print("adding enemy black king")
                elif white == False and piece == 'K' and enemyPawn == True:
                    inCheck += 1
                    print("adding enemy white king")
        return inCheck
    # In this function, legal1 wil be the matrix and legal2 will be the vector.
    def legal_convolution(self, legal1, legal2):
        self.finalMoves = [None] * 8
        if legal2 != []:
            for i in range(8):
                self.finalMoves[i] = ['X','X','X','X','X','X','X','X'] 
                for j in range(8):
                    for k in range(len(legal2)):
                        if (i,j) == legal2[k] and legal1[i][j] == 'O':
                            self.finalMoves[i][j] = 'O'
        # This method will take the inputted position and piece and update a csv file of its legal moves.
        # By default, the file will be filled with 'X's (illegal moves).
        # When a piece is clicked, it will update its legal moves to be shown with 'O's
        # The formula for calculating legal moves is as follows:
        # Legal Moves = (Normal Moves) - (Obstacle Moves) - !(Pinned Moves) + (Special Moves)

        # If piece isn't pinned, then only general legality applies.
        else:
            self.finalMoves = legal1
        with open('piece.csv', 'w') as writer:
                writerRow = csv.writer(writer)
                for row in self.finalMoves:
                    writerRow.writerow(row)

    def getLegal_pawn(self, pos, white): 
        # Initialize pawn vector parameters.
        self.pawnRange = []
    #for debugging
        if white == True:
            forward1 = (pos[0] - 1,pos[1])
            forward2 = (pos[0] - 2,pos[1])
            capture1 = (pos[0]-1, pos[1]-1)
            print("capture1 = " + str(capture1))
            capture2 = (pos[0]-1, pos[1]+1)
            if -1<capture1[0]<8 and -1<capture1[1]<8:
                capturePiece1 = self.get_piece(capture1)
                print("capture piece: " + str(capturePiece1))
            else:
                capturePiece1 = 'o'
            if -1<capture2[0]<8 and -1<capture2[1]<8:
                capturePiece2 = self.get_piece(capture2)
                print(capturePiece2)
            else:
                capturePiece2 ='o'
            for i in self.blackPieces:
                # print(i)
                # print(capture1)
                if capturePiece1 == i:      
                    self.pawnRange += [capture1]
                    break
            for i in self.blackPieces:
                if capturePiece2 == i:
                    self.pawnRange += [capture2]
                    break
            if self.get_piece(forward1) == 'o':
                self.pawnRange += [forward1]
                print(self.pawnRange)        
                if pos[0] == 6 and self.get_piece(forward2) == 'o': # if pawn at starting position and 2 empty spaces
                        self.pawnRange += [forward2]
            #print(tuple([pos[0]-1, pos[1]+1]))
            # print(capture2)
            
        else:
            forward1 = (pos[0] + 1,pos[1])
            forward2 = (pos[0] + 2,pos[1])
            capture1 = (pos[0]+1, pos[1]-1)
            capture2 = (pos[0]+1, pos[1]+1)
            if -1<capture1[0]<8 and -1<capture1[1]<8:
                capturePiece1 = self.get_piece(capture1)
            else:
                capturePiece1 = 'o'
            if -1<capture2[0]<8 and -1<capture2[1]<8:
                capturePiece2 = self.get_piece(capture2)
            else:
                capturePiece2 = 'o'
            for i in self.whitePieces:
                if capturePiece1 == i:
                    self.pawnRange += [capture1]
                    break
            for i in self.whitePieces:
                if capturePiece2 == i:
                    self.pawnRange += [capture2]
                    break
            if self.get_piece(forward1) == 'o':
                self.pawnRange += [forward1]
                print(self.pawnRange)
                if pos[0] == 1 and self.get_piece(forward2) == 'o': # if pawn at starting position and 2 empty spaces
                        self.pawnRange += [forward2]
    
        # Now to transfer possible moves list to self.legalMoves_general.
        for element in self.pawnRange:
            #print("hi")
            self.legalMoves_general[element[0]][element[1]] = 'O'

board = Board()
piece = Piece()
