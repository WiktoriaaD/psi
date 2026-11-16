import math
import tkinter as tk


def get_lines(board, n):
    lines = [board[i] for i in range(n)]
    lines += [[board[r][i] for r in range(n)] for i in range(n)]
    lines.append([board[i][i] for i in range(n)])
    lines.append([board[i][n - 1 - i] for i in range(n)])
    return lines


def check_winner(board, n):
    for line in get_lines(board, n):
        if line[0] != " " and all(cell == line[0] for cell in line):
            return line[0]
    return None


def is_full(board):
    return all(cell != " " for row in board for cell in row)


def evaluate(board, n):
    score = 0
    for line in get_lines(board, n):
        if "X" not in line and "O" in line:
            score += line.count("O")
        elif "O" not in line and "X" in line:
            score -= line.count("X")
    return score


def minimax(board, depth, is_maximizing, max_depth, n):
    winner = check_winner(board, n)
    if winner == "O":
        return 100 - depth
    if winner == "X":
        return -100 + depth
    if is_full(board):
        return 0
    if depth == max_depth:
        return evaluate(board, n)

    if is_maximizing:
        best = -math.inf
        for r in range(n):
            for c in range(n):
                if board[r][c] == " ":
                    board[r][c] = "O"
                    best = max(best, minimax(board, depth + 1, False, max_depth, n))
                    board[r][c] = " "
        return best
    else:
        best = math.inf
        for r in range(n):
            for c in range(n):
                if board[r][c] == " ":
                    board[r][c] = "X"
                    best = min(best, minimax(board, depth + 1, True, max_depth, n))
                    board[r][c] = " "
        return best


def best_move(board, max_depth, n):
    best_val = -math.inf
    move = None
    for r in range(n):
        for c in range(n):
            if board[r][c] == " ":
                board[r][c] = "O"
                val = minimax(board, 1, False, max_depth, n)
                board[r][c] = " "
                if val > best_val:
                    best_val = val
                    move = (r, c)
    return move


class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Kółko i Krzyżyk - Minimax")

        ctrl = tk.Frame(root, padx=10, pady=10)
        ctrl.pack()

        tk.Label(ctrl, text="Rozmiar:").grid(row=0, column=0)
        self.size_var = tk.IntVar(value=3)
        tk.Spinbox(ctrl, from_=3, to=6, width=3, textvariable=self.size_var).grid(row=0, column=1, padx=5)

        tk.Label(ctrl, text="Głębokość:").grid(row=0, column=2)
        self.depth_var = tk.IntVar(value=9)
        tk.Spinbox(ctrl, from_=1, to=9, width=3, textvariable=self.depth_var).grid(row=0, column=3, padx=5)

        self.first_var = tk.StringVar(value="user")
        tk.Radiobutton(ctrl, text="Zaczyna Gracz (X)", variable=self.first_var, value="user").grid(row=1, column=0, columnspan=2, sticky="w")
        tk.Radiobutton(ctrl, text="Zaczyna Komputer (O)", variable=self.first_var, value="comp").grid(row=1, column=2, columnspan=2, sticky="w")

        tk.Button(ctrl, text="Nowa gra", command=self.start_game).grid(row=2, column=0, columnspan=4, pady=5, sticky="ew")

        self.status = tk.Label(root, text="", font=("Arial", 11, "bold"))
        self.status.pack(pady=5)

        #plansza
        self.board_frame = tk.Frame(root, padx=10, pady=10)
        self.board_frame.pack()

        self.start_game()

    def start_game(self):
        self.n = self.size_var.get()
        self.max_depth = self.depth_var.get()

        # Optymalizacja głębokości dla plansz większych niż 3x3
        if self.n > 3 and self.max_depth > 3:
            self.max_depth = 3
            self.depth_var.set(3)

        self.board = [[" " for _ in range(self.n)] for _ in range(self.n)]
        self.game_over = False

        #cleanup
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        self.buttons = []
        for r in range(self.n):
            row_btns = []
            for c in range(self.n):
                btn = tk.Button(
                    self.board_frame,
                    text=" ",
                    font=("Arial", 20, "bold"),
                    width=4,
                    height=2,
                    command=lambda r=r, c=c: self.on_click(r, c)
                )
                btn.grid(row=r, column=c)
                row_btns.append(btn)
            self.buttons.append(row_btns)

        if self.first_var.get() == "comp":
            self.computer_turn()
        else:
            self.status.config(text="Twój ruch (X)")

    def on_click(self, r, c):
        if self.game_over or self.board[r][c] != " ":
            return

        self.board[r][c] = "X"
        self.buttons[r][c].config(text="X", fg="blue")

        if self.check_end():
            return

        self.computer_turn()

    def computer_turn(self):
        self.status.config(text="Ruch komputera...")
        self.root.update()  # odswieza

        move = best_move(self.board, self.max_depth, self.n)
        if move:
            r, c = move
            self.board[r][c] = "O"
            self.buttons[r][c].config(text="O", fg="red")

        if not self.check_end():
            self.status.config(text="Twój ruch (X)")

    def check_end(self):
        winner = check_winner(self.board, self.n)
        if winner:
            self.game_over = True
            self.status.config(text="Wygrywa komputer (O)!" if winner == "O" else "Wygrywasz (X)!")
            return True
        if is_full(self.board):
            self.game_over = True
            self.status.config(text="Remis!")
            return True
        return False


if __name__ == "__main__":
    root = tk.Tk()
    TicTacToeGUI(root)
    root.mainloop()
