import os
import sys
import argparse
import chess
import chess.engine
import chess.svg
from IPython.display import display, SVG, clear_output, Audio, Javascript
import ipywidgets as widgets
import threading
import concurrent.futures
from openings import process_moves, uci_to_san, check_openings, get_user_moves
from gm_database import fetch_gm_data, process_gm_data
from engines import fetch_komodo_data, fetch_stockfish_data
from endgame import fetch_endgame_tablebase_data, best_endgame_move
from evaluation import evaluate_material, evaluate_position, evaluate_space_control, evaluate_mobility

class ChessGUI:
    def __init__(self):
        # Board and caching
        self.board = chess.Board()
        self.fen_cache = {}
        self.previous_fen = None
        self.is_initial_render = True

        # Move sequences
        self.current_uci_sequence = []
        self.current_san_sequence = []

        # Thread pool for asynchronous tasks
        self.executor = concurrent.futures.ThreadPoolExecutor()

        # GUI elements
        self.input_box = widgets.Text(
            placeholder='Enter your move or command', description='Command:')
        self.submit_button = widgets.Button(description="Submit")
        self.reset_button = widgets.Button(description="Reset")
        self.undo_button = widgets.Button(description="Undo")
        self.output_area = widgets.Output()
        self.chessboard_output = widgets.Output()
        self.button_layout = widgets.HBox(
            [self.submit_button, self.reset_button, self.undo_button])
        self.layout_container = widgets.VBox(
            [self.input_box, self.button_layout, self.chessboard_output, self.output_area])

        # Button styling
        self._style_buttons()

        # Attach event handlers
        self.submit_button.on_click(self.on_submit_click)
        self.reset_button.on_click(self.on_reset_click)

        # Render initial board
        self.render_board(
            game_start_sound="/content/sample_data/sounds/game_start.mp3")
        display(self.layout_container)

    def _style_buttons(self):
        """Set button styles."""
        for button in [self.submit_button, self.reset_button, self.undo_button]:
            button.layout.width = '7%'
            button.layout.height = '20px'
            button.style.font = 'Arial 5pt'

    def dynamic_depth(self):
        """Dynamically adjust engine depth based on the number of pieces."""
        piece_count = len(self.board.piece_map())
        if piece_count > 16:
            return 6
        elif piece_count > 8:
            return 8
        else:
            return 12

    def render_board(self, scale=0.6, game_start_sound=None, move_sound=None, hide_controls=True):
        """Render the chessboard."""
        current_fen = self.board.fen()
        if current_fen == self.previous_fen:
            return
        self.previous_fen = current_fen

        with self.chessboard_output:
            clear_output(wait=True)
            board_svg = chess.svg.board(self.board, size=400 * scale)
            display(SVG(board_svg))
            if self.is_initial_render and game_start_sound:
                self.play_sound_async(game_start_sound, hide_controls)
                self.is_initial_render = False
            elif move_sound:
                self.play_sound_async(move_sound, hide_controls)

    def play_sound_async(self, file_path, hide_controls=True):
        """Play sound asynchronously."""
        try:
            display(Audio(file_path, autoplay=True, embed=True))
            if hide_controls:
                display(Javascript("""
                    var audio = document.querySelector('audio');
                    if (audio) {
                        audio.style.display = 'none';
                        audio.play();
                    }
                """))
        except Exception as e:
            print(f"Error playing sound: {e}")

    def fetch_and_process(self, fen):
        """Fetch and process data with caching."""
        if fen in self.fen_cache:
            return self.fen_cache[fen]

        gm_data = fetch_gm_data(fen)
        best_move_uci, _, _, _, top_games = process_gm_data(gm_data)

        depth = self.dynamic_depth()
        best_move_stockfish = fetch_stockfish_data(
            fen, depth=depth) or "No best move available"
        best_move_komodo = fetch_komodo_data(
            fen, depth=depth) or "No best move available"
        best_move_syzygy = best_endgame_move(
            fen, turn="white" if self.board.turn else "black") or "No endgame move available"

        opening_matches = check_openings(get_user_moves(self.board))
        endgame_data = fetch_endgame_tablebase_data(fen)
        wdl = endgame_data.get("WDL", "N/A")
        dtz = endgame_data.get("DTZ", "N/A")

        data = {
            "best_move_uci": best_move_uci,
            "top_games": top_games,
            "best_move_stockfish": best_move_stockfish,
            "best_move_komodo": best_move_komodo,
            "best_move_syzygy": best_move_syzygy,
            "wdl": wdl,
            "dtz": dtz,
            "opening_matches": opening_matches
        }
        self.fen_cache[fen] = data
        return data

    def display_best_moves_and_analysis(self, data, fen):
        """Display analysis data in a table format."""
        uci_sequence = " ".join(self.current_uci_sequence)
        san_sequence = " ".join(self.current_san_sequence)
        board = chess.Board(fen)
        material = evaluate_material(board)
        position = evaluate_position(board)
        mobility = evaluate_mobility(board)
        space_control = evaluate_space_control(board)
        evaluations = f"{material}, {position}, {mobility}, {space_control}"

        table_rows = [
            ("Current FEN:", fen),
            ("Current UCI Sequence:", uci_sequence),
            ("Current SAN Sequence:", san_sequence),
            ("Matched Opening from Lichess Openings Dataset:",
             data["opening_matches"] or "No matched opening available"),
            ("Evaluation from Sapientia:", evaluations),
            ("Best Move from GM Database:", data["best_move_uci"] or "No best move available"),
            ("Top Games with Best Move:", data["top_games"] or "No GM games found"),
            ("Best Move from Stockfish:", data["best_move_stockfish"]),
            ("Best Move from Komodo:", data["best_move_komodo"]),
            ("Best Endgame Move from Syzygy:", data["best_move_syzygy"]),
            ("WDL (Win/Draw/Loss):", data["wdl"]),
            ("DTZ (Depth to Zero):", data["dtz"]),
        ]

        table_html = "<table style='border-collapse: collapse; width: 100%; margin: 0 auto; font-size: 10px;'>"
        table_html += """
        <tr style='background-color: #f2f2f2;'>
            <th style='border: 0px solid black; padding: 3px 5px; text-align: left; font-weight: bold;'>Variable</th>
            <th style='border: 0px solid black; padding: 3px 5px; text-align: left; font-weight: bold;'>Value</th>
        </tr>
        """
        for index, row in enumerate(table_rows):
            row_color = "#ffffff" if index % 2 == 0 else "#f9f9f9"
            table_html += f"""
            <tr style='background-color: {row_color};'>
                <td style='border: 0px solid black; padding: 2px 5px;'>{row[0]}</td>
                <td style='border: 0px solid black; padding: 2px 5px;'>{row[1]}</td>
            </tr>
            """
        table_html += "</table>"

        with self.output_area:
            clear_output(wait=True)
            display(widgets.HTML(value=table_html))

    def process_command(self, msg):
        """Process user commands."""
        msg = msg.strip().lower()
        if msg == "reset":
            self.board.reset()
            self.render_board(game_start_sound="/content/sample_data/sounds/game_start.mp3")
        elif msg == "undo":
            if self.board.move_stack:
                self.board.pop()
            self.render_board()
        elif msg == "quit":
            sys.exit()
        else:
            try:
                # Ensure the move string is valid before proceeding
                if len(msg) not in [4, 5]:
                    print(f"Invalid input: {msg}. Please enter a UCI move (e.g., 'e2e4').")
                    return

                move = chess.Move.from_uci(msg)
                if move in self.board.legal_moves:
                    self.board.push(move)  # Push the move first
                    self.current_uci_sequence = [move.uci() for move in self.board.move_stack]
                    self.current_san_sequence = uci_to_san(self.current_uci_sequence)  # Convert UCI to SAN

                    self.render_board(move_sound="/content/sample_data/sounds/move.mp3")

                    fen = self.board.fen()
                    data = self.fetch_and_process(fen)  # Fetch data for the new position
                    self.display_best_moves_and_analysis(data, fen)  # Display analysis
                else:
                    print(f"Illegal move: {msg}")
            except ValueError as e:
                print(f"Invalid move or command: {msg}. Error: {e}")
            except AssertionError as e:
                print(f"Error processing move: {msg}. {e}")

    def on_submit_click(self, _):
        """Handle submit button click."""
        self.process_command(self.input_box.value)
        self.input_box.value = ""

    def on_reset_click(self, _):
        """Handle reset button click."""
        self.board.reset()
        self.render_board(
            game_start_sound="/content/sample_data/sounds/game_start.mp3")
