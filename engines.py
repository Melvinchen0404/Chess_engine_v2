import chess
import os
from chess.engine import SimpleEngine

def fetch_stockfish_data(fen, depth=3, stockfish_path="/usr/games/stockfish"):
    """
    Fetch the best move for a given FEN position using the Stockfish engine.
    """
    try:
        # Ensure the Stockfish engine has execute permissions
        os.chmod(stockfish_path, 0o755)

        board = chess.Board(fen)
        with SimpleEngine.popen_uci(stockfish_path) as engine:
            result = engine.play(board, chess.engine.Limit(depth=depth))
            return result.move.uci()
    except Exception as e:
        print(f"Error while fetching best move from Stockfish: {e}")
        return None

def fetch_komodo_data(fen, depth=3, komodo_path="/content/komodo3sse42"):
    """
    Fetch the best move for a given FEN position using the Komodo engine.
    """
    try:
        # Ensure that the Komodo engine has execute permissions
        os.chmod(komodo_path, 0o755)

        board = chess.Board(fen)
        with SimpleEngine.popen_uci(komodo_path) as engine:
            result = engine.play(board, chess.engine.Limit(depth=depth))
            return result.move.uci()
    except Exception as e:
        print(f"Error while fetching best move from Komodo: {e}")
        return None
