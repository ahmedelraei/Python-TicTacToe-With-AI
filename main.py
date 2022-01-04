import pygame
import sys

pygame.font.init()
class Board:
    player = 'X'
    #SCORES = {'X': 1, 'O': -1, 'tie': 0}

    grid = [[' ' for x in range(3)] for y in range(3)]
 
    def __init__(self, win, win_size):
        self.win = win
        self.width = win_size[0]
        self.height = win_size[1]
        self.cells = [[Cell(self.grid[i][j], win_size, (i, j)) for j in range(3)] for i in range(3)]
        self.is_maximizing = False

    def draw(self):
        i = 1
        gap = self.width / 3
        while (i * gap) < 720:
            pygame.draw.line(self.win, (0, 0, 0), pygame.Vector2(i * gap, 0), pygame.Vector2(i * gap, 450), 5)
            pygame.draw.line(self.win, (0, 0, 0), pygame.Vector2(0, i * gap), pygame.Vector2(450, i * gap), 5)
            i += 1
        
        for i in range(3):
            for j in range(3):
                self.cells[i][j].draw(self.win)

 
    def insert(self, pos, player):
        if self.cells[pos[0]][pos[1]].value == None:
            self.cells[pos[0]][pos[1]].value = player
            self.player = 'X' if self.player == 'O' else 'O'
    
    def wins(self, le):
        return ((self.cells[0][0].value == le and self.cells[1][0].value == le and self.cells[2][0].value == le) or # across the top
        (self.cells[0][1].value == le and self.cells[1][1].value == le and self.cells[2][1].value == le) or # across the middle
        (self.cells[0][2].value == le and self.cells[1][2].value == le and self.cells[2][2].value == le) or # across the bottom
        (self.cells[0][0].value == le and self.cells[1][1].value == le and self.cells[2][2].value == le) or # diagonal
        (self.cells[1][0].value == le and self.cells[1][1].value == le and self.cells[1][2].value == le) or # down the middle
        (self.cells[2][0].value == le and self.cells[1][1].value == le and self.cells[0][2].value == le) or # diagonal
        (self.cells[0][0].value == le and self.cells[0][1].value == le and self.cells[0][2].value == le) or # Left side
        (self.cells[2][0].value == le and self.cells[2][1].value == le and self.cells[2][2].value == le)) # right side
    
    def check_winner(self):
        winner = self.is_winner(self.player)
        if winner == 'X':
            return self.SCORES['X']
        elif winner == 'O':
            return self.SCORES['O']
        else:
            return self.SCORES['tie']

    

    def minimax(self):
        if self.wins('X'):
            return (1, (0,0))
        elif self.wins('O'):
            return (-1, (0,0))

        if self.is_maximizing:
            best_score = float('-inf')
            best_move = (0,0)
            for i in range(0, 3):
                for j in range(0, 3):
                    if(self.cells[i][j].value == None):
                        self.cells[i][j].value = 'X'
                        self.is_maximizing = False
                        score = self.minimax()[0]
                        self.cells[i][j].value = None
                        if(score > best_score):
                            best_score = score
                            best_move = (i,j)
            return (best_score, best_move)

        else:
            best_score = float('inf')
            best_move = (0,0)
            for i in range(0, 3):
                for j in range(0, 3):
                    if(self.cells[i][j].value == None):
                        self.cells[i][j].value = 'X'
                        self.is_maximizing = True
                        score = self.minimax()[0]
                        self.cells[i][j].value = None
                        if(score < best_score):
                            best_score = score
                            best_move = (i,j)
            return (best_score, best_move)     
 
 
class Cell:
    def __init__(self, grid, win_size, pos):
        self.grid = grid
        self.value = None
        self.win_size = win_size
        self.pos = pos
 
    def draw(self, win):
        gap = self.win_size[0] / 3
        font = pygame.font.SysFont(None, 200)
        char = font.render(self.value, True, (0, 0, 0))
        win.blit(char, pygame.Vector2(self.pos[0] * gap  + (gap/2 - char.get_width()/2), self.pos[1] * gap + (gap/2 - char.get_width()/2)))    
 
 
def redraw_window(win, board):
    win.fill((255,255,255))
    board.draw()
 
 
def main():
    global PLAYERS, current_player
    WIN_SIZE = 450, 450
    gap = WIN_SIZE[0] / 3
    win = pygame.display.set_mode(WIN_SIZE)
    pygame.display.set_caption('Tic Tac Toe')
    board= Board(win ,WIN_SIZE)
    gameover = False
    #icon = pygame.image.load(resource_path('icon.png'))
    #pygame.display.set_icon(icon)
 
    while 1:
        if board.player == 'X':
            move = board.minimax()[1]
            board.insert((move[0],move[1]), 'X')
            board.player = 'O'

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and board.player == 'O' and not gameover:
                board.insert((int(event.pos[0] // gap), int(event.pos[1] // gap)), 'O')
                    

 
        redraw_window(win, board)
        pygame.display.update()
 
if __name__ == '__main__':
    main()
    pygame.quit()