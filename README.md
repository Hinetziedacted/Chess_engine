# Chess Engine GUI

A modern, lightweight chess engine with a graphical user interface (GUI), developed entirely in Python. Features AI opponent, real-time move analysis, and a clean, user-friendly interface. Designed for rapid play, academic demonstration, and portfolio use.

##  Features

- **Full GUI**: Built using `tkinter` for a responsive, cross-platform interface.
- **AI Opponent**: Implements Minimax algorithm with alpha-beta pruning (search depth adjustable for difficulty).
- **Positional Evaluation**: Piece-square tables for realistic move analysis and strength (estimated ~1200–1600 Elo).
- **Move History**: Track all moves with algebraic notation.
- **Captured Pieces**: Visual tracking of material balance during play.
- **Board Flip, Undo, and Reset**: Flexible controls for both practice and analysis.
- **Load FEN**: Supports custom starting positions and chess puzzles.
- **Lightweight & Fast**: Designed to run on any modern laptop without external dependencies beyond `python-chess` and `Pillow`.

##  Academic Value

This project demonstrates practical knowledge of:
- Algorithmic thinking (AI search, evaluation functions)
- Python programming (data structures, GUI, modularity)
- Software design (clean code, user experience)
- Application packaging and open-source workflow

##  Screenshots

![image](https://github.com/user-attachments/assets/2cf4392f-0639-4780-b932-be35ac4de8e5)

##  How to Run

1. **Clone this repository**
2. **Install dependencies:**
    ```bash
    pip install python-chess pillow
    ```
3. **Ensure you have the images:**
   - Place PNGs for all chess pieces (`wp.png`, `bn.png`, etc.) in an `images/` folder.
4. **Run:**
    ```bash
    python Full_GUI_Chess_Engine.py
    ```

## Piece Images

You’ll need the following PNGs in your `images/` folder:




![wb](https://github.com/user-attachments/assets/fcab4546-15c4-41e7-b00a-a20e72a53a02)
![br](https://github.com/user-attachments/assets/a5c67c52-84a3-4384-9f07-c3a168e0cc2e)
![bq](https://github.com/user-attachments/assets/d90a1e14-01ee-44a7-8484-f64842c0fc82)
![bp](https://github.com/user-attachments/assets/bda8eba1-701a-4fe0-b2f0-86ed2f260706)
![bn](https://github.com/user-attachments/assets/1ade0b92-72f6-4e77-91c6-737915afc43e)
![bk](https://github.com/user-attachments/assets/0ecca8ee-5f9f-48f8-b27b-9a8e854d487a)
![bb](https://github.com/user-attachments/assets/9057d11d-9fdb-4d71-9131-7840ff29ff43)
![wr](https://github.com/user-attachments/assets/a1b1083e-1d92-4da1-9b1c-baef185f7d48)
![wq](https://github.com/user-attachments/assets/e0aeddf0-ae43-4c93-aef0-c397bbd30de8)
![wp](https://github.com/user-attachments/assets/d24e64ab-54e3-4e09-b12b-96bcc60a8446)
![wn](https://github.com/user-attachments/assets/5155926f-5e3f-4b8f-883e-38b88d67a377)
![wk](https://github.com/user-attachments/assets/013243eb-ef0f-455a-a219-06f88bf7b776)

