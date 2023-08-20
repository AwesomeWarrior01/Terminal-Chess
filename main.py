from legal import *

if __name__ == '__main__':

    # Initialize some variables for when starting the game.
    white = True
    kingPos = board.whiteKing_pos
    
    lastEnemyPawnMove = (-1,-1) # This last enemy move is set to a dummy value since there's no checks on move #1

    print("white to move:")
    while True:
        promotionMove = False
        # This is really bad, and I should definitely have variable arguements, but this should also work.
        numChecks = piece.getLegal_pieceControl(kingPos, kingPos, white, True, True)
        print("check vector: " +  str(piece.checkVector))
        pieceVectorTemp = piece.checkVector
        piece.getLegal_mate(kingPos, numChecks, white, pieceVectorTemp)

        legalMoves_pin = []
        while True:
            print("Select a piece.")
            # weird stuff is being written to piece.csv, so I'm wiping it before every input.
            Piece()
            inputString = input()
            try:
                inputString = board.letterNum_to_coords(inputString)
                oldPos= inputString
                if -1<oldPos[0]<8 and -1<oldPos[1]<8:
                    break
                else:
                    print("Piece coords out of range. Try again.")
            except:
                print("piece coords not in correct format. Try again.")
        #print(myPos)

        myPiece = piece.get_piece(oldPos)
        if myPiece == 'o':
            print("Not a valid piece. Try again.")
            continue
        # Determine piece color from chosen position.
        superBreak = False
        for i in range(6):
            if myPiece == piece.blackPieces[i] and white == True:
                superBreak = True
                break
            elif myPiece == piece.whitePieces[i] and white == False:
                superBreak = True
                break
        if superBreak == True:
            print("Piece is not your color! Try again.")
            continue
        # piece.getLegal_mate()
        print(myPiece)
        print("white: " + str(white))
        piece.getLegal(oldPos, kingPos, myPiece, white)
        piece.getLegal_special(oldPos, kingPos, myPiece, lastEnemyPawnMove, numChecks)
        legalMoves_general = piece.legalMoves_general
        legalMoves_pin = piece.getLegal_pin(white, oldPos, kingPos)
        piece.legal_convolution(legalMoves_general, legalMoves_pin)
        #print(piece.finalMoves)
        # This if-statement is needed so that king pieces are not convoluted with final check vector.
        if myPiece != 'k' and myPiece != 'K':
            piece.legal_convolution(piece.finalMoves, piece.checkVectorPermanent)
            #print(piece.finalMoves)

        #print(piece.finalMoves)
        print("Select new position for piece, or type 'exit")
        while True:
            inputString = input()
            #print(board.whiteKing_pos)
            if inputString == "exit": break
            else:
                try:
                    inputString = board.letterNum_to_coords(inputString)
                    newPos= inputString
                    if -1<newPos[0]<8 and -1<newPos[1]<8:
                        pass
                    else:
                        print("Piece coords out of range. Try again.")
                except:
                    print("Piece coords not in correct format. Try again.")
                    continue
            if piece.finalMoves[newPos[0]][newPos[1]] == 'O':
                #TODO: add code for special moves here!
                # Special moves pawn
                if myPiece == 'p' or myPiece == 'P':
                    lastEnemyPawnMove = newPos
                    print("en-passant could be legal next turn!")
                    if newPos[0] == 0 or newPos[0] == 7:
                        # TODO: there will be another prompt for promotion here.
                        print("select a piece you would like to promote to\n\
                        (i.e. 'queen', 'rook'. 'bishop', or 'knight') or select\n\
                        'exit' to go back to piece seletion.")
                        inputString = input()
                        if inputString == "exit":
                            break
                        elif inputString == "queen":
                            myPiece = 'Q' if white == True else 'q'
                        elif inputString == "rook":
                            myPiece = 'R' if white == True else 'r'
                        elif inputString == "bishop":
                            myPiece = 'B' if white == True else 'b'
                        elif inputString == "knight":
                            myPiece = 'K' if white == True else 'k'
                        else:
                            print("Not a valid piece. Try again."); continue

                else:
                    lastEnemyPawnMove = (-1,-1) # set to some dummy coord.
                board.update(oldPos, newPos, myPiece, white)
                print("move successful!")
                
                # Update king position if king moved.
                if white == True:
                    white = False
                    # Special moves king
                    if myPiece == 'K':
                        board.whiteKing_pos = newPos
                        print("new white king pos is: " + str(newPos))
                    kingPos = board.blackKing_pos
                    print("Black to move:")
                else: # Black
                    white = True
                    kingPos = board.whiteKing_pos
                    # Special moves king
                    if myPiece == 'k':
                        board.blackKing_pos = newPos
                        print("new black king pos is: " + str(newPos))
                    kingPos = board.whiteKing_pos
                    print("White to move:")
                break
            else:
                print("Not a valid move. Try again")
            
            

