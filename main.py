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


# ============================================================
# BOARD SETTINGS
# ============================================================

BOARD_SIZE = 480
CELL_SIZE = BOARD_SIZE // 3

BOARD_X = (SCREEN_WIDTH - BOARD_SIZE) // 2
BOARD_Y = 150


# ============================================================
# FONTS
# ============================================================

TITLE_FONT_SIZE = 42
CELL_FONT_SIZE = 90
INFO_FONT_SIZE = 24
BUTTON_FONT_SIZE = 20


# ============================================================
# DRAWING FUNCTIONS
# ============================================================

def draw_title(screen, font):
    """Draw the game title."""

    title = font.render(
        "TIC-TAC-TOE PRO",
        True,
        WHITE
    )

    title_rect = title.get_rect(
        center=(SCREEN_WIDTH // 2, 50)
    )

    screen.blit(title, title_rect)


def draw_difficulty(screen, font, difficulty):
    """Display the current difficulty."""

    text = font.render(
        f"Difficulty: {difficulty}",
        True,
        ACCENT_COLOR
    )

    text_rect = text.get_rect(
        center=(SCREEN_WIDTH // 2, 95)
    )

    screen.blit(text, text_rect)


def draw_board(screen, game):
    """Draw the Tic-Tac-Toe board and player marks."""

    # Draw board background.
    board_rect = pygame.Rect(
        BOARD_X,
        BOARD_Y,
        BOARD_SIZE,
        BOARD_SIZE
    )

    pygame.draw.rect(
        screen,
        (18, 18, 35),
        board_rect,
        border_radius=12
    )

    # Draw grid lines.
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

    # Draw player marks.
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

        screen.blit(text, text_rect)


def draw_status(screen, font, game, difficulty):
    """Draw the current game status."""

    if game.is_round_over:

        if game.winner:
            message = f"{game.winner} WINS!"

            if game.winner == PLAYER_X:
                color = PLAYER_X_COLOR
            else:
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

    status = font.render(
        message,
        True,
        color
    )

    status_rect = status.get_rect(
        center=(SCREEN_WIDTH // 2, 660)
    )

    screen.blit(status, status_rect)

    difficulty_text = font.render(
        f"Mode: {difficulty}",
        True,
        WHITE
    )

    difficulty_rect = difficulty_text.get_rect(
        center=(SCREEN_WIDTH // 2, 625)
    )

    screen.blit(
        difficulty_text,
        difficulty_rect
    )


def draw_restart_button(screen, font):
    """Draw the restart instruction."""

    text = font.render(
        "Press R to restart",
        True,
        WHITE
    )

    rect = text.get_rect(
        center=(SCREEN_WIDTH // 2, 125)
    )

    screen.blit(text, rect)


# ============================================================
# MAIN GAME
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

    button_font = pygame.font.SysFont(
        "arial",
        BUTTON_FONT_SIZE
    )

    game = Game()

    difficulty_index = DIFFICULTIES.index(
        DEFAULT_DIFFICULTY
    )

    difficulty = DIFFICULTIES[difficulty_index]

    ai = AI(difficulty)

    running = True

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            # ------------------------------------------------
            # Mouse input
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
            # Keyboard input
            # ------------------------------------------------

            elif event.type == pygame.KEYDOWN:

                # Restart round.
                if event.key == pygame.K_r:
                    game.reset_round()

                # Change difficulty.
                elif event.key == pygame.K_d:

                    difficulty_index = (
                        difficulty_index + 1
                    ) % len(DIFFICULTIES)

                    difficulty = (
                        DIFFICULTIES[difficulty_index]
                    )

                    ai.set_difficulty(
                        difficulty
                    )

                    game.reset_round()

                # Quick difficulty selection.
                elif event.key == pygame.K_1:

                    difficulty = "EASY"
                    ai.set_difficulty(difficulty)
                    game.reset_round()

                elif event.key == pygame.K_2:

                    difficulty = "MEDIUM"
                    ai.set_difficulty(difficulty)
                    game.reset_round()

                elif event.key == pygame.K_3:

                    difficulty = "HARD"
                    ai.set_difficulty(difficulty)
                    game.reset_round()

                # Escape closes the game.
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
        # DRAW
        # ====================================================

        screen.fill(BACKGROUND_COLOR)

        draw_title(
            screen,
            title_font
        )

        draw_difficulty(
            screen,
            info_font,
            difficulty
        )

        draw_restart_button(
            screen,
            button_font
        )

        draw_board(
            screen,
            game
        )

        draw_status(
            screen,
            info_font,
            game,
            difficulty
        )

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()