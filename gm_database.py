import requests
import re

# Function to fetch GM data from Lichess
def fetch_gm_data(fen):
    url = f"https://explorer.lichess.ovh/master?fen={fen}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()  # Return the JSON data if successful
    else:
        print(f"Failed to fetch GM data. Status code: {response.status_code}")
        return {}

# Function to extract best move and top GM games
def process_gm_data(data):
    moves = data.get("moves", [])
    games = data.get("topGames", [])

    # Find the best move (most played move in the database)
    if moves:
        best_move = max(moves, key=lambda move: move["white"] + move["black"])
        best_move_uci = best_move['uci']
        best_move_white_wins = best_move['white']
        best_move_black_wins = best_move['black']
        best_move_draws = best_move['draws']
    else:
        best_move_uci = "No best move found"
        best_move_white_wins = best_move_black_wins = best_move_draws = "N/A"

    # Process top games if they exist
    top_games = []
    if games:
        for i, game in enumerate(games[:5]):  # Limit to 5 games
            white = re.sub(r"[^\w\s]", "", game.get("white", {}).get("name", "Unknown").split()[0])
            black = re.sub(r"[^\w\s]", "", game.get("black", {}).get("name", "Unknown").split()[0])
            year = game.get("year", "Unknown")
            winner = game.get("winner", "Unknown")
            
            if winner == "white":
                result = "1-0"
            elif winner == "black":
                result = "0-1"
            else:
                result = "1/2-1/2"  # No winner implies a draw

            top_games.append(f"Game {i + 1}: {white} vs {black} ({year}), Result: {result}")
    else:
        top_games.append("No GM games found for the given position.")
    
    return best_move_uci, best_move_white_wins, best_move_black_wins, best_move_draws, top_games
