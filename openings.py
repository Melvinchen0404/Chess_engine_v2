import chess
from datasets import load_dataset
from IPython.display import display, clear_output, Markdown

# Global variables for storing move sequences
uci_sequence = []  # To store moves in UCI notation

# Load the Lichess chess openings dataset
dset = load_dataset("Lichess/chess-openings")
train_data = dset['train']
openings_dict = {entry["name"]: entry["uci"] for entry in train_data}

def get_user_moves(board):
    """Return all moves made on the board as a space-separated UCI string."""
    return " ".join([move.uci() for move in board.move_stack])

def check_openings(user_moves):
    """Check the openings database for matches with the current user moves."""
    return [
        (name, uci) for name, uci in openings_dict.items()
        if user_moves.startswith(uci)
    ]

def process_moves(msg, board):
    """Process user moves and update the board."""
    msg = msg.strip()
    if ' ' in msg:
        moves = msg.split()
        for move_uci in moves:
            try:
                move = chess.Move.from_uci(move_uci)
                if move in board.legal_moves:
                    board.push(move)
                else:
                    print(f"Illegal move: {move_uci}. Try again.")
            except Exception as e:
                print(f"Invalid move format: {move_uci}. Error: {e}")
    else:
        try:
            move = chess.Move.from_uci(msg)
            if move in board.legal_moves:
                board.push(move)
            else:
                print(f"Illegal move: {msg}. Try again.")
        except Exception as e:
            print(f"Invalid move format: {msg}. Error: {e}")

def uci_to_san(uci_moves):
    """
    Convert a sequence of UCI moves into SAN moves for the given chess position.

    Args:
        uci_moves (list): List of UCI moves as strings (e.g., ["e2e4", "e7e5"]).

    Returns:
        list: List of SAN moves corresponding to the input UCI moves.
    """
    board = chess.Board()
    san_moves = []
    for move in uci_moves:
        try:
            san_move = board.san(chess.Move.from_uci(move))
            san_moves.append(san_move)
            board.push_san(san_move)
        except ValueError as e:
            print(f"Error processing move {move}: {e}")
            break
    return san_moves
