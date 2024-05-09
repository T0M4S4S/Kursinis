import pygame
import sys
import csv
import os

# Constants
WIDTH, HEIGHT = 400, 400
LINE_WIDTH = 5
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Define button parameters
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
BUTTON_MARGIN = 20
PLAY_BUTTON_POS = (WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 - BUTTON_HEIGHT - BUTTON_MARGIN)
LEADERBOARD_BUTTON_POS = (WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 + BUTTON_MARGIN)

class Model:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.board = [['' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
            self.player = 'X'
            self.winner = None
            self.initialized = True

    def reset_board(self):
        self.board = [['' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
        self.player = 'X'
        self.winner = None

    def make_move(self, row, col):
        if self.board[row][col] == '' and not self.winner:
            self.board[row][col] = self.player
            if self.player == 'X':
                self.player = 'O'
            else:
                self.player = 'X'
            self.check_winner()

    def check_winner(self):
        for row in self.board:
            if row[0] == row[1] == row[2] != '':
                self.winner = row[0]
        for col in range(BOARD_COLS):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != '':
                self.winner = self.board[0][col]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            self.winner = self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            self.winner = self.board[0][2]
        draw = True
        for row in self.board:
            if '' in row:
                draw = False
                break
        if draw:
            self.winner = 'draw'

class View:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tic Tac Toe")
        self.font = pygame.font.SysFont(None, 30)
        self.game_started = False
        self.pradzios_image = pygame.image.load("pradzios.png")

    def create_button(self, text, position):
        button_rect = pygame.Rect(position[0], position[1], BUTTON_WIDTH, BUTTON_HEIGHT)
        pygame.draw.rect(self.screen, WHITE, button_rect)
        pygame.draw.rect(self.screen, BLACK, button_rect, 2)
        button_text = self.font.render(text, True, BLACK)
        text_rect = button_text.get_rect(center=button_rect.center)
        self.screen.blit(button_text, text_rect)
        return button_rect

    def draw_buttons(self):
        if not self.game_started:
            play_button_rect = self.create_button("Play", PLAY_BUTTON_POS)
            leaderboard_button_rect = self.create_button("Leaderboard", LEADERBOARD_BUTTON_POS)
            return play_button_rect, leaderboard_button_rect

    def draw_board(self, board):
        self.screen.fill(BLACK)
        for i in range(1, BOARD_ROWS):
            pygame.draw.line(self.screen, WHITE, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)
        for i in range(1, BOARD_COLS):
            pygame.draw.line(self.screen, WHITE, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == 'X':
                    self.draw_X(row, col)
                elif board[row][col] == 'O':
                    self.draw_O(row, col)

    def draw_X(self, row, col):
        center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
        center_y = row * SQUARE_SIZE + SQUARE_SIZE // 2
        pygame.draw.line(self.screen, RED, (center_x - SQUARE_SIZE // 3, center_y - SQUARE_SIZE // 3),
                         (center_x + SQUARE_SIZE // 3, center_y + SQUARE_SIZE // 3), 3)
        pygame.draw.line(self.screen, RED, (center_x - SQUARE_SIZE // 3, center_y + SQUARE_SIZE // 3),
                         (center_x + SQUARE_SIZE // 3, center_y - SQUARE_SIZE // 3), 3)

    def draw_O(self, row, col):
        center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
        center_y = row * SQUARE_SIZE + SQUARE_SIZE // 2
        pygame.draw.circle(self.screen, BLUE, (center_x, center_y), SQUARE_SIZE // 3, 3)

    def draw_winner(self, winner):
        if winner:
            if winner == 'draw':
                text = self.font.render("It's a draw!", True, WHITE)
            else:
                text = self.font.render(f"Player {winner} wins!", True, WHITE)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(text, text_rect)

    def draw_pradzios_image(self):
        if not self.game_started:
            self.screen.blit(self.pradzios_image, (0, 0))

    def update(self):
        pygame.display.update()

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.game_started = False
        self.leaderboard_file = "leaderboard.csv"

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if PLAY_BUTTON_POS[0] < mouse_x < PLAY_BUTTON_POS[0] + BUTTON_WIDTH and \
                        PLAY_BUTTON_POS[1] < mouse_y < PLAY_BUTTON_POS[1] + BUTTON_HEIGHT:
                    self.model.reset_board()
                    self.view.game_started = True
                    self.view.draw_board(self.model.board)

                elif LEADERBOARD_BUTTON_POS[0] < mouse_x < LEADERBOARD_BUTTON_POS[0] + BUTTON_WIDTH and \
                        LEADERBOARD_BUTTON_POS[1] < mouse_y < LEADERBOARD_BUTTON_POS[1] + BUTTON_HEIGHT:
                    self.show_leaderboard()

                elif self.view.game_started:
                    clicked_row = mouse_y // SQUARE_SIZE
                    clicked_col = mouse_x // SQUARE_SIZE
                    self.model.make_move(clicked_row, clicked_col)
                    self.view.draw_board(self.model.board)

                    if self.model.winner or self.model.winner == 'draw':
                        self.update_leaderboard()
                        self.view.draw_winner(self.model.winner)
                        self.view.game_started = False  # Stop the game

    def show_leaderboard(self):
        if not os.path.exists(self.leaderboard_file):
            print("Leaderboard file not found.")
            return

        with open(self.leaderboard_file, 'r') as file:
            reader = csv.DictReader(file)
            leaderboard_data = list(reader)

        x_wins = sum(1 for row in leaderboard_data if row['Winner'] == 'X')
        o_wins = sum(1 for row in leaderboard_data if row['Winner'] == 'O')
        draws = sum(1 for row in leaderboard_data if row['Winner'] == 'draw')

        leaderboard_text = f"X Wins: {x_wins}, O Wins: {o_wins}, Draws: {draws}"
        print(leaderboard_text)

    def update_leaderboard(self):
        if not os.path.exists(self.leaderboard_file):
            with open(self.leaderboard_file, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['Winner'])
                writer.writeheader()

        with open(self.leaderboard_file, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['Winner'])
            writer.writerow({'Winner': self.model.winner})

def main():
    pygame.init()
    model = Model()
    view = View()
    controller = Controller(model, view)

    while True:
        view.draw_pradzios_image()
        view.draw_buttons()
        controller.handle_events()
        view.update()

if __name__ == "__main__":
    main()
