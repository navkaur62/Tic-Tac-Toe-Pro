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
from src.settings import Settings


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
# ============================================================
# MENU / RESULT / SETTINGS UI
# ============================================================

MENU_TITLE_Y = 115
MENU_SUBTITLE_Y = 175

MENU_BUTTON_WIDTH = 300
MENU_BUTTON_HEIGHT = 58
MENU_BUTTON_GAP = 18

RESULT_TITLE_Y = 135
RESULT_SUBTITLE_Y = 190

SETTINGS_TITLE_Y = 115
SETTINGS_SUBTITLE_Y = 175
SETTINGS_PANEL_WIDTH = 520
SETTINGS_PANEL_HEIGHT = 300
SETTINGS_TOGGLE_WIDTH = 170
SETTINGS_TOGGLE_HEIGHT = 52
SETTINGS_SLIDER_WIDTH = 300
SETTINGS_SLIDER_HEIGHT = 8

STATISTICS_TITLE_Y = 115
STATISTICS_SUBTITLE_Y = 175
STATISTICS_PANEL_WIDTH = 560
STATISTICS_PANEL_HEIGHT = 340


def draw_centered_text(screen, text, font, color, y):
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(center=(SCREEN_WIDTH // 2, y))
    screen.blit(rendered, rect)


def draw_menu_button(screen, rect, text, font, selected=False):
    mouse_pos = pygame.mouse.get_pos()
    hovered = rect.collidepoint(mouse_pos)
    active = selected or hovered

    fill_color = (42, 45, 75) if active else (28, 30, 52)
    edge_color = ACCENT_COLOR if active else PANEL_EDGE_COLOR

    if active:
        draw_glow_rect(screen, rect, ACCENT_COLOR, radius=14, strength=55)

    pygame.draw.rect(screen, fill_color, rect, border_radius=14)
    pygame.draw.rect(screen, edge_color, rect, width=2 if active else 1, border_radius=14)

    rendered = font.render(text, True, WHITE if active else SOFT_WHITE)
    screen.blit(rendered, rendered.get_rect(center=rect.center))


def get_menu_buttons():
    center_x = SCREEN_WIDTH // 2
    start_y = 205

    return {
        "PLAY": pygame.Rect(center_x - MENU_BUTTON_WIDTH // 2, start_y, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT),
        "DIFFICULTY": pygame.Rect(center_x - MENU_BUTTON_WIDTH // 2, start_y + MENU_BUTTON_HEIGHT + MENU_BUTTON_GAP, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT),
        "STATISTICS": pygame.Rect(center_x - MENU_BUTTON_WIDTH // 2, start_y + 2 * (MENU_BUTTON_HEIGHT + MENU_BUTTON_GAP), MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT),
        "SETTINGS": pygame.Rect(center_x - MENU_BUTTON_WIDTH // 2, start_y + 3 * (MENU_BUTTON_HEIGHT + MENU_BUTTON_GAP), MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT),
        "QUIT": pygame.Rect(center_x - MENU_BUTTON_WIDTH // 2, start_y + 4 * (MENU_BUTTON_HEIGHT + MENU_BUTTON_GAP), MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT),
    }


def draw_main_menu(screen, title_font, info_font, button_font):
    draw_background(screen)

    draw_centered_text(screen, "TIC-TAC-TOE PRO", title_font, WHITE, MENU_TITLE_Y)
    draw_centered_text(screen, "A STRATEGIC TIC-TAC-TOE EXPERIENCE", info_font, MUTED_TEXT, MENU_SUBTITLE_Y)

    pygame.draw.line(screen, (45, 48, 75), (SCREEN_WIDTH // 2 - 160, 185), (SCREEN_WIDTH // 2 + 160, 185), 1)

    buttons = get_menu_buttons()

    draw_menu_button(screen, buttons["PLAY"], "PLAY GAME", button_font)
    draw_menu_button(screen, buttons["DIFFICULTY"], "DIFFICULTY", button_font)
    draw_menu_button(screen, buttons["STATISTICS"], "STATISTICS", button_font)
    draw_menu_button(screen, buttons["SETTINGS"], "SETTINGS", button_font)
    draw_menu_button(screen, buttons["QUIT"], "EXIT", button_font)

    control_font = pygame.font.SysFont("arial", CONTROL_FONT_SIZE)
    draw_centered_text(screen, "ENTER PLAY    D DIFFICULTY    T STATISTICS    S SETTINGS    ESC EXIT", control_font, MUTED_TEXT, 650)

    return buttons


def get_difficulty_buttons():
    center_x = SCREEN_WIDTH // 2
    start_y = 255
    return {
        difficulty_name: pygame.Rect(
            center_x - MENU_BUTTON_WIDTH // 2,
            start_y + index * (MENU_BUTTON_HEIGHT + MENU_BUTTON_GAP),
            MENU_BUTTON_WIDTH,
            MENU_BUTTON_HEIGHT,
        )
        for index, difficulty_name in enumerate(DIFFICULTIES)
    }


def draw_difficulty_menu(screen, title_font, info_font, button_font, selected_difficulty):
    draw_background(screen)
    draw_centered_text(screen, "SELECT DIFFICULTY", title_font, WHITE, MENU_TITLE_Y)
    draw_centered_text(screen, "Choose how challenging the AI should be", info_font, MUTED_TEXT, MENU_SUBTITLE_Y)

    buttons = get_difficulty_buttons()
    for difficulty_name in DIFFICULTIES:
        draw_menu_button(screen, buttons[difficulty_name], difficulty_name, button_font, selected=(difficulty_name == selected_difficulty))

    control_font = pygame.font.SysFont("arial", CONTROL_FONT_SIZE)
    draw_centered_text(screen, "1 EASY    2 MEDIUM    3 HARD    BACKSPACE BACK", control_font, MUTED_TEXT, 650)
    return buttons


def get_result_buttons():
    center_x = SCREEN_WIDTH // 2
    start_y = 365
    return {
        "REMATCH": pygame.Rect(center_x - MENU_BUTTON_WIDTH // 2, start_y, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT),
        "DIFFICULTY": pygame.Rect(center_x - MENU_BUTTON_WIDTH // 2, start_y + MENU_BUTTON_HEIGHT + MENU_BUTTON_GAP, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT),
        "MENU": pygame.Rect(center_x - MENU_BUTTON_WIDTH // 2, start_y + 2 * (MENU_BUTTON_HEIGHT + MENU_BUTTON_GAP), MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT),
    }


def draw_result_screen(screen, title_font, info_font, button_font, game, statistics, difficulty):
    draw_background(screen)

    if game.winner == PLAYER_X:
        title, title_color, subtitle = "YOU WIN!", PLAYER_X_COLOR, "Excellent move. Ready for another round?"
    elif game.winner == PLAYER_O:
        title, title_color, subtitle = "AI WINS!", PLAYER_O_COLOR, "The AI took this round. Try again?"
    else:
        title, title_color, subtitle = "DRAW!", WHITE, "A balanced round. Play again?"

    draw_centered_text(screen, title, title_font, title_color, RESULT_TITLE_Y)
    draw_centered_text(screen, subtitle, info_font, SOFT_WHITE, RESULT_SUBTITLE_Y)
    draw_centered_text(screen, f"{difficulty} MODE", info_font, ACCENT_COLOR, 235)

    scoreboard_width = 430
    scoreboard_height = 58
    scoreboard_rect = pygame.Rect((SCREEN_WIDTH - scoreboard_width) // 2, 265, scoreboard_width, scoreboard_height)

    pygame.draw.rect(screen, PANEL_COLOR, scoreboard_rect, border_radius=14)
    pygame.draw.rect(screen, PANEL_EDGE_COLOR, scoreboard_rect, width=1, border_radius=14)

    score_font = pygame.font.SysFont("arial", SCORE_FONT_SIZE, bold=True)
    score_items = [
        (f"YOU  {statistics.get_player_wins()}", PLAYER_X_COLOR, 75),
        (f"AI  {statistics.get_ai_wins()}", PLAYER_O_COLOR, 215),
        (f"DRAWS  {statistics.get_draws()}", SOFT_WHITE, 350),
    ]

    for text, color, offset in score_items:
        rendered = score_font.render(text, True, color)
        screen.blit(rendered, rendered.get_rect(center=(scoreboard_rect.x + offset, scoreboard_rect.centery)))

    buttons = get_result_buttons()
    draw_menu_button(screen, buttons["REMATCH"], "REMATCH", button_font)
    draw_menu_button(screen, buttons["DIFFICULTY"], "CHANGE DIFFICULTY", button_font)
    draw_menu_button(screen, buttons["MENU"], "MAIN MENU", button_font)
    return buttons


def get_statistics_buttons():
    center_x = SCREEN_WIDTH // 2

    return {
        "BACK": pygame.Rect(
            center_x - MENU_BUTTON_WIDTH // 2,
            545,
            MENU_BUTTON_WIDTH,
            MENU_BUTTON_HEIGHT,
        ),
    }


def draw_stat_card(screen, rect, label, value, value_color, label_font, value_font):
    pygame.draw.rect(screen, (24, 26, 46), rect, border_radius=14)
    pygame.draw.rect(screen, PANEL_EDGE_COLOR, rect, width=1, border_radius=14)

    label_surface = label_font.render(label, True, MUTED_TEXT)
    value_surface = value_font.render(str(value), True, value_color)

    screen.blit(
        label_surface,
        label_surface.get_rect(center=(rect.centerx, rect.y + 23)),
    )
    screen.blit(
        value_surface,
        value_surface.get_rect(center=(rect.centerx, rect.y + 54)),
    )


def draw_statistics_screen(screen, title_font, info_font, button_font, statistics):
    draw_background(screen)

    draw_centered_text(screen, "STATISTICS", title_font, WHITE, STATISTICS_TITLE_Y)
    draw_centered_text(
        screen,
        "Track your Tic-Tac-Toe Pro performance",
        info_font,
        MUTED_TEXT,
        STATISTICS_SUBTITLE_Y,
    )

    panel_rect = pygame.Rect(
        (SCREEN_WIDTH - STATISTICS_PANEL_WIDTH) // 2,
        205,
        STATISTICS_PANEL_WIDTH,
        STATISTICS_PANEL_HEIGHT,
    )

    pygame.draw.rect(screen, PANEL_COLOR, panel_rect, border_radius=18)
    pygame.draw.rect(screen, PANEL_EDGE_COLOR, panel_rect, width=1, border_radius=18)

    total_games = statistics.get_rounds_played()
    player_wins = statistics.get_player_wins()
    ai_wins = statistics.get_ai_wins()
    draws = statistics.get_draws()

    if total_games > 0:
        win_rate = (player_wins / total_games) * 100
    else:
        win_rate = 0.0

    label_font = pygame.font.SysFont("arial", 16, bold=True)
    value_font = pygame.font.SysFont("arial", 28, bold=True)
    small_font = pygame.font.SysFont("arial", 15, bold=True)

    card_width = 150
    card_height = 78
    gap = 18
    first_x = panel_rect.x + 30
    card_y = panel_rect.y + 32

    cards = [
        ("GAMES PLAYED", total_games, SOFT_WHITE),
        ("YOUR WINS", player_wins, PLAYER_X_COLOR),
        ("AI WINS", ai_wins, PLAYER_O_COLOR),
    ]

    for index, (label, value, value_color) in enumerate(cards):
        rect = pygame.Rect(
            first_x + index * (card_width + gap),
            card_y,
            card_width,
            card_height,
        )
        draw_stat_card(
            screen,
            rect,
            label,
            value,
            value_color,
            label_font,
            value_font,
        )

    second_y = card_y + card_height + 22

    draws_rect = pygame.Rect(
        first_x,
        second_y,
        220,
        78,
    )
    win_rate_rect = pygame.Rect(
        first_x + 238,
        second_y,
        220,
        78,
    )

    draw_stat_card(
        screen,
        draws_rect,
        "DRAWS",
        draws,
        SOFT_WHITE,
        label_font,
        value_font,
    )

    draw_stat_card(
        screen,
        win_rate_rect,
        "WIN RATE",
        f"{win_rate:.1f}%",
        ACCENT_COLOR,
        label_font,
        value_font,
    )

    summary = small_font.render(
        "Wins are player victories recorded across completed rounds.",
        True,
        MUTED_TEXT,
    )
    screen.blit(
        summary,
        summary.get_rect(center=(SCREEN_WIDTH // 2, panel_rect.bottom - 28)),
    )

    buttons = get_statistics_buttons()
    draw_menu_button(screen, buttons["BACK"], "BACK", button_font)

    control_font = pygame.font.SysFont("arial", CONTROL_FONT_SIZE)
    draw_centered_text(
        screen,
        "BACKSPACE BACK    ESC MAIN MENU",
        control_font,
        MUTED_TEXT,
        650,
    )

    return buttons


def get_settings_buttons():
    """Return clickable controls for the Settings screen.

    The volume row is spaced so the VOLUME label, minus button, slider,
    and plus button never overlap.
    """

    center_x = SCREEN_WIDTH // 2

    return {
        "SOUND": pygame.Rect(
            center_x + 70,
            260,
            SETTINGS_TOGGLE_WIDTH,
            SETTINGS_TOGGLE_HEIGHT,
        ),

        # Volume controls are intentionally arranged from left to right:
        # VOLUME label -> minus -> slider -> plus.
        "VOLUME_DOWN": pygame.Rect(
            center_x - 100,
            325,
            45,
            45,
        ),

        "VOLUME_UP": pygame.Rect(
            center_x + 150,
            325,
            45,
            45,
        ),

        "BACK": pygame.Rect(
            center_x - MENU_BUTTON_WIDTH // 2,
            480,
            MENU_BUTTON_WIDTH,
            MENU_BUTTON_HEIGHT,
        ),
    }


def draw_settings_screen(screen, title_font, info_font, button_font, settings):
    draw_background(screen)

    draw_centered_text(screen, "SETTINGS", title_font, WHITE, SETTINGS_TITLE_Y)
    draw_centered_text(screen, "Customize your game experience", info_font, MUTED_TEXT, SETTINGS_SUBTITLE_Y)

    panel_rect = pygame.Rect(
        (SCREEN_WIDTH - SETTINGS_PANEL_WIDTH) // 2,
        215,
        SETTINGS_PANEL_WIDTH,
        SETTINGS_PANEL_HEIGHT,
    )
    pygame.draw.rect(screen, PANEL_COLOR, panel_rect, border_radius=18)
    pygame.draw.rect(screen, PANEL_EDGE_COLOR, panel_rect, width=1, border_radius=18)

    buttons = get_settings_buttons()
    label_font = pygame.font.SysFont("arial", 21, bold=True)
    value_font = pygame.font.SysFont("arial", 18, bold=True)

    sound_label = label_font.render("SOUND EFFECTS", True, SOFT_WHITE)
    screen.blit(sound_label, sound_label.get_rect(midleft=(panel_rect.x + 35, buttons["SOUND"].centery)))

    sound_active = settings.sound_enabled
    sound_fill = ACCENT_COLOR if sound_active else (45, 47, 65)
    pygame.draw.rect(screen, sound_fill, buttons["SOUND"], border_radius=12)
    pygame.draw.rect(screen, PANEL_EDGE_COLOR, buttons["SOUND"], width=1, border_radius=12)
    sound_text = value_font.render("ON" if sound_active else "OFF", True, WHITE if sound_active else MUTED_TEXT)
    screen.blit(sound_text, sound_text.get_rect(center=buttons["SOUND"].center))

    volume_label = label_font.render("VOLUME", True, SOFT_WHITE)
    screen.blit(volume_label, volume_label.get_rect(midleft=(panel_rect.x + 35, buttons["VOLUME_DOWN"].centery)))

    for key, symbol in (("VOLUME_DOWN", "-"), ("VOLUME_UP", "+")):
        pygame.draw.rect(screen, (35, 37, 58), buttons[key], border_radius=10)
        pygame.draw.rect(screen, PANEL_EDGE_COLOR, buttons[key], width=1, border_radius=10)
        text = label_font.render(symbol, True, WHITE)
        screen.blit(text, text.get_rect(center=buttons[key].center))

    # Keep the slider between the minus and plus buttons.
    slider_left = SCREEN_WIDTH // 2 - 45
    slider_width = 180
    slider_y = buttons["VOLUME_DOWN"].centery

    slider_rect = pygame.Rect(
        slider_left,
        slider_y - SETTINGS_SLIDER_HEIGHT // 2,
        slider_width,
        SETTINGS_SLIDER_HEIGHT,
    )

    pygame.draw.rect(screen, (45, 48, 70), slider_rect, border_radius=4)

    filled_width = int(slider_width * settings.volume)
    if filled_width > 0:
        filled_rect = pygame.Rect(slider_left, slider_rect.y, filled_width, SETTINGS_SLIDER_HEIGHT)
        pygame.draw.rect(screen, ACCENT_COLOR, filled_rect, border_radius=4)

    knob_x = slider_left + int(slider_width * settings.volume)
    pygame.draw.circle(screen, WHITE, (knob_x, slider_y), 8)

    percentage = value_font.render(f"{int(settings.volume * 100)}%", True, ACCENT_COLOR)
    screen.blit(
        percentage,
        percentage.get_rect(
            center=(SCREEN_WIDTH // 2, slider_y + 58)
        ),
    )

    draw_menu_button(screen, buttons["BACK"], "BACK", button_font)

    control_font = pygame.font.SysFont("arial", CONTROL_FONT_SIZE)
    draw_centered_text(screen, "S SOUND    - / + VOLUME    BACKSPACE BACK", control_font, MUTED_TEXT, 650)
    return buttons


# ============================================================
# GAME HELPERS
# ============================================================

def reset_game_round(game, move_animation, win_animation, particles):
    game.reset_round()
    move_animation.reset()
    win_animation.reset()
    particles.clear()


def start_difficulty(difficulty_name, ai, game, move_animation, win_animation, particles):
    ai.set_difficulty(difficulty_name)
    reset_game_round(game, move_animation, win_animation, particles)


def get_board_position(mouse_pos):
    mouse_x, mouse_y = mouse_pos
    if not (BOARD_X <= mouse_x < BOARD_X + BOARD_SIZE and BOARD_Y <= mouse_y < BOARD_Y + BOARD_SIZE):
        return None

    col = (mouse_x - BOARD_X) // CELL_SIZE
    row = (mouse_y - BOARD_Y) // CELL_SIZE
    return row * 3 + col


def start_win_animation(game, win_animation, particles, particle_color):
    if not game.winning_positions:
        return

    first_position = game.winning_positions[0]
    last_position = game.winning_positions[-1]

    win_start = (
        BOARD_X + (first_position % 3) * CELL_SIZE + CELL_SIZE // 2,
        BOARD_Y + (first_position // 3) * CELL_SIZE + CELL_SIZE // 2,
    )
    win_end = (
        BOARD_X + (last_position % 3) * CELL_SIZE + CELL_SIZE // 2,
        BOARD_Y + (last_position // 3) * CELL_SIZE + CELL_SIZE // 2,
    )

    win_animation.start(win_start, win_end)

    for position in game.winning_positions:
        win_x = BOARD_X + (position % 3) * CELL_SIZE + CELL_SIZE // 2
        win_y = BOARD_Y + (position // 3) * CELL_SIZE + CELL_SIZE // 2
        particles.emit(win_x, win_y, particle_color, count=8)


def handle_player_move(position, game, move_animation, win_animation, particles, sound_manager):
    if not game.make_move(position):
        return False

    sound_manager.play("player_move")
    move_animation.start(position, PLAYER_X)

    center_x = BOARD_X + (position % 3) * CELL_SIZE + CELL_SIZE // 2
    center_y = BOARD_Y + (position // 3) * CELL_SIZE + CELL_SIZE // 2
    particles.emit(center_x, center_y, PLAYER_X_COLOR, count=14)

    if game.is_round_over and game.winning_positions:
        start_win_animation(game, win_animation, particles, PLAYER_X_COLOR)

    return True


def handle_ai_move(game, ai, move_animation, win_animation, particles, sound_manager):
    ai_move = ai.get_move(game.board)

    if ai_move is None or not game.make_move(ai_move):
        return False

    sound_manager.play("ai_move")
    move_animation.start(ai_move, PLAYER_O)

    center_x = BOARD_X + (ai_move % 3) * CELL_SIZE + CELL_SIZE // 2
    center_y = BOARD_Y + (ai_move // 3) * CELL_SIZE + CELL_SIZE // 2
    particles.emit(center_x, center_y, PLAYER_O_COLOR, count=14)

    if game.is_round_over and game.winning_positions:
        start_win_animation(game, win_animation, particles, PLAYER_O_COLOR)

    return True


# ============================================================
# MAIN
# ============================================================

def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()

    title_font = pygame.font.SysFont("arial", TITLE_FONT_SIZE, bold=True)
    info_font = pygame.font.SysFont("arial", INFO_FONT_SIZE, bold=True)
    status_font = pygame.font.SysFont("arial", STATUS_FONT_SIZE, bold=True)
    control_font = pygame.font.SysFont("arial", CONTROL_FONT_SIZE)
    score_font = pygame.font.SysFont("arial", SCORE_FONT_SIZE, bold=True)
    round_font = pygame.font.SysFont("arial", ROUND_FONT_SIZE, bold=True)
    menu_button_font = pygame.font.SysFont("arial", 21, bold=True)
    menu_info_font = pygame.font.SysFont("arial", 20, bold=True)

    game = Game()
    statistics = Statistics()
    settings = Settings()

    move_animation = MoveAnimation(duration=250)
    win_animation = WinAnimation(duration=500)
    particles = ParticleSystem()

    sound_manager = SoundManager(
        enabled=settings.sound_enabled,
        volume=settings.volume,
    )

    difficulty_index = DIFFICULTIES.index(DEFAULT_DIFFICULTY)
    difficulty = DIFFICULTIES[difficulty_index]
    ai = AI(difficulty)

    MENU = "MENU"
    DIFFICULTY = "DIFFICULTY"
    SETTINGS_SCREEN = "SETTINGS"
    STATISTICS_SCREEN = "STATISTICS"
    GAME_SCREEN = "GAME"
    RESULT = "RESULT"

    current_screen = MENU
    result_recorded = False
    running = True

    while running:
        dt = clock.tick(FPS)

        move_animation.update(dt)
        win_animation.update(dt)
        particles.update(dt)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if current_screen == MENU:
                    buttons = get_menu_buttons()

                    if buttons["PLAY"].collidepoint(event.pos):
                        start_difficulty(difficulty, ai, game, move_animation, win_animation, particles)
                        result_recorded = False
                        current_screen = GAME_SCREEN
                        sound_manager.play("click")

                    elif buttons["DIFFICULTY"].collidepoint(event.pos):
                        current_screen = DIFFICULTY
                        sound_manager.play("click")

                    elif buttons["STATISTICS"].collidepoint(event.pos):
                        current_screen = STATISTICS_SCREEN
                        sound_manager.play("click")

                    elif buttons["SETTINGS"].collidepoint(event.pos):
                        current_screen = SETTINGS_SCREEN
                        sound_manager.play("click")

                    elif buttons["QUIT"].collidepoint(event.pos):
                        running = False

                elif current_screen == DIFFICULTY:
                    buttons = get_difficulty_buttons()
                    for index, difficulty_name in enumerate(DIFFICULTIES):
                        if buttons[difficulty_name].collidepoint(event.pos):
                            difficulty_index = index
                            difficulty = difficulty_name
                            ai.set_difficulty(difficulty)
                            sound_manager.play("difficulty")
                            current_screen = MENU
                            break

                elif current_screen == STATISTICS_SCREEN:
                    buttons = get_statistics_buttons()

                    if buttons["BACK"].collidepoint(event.pos):
                        current_screen = MENU
                        sound_manager.play("click")

                elif current_screen == SETTINGS_SCREEN:
                    buttons = get_settings_buttons()

                    if buttons["SOUND"].collidepoint(event.pos):
                        new_state = settings.toggle_sound()
                        sound_manager.set_enabled(new_state)
                        if new_state:
                            sound_manager.play("click")

                    elif buttons["VOLUME_DOWN"].collidepoint(event.pos):
                        settings.decrease_volume(0.05)
                        sound_manager.set_volume(settings.volume)
                        if settings.sound_enabled:
                            sound_manager.play("click")

                    elif buttons["VOLUME_UP"].collidepoint(event.pos):
                        settings.increase_volume(0.05)
                        sound_manager.set_volume(settings.volume)
                        if settings.sound_enabled:
                            sound_manager.play("click")

                    elif buttons["BACK"].collidepoint(event.pos):
                        current_screen = MENU
                        sound_manager.play("click")

                elif current_screen == GAME_SCREEN:
                    if (
                        not game.is_round_over
                        and not move_animation.is_active()
                        and game.get_current_player() == PLAYER_X
                    ):
                        position = get_board_position(event.pos)
                        if position is not None and game.board.is_valid_move(position):
                            handle_player_move(position, game, move_animation, win_animation, particles, sound_manager)

                elif current_screen == RESULT:
                    buttons = get_result_buttons()

                    if buttons["REMATCH"].collidepoint(event.pos):
                        start_difficulty(difficulty, ai, game, move_animation, win_animation, particles)
                        result_recorded = False
                        current_screen = GAME_SCREEN
                        sound_manager.play("click")

                    elif buttons["DIFFICULTY"].collidepoint(event.pos):
                        current_screen = DIFFICULTY
                        sound_manager.play("click")

                    elif buttons["MENU"].collidepoint(event.pos):
                        current_screen = MENU
                        sound_manager.play("click")

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if current_screen == MENU:
                        running = False
                    else:
                        current_screen = MENU
                    continue

                if current_screen == MENU:
                    if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        start_difficulty(difficulty, ai, game, move_animation, win_animation, particles)
                        result_recorded = False
                        current_screen = GAME_SCREEN
                        sound_manager.play("click")
                    elif event.key == pygame.K_d:
                        current_screen = DIFFICULTY
                        sound_manager.play("click")
                    elif event.key == pygame.K_t:
                        current_screen = STATISTICS_SCREEN
                        sound_manager.play("click")
                    elif event.key == pygame.K_s:
                        current_screen = SETTINGS_SCREEN
                        sound_manager.play("click")

                elif current_screen == DIFFICULTY:
                    selected = None
                    if event.key == pygame.K_1:
                        selected = "EASY"
                    elif event.key == pygame.K_2:
                        selected = "MEDIUM"
                    elif event.key == pygame.K_3:
                        selected = "HARD"
                    elif event.key in (pygame.K_BACKSPACE, pygame.K_LEFT):
                        current_screen = MENU

                    if selected in DIFFICULTIES:
                        difficulty = selected
                        difficulty_index = DIFFICULTIES.index(selected)
                        ai.set_difficulty(difficulty)
                        sound_manager.play("difficulty")
                        current_screen = MENU

                elif current_screen == STATISTICS_SCREEN:
                    if event.key in (pygame.K_BACKSPACE, pygame.K_LEFT, pygame.K_t):
                        current_screen = MENU
                        sound_manager.play("click")

                elif current_screen == SETTINGS_SCREEN:
                    if event.key == pygame.K_s:
                        new_state = settings.toggle_sound()
                        sound_manager.set_enabled(new_state)
                        if new_state:
                            sound_manager.play("click")

                    elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                        settings.decrease_volume(0.05)
                        sound_manager.set_volume(settings.volume)

                    elif event.key in (pygame.K_EQUALS, pygame.K_KP_PLUS):
                        settings.increase_volume(0.05)
                        sound_manager.set_volume(settings.volume)
                        if settings.sound_enabled:
                            sound_manager.play("click")

                    elif event.key in (pygame.K_BACKSPACE, pygame.K_LEFT):
                        current_screen = MENU

                elif current_screen == GAME_SCREEN:
                    if event.key == pygame.K_r:
                        reset_game_round(game, move_animation, win_animation, particles)
                        result_recorded = False
                        sound_manager.play("restart")

                    elif event.key == pygame.K_1:
                        difficulty = "EASY"
                        difficulty_index = 0
                        start_difficulty(difficulty, ai, game, move_animation, win_animation, particles)
                        result_recorded = False
                        sound_manager.play("difficulty")

                    elif event.key == pygame.K_2:
                        difficulty = "MEDIUM"
                        difficulty_index = 1
                        start_difficulty(difficulty, ai, game, move_animation, win_animation, particles)
                        result_recorded = False
                        sound_manager.play("difficulty")

                    elif event.key == pygame.K_3:
                        difficulty = "HARD"
                        difficulty_index = 2
                        start_difficulty(difficulty, ai, game, move_animation, win_animation, particles)
                        result_recorded = False
                        sound_manager.play("difficulty")

                    elif event.key == pygame.K_d:
                        current_screen = DIFFICULTY
                        sound_manager.play("click")

                    elif event.key == pygame.K_m:
                        current_screen = MENU
                        sound_manager.play("click")

                elif current_screen == RESULT:
                    if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_r):
                        start_difficulty(difficulty, ai, game, move_animation, win_animation, particles)
                        result_recorded = False
                        current_screen = GAME_SCREEN
                        sound_manager.play("click")

                    elif event.key == pygame.K_d:
                        current_screen = DIFFICULTY
                        sound_manager.play("click")

                    elif event.key in (pygame.K_m, pygame.K_BACKSPACE):
                        current_screen = MENU
                        sound_manager.play("click")

        # ========================================================
        # AI TURN
        # ========================================================
        if (
            current_screen == GAME_SCREEN
            and not game.is_round_over
            and not move_animation.is_active()
            and game.get_current_player() == PLAYER_O
        ):
            handle_ai_move(game, ai, move_animation, win_animation, particles, sound_manager)

        # ========================================================
        # RECORD RESULT
        # ========================================================
        if (
            current_screen == GAME_SCREEN
            and game.is_round_over
            and not result_recorded
        ):
            winner = game.get_winner()
            statistics.record_result(winner)

            if winner == PLAYER_X:
                sound_manager.play("win")
            elif winner == PLAYER_O:
                sound_manager.play("win")
            else:
                sound_manager.play("draw")

            result_recorded = True
            current_screen = RESULT

        # ========================================================
        # DRAW
        # ========================================================
        if current_screen == MENU:
            draw_main_menu(screen, title_font, menu_info_font, menu_button_font)

        elif current_screen == DIFFICULTY:
            draw_difficulty_menu(screen, title_font, menu_info_font, menu_button_font, difficulty)

        elif current_screen == SETTINGS_SCREEN:
            draw_settings_screen(screen, title_font, menu_info_font, menu_button_font, settings)

        elif current_screen == STATISTICS_SCREEN:
            draw_statistics_screen(screen, title_font, menu_info_font, menu_button_font, statistics)

        elif current_screen == GAME_SCREEN:
            draw_background(screen)
            draw_title(screen, title_font)

            pygame.draw.line(
                screen,
                (45, 48, 75),
                (SCREEN_WIDTH // 2 - 120, 92),
                (SCREEN_WIDTH // 2 + 120, 92),
                1,
            )

            draw_difficulty(screen, info_font, difficulty)
            draw_round_info(screen, round_font, statistics)
            draw_board(screen, game, move_animation, win_animation, pygame.mouse.get_pos())
            particles.draw(screen)
            draw_status(screen, status_font, game)
            draw_scoreboard(screen, statistics, score_font)
            draw_controls(screen, control_font)

        elif current_screen == RESULT:
            draw_result_screen(screen, title_font, menu_info_font, menu_button_font, game, statistics, difficulty)

        pygame.display.flip()

    sound_manager.shutdown()
    pygame.quit()


# ============================================================
# PROGRAM ENTRY
# ============================================================

if __name__ == "__main__":
    main()
