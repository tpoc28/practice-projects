import pygame
import tkinter as tk
from tkinter import simpledialog
import os
pygame.init()

WIDTH = 600
HEIGHT = 640
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 40

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 128, 180)
GREY = (128, 128, 128)
LIGHT_GREY = (225, 225, 225)
FPS = 60

FONT = pygame.font.SysFont(None, size=48)
GAME_SPEED_FONT = pygame.font.SysFont(None, size=20)

def get_input():
    rows = simpledialog.askinteger("Conway's Game of Life", "Welcome to Conway's Game of Life!\n\nThe game is simple: initialize the board, then watch life blossom.\nIf a living tile has 2 or 3 living neighbors, that tile survives. Otherwise, it dies.\nIf a dead tile has exactly 3 living neighbors, it is revived. \n\nNow, how many rows do you want in your grid? (5-100)", minvalue=5, maxvalue=100)

    return rows

def get_clicked_pos(width, rows, pos): #returns row and col of clicked tile
    gap = width // rows
    x, y = pos

    row = x // gap
    col = y // gap

    return row, col

class Tile:
    def __init__(self, row, col, width, rows):
        self.row = row
        self.col = col
        self.x = width // rows * row
        self.y = width // rows * col
        self.gap = width // rows
        self.neighbors = []
        self.alive = False
        self.color = BLACK

    def make_alive(self, win):
        self.color = WHITE
        self.alive = True
        self.draw_tile(win)

    def make_dead(self, win):
        self.color = BLACK
        self.alive = False
        self.draw_tile(win)

    def draw_tile(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.gap, self.gap))

    def find_neighbors(self, rows): #find all neighbors and removes out of range elements
        neighbors = [[self.row - 1, self.col - 1], [self.row + 1, self.col + 1], [self.row - 1, self.col + 1], [self.row + 1, self.col - 1], [self.row, self.col - 1], [self.row - 1, self.col], [self.row + 1, self.col], [self.row, self.col + 1]]
        out_of_range = []
        for i in range(len(neighbors)):
            if neighbors[i][0] < 0 or neighbors[i][0] > rows - 1  or neighbors[i][1] < 0 or neighbors[i][1] > rows - 1:
                out_of_range.append(neighbors[i])
        for element in out_of_range:
            if element in neighbors:
                neighbors.remove(element)

        return neighbors

    def check_neighbors(self, tiles): #returns number of alive neighbors
        alive_neighbors = 0
        for i in range(len(self.neighbors)):
            neighbor_row, neighbor_col = self.neighbors[i]
            if tiles[neighbor_row][neighbor_col].alive:
                alive_neighbors += 1

        return alive_neighbors



class Button:
    def __init__(self, text, width, height, pos):
        self.x, self.y = pos
        self.top_rect = pygame.Rect(self.x, self.y, width, height)
        self.border = pygame.Rect(self.x, self.y, width, height)
        self.top_color = GREY
        self.border_color = LIGHT_GREY
        self.botton_rect = pygame.Rect(self.x, self.y, width, height)
        self.text_surf = FONT.render(text, 1, WHITE)
        self.text_rect = self.text_surf.get_rect(centerx = self.top_rect.centerx, centery = self.top_rect.centery)

    def draw(self):
        pygame.draw.rect(WIN, self.top_color, self.top_rect, border_radius=12)
        pygame.draw.rect(WIN, self.border_color, self.border,border_radius=12, width = 4)
        WIN.blit(self.text_surf,self.text_rect)

    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            clicked = True
        else:
            clicked = False
        return clicked


  
def draw_grid(win, width, rows, algo_run): #draws lines and buttons
    gap = width // rows
    pygame.display.set_caption("Conway's Game of Life")
    for i in range(rows + 1):
        tiles.append([])
        pygame.draw.line(win, GREY, (i * gap, 0), (i * gap, width))
        for j in range(rows + 1):
            pygame.draw.line(win, GREY, (0, j * gap), (width, j * gap))   
    if algo_run:
        Button.draw(stop_button)
    else:
        Button.draw(start_button)
    Button.draw(clear_button)    
    Button.draw(game_speed_button)    
    pygame.display.update()

def draw_tiles(win, width, rows): #creates tile objects
    gap = width // rows
    tiles = []
    for i in range(rows):
        tiles.append([])
        for j in range(rows):
            tile = Tile(i, j, width, rows)
            tile.draw_tile(win)
            tiles[i].append(tile)

    pygame.display.update()

    return tiles

def main(win, width, rows, tiles):
    algo_run = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            if pos[0] < (width // rows) * rows and pos[1] < (width // rows) * rows:
                row, col = get_clicked_pos(width, rows, pos)
                tile = tiles[row][col]
                if tile.alive == False:
                    tile.make_alive(WIN)             
                elif tile.alive == True:
                    tile.make_dead(WIN)
                draw_grid(win, width, rows, algo_run)
                pygame.display.update()
            elif start_button.is_clicked():
                algorithm(win, width, rows, tiles)
                algo_run = True
            elif clear_button.is_clicked():
                for row in range(rows):
                    for col in range(rows):
                        tiles[row][col].make_dead(win)
                algo_run = False
                draw_grid(win, width, rows, algo_run)
                pygame.display.update()
            elif game_speed_button.is_clicked():
                pass
            else:
                print(pos)

def algorithm(win, width, rows, tiles):  
    run = True
    alive_tiles_last_round = []
    alive_tiles = []
    dead_tiles = []
    while run:
        fps = 2
        clock.tick(fps)  
        alive_tiles_last_round = alive_tiles      
        alive_tiles = []
        dead_tiles = []
        for i in range(rows):
            for j in range(rows):
                tiles[i][j].neighbors = tiles[i][j].find_neighbors(rows)
                if (tiles[i][j].alive and tiles[i][j].check_neighbors(tiles) in range(2,4)) or (tiles[i][j].alive == False and tiles[i][j].check_neighbors(tiles) == 3):
                    alive_tiles.append(tiles[i][j])
                else:
                    dead_tiles.append(tiles[i][j])
        for alive in range(len(alive_tiles)):
            if any(alive_tiles[alive] in row_list for row_list in tiles):
                row = alive_tiles[alive].row
                col = alive_tiles[alive].col           
                tiles[row][col].make_alive(win)

        for dead in range(len(dead_tiles)):
            if any(dead_tiles[dead] in row_list for row_list in tiles):
                row = dead_tiles[dead].row
                col = dead_tiles[dead].col
                tiles[row][col].make_dead(win)
       
        run = False
        for i in range(rows):
            for j in range(rows):
                if tiles[i][j].alive:
                    run = True
        if alive_tiles_last_round == alive_tiles:
            run = False

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_button.is_clicked() and run == False:
                    run = True
                if stop_button.is_clicked() and run:
                    run = False
                    Button.draw(stop_button)
                if clear_button.is_clicked():
                    run = False
                    for row in range(rows):
                        for col in range(rows):
                            tiles[row][col].make_dead(win)

        draw_grid(win, width, rows, run)
        pygame.display.update()


rows = get_input()
if rows == None:
    run = False
else: run = True
WIDTH = min(600, (600 // rows) * rows)
HEIGHT = min(640, (600 // rows) * rows + BUTTON_HEIGHT)
BUTTON_WIDTH = min(200, (600 // rows) * rows // 3)
BUTTON_HEIGHT = 40
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WIN.fill(BLACK)
tiles = draw_tiles(WIN, WIDTH, rows)
start_button = Button('Start', BUTTON_WIDTH, BUTTON_HEIGHT, (0, WIDTH))
stop_button = Button('Stop', BUTTON_WIDTH, BUTTON_HEIGHT, (0, WIDTH))
clear_button = Button('Clear', BUTTON_WIDTH, BUTTON_HEIGHT, (BUTTON_WIDTH, WIDTH))
game_speed_button = Button("", BUTTON_WIDTH, BUTTON_HEIGHT, (2*BUTTON_WIDTH, WIDTH))
game_speed_button.text_surf =  GAME_SPEED_FONT.render("2 Generations per Second", 1, WHITE)
game_speed_button.text_rect = game_speed_button.text_surf.get_rect(centerx = game_speed_button.top_rect.centerx, centery = game_speed_button.top_rect.centery)
algo_run = False
draw_grid(WIN, WIDTH, rows, algo_run)
clock = pygame.time.Clock()
while run:
    clock.tick(FPS)
    main(WIN, WIDTH, rows, tiles)
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and start_button.is_clicked():
                run = True
                algo_run = True
    
pygame.quit()


