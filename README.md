# Kursinis
# Atlieka: Tomas Armalis EAf-23
# Tic-Tac-Toe Game

## Description
This is a simple Tic-Tac-Toe game implemented using Pygame. It allows two players to take turns marking the spaces in a 3x3 grid with their respective symbols (X or O). The game checks for a winner after each move and displays the winner or a draw if the game ends in a tie. It also includes a leaderboard to track the number of wins for each player.

## Features
- Two-player Tic-Tac-Toe game.
- Graphical user interface implemented with Pygame.
- Leaderboard to track wins for each player.
- Play and Leaderboard buttons to navigate through the game.

## Requirements
- Python 3.x
- Pygame library

## Installation
1. Clone the repository:
2. Install Pygame library:

## Usage
1. Run the game:
2. Click the "Play" button to start a new game.
3. Click the squares on the board to make your moves.
4. The game will display the winner or a draw when the game ends.
5. Click the "Leaderboard" button to view the current leaderboard.

## Files
- `kryziukai.py`: Contains the Model, View, and Controller classes for the game.
- `pradzios.png`: Image file for the game logo.
- `leaderboard.csv`: CSV file to store the leaderboard data.

## Code analysis
- Abstraction:
  - The Model class abstracts the game logic, hiding the details of how the game state is managed.
  - The View class abstracts the display logic, encapsulating the details of drawing the game board and buttons.
  - The Controller class abstracts the event handling logic, hiding the implementation details of how user input is processed.
- Encapsulation:
  - The Model class encapsulates the game state data (board, player, winner) and methods to manipulate it (reset_board, make_move, check_winner).
  - The View class encapsulates the display logic and UI elements (buttons, board drawing).
  - The Controller class encapsulates the event handling logic and interaction between the model and view.

- In this code I am using two design patterns one of the is Singleton and Factory method. Singleton we can see here:

  
class Model:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # Initialize only if the instance is not already created
        if not hasattr(self, 'initialized'):
            self.board = [['' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
            self.player = 'X'
            self.winner = None
            self.initialized = True

            
And the factory method is herte:


class View:

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
  
- The reading and writing I did when I save the winner in leaderboard and I can read winners history from leaderboard.
## Summary
- Writing this code was a really good experience, but I faced a lot of challenges.
One of the biggest achievements is that we can see the main board, we can draw X's and O's on the board.

Improvements: 
- It would be great to display the achievement history on the home screen.
- Implement a feature to determine the winner at the end of each game.
