import copy
import time
import tkinter as tk
import random

class Game2048:
    WIDTH = 8
    HEIGHT = 8
        
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("2048 Trop coole")
        self.score = 0
        
        self.score_label = tk.Label(self.window, text="Score: 0", font=("Helvetica", 16))
        self.score_label.grid(row=0, column=0, columnspan=self.WIDTH, pady=10, sticky="n")
        
        self.grid_frame = tk.Frame(self.window)
        self.grid_frame.grid(row=1, column=0, columnspan=self.WIDTH)


        self.start_game()
        self.place_random_tile()
        self.place_random_tile()
        
        self.reload_board()

        self.window.bind("<Up>", self.move_up)
        self.window.bind("<Down>", self.move_down)
        self.window.bind("<Left>", self.move_left)
        self.window.bind("<Right>", self.move_right)

        self.window.mainloop()

    def start_game(self):
        self.tiles = []
        self.board = []
        for i in range(self.HEIGHT):
            tile_row = []
            board_row = []
            for j in range(self.WIDTH):
                tile = tk.Label(self.grid_frame, text="", width=5, height=2, font=('Arial', 20, 'bold'), relief="solid")
                tile.grid(row=i, column=j, padx=5, pady=5)
                tile_row.append(tile)
                
                board_row.append(0)
            self.tiles.append(tile_row)
            self.board.append(board_row)

        self.reload_board()

        self.window.bind("<Up>", self.move_up)
        self.window.bind("<Down>", self.move_down)
        self.window.bind("<Left>", self.move_left)
        self.window.bind("<Right>", self.move_right)

    def reload_board(self):
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                value = self.board[i][j]
                text = str(value) if value != 0 else ""
                self.tiles[i][j].configure(text=text, bg="white")
                
        self.score_label.configure(text=f"Score: {self.score}")

    def place_random_tile(self):
        empty_cells = [(i, j) for i in range(self.HEIGHT) for j in range(self.WIDTH) if self.board[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            # 32 bonus hehe
            self.board[i][j] = 32 if random.random() < 0.01 else (2 if random.random() < 0.9 else 4)

    def move(self, direction, board):
        if direction in ["Left", "Right"]:
            for i in range(self.WIDTH):
                row = []
                
                if direction == 'Left':
                    row = board[i]
                elif direction == 'Right':
                    row = board[i][::-1]
                    
                row = self.apply_move_on_row_or_col(row)
                
                if direction == 'Left':
                    board[i] = row
                elif direction == 'Right':
                    board[i] = row[::-1]
                    
        
        if direction in ["Up", "Down"]:
            for i in range(self.HEIGHT):
                col = []
                
                if direction == 'Up':
                    col = [board_row[i] for board_row in board]
                elif direction == 'Down':
                    col = [board_row[i] for board_row in board][::-1]
                    
                col = self.apply_move_on_row_or_col(col)

                if direction == 'Up':
                    for k, board_row in enumerate(board):
                        board_row[i] = col[k]
                elif direction == 'Down':
                    for k, board_row in enumerate(board):
                        board_row[i] = col[self.HEIGHT - 1 - k]
                        
        self.place_random_tile()
        self.reload_board()
        
    def apply_move_on_row_or_col(self, row_or_col):
        length = len(row_or_col)
        row_or_col = [value for value in row_or_col if value != 0]
            
        for j in range(len(row_or_col) - 1):
            if row_or_col[j] == row_or_col[j + 1]:
                row_or_col[j] = row_or_col[j] * 2
                row_or_col[j + 1] = 0
                
                self.score += row_or_col[j]
                
        row_or_col = [value for value in row_or_col if value != 0]
        row_or_col += [0] * (length - len(row_or_col))
        
        return row_or_col
    
    def handle_endgame(self):
        if self.detect_loss():
            self.open_blocking_window('T poche')
        if self.detect_win():
            self.open_blocking_window('T tro coole ta u sink çan dooz')
            
    def open_blocking_window(self, message):
        blocking_window = tk.Toplevel(self.window)
        blocking_window.title("Blocking Window")
        
        label = tk.Label(blocking_window, text=message)
        label.pack(padx=20, pady=20)
        blocking_window.protocol("WM_DELETE_WINDOW", lambda: self.window.destroy())
    
    def detect_loss(self):
        copied_board = copy.deepcopy(self.board)
        
        self.move('Up', copied_board)
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                if copied_board[i][j] != self.board[i][j]:
                    return False
                
        self.move('Down', copied_board)
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                if copied_board[i][j] != self.board[i][j]:
                    return False
                
        self.move('Left', copied_board)
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                if copied_board[i][j] != self.board[i][j]:
                    return False
                
        self.move('Right', copied_board)
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                if copied_board[i][j] != self.board[i][j]:
                    return False
                
        return True
    
    def detect_win(self):
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                if self.board[i][j] == 512: # Je suis trop poche pour 2048
                    return True
        return False
            
        

    def move_up(self, _):
        self.move('Up', self.board)
        self.handle_endgame()

    def move_down(self, _):
        self.move('Down', self.board)
        self.handle_endgame()

    def move_left(self, _):
        self.move('Left', self.board)
        self.handle_endgame()

    def move_right(self, _):
        self.move('Right', self.board)
        self.handle_endgame()


if __name__ == "__main__":
    game = Game2048()
