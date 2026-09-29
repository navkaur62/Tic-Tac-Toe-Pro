import pygame
import math

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
from src.animations import MoveAnimation, WinAnimation
from src.particles import ParticleSystem
from src.sound_manager import SoundManager


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
# AESTHETIC THEME
# ============================================================

PANEL_COLOR = (15, 16, 32)
PANEL_EDGE_COLOR = (58, 62, 95)
CELL_HOVER_COLOR = (35, 38, 68)
SOFT_WHITE = (215, 218, 235)
MUTED_TEXT = (145, 150, 175)
GLOW_STEPS = 7


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


def draw_glow_rect(screen, rect, color, radius=16, strength=90):
    """Draw a soft glow around a rounded rectangle."""
    for i in range(GLOW_STEPS, 0, -1):
        spread = i * 3
        alpha = int(strength * (1 - i / (GLOW_STEPS + 1)))
        glow_surface = pygame.Surface(
            (rect.width + spread * 2, rect.height + spread * 2),
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            glow_surface,
            (*color, alpha),
            glow_surface.get_rect(),
            border_radius=radius + spread // 2
        )

        screen.blit(
            glow_surface,
            (rect.x - spread, rect.y - spread)
        )


def draw_background(screen):
    """Draw a subtle vertical gradient background."""
    width, height = screen.get_size()

    top = (8, 10, 24)
    bottom = (22, 18, 40)

    for y in range(height):
        ratio = y / max(1, height - 1)

        color = (
            int(top[0] + (bottom[0] - top[0]) * ratio),
            int(top[1] + (bottom[1] - top[1]) * ratio),
            int(top[2] + (bottom[2] - top[2]) * ratio),
        )

        pygame.draw.line(
            screen,
            color,
            (0, y),
            (width, y)
        )


def draw_title(screen, font):
    """Draw the main game title with a soft glow."""

    title = font.render(
        "TIC-TAC-TOE PRO",
        True,
        WHITE
    )

    rect = title.get_rect(
        center=(SCREEN_WIDTH // 2, TITLE_Y)
    )

    # Soft title glow.
    glow = pygame.Surface(
        (title.get_width() + 40, title.get_height() + 30),
        pygame.SRCALPHA
    )

    glow_text = font.render(
        "TIC-TAC-TOE PRO",
        True,
        ACCENT_COLOR
    )

    glow_text.set_alpha(45)

    glow.blit(
        glow_text,
        glow_text.get_rect(
            center=glow.get_rect().center
        )
    )

    screen.blit(
        glow,
        glow.get_rect(center=rect.center)
    )

    screen.blit(title, rect)


def draw_difficulty(screen, font, difficulty):
    """Display difficulty in a compact pill."""

    text = font.render(
        f"  {difficulty} MODE  ",
        True,
        ACCENT_COLOR
    )

    rect = text.get_rect(
        center=(SCREEN_WIDTH // 2, DIFFICULTY_Y)
    )

    pill = pygame.Rect(
        rect.x - 8,
        rect.y - 4,
        rect.width + 16,
        rect.height + 8
    )

    pygame.draw.rect(
        screen,
        PANEL_COLOR,
        pill,
        border_radius=12
    )

    pygame.draw.rect(
        screen,
        PANEL_EDGE_COLOR,
        pill,
        width=1,
        border_radius=12
    )

    screen.blit(text, rect)


def draw_round_info(screen, font, statistics):
    """Display the current round number."""

    round_number = statistics.get_rounds_played() + 1

    text = font.render(
        f"ROUND {round_number}",
        True,
        SOFT_WHITE
    )

    rect = text.get_rect(
        center=(SCREEN_WIDTH // 2, ROUND_Y)
    )

    screen.blit(text, rect)


def draw_board(
    screen,
    game,
    move_animation=None,
    win_animation=None,
    mouse_pos=None
):
    """Draw the polished game board with hover and glow effects."""

    board_rect = pygame.Rect(
        BOARD_X,
        BOARD_Y,
        BOARD_SIZE,
        BOARD_SIZE
    )

    # Board glow.
    draw_glow_rect(
        screen,
        board_rect,
        ACCENT_COLOR,
        radius=16,
        strength=65 + int(
            15 * (0.5 + 0.5 * math.sin(pygame.time.get_ticks() / 500))
        )
    )

    # Board panel.
    pygame.draw.rect(
        screen,
        PANEL_COLOR,
        board_rect,
        border_radius=16
    )

    pygame.draw.rect(
        screen,
        PANEL_EDGE_COLOR,
        board_rect,
        width=2,
        border_radius=16
    )

    # Subtle inner border.
    inner_rect = board_rect.inflate(-8, -8)

    pygame.draw.rect(
        screen,
        (28, 30, 52),
        inner_rect,
        width=1,
        border_radius=12
    )

    # ========================================================
    # CELL HOVER
    # ========================================================

    hover_position = None

    if (
        mouse_pos is not None
        and not game.is_round_over
        and not (move_animation and move_animation.is_active())
        and game.get_current_player() == PLAYER_X
    ):
        mouse_x, mouse_y = mouse_pos

        if (
            BOARD_X <= mouse_x < BOARD_X + BOARD_SIZE
            and BOARD_Y <= mouse_y < BOARD_Y + BOARD_SIZE
        ):
            col = (mouse_x - BOARD_X) // CELL_SIZE
            row = (mouse_y - BOARD_Y) // CELL_SIZE
            hover_position = row * 3 + col

            if game.board.is_valid_move(hover_position):
                hover_rect = pygame.Rect(
                    BOARD_X + col * CELL_SIZE + 7,
                    BOARD_Y + row * CELL_SIZE + 7,
                    CELL_SIZE - 14,
                    CELL_SIZE - 14
                )

                pygame.draw.rect(
                    screen,
                    CELL_HOVER_COLOR,
                    hover_rect,
                    border_radius=12
                )

                pygame.draw.rect(
                    screen,
                    (65, 70, 105),
                    hover_rect,
                    width=1,
                    border_radius=12
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
            (x, BOARD_Y + 12),
            (x, BOARD_Y + BOARD_SIZE - 12),
            3
        )

        pygame.draw.line(
            screen,
            GRID_COLOR,
            (BOARD_X + 12, y),
            (BOARD_X + BOARD_SIZE - 12, y),
            3
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

        is_animated_move = (
            move_animation is not None
            and move_animation.position == position
        )

        if is_animated_move:
            progress = move_animation.get_progress()
            scale = 1.0 - (1.0 - progress) ** 3
        else:
            scale = 1.0

        if scale <= 0:
            continue

        # Soft mark glow.
        glow_size = int(CELL_FONT_SIZE * scale) + 20

        glow_surface = pygame.Surface(
            (glow_size * 2, glow_size * 2),
            pygame.SRCALPHA
        )

        glow_font = pygame.font.SysFont(
            "arial",
            max(1, int(CELL_FONT_SIZE * scale)),
            bold=True
        )

        glow_text = glow_font.render(
            value,
            True,
            (*color,)
        )
        glow_text.set_alpha(32)

        glow_rect = glow_text.get_rect(
            center=glow_surface.get_rect().center
        )

        glow_surface.blit(
            glow_text,
            glow_rect
        )

        screen.blit(
            glow_surface,
            glow_surface.get_rect(
                center=(center_x, center_y)
            )
        )

        text = font.render(
            value,
            True,
            color
        )

        if scale < 1.0:
            scaled_size = (
                max(1, int(text.get_width() * scale)),
                max(1, int(text.get_height() * scale))
            )

            text = pygame.transform.smoothscale(
                text,
                scaled_size
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

        progress = 1.0

        if win_animation is not None:
            progress = win_animation.get_progress()

        progress = 1.0 - (1.0 - progress) ** 3

        animated_end_x = (
            start_x + (end_x - start_x) * progress
        )

        animated_end_y = (
            start_y + (end_y - start_y) * progress
        )

        # Glow behind the winning line.
        glow_surface = pygame.Surface(
            (SCREEN_WIDTH, SCREEN_HEIGHT),
            pygame.SRCALPHA
        )

        pygame.draw.line(
            glow_surface,
            (*highlight_color, 45),
            (start_x, start_y),
            (animated_end_x, animated_end_y),
            20
        )

        screen.blit(
            glow_surface,
            (0, 0)
        )

        pygame.draw.line(
            screen,
            highlight_color,
            (start_x, start_y),
            (animated_end_x, animated_end_y),
            8
        )

        # Bright center line.
        pygame.draw.line(
            screen,
            WHITE,
            (start_x, start_y),
            (animated_end_x, animated_end_y),
            2
        )

# ============================================================
# DRAW GAME STATUS
# ============================================================

def draw_status(screen, font, game):
    """Display a polished game status panel."""

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
            message = "YOUR TURN  •  X"
            color = PLAYER_X_COLOR
        else:
            message = "AI TURN  •  O"
            color = PLAYER_O_COLOR

    text = font.render(
        message,
        True,
        color
    )

    rect = text.get_rect(
        center=(SCREEN_WIDTH // 2, BOARD_STATUS_Y)
    )

    panel = pygame.Rect(
        rect.x - 22,
        rect.y - 7,
        rect.width + 44,
        rect.height + 14
    )

    pygame.draw.rect(
        screen,
        PANEL_COLOR,
        panel,
        border_radius=14
    )

    pygame.draw.rect(
        screen,
        (48, 51, 78),
        panel,
        width=1,
        border_radius=14
    )

    screen.blit(text, rect)


# ============================================================
# DRAW SCOREBOARD
# ============================================================

def draw_scoreboard(screen, statistics, font):
    """Draw the polished match scoreboard."""

    scoreboard_width = 430
    scoreboard_height = 54

    scoreboard_x = (
        SCREEN_WIDTH - scoreboard_width
    ) // 2

    scoreboard_y = 608

    rect = pygame.Rect(
        scoreboard_x,
        scoreboard_y,
        scoreboard_width,
        scoreboard_height
    )

    pygame.draw.rect(
        screen,
        PANEL_COLOR,
        rect,
        border_radius=14
    )

    pygame.draw.rect(
        screen,
        PANEL_EDGE_COLOR,
        rect,
        width=1,
        border_radius=14
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
        SOFT_WHITE
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
    """Display clean keyboard controls."""

    text = font.render(
        "1 EASY    2 MEDIUM    3 HARD    •    "
        "R RESTART    ESC EXIT",
        True,
        MUTED_TEXT
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

    # Visual effects
    move_animation = MoveAnimation(duration=250)
    win_animation = WinAnimation(duration=500)
    particles = ParticleSystem()
    sound_manager = SoundManager(enabled=True, volume=0.32)

    difficulty_index = DIFFICULTIES.index(
        DEFAULT_DIFFICULTY
    )

    difficulty = DIFFICULTIES[
        difficulty_index
    ]

    ai = AI(difficulty)

    running = True

    while running:

        dt = clock.tick(FPS)

        # Update visual effects every frame.
        move_animation.update(dt)
        win_animation.update(dt)
        particles.update(dt)

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
                    and not move_animation.is_active()
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

                        if game.make_move(position):
                            sound_manager.play("player_move")
                            move_animation.start(
                                position,
                                PLAYER_X
                            )

                            center_x = (
                                BOARD_X
                                + (position % 3) * CELL_SIZE
                                + CELL_SIZE // 2
                            )
                            center_y = (
                                BOARD_Y
                                + (position // 3) * CELL_SIZE
                                + CELL_SIZE // 2
                            )

                            particles.emit(
                                center_x,
                                center_y,
                                PLAYER_X_COLOR,
                                count=14
                            )

                            if game.is_round_over and game.winning_positions:
                                first_position = game.winning_positions[0]
                                last_position = game.winning_positions[-1]

                                win_start = (
                                    BOARD_X
                                    + (first_position % 3) * CELL_SIZE
                                    + CELL_SIZE // 2,
                                    BOARD_Y
                                    + (first_position // 3) * CELL_SIZE
                                    + CELL_SIZE // 2
                                )

                                win_end = (
                                    BOARD_X
                                    + (last_position % 3) * CELL_SIZE
                                    + CELL_SIZE // 2,
                                    BOARD_Y
                                    + (last_position // 3) * CELL_SIZE
                                    + CELL_SIZE // 2
                                )

                                win_animation.start(
                                    win_start,
                                    win_end
                                )

                                for winning_position in game.winning_positions:
                                    win_x = (
                                        BOARD_X
                                        + (winning_position % 3) * CELL_SIZE
                                        + CELL_SIZE // 2
                                    )
                                    win_y = (
                                        BOARD_Y
                                        + (winning_position // 3) * CELL_SIZE
                                        + CELL_SIZE // 2
                                    )

                                    particles.emit(
                                        win_x,
                                        win_y,
                                        PLAYER_X_COLOR,
                                        count=8
                                    )

            # ------------------------------------------------
            # Keyboard
            # ------------------------------------------------

            elif event.type == pygame.KEYDOWN:

                # Restart round
                if event.key == pygame.K_r:

                    game.reset_round()
                    move_animation.reset()
                    win_animation.reset()
                    particles.clear()
                    sound_manager.play("restart")

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
                    move_animation.reset()
                    win_animation.reset()
                    particles.clear()
                    sound_manager.play("difficulty")

                    result_recorded = False

                # Easy
                elif event.key == pygame.K_1:

                    difficulty = "EASY"

                    ai.set_difficulty(
                        difficulty
                    )

                    game.reset_round()
                    move_animation.reset()
                    win_animation.reset()
                    particles.clear()
                    sound_manager.play("difficulty")

                    result_recorded = False

                # Medium
                elif event.key == pygame.K_2:

                    difficulty = "MEDIUM"

                    ai.set_difficulty(
                        difficulty
                    )

                    game.reset_round()
                    move_animation.reset()
                    win_animation.reset()
                    particles.clear()
                    sound_manager.play("difficulty")

                    result_recorded = False

                # Hard
                elif event.key == pygame.K_3:

                    difficulty = "HARD"

                    ai.set_difficulty(
                        difficulty
                    )

                    game.reset_round()
                    move_animation.reset()
                    win_animation.reset()
                    particles.clear()
                    sound_manager.play("difficulty")

                    result_recorded = False

                # Exit
                elif event.key == pygame.K_ESCAPE:
                    running = False

        # ====================================================
        # AI TURN
        # ====================================================

        if (
            not game.is_round_over
            and not move_animation.is_active()
            and game.get_current_player() == PLAYER_O
        ):

            ai_move = ai.get_move(
                game.board
            )

            if ai_move is not None and game.make_move(ai_move):
                sound_manager.play("ai_move")
                move_animation.start(
                    ai_move,
                    PLAYER_O
                )

                center_x = (
                    BOARD_X
                    + (ai_move % 3) * CELL_SIZE
                    + CELL_SIZE // 2
                )
                center_y = (
                    BOARD_Y
                    + (ai_move // 3) * CELL_SIZE
                    + CELL_SIZE // 2
                )

                particles.emit(
                    center_x,
                    center_y,
                    PLAYER_O_COLOR,
                    count=14
                )

                if game.is_round_over and game.winning_positions:
                    first_position = game.winning_positions[0]
                    last_position = game.winning_positions[-1]

                    win_start = (
                        BOARD_X
                        + (first_position % 3) * CELL_SIZE
                        + CELL_SIZE // 2,
                        BOARD_Y
                        + (first_position // 3) * CELL_SIZE
                        + CELL_SIZE // 2
                    )

                    win_end = (
                        BOARD_X
                        + (last_position % 3) * CELL_SIZE
                        + CELL_SIZE // 2,
                        BOARD_Y
                        + (last_position // 3) * CELL_SIZE
                        + CELL_SIZE // 2
                    )

                    win_animation.start(
                        win_start,
                        win_end
                    )

                    for winning_position in game.winning_positions:
                        win_x = (
                            BOARD_X
                            + (winning_position % 3) * CELL_SIZE
                            + CELL_SIZE // 2
                        )
                        win_y = (
                            BOARD_Y
                            + (winning_position // 3) * CELL_SIZE
                            + CELL_SIZE // 2
                        )

                        particles.emit(
                            win_x,
                            win_y,
                            PLAYER_O_COLOR,
                            count=8
                        )

        # ====================================================
        # RECORD RESULT
        # ====================================================

        if (
            game.is_round_over
            and not result_recorded
        ):

            winner = game.get_winner()

            statistics.record_result(
                winner
            )

            if winner == PLAYER_X:
                sound_manager.play("win")
            elif winner == PLAYER_O:
                sound_manager.play("win")
            else:
                sound_manager.play("draw")

            result_recorded = True

        # ====================================================
        # DRAW
        # ====================================================

        draw_background(screen)

        draw_title(
            screen,
            title_font
        )

        pygame.draw.line(
            screen,
            (45, 48, 75),
            (SCREEN_WIDTH // 2 - 120, 92),
            (SCREEN_WIDTH // 2 + 120, 92),
            1
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
            game,
            move_animation,
            win_animation,
            pygame.mouse.get_pos()
        )

        particles.draw(screen)

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

    sound_manager.shutdown()
    pygame.quit()


if __name__ == "__main__":
    main()