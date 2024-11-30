import pygame, sys
from constants import *

class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.sketched_value = 0
        self.row = row
        self.col = col
        self.selected = False
        self.screen = screen
        self.font = pygame.font.Font(None, NUMBER_FONT_SIZE)

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    def draw(self):
        x = self.col * SQUARE_SIZE
        y = self.row * SQUARE_SIZE

        if self.selected:
            color = HIGHLIGHT_COLOR
        else:
            color = LINE_COLOR
        pygame.draw.rect(self.screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE), LINE_WIDTH)

        if self.value != 0:
            text = str(self.value)
            text_surface = self.font.render(text, True, FILLED_NUMBER_COLOR)
            text_rect = text_surface.get_rect(center=(x + SQUARE_SIZE // 2, y + SQUARE_SIZE // 2))
            self.screen.blit(text_surface, text_rect)
        elif self.sketched_value != 0:
            text = str(self.sketched_value)
            text_surface = self.font.render(text, True, TEXT_COLOR)
            text_rect = text_surface.get_rect(topleft=(x + 5, y + 5))
            self.screen.blit(text_surface, text_rect)

class Board:
    def __init__(self, board, width, height, screen, difficulty):
        self.board = board
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.cells = []
        for r in range(9):
            row = []
            for c in range(9):
                row.append(Cell(0, r, c, screen))
            self.cells.append(row)
        self.selected_cell = None

    def draw(self):
        for i in range(1, 9):
            if i % 3 == 0:
                thickness = BOLD_LINE_WIDTH
            else:
                thickness = LINE_WIDTH
            pygame.draw.line(self.screen, LINE_COLOR, (0, i * SQUARE_SIZE), (self.width, i * SQUARE_SIZE), thickness)
            pygame.draw.line(self.screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, self.height), thickness)

        for row in self.cells:
            for cell in row:
                cell.draw()

    def select(self, row, col):
        if self.selected_cell is not None:
            self.selected_cell.selected = False
        self.selected_cell = self.cells[row][col]
        self.selected_cell.selected = True

    def click(self, x, y):
        if x >= self.width or y >= self.height:
            return None
        row = y // SQUARE_SIZE
        col = x // SQUARE_SIZE
        return row, col

    def clear(self):
        if self.selected_cell is not None:
            if self.selected_cell.value == 0:
                self.selected_cell.sketched_value = 0

    def sketch(self, value):
        if self.selected_cell is not None:
            if self.selected_cell.value == 0:
                self.selected_cell.sketched_value = value

    def place_number(self, value):
        if self.selected_cell is not None:
            if self.selected_cell.value == 0:
                self.selected_cell.value = value
                self.selected_cell.sketched_value = 0

    def reset_to_original(self):
        for row in self.cells:
            for cell in row:
                if cell.value == 0:
                    cell.sketched_value = 0

    def is_full(self):
        for row in self.cells:
            for cell in row:
                if cell.value == 0:
                    return False
        return True

    def update_board(self):
        new_board = []
        for row in self.cells:
            new_row = []
            for cell in row:
                new_row.append(cell.value)
            new_board.append(new_row)
        self.board = new_board

    def find_empty(self):
        for row in self.cells:
            for cell in row:
                if cell.value == 0:
                    return cell.row, cell.col
        return None

    def check_board(self):
        for row in self.cells:
            values = [cell.value for cell in row if cell.value != 0]
            if len(values) != len(set(values)):
                return False

        for col in range(9):
            values = [self.cells[row][col].value for row in range(9) if self.cells[row][col].value != 0]
            if len(values) != len(set(values)):
                return False

        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                values = [
                    self.cells[r][c].value
                    for r in range(box_row, box_row + 3)
                    for c in range(box_col, box_col + 3)
                    if self.cells[r][c].value != 0
                ]
                if len(values) != len(set(values)):
                    return False

        return True