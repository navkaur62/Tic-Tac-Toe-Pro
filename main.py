import pygame

from src.ai import AI
from src.constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    WINDOW_TITLE,
    FPS,
    BACKGROUND_COLOR,
    WHITE,
    GRID_COLOR,
    PLAYER_X_COLOR,
    PLAYER_O_COLOR,
    ACCENT_COLOR,
    PLAYER_X,
    PLAYER_O,
    DEFAULT_DIFFICULTY,
    DIFFICULTIES,
)
from src.game import Game
from src.statistics import Statistics


# ============================================================
# BOARD SETTINGS
# ============================================================

BOARD_SIZE = 380
CELL_SIZE = BOARD_SIZE // 3

BOARD_X = (SCREEN_WIDTH - BOARD_SIZE) // 2
BOARD_Y = 175

# ============================================================
# FONTS
# ============================================================

TITLE_FONT_SIZE = 44
CELL_FONT_SIZE = 82
INFO_FONT_SIZE = 22
STATUS_FONT_SIZE = 25
CONTROL_FONT_SIZE = 17
SCORE_FONT_SIZE = 20
ROUND_FONT_SIZE = 20


# ============================================================
# UI POSITIONS
# ============================================================

TITLE_Y = 65
DIFFICULTY_Y = 115
ROUND_Y = 150
BOARD_STATUS_Y = 575
SCORE_Y = 630
CONTROL_Y = 680


# ============================================================
# DRAW TITLE
# ============================================================

def draw_title(screen, font):
    """Draw the main game title."""

    title = font.render(
        "TIC-TAC-TOE PRO",
        True,
        WHITE
    )

    rect = title.get_rect(
        center=(SCREEN_WIDTH // 2, TITLE_Y)
    )

    screen.blit(title, rect)


# ============================================================
# DRAW DIFFICULTY
# ============================================================

def draw_difficulty(screen, font, difficulty):
    """Display the current difficulty."""

    text = font.render(
        f"Difficulty: {difficulty}",
        True,
        ACCENT_COLOR
    )

    rect = text.get_rect(
        center=(SCREEN_WIDTH // 2, DIFFICULTY_Y)
    )

    screen.blit(text, rect)


# ============================================================
# DRAW ROUND INFORMATION
# ============================================================

def draw_round_info(screen, font, statistics):
    """Display the current round number."""

    round_number = statistics.get_rounds_played() + 1

    text = font.render(
        f"ROUND {round_number}",
        True,
        WHITE
    )

    rect = text.get_rect(
        center=(SCREEN_WIDTH // 2, ROUND_Y)
    )

    screen.blit(text, rect)


def draw_board(screen, game):
    """Draw the Tic-Tac-Toe board and winning-line highlight."""

    board_rect = pygame.Rect(
        BOARD_X,
        BOARD_Y,
        BOARD_SIZE,
        BOARD_SIZE
    )

    # ========================================================
    # BOARD BACKGROUND
    # ========================================================

    pygame.draw.rect(
        screen,
        (18, 18, 35),
        board_rect,
        border_radius=14
    )

    # ========================================================
    # BOARD BORDER
    # ========================================================

    pygame.draw.rect(
        screen,
        ACCENT_COLOR,
        board_rect,
        width=2,
        border_radius=14
    )

    # ========================================================
    # GRID
    # ========================================================

    for i in range(1, 3):

        x = BOARD_X + i * CELL_SIZE
        y = BOARD_Y + i * CELL_SIZE

        pygame.draw.line(
            screen,
            GRID_COLOR,
            (x, BOARD_Y),
            (x, BOARD_Y + BOARD_SIZE),
            4
        )

        pygame.draw.line(
            screen,
            GRID_COLOR,
            (BOARD_X, y),
            (BOARD_X + BOARD_SIZE, y),
            4
        )

    # ========================================================
    # PLAYER MARKS
    # ========================================================

    board_state = game.get_board_state()

    font = pygame.font.SysFont(
        "arial",
        CELL_FONT_SIZE,
        bold=True
    )

    for position, value in enumerate(board_state):

        if value == "":
            continue

        row = position // 3
        col = position % 3

        center_x = (
            BOARD_X
            + col * CELL_SIZE
            + CELL_SIZE // 2
        )

        center_y = (
            BOARD_Y
            + row * CELL_SIZE
            + CELL_SIZE // 2
        )

        if value == PLAYER_X:
            color = PLAYER_X_COLOR
        else:
            color = PLAYER_O_COLOR

        text = font.render(
            value,
            True,
            color
        )

        text_rect = text.get_rect(
            center=(center_x, center_y)
        )

        screen.blit(
            text,
            text_rect
        )

    # ========================================================
    # WINNING LINE
    # ========================================================

    if game.is_round_over and game.winning_positions:

        winning_player = game.winner

        if winning_player == PLAYER_X:
            highlight_color = PLAYER_X_COLOR
        else:
            highlight_color = PLAYER_O_COLOR

        first_position = game.winning_positions[0]
        last_position = game.winning_positions[-1]

        first_row = first_position // 3
        first_col = first_position % 3

        last_row = last_position // 3
        last_col = last_position % 3

        start_x = (
            BOARD_X
            + first_col * CELL_SIZE
            + CELL_SIZE // 2
        )

        start_y = (
            BOARD_Y
            + first_row * CELL_SIZE
            + CELL_SIZE // 2
        )

        end_x = (
            BOARD_X
            + last_col * CELL_SIZE
            + CELL_SIZE // 2
        )

        end_y = (
            BOARD_Y
            + last_row * CELL_SIZE
            + CELL_SIZE // 2
        )

        pygame.draw.line(
            screen,
            highlight_color,
            (start_x, start_y),
            (end_x, end_y),
            8
        )
# ============================================================
# DRAW GAME STATUS
# ============================================================

def draw_status(screen, font, game):
    """Display winner, draw, or current turn."""

    if game.is_round_over:

        if game.winner:

            if game.winner == PLAYER_X:
                message = "YOU WIN!"
                color = PLAYER_X_COLOR
            else:
                message = "AI WINS!"
                color = PLAYER_O_COLOR

        else:
            message = "DRAW!"
            color = WHITE

    else:

        if game.get_current_player() == PLAYER_X:
            message = "YOUR TURN - X"
            color = PLAYER_X_COLOR
        else:
            message = "AI TURN - O"
            color = PLAYER_O_COLOR

    text = font.render(
        message,
        True,
        color
    )

    rect = text.get_rect(
        center=(SCREEN_WIDTH // 2, BOARD_STATUS_Y)
    )

    screen.blit(
        text,
        rect
    )


# ============================================================
# DRAW SCOREBOARD
# ============================================================

def draw_scoreboard(screen, statistics, font):
    """Draw the match scoreboard."""

    scoreboard_width = 430
    scoreboard_height = 50

    scoreboard_x = (
        SCREEN_WIDTH - scoreboard_width
    ) // 2

    scoreboard_y = 610

    rect = pygame.Rect(
        scoreboard_x,
        scoreboard_y,
        scoreboard_width,
        scoreboard_height
    )

    pygame.draw.rect(
        screen,
        (18, 18, 35),
        rect,
        border_radius=12
    )

    pygame.draw.rect(
        screen,
        GRID_COLOR,
        rect,
        width=2,
        border_radius=12
    )

    player_text = font.render(
        f"YOU  {statistics.get_player_wins()}",
        True,
        PLAYER_X_COLOR
    )

    ai_text = font.render(
        f"AI  {statistics.get_ai_wins()}",
        True,
        PLAYER_O_COLOR
    )

    draw_text = font.render(
        f"DRAWS  {statistics.get_draws()}",
        True,
        WHITE
    )

    player_rect = player_text.get_rect(
        center=(
            scoreboard_x + 75,
            scoreboard_y + scoreboard_height // 2
        )
    )

    ai_rect = ai_text.get_rect(
        center=(
            scoreboard_x + 215,
            scoreboard_y + scoreboard_height // 2
        )
    )

    draw_rect = draw_text.get_rect(
        center=(
            scoreboard_x + 350,
            scoreboard_y + scoreboard_height // 2
        )
    )

    screen.blit(player_text, player_rect)
    screen.blit(ai_text, ai_rect)
    screen.blit(draw_text, draw_rect)


# ============================================================
# DRAW CONTROLS
# ============================================================

def draw_controls(screen, font):
    """Display keyboard controls."""

    text = font.render(
        "1 Easy    2 Medium    3 Hard    |    "
        "R Restart    ESC Exit",
        True,
        (170, 170, 185)
    )

    rect = text.get_rect(
        center=(SCREEN_WIDTH // 2, CONTROL_Y)
    )

    screen.blit(
        text,
        rect
    )


# ============================================================
# MAIN
# ============================================================

def main():

    pygame.init()

    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT)
    )

    pygame.display.set_caption(
        WINDOW_TITLE
    )

    clock = pygame.time.Clock()

    title_font = pygame.font.SysFont(
        "arial",
        TITLE_FONT_SIZE,
        bold=True
    )

    info_font = pygame.font.SysFont(
        "arial",
        INFO_FONT_SIZE,
        bold=True
    )

    status_font = pygame.font.SysFont(
        "arial",
        STATUS_FONT_SIZE,
        bold=True
    )

    control_font = pygame.font.SysFont(
        "arial",
        CONTROL_FONT_SIZE
    )

    score_font = pygame.font.SysFont(
        "arial",
        SCORE_FONT_SIZE,
        bold=True
    )

    round_font = pygame.font.SysFont(
        "arial",
        ROUND_FONT_SIZE,
        bold=True
    )

    game = Game()
    statistics = Statistics()

    result_recorded = False

    difficulty_index = DIFFICULTIES.index(
        DEFAULT_DIFFICULTY
    )

    difficulty = DIFFICULTIES[
        difficulty_index
    ]

    ai = AI(difficulty)

    running = True

    while running:

        # ====================================================
        # EVENTS
        # ====================================================

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            # ------------------------------------------------
            # Mouse
            # ------------------------------------------------

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if (
                    event.button == 1
                    and not game.is_round_over
                    and game.get_current_player() == PLAYER_X
                ):

                    mouse_x, mouse_y = event.pos

                    if (
                        BOARD_X <= mouse_x <= BOARD_X + BOARD_SIZE
                        and
                        BOARD_Y <= mouse_y <= BOARD_Y + BOARD_SIZE
                    ):

                        col = (
                            mouse_x - BOARD_X
                        ) // CELL_SIZE

                        row = (
                            mouse_y - BOARD_Y
                        ) // CELL_SIZE

                        position = row * 3 + col

                        game.make_move(position)

            # ------------------------------------------------
            # Keyboard
            # ------------------------------------------------

            elif event.type == pygame.KEYDOWN:

                # Restart round
                if event.key == pygame.K_r:

                    game.reset_round()

                    result_recorded = False

                # Cycle difficulty
                elif event.key == pygame.K_d:

                    difficulty_index = (
                        difficulty_index + 1
                    ) % len(DIFFICULTIES)

                    difficulty = (
                        DIFFICULTIES[
                            difficulty_index
                        ]
                    )

                    ai.set_difficulty(
                        difficulty
                    )

                    game.reset_round()

                    result_recorded = False

                # Easy
                elif event.key == pygame.K_1:

                    difficulty = "EASY"

                    ai.set_difficulty(
                        difficulty
                    )

                    game.reset_round()

                    result_recorded = False

                # Medium
                elif event.key == pygame.K_2:

                    difficulty = "MEDIUM"

                    ai.set_difficulty(
                        difficulty
                    )

                    game.reset_round()

                    result_recorded = False

                # Hard
                elif event.key == pygame.K_3:

                    difficulty = "HARD"

                    ai.set_difficulty(
                        difficulty
                    )

                    game.reset_round()

                    result_recorded = False

                # Exit
                elif event.key == pygame.K_ESCAPE:
                    running = False

        # ====================================================
        # AI TURN
        # ====================================================

        if (
            not game.is_round_over
            and game.get_current_player() == PLAYER_O
        ):

            ai_move = ai.get_move(
                game.board
            )

            if ai_move is not None:
                game.make_move(ai_move)

        # ====================================================
        # RECORD RESULT
        # ====================================================

        if (
            game.is_round_over
            and not result_recorded
        ):

            statistics.record_result(
                game.get_winner()
            )

            result_recorded = True

        # ====================================================
        # DRAW
        # ====================================================

        screen.fill(
            BACKGROUND_COLOR
        )

        draw_title(
            screen,
            title_font
        )

        draw_difficulty(
            screen,
            info_font,
            difficulty
        )

        draw_round_info(
            screen,
            round_font,
            statistics
        )

        draw_board(
            screen,
            game
        )

        draw_status(
            screen,
            status_font,
            game
        )

        draw_scoreboard(
            screen,
            statistics,
            score_font
        )

        draw_controls(
            screen,
            control_font
        )

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()