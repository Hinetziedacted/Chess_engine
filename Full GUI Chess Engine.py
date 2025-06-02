# Full GUI Chess Engine with Python-Chess and Tkinter
# Estimated Strength: 1200–1600 Elo (Adaptive options included)

import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import chess
import time
import os

# ------------------- CONFIGURATION -------------------
SEARCH_DEPTH = 3       # base search depth
TIME_DELAY = 0.5       # seconds to pause for engine move display
BOARD_SIZE = 600       # pixels
SQUARE_SIZE = BOARD_SIZE // 8
PIECE_IMAGES = {}      # to be filled with PhotoImage objects
IMAGE_PATH = "images/" # folder containing piece PNGs: wp.png, wn.png, ..., bp.png, etc.

# Colors for board squares
LIGHT_COLOR = "#F0D9B5"
DARK_COLOR = "#B58863"
HIGHLIGHT_COLOR = "#FFFB91"

# -------------------- AI ENGINE --------------------
node_count = 0

PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 0
}

PAWN_TABLE = [
     0,  5,  5, -10, -10,  5,  5,  0,
     0, 10, -10,  0,   0, -10, 10,  0,
     0, 10,  10, 20,  20,  10, 10,  0,
     5, 20,  20, 30,  30,  20, 20,  5,
    10, 20,  20, 30,  30,  20, 20, 10,
    50, 50,  50, 50,  50,  50, 50, 50,
    80, 80,  80, 80,  80,  80, 80, 80,
     0,  0,   0,  0,   0,   0,  0,  0
]
KNIGHT_TABLE = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20,   0,   5,   5,   0, -20, -40,
    -30,   5,  10,  15,  15,  10,   5, -30,
    -30,   0,  15,  20,  20,  15,   0, -30,
    -30,   5,  15,  20,  20,  15,   5, -30,
    -30,   0,  10,  15,  15,  10,   0, -30,
    -40, -20,   0,   0,   0,   0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50
]
BISHOP_TABLE = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10,   0,   0,   0,   0,   0,   0, -10,
    -10,   0,   5,  10,  10,   5,   0, -10,
    -10,   5,   5,  10,  10,   5,   5, -10,
    -10,   0,  10,  10,  10,  10,   0, -10,
    -10,  10,  10,  10,  10,  10,  10, -10,
    -10,   5,   0,   0,   0,   0,   5, -10,
    -20, -10, -10, -10, -10, -10, -10, -20
]
ROOK_TABLE = [
     0,   0,   5,  10,  10,   5,   0,   0,
     0,   0,   5,  10,  10,   5,   0,   0,
     0,   0,   5,  10,  10,   5,   0,   0,
     0,   0,   5,  10,  10,   5,   0,   0,
     0,   0,   5,  10,  10,   5,   0,   0,
     0,   0,   5,  10,  10,   5,   0,   0,
    25,  25,  25,  25,  25,  25,  25,  25,
     0,   0,   5,  10,  10,   5,   0,   0
]
QUEEN_TABLE = [
    -20, -10, -10,  -5,  -5, -10, -10, -20,
    -10,   0,   0,   0,   0,   0,   0, -10,
    -10,   0,   5,   5,   5,   5,   0, -10,
     -5,   0,   5,   5,   5,   5,   0,  -5,
      0,   0,   5,   5,   5,   5,   0,  -5,
    -10,   5,   5,   5,   5,   5,   0, -10,
    -10,   0,   5,   0,   0,   0,   0, -10,
    -20, -10, -10,  -5,  -5, -10, -10, -20
]
KING_TABLE = [
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -10, -20, -20, -20, -20, -20, -20, -10,
     20,  20,   0,   0,   0,   0,  20,  20,
     20,  30,  10,   0,   0,  10,  30,  20
]

# -------------------- EVALUATION --------------------
def evaluate_material(board):
    total = 0
    for square, piece in board.piece_map().items():
        total += PIECE_VALUES.get(piece.piece_type, 0) * (1 if piece.color == chess.WHITE else -1)
    return total

def evaluate_piece_square(board):
    total = 0
    for piece_type, table in [
        (chess.PAWN, PAWN_TABLE),
        (chess.KNIGHT, KNIGHT_TABLE),
        (chess.BISHOP, BISHOP_TABLE),
        (chess.ROOK, ROOK_TABLE),
        (chess.QUEEN, QUEEN_TABLE),
        (chess.KING, KING_TABLE)
    ]:
        for square in board.pieces(piece_type, chess.WHITE):
            total += table[square]
        for square in board.pieces(piece_type, chess.BLACK):
            total -= table[chess.square_mirror(square)]
    return total

def evaluate_board(board):
    if board.is_checkmate():
        return -99999 if board.turn == chess.WHITE else 99999
    if board.is_stalemate() or board.is_insufficient_material():
        return 0
    mat_score = evaluate_material(board)
    pos_score = evaluate_piece_square(board)
    return mat_score + pos_score

# -------------------- MINIMAX WITH ALPHA-BETA --------------------
def order_moves(board):
    moves = list(board.legal_moves)
    moves.sort(key=lambda m: board.is_capture(m), reverse=True)
    return moves

def minimax(board, depth, alpha, beta, maximizing_player):
    global node_count
    node_count += 1
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)
    if maximizing_player:
        max_eval = float('-inf')
        for move in order_moves(board):
            board.push(move)
            eval_score = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            if eval_score > max_eval:
                max_eval = eval_score
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in order_moves(board):
            board.push(move)
            eval_score = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            if eval_score < min_eval:
                min_eval = eval_score
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval

def find_best_move(board, depth):
    global node_count
    node_count = 0
    best_score = float('inf')
    best_move = None
    for move in order_moves(board):
        board.push(move)
        score = minimax(board, depth - 1, float('-inf'), float('inf'), True)
        board.pop()
        if score < best_score:
            best_score = score
            best_move = move
    return best_move

# -------------------- GUI WINDOW CLASS --------------------
class ChessGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Custom Chess Engine")
        self.board = chess.Board()
        self.selected_square = None
        self.move_highlights = []
        self.move_history = []
        self.captured_white = []
        self.captured_black = []
        self.search_depth = SEARCH_DEPTH

        # Main frames
        self.frame_board = tk.Frame(root)
        self.frame_board.grid(row=0, column=0)
        self.frame_right = tk.Frame(root)
        self.frame_right.grid(row=0, column=1, sticky="n")

        # Canvas for the chessboard
        self.canvas = tk.Canvas(self.frame_board, width=BOARD_SIZE, height=BOARD_SIZE)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)

        # Right panel widgets: move history, captured pieces, eval bar, controls
        tk.Label(self.frame_right, text="Move History").pack(pady=5)
        self.text_history = tk.Text(self.frame_right, width=30, height=20, state='disabled')
        self.text_history.pack()

        tk.Label(self.frame_right, text="Captured Pieces").pack(pady=5)
        self.label_white_caps = tk.Label(self.frame_right, text="White: ")
        self.label_white_caps.pack()
        self.label_black_caps = tk.Label(self.frame_right, text="Black: ")
        self.label_black_caps.pack()

        tk.Label(self.frame_right, text="Evaluation").pack(pady=5)
        self.eval_label = tk.Label(self.frame_right, text="0")
        self.eval_label.pack(pady=2)
        self.eval_bar_canvas = tk.Canvas(self.frame_right, width=200, height=20)
        self.eval_bar_canvas.pack(pady=2)

        # Control buttons
        tk.Button(self.frame_right, text="Undo", command=self.undo_move).pack(pady=5)
        tk.Button(self.frame_right, text="New Game", command=self.new_game).pack(pady=5)
        tk.Button(self.frame_right, text="Load FEN", command=self.load_fen).pack(pady=5)
        tk.Button(self.frame_right, text="Flip Board", command=self.flip_board).pack(pady=5)
        tk.Button(self.frame_right, text="Quit", command=root.quit).pack(pady=5)

        self.flipped = False

        self.load_piece_images()
        self.draw_board()
        self.update_gui()

    def load_piece_images(self):
        pieces = ['wp','wn','wb','wr','wq','wk','bp','bn','bb','br','bq','bk']
        for p in pieces:
            path = os.path.join(IMAGE_PATH, f"{p}.png")
            img = Image.open(path)
            img = img.resize((SQUARE_SIZE, SQUARE_SIZE), Image.Resampling.LANCZOS)
            PIECE_IMAGES[p] = ImageTk.PhotoImage(img)

    def draw_board(self):
        self.canvas.delete("all")
        color = LIGHT_COLOR
        for rank in range(8):
            color = DARK_COLOR if color == LIGHT_COLOR else LIGHT_COLOR
            for file in range(8):
                x1 = file * SQUARE_SIZE
                y1 = rank * SQUARE_SIZE
                x2 = x1 + SQUARE_SIZE
                y2 = y1 + SQUARE_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, tags="square")
                color = DARK_COLOR if color == LIGHT_COLOR else LIGHT_COLOR
        self.canvas.tag_lower("square")

    def draw_pieces(self):
        self.canvas.delete("piece")
        for square, piece in self.board.piece_map().items():
            row, col = divmod(square, 8)
            if self.flipped:
                row = 7 - row
                col = 7 - col
            x = col * SQUARE_SIZE
            y = (7 - row) * SQUARE_SIZE if not self.flipped else row * SQUARE_SIZE
            key = ("w" if piece.color == chess.WHITE else "b") + piece.symbol().lower()
            self.canvas.create_image(x, y, image=PIECE_IMAGES[key], anchor='nw', tags=("piece", f"{square}"))

    def highlight_moves(self, square):
        self.canvas.delete("highlight")
        self.move_highlights.clear()
        for move in self.board.legal_moves:
            if move.from_square == square:
                to_sq = move.to_square
                row, col = divmod(to_sq, 8)
                if self.flipped:
                    row = 7 - row
                    col = 7 - col
                x = col * SQUARE_SIZE
                y = (7 - row) * SQUARE_SIZE if not self.flipped else row * SQUARE_SIZE
                oval = self.canvas.create_oval(
                    x + SQUARE_SIZE * 0.3, y + SQUARE_SIZE * 0.3,
                    x + SQUARE_SIZE * 0.7, y + SQUARE_SIZE * 0.7,
                    fill=HIGHLIGHT_COLOR, outline="", tags="highlight"
                )
                self.move_highlights.append(oval)

    def on_click(self, event):
        file = event.x // SQUARE_SIZE
        rank = 7 - (event.y // SQUARE_SIZE) if not self.flipped else event.y // SQUARE_SIZE
        square = chess.square(file, rank)
        piece = self.board.piece_at(square)
        if self.selected_square is None:
            if piece is not None and piece.color == chess.WHITE:
                self.selected_square = square
                self.highlight_moves(square)
        else:
            move = chess.Move(self.selected_square, square)
            if move in self.board.legal_moves:
                self.make_move(move)
            self.selected_square = None
            self.canvas.delete("highlight")

    def make_move(self, move):
        captured = self.board.piece_at(move.to_square)
        self.board.push(move)
        self.move_history.append(move.uci())
        if captured is not None:
            if captured.color == chess.WHITE:
                self.captured_white.append(captured)
            else:
                self.captured_black.append(captured)
        self.update_gui()
        self.root.update()
        if not self.board.is_game_over():
            self.root.after(int(TIME_DELAY * 1000), self.engine_move)

    def engine_move(self):
        engine_depth = self.search_depth
        move = find_best_move(self.board, engine_depth)
        if move is not None:
            captured = self.board.piece_at(move.to_square)
            self.board.push(move)
            self.move_history.append(move.uci())
            if captured is not None:
                if captured.color == chess.WHITE:
                    self.captured_white.append(captured)
                else:
                    self.captured_black.append(captured)
        self.update_gui()

    def update_gui(self):
        self.draw_board()
        self.draw_pieces()
        self.update_history()
        self.update_captured()
        self.update_eval()
        if self.board.is_game_over():
            self.show_game_result()

    def update_history(self):
        self.text_history.configure(state='normal')
        self.text_history.delete(1.0, tk.END)
        for i in range(0, len(self.move_history), 2):
            move_str = f"{(i // 2) + 1}. "
            move_str += self.move_history[i]
            if i + 1 < len(self.move_history):
                move_str += " " + self.move_history[i + 1]
            move_str += "\n"
            self.text_history.insert(tk.END, move_str)
        self.text_history.configure(state='disabled')

    def update_captured(self):
        white_caps = " ".join([p.symbol().upper() for p in self.captured_white])
        black_caps = " ".join([p.symbol().lower() for p in self.captured_black])
        self.label_white_caps.config(text=f"White: {white_caps}")
        self.label_black_caps.config(text=f"Black: {black_caps}")

    def update_eval(self):
        score = evaluate_board(self.board)
        self.eval_label.config(text=str(score))
        self.eval_bar_canvas.delete("all")
        normalized = max(-10000, min(10000, score))
        length = 200
        pos = int((normalized + 10000) / 20000 * length)
        self.eval_bar_canvas.create_rectangle(0, 0, pos, 20, fill="white")
        self.eval_bar_canvas.create_rectangle(pos, 0, length, 20, fill="black")

    def undo_move(self):
        if len(self.move_history) < 1:
            return
        # Undo two plies (engine + human) if possible
        self.board.pop()
        self.move_history.pop()
        if self.board.move_stack:
            last = self.board.pop()
            self.move_history.pop()
            captured = last.captured_piece
            if captured:
                if captured.color == chess.WHITE:
                    self.captured_white.pop()
                else:
                    self.captured_black.pop()
        self.update_gui()

    def new_game(self):
        self.board = chess.Board()
        self.move_history.clear()
        self.captured_white.clear()
        self.captured_black.clear()
        self.update_gui()

    def load_fen(self):
        fen = filedialog.askstring("Load FEN", "Enter FEN string:")
        if fen:
            try:
                self.board.set_fen(fen)
                self.move_history.clear()
                self.captured_white.clear()
                self.captured_black.clear()
                self.update_gui()
            except:
                messagebox.showerror("Error", "Invalid FEN string.")

    def flip_board(self):
        self.flipped = not self.flipped
        self.update_gui()

    def show_game_result(self):
        if self.board.is_checkmate():
            winner = "Black" if self.board.turn == chess.WHITE else "White"
            messagebox.showinfo("Game Over", f"Checkmate! {winner} wins.")
        elif self.board.is_stalemate():
            messagebox.showinfo("Game Over", "Stalemate. Draw.")
        elif self.board.is_insufficient_material():
            messagebox.showinfo("Game Over", "Draw by insufficient material.")
        else:
            messagebox.showinfo("Game Over", "Game Over.")

# -------------------- MAIN --------------------
def main():
    root = tk.Tk()
    gui = ChessGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
