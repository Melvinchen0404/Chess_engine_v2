import requests

# Function to fetch WDL and DTZ from Lichess Syzygy tablebase
def fetch_endgame_tablebase_data(fen: str):
    """
    Fetch WDL (Win/Draw/Loss) and DTZ (Distance to Zero) for a given FEN
    from the Lichess Syzygy tablebase API, replacing spaces with underscores.
    """
    # Save original FEN for local processing
    original_fen = fen
    
    # Replace spaces with underscores in the FEN string for API compatibility
    fen = fen.replace(" ", "_")
    
    # Construct the URL for the Lichess Syzygy API request
    url = f"http://tablebase.lichess.ovh/standard?fen={fen}"
    
    try:
        # Make a GET request to the Lichess API
        response = requests.get(url)
        data = response.json()
        
        # Check if the 'category' field exists in the response
        if "category" in data:
            wdl = data["category"]
            dtz = data["dtz"]

            # Extract which player's turn it is from the original FEN (the second part of the FEN string)
            turn = original_fen.split()[1]  # "w" or "b"

            # Map WDL to the output text (Win/Draw/Loss) based on whose turn it is
            if wdl == "win":
                result = "Win for White" if turn == 'w' else "Win for Black"
            elif wdl == "loss":
                result = "Loss for White" if turn == 'w' else "Loss for Black"
            elif wdl == "draw":
                result = "Draw"
            else:
                result = "Unknown result"

            # Return the result as a dictionary
            return {
                "FEN": original_fen,
                "WDL": result,
                "DTZ": dtz,
                "WDL_numeric": 1 if wdl == "win" else -1 if wdl == "loss" else 0,
                "DTZ_numeric": dtz
            }
        else:
            return {"FEN": original_fen, "Error": "Position not available in tablebase."}
    except requests.exceptions.RequestException as e:
        return {"FEN": original_fen, "Error": f"Request failed: {e}"}

def best_endgame_move(fen: str, turn: str) -> str:
    """
    Fetch the best move from the Lichess Syzygy tablebase API for a given position (FEN) and turn.
    
    Args:
        fen (str): The FEN string representing the current board state.
        turn (str): The color of the player to move. Should be 'white' or 'black'.
    
    Returns:
        str: The best move in UCI notation or None if no valid move found or category is 'null' or 'unknown'.
    """
    # Replace spaces with underscores in the FEN string for API compatibility
    fen = fen.replace(" ", "_")
    
    # Construct the URL for the Lichess Syzygy API request
    url = f"http://tablebase.lichess.ovh/standard?fen={fen}"
    
    try:
        # Make a GET request to the Lichess API
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        
        # Parse the response JSON
        data = response.json()

        # Check if 'category' exists and is neither 'null' nor 'unknown'
        category = data.get('category')
        if category not in ['null', 'unknown']:
            # Check if the 'moves' key exists and the list is not empty
            if 'moves' in data and len(data['moves']) > 0:
                # Extract the first UCI move
                first_move_uci = data['moves'][0]['uci']

                # Validate the UCI move string (length check for UCI moves)
                if len(first_move_uci) in [4, 5]:  # UCI move must be 4 or 5 characters long
                    return first_move_uci
                else:
                    return None
            else:
                # If no valid moves were found, return None
                return None
        else:
            # If 'category' is 'null' or 'unknown', return None
            return None
    
    except requests.exceptions.RequestException as e:
        # Handle any errors that occur during the request (e.g., network issues)
        print(f"Error: {e}")
        return None