# Chess_engine_v2
**Lichess GM database** 

File for retrieving the correct keys for the dictionary metadata to extract information: <code>gm_database_testing.py</code>

Dictionary keys: <code>'white', 'draws', 'black', 'moves', 'topGames', 'opening'</code> 

The structure for <code>'topGames'</code>: <code>'uci', 'id', 'winner', 'white' {'name', 'rating'}, 'black' {'name', 'rating'}, 'year', 'month'</code>

File for checking the GM database for the best move from the current position (given in FEN notation): <code>gm_database.py</code>

Up to 5 games displayed, with surnames kept (using the <code>.split()[0]</code> function) and commas after surnames removed (using the <code>re.sub(r"[^\w\s]", ""</code> function to remove non-alphanumeric and non-whitespace characters from a string)

**Chess engines**

Stockfish: <a href="https://stockfishchess.org/">https://stockfishchess.org/</a>

Initialize the environment with !apt-get install stockfish, before accessing the Stockfish (Linux-based) engine through the path <code>/usr/games/stockfish</code>

Komodo: https://komodochess.com

Download a Linux-based version of Komodo from <a href="https://komodochess.com/downloads.htm">https://komodochess.com/downloads.htm</a>

Upload the executable (<code>.exe</code> file) on Colab and access the Komodo engine

**Endgame tablebase**

**Lichess Syzygy endgame tablebase (EGTB)** is accessible through API requests: <code>http://tablebase.lichess.ovh/standard?fen={fen}</code>

The **Lichess Syzygy EGTB** allows us to access information about WDL (Win/Draw/Loss) and DTZ (Depth to Zero)
