from legal import *

if __name__ == '__main__':
    # Initialize game, constants
    Board()
    #TODO: change these to be variable inside piece class.
    whiteKing_pos = (7,4)
    blackKing_pos = (0,4)

    white = True
    specialMove = False
    while True:
        temp = []
        print("Select a piece.")
        while True:

            inputString = input()
            Piece()
            try:
                oldPos= tuple(map(int, inputString.split(',')))
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
        # TODO: modify for turn-base.
        for i in range(6):
            if myPiece == piece.blackPieces[i]:
                white = False
                kingPos = blackKing_pos
                
                break
            elif myPiece == piece.whitePieces[i]:
                white = True
                kingPos = whiteKing_pos
                break
        # piece.getLegal_mate()
        print(myPiece)
        print("white: " + str(white))
        piece.getLegal(oldPos, myPiece, white)
        legalMoves_general = piece.legalMoves_general
        temp = piece.getLegal_pin(white, oldPos, kingPos)
        #print(temp)
        piece.legal_convolution(legalMoves_general, temp)
        #print(piece.finalMoves)
        print("Select new position for piece, or type 'exit")
        while True:
            inputString = input()
            print(whiteKing_pos)
            if inputString == "exit":
                break
            else:
                try:
                    newPos= tuple(map(int, inputString.split(',')))
                    if -1<newPos[0]<8 and -1<newPos[1]<8:
                        pass
                    else:
                        print("Piece coords out of range. Try again.")
                except:
                    print("Piece coords not in correct format. Try again.")
            if piece.finalMoves[newPos[0]][newPos[1]] == 'O':
                board.move(oldPos, newPos, myPiece)
                print("move successful!")
                break
            else:
                print("Not a valid move. Try again")
            
            

