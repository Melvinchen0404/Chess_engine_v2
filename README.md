# Chess_engine (Sapientia_v6)
**Lichess GM database**

File for retrieving the correct keys for the dictionary metadata to extract information: <code>gm_database_testing.py</code>

Dictionary keys: <code>'white', 'draws', 'black', 'moves', 'topGames', 'opening'</code> 

The structure for <code>'topGames'</code>: <code>'uci', 'id', 'winner', 'white' {'name', 'rating'}, 'black' {'name', 'rating'}, 'year', 'month'</code>

File for checking the GM database for the best move from the current position (given in FEN notation): <code>gm_database.py</code>

Up to 5 games displayed, with surnames kept (using the <code>.split()[0]</code> function) and commas after surnames removed (using the <code>re.sub(r"[^\w\s]", ""</code> function to remove non-alphanumeric and non-whitespace characters from a string)

**Chess engines**

<table>
  <tr>
    <th>Engine</th>
    <th>Link</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>Stockfish</td>
    <td><a href="https://stockfishchess.org/">https://stockfishchess.org/</a></td>
    <td>Initialize the environment with !apt-get install stockfish, before accessing the Stockfish (Linux-based) engine through the path <code>/usr/games/stockfish</code></td>
  </tr>
  <tr>
    <td>Komodo</td>
    <td>https://komodochess.com</td>
    <td>Download a Linux-based version of Komodo from <a href="https://komodochess.com/downloads.htm">https://komodochess.com/downloads.htm</a>. Upload the executable (<code>.exe</code> file) on Colab and access the Komodo engine</td>
  </tr>
</table>

**Lichess openings dataset**

**Lichess openings dataset** is available on Hugging Face: https://huggingface.co/datasets/Lichess/chess-openings

<table>
  <tr>
    <th>Dictionary Keys</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><code>'eco-volume'</code></td>
    <td>The <i>Encyclopaedia of Chess Openings</i> (<i>ECO</i>) volume in which the opening appears. <i>ECO</i> is a reference work, originally published in five volumes (A-E) from 1974-1979</td>
  </tr>
  <tr>
    <td><code>'eco'</code></td>
    <td>The <i>ECO</i> classification code for the opening</td>
  </tr>
    <tr>
    <td><code>'name'</code></td>
    <td>Name of opening (for instance, Polish Opening, Nimzo-Larsen Attack, Zukertort Defense: Sicilian Knight Variation, and so on)</td>
  </tr>
    <tr>
    <td><code>'pgn'</code></td>
    <td>The PGN (Portable Game Notation) for the opening. PGN typically uses Standard Algebraic Notation (SAN) to represent chess moves</td>
  </tr>
  </tr>
  <tr>
    <td><code>'uci'</code></td>
    <td>The Universal Chess Interface (UCI) chess protocol for communicating the opening</td>
  </tr>
  <tr>
    <td><code>'epd'</code></td>
    <td>The Extended Position Description (EPD) for the opening. EPD is an extension of FEN (Forsyth–Edwards Notation)</td>
  </tr>
</table>

**Endgame tablebase**

**Lichess Syzygy endgame tablebase (EGTB)** is accessible through API requests: <a href="http://tablebase.lichess.ovh/standard?fen=">http://tablebase.lichess.ovh/standard?fen=</a><code>{fen}</code>

The **Lichess Syzygy EGTB** allows us to access information about WDL (Win/Draw/Loss) and DTZ (Depth to Zero)

**Sound files**

The following <code>.mp3</code> files should be uploaded in a 'sounds' folder:
<table>
  <tr>
    <th>File Name</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><code>game_start.mp3</code></td>
    <td>For initialization and reset of board</td>
  </tr>
  <tr>
    <td><code>move.mp3</code></td>
    <td>For each valid move</td>
  </tr>
</table>

Source: https://www.chess.com/forum/view/general/chessboard-sound-files?page=2#comment-89885805
