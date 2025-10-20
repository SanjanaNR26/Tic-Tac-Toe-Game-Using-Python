import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe vs Smart Computer")
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_turn = "X"  # "X" = user, "O" = computer
        self.round_number = 0
        self.create_board()
        self.start_new_round()

    def create_board(self):
        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.root, text="", font=("Helvetica", 32), width=5, height=2,
                                command=lambda row=i, col=j: self.player_move(row, col))
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

    def start_new_round(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", state="normal")
        self.round_number += 1
        self.current_turn = "X" if self.round_number % 2 == 1 else "O"

        if self.current_turn == "O":
            self.root.after(300, self.computer_move)

    def player_move(self, row, col):
        if self.board[row][col] == "" and self.current_turn == "X":
            self.make_move(row, col, "X")
            if not self.check_game_end("X"):
                self.current_turn = "O"
                self.root.after(300, self.computer_move)

    def computer_move(self):
        best_score = float("-inf")
        best_move = None

        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = "O"
                    score = self.minimax(self.board, 0, False)
                    self.board[i][j] = ""
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)

        if best_move:
            row, col = best_move
            self.make_move(row, col, "O")
            if not self.check_game_end("O"):
                self.current_turn = "X"

    def make_move(self, row, col, player):
        self.board[row][col] = player
        self.buttons[row][col].config(text=player, state="disabled")

    def check_game_end(self, player):
        if self.check_winner(self.board, player):
            winner = "You" if player == "X" else "Computer"
            messagebox.showinfo("Game Over", f"🏆 {winner} wins!")
            self.start_new_round()
            return True
        elif self.is_draw(self.board):
            messagebox.showinfo("Game Over", "🤝 It's a draw!")
            self.start_new_round()
            return True
        return False

    def check_winner(self, board, player):
        for i in range(3):
            if all(board[i][j] == player for j in range(3)) or \
               all(board[j][i] == player for j in range(3)):
                return True
        if all(board[i][i] == player for i in range(3)) or \
           all(board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def is_draw(self, board):
        return all(board[i][j] != "" for i in range(3) for j in range(3))

    def minimax(self, board, depth, is_maximizing):
        if self.check_winner(board, "O"):
            return 1
        elif self.check_winner(board, "X"):
            return -1
        elif self.is_draw(board):
            return 0

        if is_maximizing:
            best_score = float("-inf")
            for i in range(3):
                for j in range(3):
                    if board[i][j] == "":
                        board[i][j] = "O"
                        score = self.minimax(board, depth + 1, False)
                        board[i][j] = ""
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float("inf")
            for i in range(3):
                for j in range(3):
                    if board[i][j] == "":
                        board[i][j] = "X"
                        score = self.minimax(board, depth + 1, True)
                        board[i][j] = ""
                        best_score = min(score, best_score)
            return best_score

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
