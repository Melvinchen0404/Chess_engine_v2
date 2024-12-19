# Chess_engine_v2
**Lichess GM database** 

File for retrieving the correct keys for the dictionary metadata to extract information: gm_database_testing.py
Dictionary keys: 'white', 'draws', 'black', 'moves', 'topGames', 'opening' 
The structure for 'topGames': 'uci', 'id', 'winner', 'white' {'name', 'rating'}, 'black' {'name', 'rating'}, 'year', 'month'

File for checking the GM database for the best move from the current position (given in FEN notation): gm_database.py
Up to 5 games displayed, with surnames kept (using the .split()[0] function) and commas after surnames removed (using the re.sub(r"[^\w\s]", "" function to remove non-alphanumeric and non-whitespace characters from a string)

**Chess engines**

Stockfish: https://stockfishchess.org/
Initialize the environment with !apt-get install stockfish, before accessing the Stockfish (Linux-based) engine through the path /usr/games/stockfish

Komodo: https://komodochess.com
Download a Linux-based version of Komodo from https://komodochess.com/downloads.htm
Upload the executable (.exe file) on Colab and access the Komodo engine

**Endgame tablebase**

**Lichess Syzygy endgame tablebase (EGTB)** is accessible through API requests: http://tablebase.lichess.ovh/standard?fen={fen}
The **Lichess Syzygy EGTB** allows us to access information about WDL (Win/Draw/Loss) and DTZ (Depth to Zero)
