import stockfish
import pygame
#stockfish = Stockfish(path="/usr/games/stockfish")
#stockfish = stockfish.Stockfish(path="/usr/games/stockfish", depth=18, parameters={"Threads": 2, "Minimum Thinking Time": 30})
stockfish = stockfish.Stockfish()
stockfish._set_option(value=True,name="stockfish")
stockfish.update_engine_parameters({"Hash": 2048, "UCI_Chess960": "true"}) # Gets stockfish to use a 2GB hash table, and also to play Chess960.
stockfish.get_wdl_stats()


wdl = stockfish.does_current_engine_version_have_wdl_option()
print(wdl)

fen = stockfish.is_fen_valid("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
print(fen)
visual = stockfish.get_board_visual(True)
print(visual)
#The way this works is it just uses coords, so no need to use piece names.
stockfish.set_position(["b1c3", "e7e6"])#This will throw an error if it is not a legal move :(

visual = stockfish.get_board_visual(True)
print(visual)

#stockfish.make_moves_from_current_position(["g2g4", "b1c3", "f1d3"])

hi = stockfish.get_best_move()
print(hi)
stockfish.get_fen_position()

