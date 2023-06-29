import pygame
import stockfish
import csv

#note to self: board will be indexed 1-8.

#TODO: There are 3 types of illegal moves. They are:

#1. moving a piece in a direction it cannot normally go (i.e. moving a king as if it were a queen).
#2. moving through pieces as with the pawn, bishop, rook, or queen.
#3. moving your own king into check.

#So far, only #1 has been taken care of with 'move _check' and 'move_check_limited'. However, #2 and #3 still need to be done.
class Board:
    def __init__(self) -> None:
        with open('chess.csv', 'w') as board:
            #This just creates the stating position by adding a whole bunch of rows to csv file
            writer = csv.writer(board)
            writer.writerow(['r','n','b','q','k','b','n','r'])
            writer.writerow(['p','p','p','p','r','p','p','p'])
            for i in range(3):
                writer.writerow(['o','o','o','o','o','o','o','q'])
            writer.writerow(['o','q','q','o','N','o','o','o'])
            writer.writerow(['P','P','P','P','o','N','P','P'])
            writer.writerow(['R','N','B','Q','K','B','N','R'])
    #This method will update piece positions in csv file
    def update(self, oldPos, newPos, specialMove):
        oldPiece = Piece.get_piece(self, oldPos)
        
         
             #This is the default case that works for any normal move or capture.
        if specialMove == 0:
            Board.move(self, oldPos, newPos, oldPiece)
        #This will be for Kingside Castling
        elif specialMove == 1:
            pass
        #Queenside Castling
        elif specialMove == 2:
            pass
        #Queen Promotion
        elif specialMove == 3:
            pass
        #Rook Promotion
        elif specialMove == 4:
            pass
        #Knight promotion
        elif specialMove == 5:
            pass
        #Bishop promotion
        elif specialMove == 6:
            pass
        else:
            print("Bruh what kinda goofy-ahh move did you just make??")


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

        
        
            
class Piece:
    def __init__(self) -> None:
        pass
    #This function will get the name of a piece on a given square,
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

     #This functon checks legality for bishop, rook, and queen (pieces that have unlimited move distance)
    def move_check(self, oldPos, newPos):
        legal = False
        super_break = False
        for i in range(4):
            self.range = [None]*8

            for j in range(8):
                
                #Here, delta_range is sent from the child class
                self.range[j] = tuple([(j+1)*x for x in self.delta_range[i]])
                #print(self.range[j])
                result = tuple(map(lambda x,y: x + y, oldPos, self.range[j]))
                
                if result == newPos and 0 < newPos[0] < 9 and 0 < newPos[1] < 9:
                    super_break = True
                    legal = True
                    print(result)
                elif ((0 > result[0] or result[0] > 8) or (0 > result[1] or result[1] > 8)):
                    break
            if super_break == True:
                break
        return legal
    #This function checks legality for king and knight (pieces that have limited move distance except pawns)
    def move_check_limited(self, oldPos, newPos):
        legal = False
        for i in range(8):
            result = tuple(map(lambda x,y: x + y, oldPos, self.range[i]))
            print(result)
            if result == newPos and 0 < newPos[0] < 9 and 0 < newPos[1] < 9:
                legal = True
                break
        return legal
    #This function checks if knight or king move is a capture. It returns 'legal' as 3 values:
    #legal = 0: move is not a capture.
    #legal = 1: move is a legal capture (opponents piece is on that square)
    #legal = -1: move is not legal (one of your own pieces is already occupying the square)
    def capture_check_limited(self, newpos):
        pass
    #This will check to see if the move made puts one's own king in check (another type of illegal move)
    #TODO: right now this method will check every square along the given vector for problematic pieces. I need to have it so that if 
    #it encounters a non problematic piece it breaks and returns legal as True. however, if it encounters a 'o' indicating an empty square, it instead should keep going.
    def kingCheck_check(self, white, piece, piece_oldPos, kingPos, specialMove):
        
        delta_range_diag = [(1,1), (-1,1), (-1,-1), (1,-1)]
        delta_range_rowcol = [(1,0), (0,1), (-1,0), (0,-1)]
        vector = None
        range_temp = [None]*8
        sus_rowcol = False
        sus_diag = False
        #sus_diag = False
        sus = True
        super_break = False
        legal = False
        #This one will be very complicated, but it will basically check to see
        #Wherever the king moves, if it is put into check.
        if piece == "king":
            pass
        #This will be used to check for legality when castling
        elif specialMove == True:
            pass
        #This will check to see if the piece that moved was actually pinned to the king
        else:
                for i in range(4):
                    for j in range(8):
                        range_temp[j] = tuple([(j+1)*x for x in delta_range_diag[i]])
                        #print(self.range[j])
                        diag_result = tuple(map(lambda x,y: x + y, kingPos, range_temp[j]))
                        if piece_oldPos == diag_result:

                            sus_diag = True
                            print("piece move may have put king in check on diagonal")
                            #This will set the vector to the diagonal unit vector that the piece was moved on
                            vector = delta_range_diag[i]
                            #So here's the thing: the vector here is currently the opposite reciprical of what it should
                            #be, since I'm going off of chess board coordinates but csv files have a different coord system.
                            #because of this, I have to do a bit of jank to fix it.
                            new_vector = tuple([-vector[1], -vector[0]])
                            print(new_vector)
                            
                            super_break = True
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
                            #This compares piece positions. If a piece is in the same unit vector direction from the king, and has only 'o' inbetween, it could be pinned
                            if piece_oldPos == rowcol_result:
                                vector = delta_range_rowcol[i]
                                print("vector:" + str(vector))
                                sus_rowcol = True
                                print("piece move may have put king in check on vertical or horizontal")
                                break
                            #This only continues checking if there is a 'o' on the square.
                            else:
                                test_piece = self.get_piece(rowcol_result)
                                if test_piece != 'o':
                                    print("moved piece not pinned on rowcol vector :)")
                                    break
                            #If the piece is an enemy piece, it is either not pinned or it is an illegal move.
                
                            
                                
                    #now if sus is True, we need to see if there was an enemy piece along the diagnal or rowcol that can put the king in check. 
                if sus_diag == True or sus_rowcol == True:
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
                                #If one of the problematic pieces exist in the direction of the vector, the move is illegal!
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
                            #This check is makes sure that the coordinate actually exists on the chess board. If not,
                            #the loop will break
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

class Knight(Piece):
    def __init__(self) -> None:
        super().__init__()
        #This list of tuples contains all legal possible changes in the position of the knight.
        self.range = [(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]
    
class Bishop(Piece):
    def __init__(self) -> None:
        super().__init__()
        self.delta_range = [(1,1), (-1,1), (-1,-1), (1,-1)]
        
class Rook(Piece):
    def __init__(self) -> None:
        super().__init__()
        self.delta_range = [(1,0), (0,1), (-1,0), (0,-1)]
    
class Queen(Piece):
    def __init__(self) -> None:
        super().__init__()
        self.delta_range = [(1,1), (-1,1), (-1,-1), (1,-1), (1,0), (0,1), (-1,0), (0,-1)]

class King(Piece):
    def __init__(self) -> None:
        super().__init__()
        self.range = [(1,1), (-1,1), (-1,-1), (1,-1), (1,0), (0,1), (-1,0), (0,-1)]
        #self.position = "e1"

    #When the king moves, check for knight, pawn, enemy king, queen, bishop, and rook covering intended move square.

    #To do this, I may need a 'get closest piece' function.
    def kingMove_check(self):
        pass
    
    

class Pawn(Piece):
    def __init__(self) -> None:
        super().__init__()
        self.whiteRange = [(-1,0)]
        self.blackRange = [(1,0)]
        self.firstMove = [None] * 8 
        
        self.blackPieces = ['p','n','b','r','q']
        self.whitePieces = ['P','N','B','R','Q']

    def move_check(self, oldPos, newPos, white, firstMove, specialMove): 
        #This needs to be fixed so that pawns moving forward do not capture pieces. (AKA they need to move onto 
        #empty squares)
        if white == True:
            if firstMove == True:
                self.whiteRange += [(-2,0)]

            print(tuple([oldPos[0]-1, oldPos[1]-1]))
            temp = tuple([oldPos[0]-1, oldPos[1]-1])
            capture1 = self.get_piece(temp)
            for i in self.blackPieces:
                #print(i)
                #print(capture1)
                if capture1 == i:      
                    self.whiteRange += [(-1,-1)]
            print(tuple([oldPos[0]-1, oldPos[1]+1]))
            capture2 = self.get_piece(tuple([oldPos[0]-1, oldPos[1]+1]))
            print(capture2)
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



board = Board()

oldPosTest = (5,6)
newPosTest = (1,1)

pawnOldPos = (6,3)
pawnNewPos = (5,0)
specialMove = False

knight = Knight()
bishop = Bishop()
rook = Rook()
king = King()
pawn = Pawn()
test_bishop = bishop.move_check(oldPosTest, newPosTest)
test_knight = knight.move_check_limited(oldPosTest, newPosTest)
test_rook = rook.move_check(oldPosTest, newPosTest)

print(test_knight)
print(test_bishop)
print(test_rook)

white = True

knight = "knight"

kingPos = (7,4)
knight_oldPos = (6,5)
knight2_oldPos = (5,4)

queen_oldPos = (7,3)
bishop_oldPos = (7,5)



pin_test = king.kingCheck_check(white, knight, knight_oldPos, kingPos, specialMove)
print(pin_test)
pin_test2 = king.kingCheck_check(white, knight, pawnOldPos, kingPos, specialMove)
print(pin_test2)
#king.get_piece((5,1))
#name = input('what is your name?')
#print(name)

#pawn = pawn.move_check(pawnOldPos, pawnNewPos, white=True, firstMove=True, specialMove=False)

#board.update(oldPosTest, newPosTest, specialMove=0) #TODO: This method is bad, since it doesn't actually create a good csv file. Fix this!
