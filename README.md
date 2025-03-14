# Snake Game

A classic Snake game implemented in Python using Pygame.

## Description

This is a complete implementation of the classic Snake game where players control a snake that grows longer as it eats food. The game features a scoring system, customizable player names, highscore tracking, sound effects, and visual elements.

## Features

- Arrow key controls for snake movement
- Player name customization
- Top 5 highscore tracking with player names
- Sound effects and background music
- Visual feedback (snake color gradient, eyes that follow direction)
- Game over detection (wall collision, self-collision)
- Separate score display area
- Replay functionality

## Requirements

- Python 3.x
- Pygame library

## Installation

1. Make sure you have Python installed on your system. You can download it from [python.org](https://python.org).

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Clone or download this repository to your local machine.

4. Create a folder named "sounds" in the same directory as the script and add the following sound files:
   - background.mp3: Background music for gameplay
   - eat.wav: Sound effect when the snake eats food
   - game_over.wav: Sound effect when the game ends
   - highscore.mp3: Music for the highscore screen

## How to Play

1. Run the script:
   ```
   python snake_game.py
   ```

2. Enter your name when prompted.

3. Press SPACE to start the game.

4. Use the arrow keys to control the snake:
   - UP: Move up
   - DOWN: Move down
   - LEFT: Move left
   - RIGHT: Move right

5. Eat the red food to grow the snake and increase your score.

6. Avoid hitting the walls or the snake's own body.

7. When the game is over, your score will be compared to the highscores.

8. Press SPACE to play again or ESC to exit.

## Game Structure

- **Snake Class**: Handles the snake's movement, growth, and collision detection
- **Food Class**: Manages the food's appearance and position
- **High Score System**: Saves and loads player scores using JSON
- **Game Screens**: 
  - Name entry screen
  - Start screen
  - Main game
  - Game over and highscore screen

## Customization

You can easily modify the game by changing these values in the code:

- `FPS`: Controls the game speed
- `GRID_SIZE`: Changes the size of each cell
- `GRID_WIDTH` and `GRID_HEIGHT`: Adjust the number of cells in the game area
- Color constants: Modify the game's appearance

## Credits

This game was created as a learning project for Python and Pygame.

## License

Feel free to use, modify, and distribute this code for personal or educational purposes.
