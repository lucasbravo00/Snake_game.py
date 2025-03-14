import pygame
import random
import json
import os
import time
import sys

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Constants
GRID_SIZE = 20
GRID_WIDTH = 40  # Number of horizontal cells
GRID_HEIGHT = 27  # Number of vertical cells
GAME_WIDTH = GRID_WIDTH * GRID_SIZE  # 800 pixels
GAME_HEIGHT = GRID_HEIGHT * GRID_SIZE  # 540 pixels
INFO_HEIGHT = 50  # Fixed height for information area
WIDTH = GAME_WIDTH  # 800 pixels
HEIGHT = GAME_HEIGHT + INFO_HEIGHT  # 590 pixels
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DARK_GREEN = (0, 155, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
SNAKE_COLOR = (50, 205, 50)
FOOD_COLOR = (255, 50, 50)
BG_COLOR = (10, 20, 30)

# Set up clock to control game speed
clock = pygame.time.Clock()

# Window configuration
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")


# Load sounds
def load_sound(filename):
    try:
        sound_path = os.path.join("sounds", filename)
        return pygame.mixer.Sound(sound_path)
    except:
        return pygame.mixer.Sound(buffer=bytes(1024))


# Load sounds
eat_sound = load_sound("eat.wav")
game_over_sound = load_sound("game_over.wav")

# Adjust volume of sound effects
eat_sound.set_volume(0.7)
game_over_sound.set_volume(0.8)

# Load or create fonts
try:
    font_large = pygame.font.Font(None, 74)
    font_medium = pygame.font.Font(None, 48)
    font_small = pygame.font.Font(None, 36)
except:
    print("Error loading fonts")
    font_large = pygame.font.SysFont('arial', 74)
    font_medium = pygame.font.SysFont('arial', 48)
    font_small = pygame.font.SysFont('arial', 36)


# Snake Class
class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.length = 1
        self.positions = [((GRID_WIDTH // 2) * GRID_SIZE, (GRID_HEIGHT // 2) * GRID_SIZE)]
        self.direction = random.choice([pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT])
        self.color = SNAKE_COLOR
        self.score = 0
        self.direction_changed = False  # New variable to control direction changes

    def get_head_position(self):
        return self.positions[0]

    def change_direction(self, new_direction):
        if self.direction_changed:  # If direction already changed in this cycle, ignore
            return

        if new_direction == pygame.K_UP and self.direction != pygame.K_DOWN:
            self.direction = new_direction
            self.direction_changed = True
        elif new_direction == pygame.K_DOWN and self.direction != pygame.K_UP:
            self.direction = new_direction
            self.direction_changed = True
        elif new_direction == pygame.K_LEFT and self.direction != pygame.K_RIGHT:
            self.direction = new_direction
            self.direction_changed = True
        elif new_direction == pygame.K_RIGHT and self.direction != pygame.K_LEFT:
            self.direction = new_direction
            self.direction_changed = True

    def move(self):
        head = self.get_head_position()

        if self.direction == pygame.K_UP:
            new_head = (head[0], head[1] - GRID_SIZE)
        elif self.direction == pygame.K_DOWN:
            new_head = (head[0], head[1] + GRID_SIZE)
        elif self.direction == pygame.K_LEFT:
            new_head = (head[0] - GRID_SIZE, head[1])
        elif self.direction == pygame.K_RIGHT:
            new_head = (head[0] + GRID_SIZE, head[1])

        # Check collision with borders
        if (new_head[0] < 0 or new_head[0] >= GAME_WIDTH or
                new_head[1] < 0 or new_head[1] >= GAME_HEIGHT):
            return True  # Game over

        # Check collision with body
        if new_head in self.positions[1:]:
            return True  # Game over

        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

        # Reset direction change flag after moving
        self.direction_changed = False

        return False  # Game not over

    def draw(self, surface):
        for i, p in enumerate(self.positions):
            # Gradient color for the snake
            color_intensity = 255 - (i * 2) % 155
            segment_color = (0, color_intensity, 50)

            # Draw segment with rounded borders
            pygame.draw.rect(surface, segment_color, pygame.Rect(p[0], p[1], GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, WHITE, pygame.Rect(p[0], p[1], GRID_SIZE, GRID_SIZE), 1)

            # Draw eyes on the head
            if i == 0:
                # Calculate eye position based on direction
                eye_size = GRID_SIZE // 5
                eye_offset = GRID_SIZE // 4

                if self.direction == pygame.K_UP:
                    left_eye = (p[0] + eye_offset, p[1] + eye_offset)
                    right_eye = (p[0] + GRID_SIZE - eye_offset - eye_size, p[1] + eye_offset)
                elif self.direction == pygame.K_DOWN:
                    left_eye = (p[0] + GRID_SIZE - eye_offset - eye_size, p[1] + GRID_SIZE - eye_offset - eye_size)
                    right_eye = (p[0] + eye_offset, p[1] + GRID_SIZE - eye_offset - eye_size)
                elif self.direction == pygame.K_LEFT:
                    left_eye = (p[0] + eye_offset, p[1] + eye_offset)
                    right_eye = (p[0] + eye_offset, p[1] + GRID_SIZE - eye_offset - eye_size)
                else:  # pygame.K_RIGHT
                    left_eye = (p[0] + GRID_SIZE - eye_offset - eye_size, p[1] + eye_offset)
                    right_eye = (p[0] + GRID_SIZE - eye_offset - eye_size, p[1] + GRID_SIZE - eye_offset - eye_size)

                pygame.draw.rect(surface, BLACK, pygame.Rect(left_eye[0], left_eye[1], eye_size, eye_size))
                pygame.draw.rect(surface, BLACK, pygame.Rect(right_eye[0], right_eye[1], eye_size, eye_size))

    def get_score(self):
        return self.score

    def add_score(self):
        self.score += 1


# Food Class
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = FOOD_COLOR
        self.randomize_position()

    def randomize_position(self):
        self.position = (
            random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self, surface):
        # Draw food with attractive appearance
        rect = pygame.Rect(self.position[0], self.position[1], GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, RED, rect, 1)

        # Draw highlight
        highlight_size = GRID_SIZE // 3
        highlight_pos = (self.position[0] + highlight_size, self.position[1] + highlight_size)
        pygame.draw.rect(surface, WHITE, pygame.Rect(highlight_pos[0], highlight_pos[1], 2, 2))


# Function to draw background grid
def draw_grid(surface):
    for y in range(0, GAME_HEIGHT, GRID_SIZE):
        for x in range(0, GAME_WIDTH, GRID_SIZE):
            rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, (40, 40, 40), rect, 1)


# Function to save/load highscores
def save_high_scores(scores):
    with open("high_scores.json", "w") as f:
        json.dump(scores, f)


def load_high_scores():
    try:
        with open("high_scores.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


# Function to get text input
def get_player_name():
    screen.fill(BG_COLOR)

    title = font_large.render("SNAKE GAME", True, GREEN)
    prompt = font_medium.render("Enter your name:", True, WHITE)
    instruction = font_small.render("Press ENTER to confirm", True, YELLOW)

    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
    screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(instruction, (WIDTH // 2 - instruction.get_width() // 2, HEIGHT // 2 + 100))

    pygame.display.flip()

    # Initial configuration
    input_box = pygame.Rect(WIDTH // 2 - 140, HEIGHT // 2, 280, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = True
    text = ''
    font = pygame.font.Font(None, 42)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                active = input_box.collidepoint(event.pos)
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        # If name is empty, use "Player"
                        if text.strip() == '':
                            return "Player"
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        # Limit length to 12 characters
                        if len(text) < 12:
                            text += event.unicode

        # Draw text box
        pygame.draw.rect(screen, BG_COLOR, input_box)
        pygame.draw.rect(screen, color, input_box, 2)

        # Render text
        text_surface = font.render(text, True, WHITE)
        screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))

        pygame.display.flip()
        clock.tick(FPS)


# Function to ask if player wants to change name
def ask_change_name():
    screen.fill(BG_COLOR)

    question = font_medium.render("Do you want to change your name?", True, WHITE)
    option_yes = font_small.render("Press Y to change", True, GREEN)
    option_no = font_small.render("Press N to keep", True, RED)

    screen.blit(question, (WIDTH // 2 - question.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(option_yes, (WIDTH // 2 - option_yes.get_width() // 2, HEIGHT // 2 + 20))
    screen.blit(option_no, (WIDTH // 2 - option_no.get_width() // 2, HEIGHT // 2 + 60))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True
                elif event.key == pygame.K_n:
                    return False
        clock.tick(FPS)


# Function to show start screen
def show_start_screen():
    screen.fill(BG_COLOR)

    # Load and play background music
    try:
        pygame.mixer.music.load(os.path.join("sounds", "background.mp3"))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
    except:
        pass

    title = font_large.render("SNAKE GAME", True, GREEN)
    subtitle = font_medium.render("Press SPACE to start", True, WHITE)

    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
    screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, HEIGHT // 2))

    # Draw decorative snake
    snake_icon_size = 15
    for i in range(10):
        x = WIDTH // 2 - (i * snake_icon_size) - 50
        y = HEIGHT * 3 // 4
        color = (0, 200 - i * 15, 0)
        pygame.draw.rect(screen, color, (x, y, snake_icon_size, snake_icon_size))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return False
        clock.tick(FPS)

    return True


# Function to show game over screen
def show_game_over_screen(score, player_name):
    # Stop background music and play game over sound
    pygame.mixer.music.stop()
    game_over_sound.play()

    # Add a 1 second delay so game over sound can be heard
    pygame.time.delay(1000)

    # Load old highscores and update
    high_scores = load_high_scores()

    # Convert old format (integers) to new format (dictionaries)
    new_high_scores = []
    for item in high_scores:
        if isinstance(item, int):
            # Old format (score only)
            new_high_scores.append({"name": "Player", "score": item})
        elif isinstance(item, dict) and "score" in item and "name" in item:
            # New format (name and score)
            new_high_scores.append(item)
        # Ignore other incorrect formats

    # Add new record with name and score
    new_high_scores.append({"name": player_name, "score": score})

    # Sort by score (highest to lowest)
    new_high_scores = sorted(new_high_scores, key=lambda x: x["score"], reverse=True)
    new_high_scores = new_high_scores[:5]  # Keep only the top 5

    # Save the new format
    save_high_scores(new_high_scores)
    high_scores = new_high_scores

    screen.fill(BG_COLOR)

    game_over_text = font_large.render("GAME OVER", True, RED)
    score_text = font_medium.render(f"Score: {score}", True, WHITE)
    player_text = font_medium.render(f"Player: {player_name}", True, GREEN)
    instruction_text = font_small.render("Press SPACE to play again or ESC to exit", True, WHITE)

    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 6))
    screen.blit(player_text, (WIDTH // 2 - player_text.get_width() // 2, HEIGHT // 3 - 50))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 3))
    screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT * 4 // 5))

    # Show highscores
    high_score_title = font_medium.render("HIGHSCORES", True, YELLOW)
    screen.blit(high_score_title, (WIDTH // 2 - high_score_title.get_width() // 2, HEIGHT // 2 - 30))

    # Play highscore music
    try:
        pygame.mixer.music.load(os.path.join("sounds", "highscore.mp3"))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(0)  # Play only once
    except:
        pass

    for i, entry in enumerate(high_scores):
        y_pos = HEIGHT // 2 + 30 + i * 30
        # Highlight current score if it's in the table (only with green color)
        if entry["score"] == score and entry["name"] == player_name and high_scores.index(entry) == i:
            hs_text = font_small.render(f"{i + 1}. {entry['name']}: {entry['score']}", True, GREEN)
        else:
            hs_text = font_small.render(f"{i + 1}. {entry['name']}: {entry['score']}", True, WHITE)
        screen.blit(hs_text, (WIDTH // 2 - 100, y_pos))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                    pygame.mixer.music.stop()
                    return True
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return False
        clock.tick(FPS)


def main():
    # Get player name
    player_name = get_player_name()

    # Show start screen
    if not show_start_screen():
        return

    snake = Snake()
    food = Food()

    game_over = False

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if not game_over:
                    if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                        snake.change_direction(event.key)

        if not game_over:
            # Move snake
            game_over = snake.move()

            # Check if snake has eaten
            if snake.get_head_position() == food.position:
                snake.length += 1
                snake.add_score()
                food.randomize_position()
                eat_sound.play()

                # Make sure food doesn't appear on snake
                while food.position in snake.positions:
                    food.randomize_position()

            # Draw
            screen.fill(BG_COLOR)

            # Draw dividing line between game area and info area
            pygame.draw.line(screen, WHITE, (0, GAME_HEIGHT), (WIDTH, GAME_HEIGHT), 3)

            # Draw game area
            draw_grid(screen)
            snake.draw(screen)
            food.draw(screen)

            # Draw information area
            score_text = font_small.render(f"Score: {snake.get_score()}", True, WHITE)
            screen.blit(score_text, (
                WIDTH // 2 - score_text.get_width() // 2,
                GAME_HEIGHT + INFO_HEIGHT // 2 - score_text.get_height() // 2))

            pygame.display.flip()
            clock.tick(FPS)

        if game_over:
            # Show game over screen and ask if player wants to play again
            play_again = show_game_over_screen(snake.get_score(), player_name)
            if play_again:
                # Ask if player wants to change name
                change_name = ask_change_name()
                if change_name:
                    player_name = get_player_name()

                # Restart the game
                snake.reset()
                food.randomize_position()
                game_over = False

                # Restart background music
                try:
                    pygame.mixer.music.load(os.path.join("sounds", "background.mp3"))
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1)
                except:
                    pass
            else:
                running = False

    pygame.quit()


if __name__ == "__main__":
    main()