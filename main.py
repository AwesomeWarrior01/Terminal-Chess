from legal import *

if __name__ == '__main__':
    # Initialize game, constants
    Board()
    whiteKing_pos = (6,6)
    blackKing_pos = (0,7)
    white = True
    specialMove = False
    while True:
        temp = []
        inputString = input()
        Piece()

        myPos= tuple(map(int, inputString.split(',')))
        #print(myPos)
        myPiece = piece.get_piece(myPos)
        if myPiece == 'o':
            print("not a valid piece")
            continue
        # Determine piece color from chosen position.
        for i in range(6):
            if myPiece == piece.blackPieces[i]:
                white = False
                kingPos = blackKing_pos
                
                break
            elif myPiece == piece.whitePieces[i]:
                white = True
                kingPos = whiteKing_pos
                break

        print(myPiece)
        print("white: " + str(white))
        piece.getLegal(myPos, myPiece, white)
        legalMoves_general = piece.legalMoves_general
        temp = piece.getLegal_pin(white, myPos, kingPos)
        #print(temp)
        piece.legal_convolution(legalMoves_general, temp)
        #print(piece.finalMoves)
        print(whiteKing_pos)
    
