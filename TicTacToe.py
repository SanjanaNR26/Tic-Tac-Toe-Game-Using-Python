import tkinter as tk
from tkinter import messagebox
import copy

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe vs Smart Computer")
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.create_board()

    def create_board(self):
        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.root, text="", font=("Helvetica", 32), width=5, height=2,
                                command=lambda row=i, col=j: self.player_move(row, col))
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

    def player_move(self, row, col):
        if self.board[row][col] == "":
            self.board[row][col] = "X"
            self.buttons[row][col].config(text="X", state="disabled")
            if self.check_winner("X"):
                self.end_game("🏆 You win!")
                return
            elif self.is_draw():
                self.end_game("🤝 It's a draw!")
                return
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
            i, j = best_move
            self.board[i][j] = "O"
            self.buttons[i][j].config(text="O", state="disabled")

            if self.check_winner("O"):
                self.end_game("😈 Computer wins!")
            elif self.is_draw():
                self.end_game("🤝 It's a draw!")

    def minimax(self, board, depth, is_maximizing):
        if self.check_winner_board(board, "O"):
            return 1
        elif self.check_winner_board(board, "X"):
            return -1
        elif self.is_draw_board(board):
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

    def check_winner(self, player):
        return self.check_winner_board(self.board, player)

    def check_winner_board(self, board, player):
        for i in range(3):
            if all(board[i][j] == player for j in range(3)) or \
               all(board[j][i] == player for j in range(3)):
                return True
        if all(board[i][i] == player for i in range(3)) or \
           all(board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def is_draw(self):
        return self.is_draw_board(self.board)

    def is_draw_board(self, board):
        return all(board[i][j] != "" for i in range(3) for j in range(3))

    def end_game(self, message):
        messagebox.showinfo("Game Over", message)
        self.reset_game()

    def reset_game(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
