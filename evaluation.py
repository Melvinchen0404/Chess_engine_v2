import chess

# Material values
PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000,  
}

# Piece-square tables for evaluation
PIECE_SQUARE_TABLES = {
    chess.PAWN: [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [5, 5, 10, 15, 15, 10, 5, 5],
        [10, 10, 20, 25, 25, 20, 10, 10],
        [20, 20, 30, 35, 35, 30, 20, 20],
        [30, 30, 40, 45, 45, 40, 30, 30],
        [40, 40, 50, 55, 55, 50, 40, 40],
        [50, 50, 60, 65, 65, 60, 50, 50],
        [100, 100, 100, 100, 100, 100, 100, 100]
],
    chess.KNIGHT: [
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20, 0, 0, 0, 0, -20, -40],
        [-30, 0, 10, 15, 15, 10, 0, -30],
        [-30, 5, 15, 20, 20, 15, 5, -30],
        [-30, 0, 15, 20, 20, 15, 0, -30],
        [-30, 5, 10, 15, 15, 10, 5, -30],
        [-40, -20, 0, 5, 5, 0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50]
],
    chess.BISHOP: [
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10, 5, 0, 0, 0, 0, 5, -10],
        [-10, 10, 10, 10, 10, 10, 10, -10],
        [-10, 0, 10, 10, 10, 10, 0, -10],
        [-10, 5, 5, 10, 10, 5, 5, -10],
        [-10, 0, 5, 10, 10, 5, 0, -10],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-20, -10, -10, -10, -10, -10, -10, -20]
],
    chess.ROOK: [
        [0, 0, 0, 5, 5, 0, 0, 0],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [5, 10, 10, 10, 10, 10, 10, 5],
        [0, 0, 0, 0, 0, 0, 0, 0]
],
    chess.QUEEN: [  # Corrected Queen's table (2D format)
        [-20, -10, -10, -5, -5, -10, -10, -20],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-10, 0, 5, 5, 5, 5, 0, -10],
        [-5, 0, 5, 5, 5, 5, 0, -5],
        [0, 0, 5, 5, 5, 5, 0, -5],
        [-10, 5, 5, 5, 5, 5, 0, -10],
        [-10, 0, 5, 0, 0, 0, 0, -10],
        [-20, -10, -10, -5, -5, -10, -10, -20]
],
    chess.KING: [
        [20, 30, 10, 0, 0, 10, 30, 20],
        [20, 20, 0, 0, 0, 0, 20, 20],
        [-10, -20, -20, -20, -20, -20, -20, -10],
        [20, -30, -30, -40, -40, -30, -30, -20],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30]
]
}

def flip_piece_square_table(table):
    """Flip the piece-square table for black pieces."""
    return [row[::-1] for row in table[::-1]]

def get_piece_square_table(piece_type, is_white):
    """Return the piece-square table for a given piece and its color."""
    if is_white:
        return PIECE_SQUARE_TABLES[piece_type]
    else:
        # Flip for Black pieces by reversing the rows and columns
        return [row[::-1] for row in PIECE_SQUARE_TABLES[piece_type]][::-1]

def evaluate_material(board):
    """Evaluate the material balance of the board."""
    white_material = sum(len(board.pieces(pt, chess.WHITE)) * PIECE_VALUES[pt] for pt in PIECE_VALUES)
    black_material = sum(len(board.pieces(pt, chess.BLACK)) * PIECE_VALUES[pt] for pt in PIECE_VALUES)
    material_diff = white_material - black_material
    
    if material_diff > 0:
        return "Material: Adv for White"
    elif material_diff < 0:
        return "Material: Adv for Black"
    else:
        return "Material: Even"

def evaluate_position(board):
    """Evaluate the positional difference between white and black."""
    white_position = 0
    black_position = 0

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is None:
            continue

        is_white = piece.color == chess.WHITE
        piece_value = PIECE_VALUES[piece.piece_type]
        
        # Positional evaluation (using flipped table for black)
        piece_square_table = get_piece_square_table(piece.piece_type, is_white)
        square_index = chess.SQUARES.index(square)
        
        # Get the positional value based on the piece's position
        piece_position_value = piece_square_table[square_index // 8][square_index % 8]

        # Accumulate the positional values for white and black
        if is_white:
            white_position += piece_position_value
        else:
            black_position += piece_position_value

    position_diff = white_position - black_position
    
    if position_diff > 0:
        return "Position: Adv for White"
    elif position_diff < 0:
        return "Position: Adv for Black"
    else:
        return "Position: Even"

def evaluate_mobility(board) -> str:
    """Evaluate the mobility of both players."""
    
    # Get mobility for white
    if board.turn == chess.WHITE:
        white_mobility = len(list(board.legal_moves))
    else:
        # Create a copy of the board to evaluate white's moves
        board_copy = board.copy()
        board_copy.turn = chess.WHITE
        white_mobility = len(list(board_copy.legal_moves))
    
    # Get mobility for black
    if board.turn == chess.BLACK:
        black_mobility = len(list(board.legal_moves))
    else:
        # Create a copy of the board to evaluate black's moves
        board_copy = board.copy()
        board_copy.turn = chess.BLACK
        black_mobility = len(list(board_copy.legal_moves))
    
    # Calculate the mobility difference
    mobility_diff = white_mobility - black_mobility
    
    # Return the mobility evaluation
    if mobility_diff > 0:
        return "Mobility: Adv for White"
    elif mobility_diff < 0:
        return "Mobility: Adv for Black"
    else:
        return "Mobility: Even"

def evaluate_space_control(board) -> str:
    # Define central squares
    central_squares = {chess.D4, chess.E4, chess.D5, chess.E5}
    
    # Initialize control counters
    white_central_control = 0
    black_central_control = 0
    white_non_central_control = 0
    black_non_central_control = 0
    
    # Evaluate control for all squares
    for square in chess.SQUARES:
        is_central = square in central_squares
        
        if board.is_attacked_by(chess.WHITE, square):
            if is_central:
                white_central_control += 1
            else:
                white_non_central_control += 1
        
        if board.is_attacked_by(chess.BLACK, square):
            if is_central:
                black_central_control += 1
            else:
                black_non_central_control += 1
    
    # Calculate scores
    white_score = white_central_control * 2 + white_non_central_control
    black_score = black_central_control * 2 + black_non_central_control
    
    # Overall evaluation
    control_diff = white_score - black_score
    if control_diff > 0:
        return "Square Control: Adv for White"
    elif control_diff < 0:
        return "Square Control: Adv for Black"
    else:
        return "Square Control: Even"