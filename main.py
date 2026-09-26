import pygame
import random
import sys
import time

from src.constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    WINDOW_TITLE,
    BACKGROUND,
    NEON_CYAN,
    NEON_BLUE,
    NEON_PINK,
    NEON_PURPLE,
    WHITE,
    LIGHT_BLUE,
    BOARD_SIZE,
    CELL_SIZE,
    PLAYER_X,
    PLAYER_O,
)


# ============================================================
# INITIALIZATION
# ============================================================

pygame.init()

screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)

pygame.display.set_caption(WINDOW_TITLE)

clock = pygame.time.Clock()


# ============================================================
# FONTS
# ============================================================

title_font = pygame.font.Font(None, 64)
subtitle_font = pygame.font.Font(None, 28)

section_font = pygame.font.Font(None, 30)
symbol_font = pygame.font.Font(None, 52)

small_font = pygame.font.Font(None, 22)
status_font = pygame.font.Font(None, 26)


# ============================================================
# COLORS
# ============================================================

GRID_COLOR = (10, 20, 55)
PANEL_COLOR = (7, 13, 40)
CELL_HOVER = (10, 35, 75)

MUTED_TEXT = (110, 145, 180)


# ============================================================
# GAME STATE
# ============================================================

board = [""] * 9

player_score = 0
computer_score = 0

round_number = 1
difficulty = "HARD"
current_turn = PLAYER_X

game_over = False
winner = None
winning_cells = []

computer_move_time = None

round_start_time = time.time()


# ============================================================
# BOARD POSITION
# ============================================================

BOARD_DISPLAY_SIZE = 390

board_x = (SCREEN_WIDTH - BOARD_DISPLAY_SIZE) // 2
board_y = 220

display_cell_size = BOARD_DISPLAY_SIZE // 3


# ============================================================
# PARTICLES
# ============================================================

particles = []

for _ in range(55):

    particles.append(
        {
            "x": random.randint(0, SCREEN_WIDTH),
            "y": random.randint(0, SCREEN_HEIGHT),
            "speed": random.uniform(0.15, 0.5),
            "size": random.randint(1, 2),
        }
    )


# ============================================================
# TEXT
# ============================================================

def draw_text(
    text,
    font,
    position,
    color,
    center=True
):

    surface = font.render(
        text,
        True,
        color
    )

    if center:

        rect = surface.get_rect(
            center=position
        )

    else:

        rect = surface.get_rect(
            topleft=position
        )

    screen.blit(surface, rect)


def draw_soft_text(
    text,
    font,
    position,
    color,
    glow_color
):

    # Very subtle glow
    glow = font.render(
        text,
        True,
        glow_color
    )

    glow.set_alpha(45)

    rect = glow.get_rect(
        center=position
    )

    screen.blit(
        glow,
        (rect.x + 2, rect.y + 2)
    )

    # Sharp main text
    draw_text(
        text,
        font,
        position,
        color
    )


# ============================================================
# BACKGROUND
# ============================================================

def draw_background():

    screen.fill(BACKGROUND)

    # Grid
    for y in range(0, SCREEN_HEIGHT, 35):

        pygame.draw.line(
            screen,
            GRID_COLOR,
            (0, y),
            (SCREEN_WIDTH, y),
            1
        )

    for x in range(0, SCREEN_WIDTH, 35):

        pygame.draw.line(
            screen,
            GRID_COLOR,
            (x, 0),
            (x, SCREEN_HEIGHT),
            1
        )

    # Particles
    for particle in particles:

        particle["y"] -= particle["speed"]

        if particle["y"] < 0:

            particle["y"] = SCREEN_HEIGHT
            particle["x"] = random.randint(
                0,
                SCREEN_WIDTH
            )

        pygame.draw.circle(
            screen,
            (20, 70, 110),
            (
                int(particle["x"]),
                int(particle["y"])
            ),
            particle["size"]
        )


# ============================================================
# NEON LINE
# ============================================================

def draw_neon_line(
    start,
    end,
    color,
    width=2
):

    # Soft outer glow
    glow_surface = pygame.Surface(
        (SCREEN_WIDTH, SCREEN_HEIGHT),
        pygame.SRCALPHA
    )

    pygame.draw.line(
        glow_surface,
        (*color, 35),
        start,
        end,
        width + 8
    )

    screen.blit(
        glow_surface,
        (0, 0)
    )

    # Main line
    pygame.draw.line(
        screen,
        color,
        start,
        end,
        width
    )


# ============================================================
# X
# ============================================================

def draw_x(
    center_x,
    center_y,
    color
):

    size = 38

    draw_neon_line(
        (
            center_x - size,
            center_y - size
        ),
        (
            center_x + size,
            center_y + size
        ),
        color,
        4
    )

    draw_neon_line(
        (
            center_x + size,
            center_y - size
        ),
        (
            center_x - size,
            center_y + size
        ),
        color,
        4
    )


# ============================================================
# O
# ============================================================

def draw_o(
    center_x,
    center_y,
    color
):

    glow_surface = pygame.Surface(
        (SCREEN_WIDTH, SCREEN_HEIGHT),
        pygame.SRCALPHA
    )

    pygame.draw.circle(
        glow_surface,
        (*color, 40),
        (
            int(center_x),
            int(center_y)
        ),
        43,
        8
    )

    screen.blit(
        glow_surface,
        (0, 0)
    )

    pygame.draw.circle(
        screen,
        color,
        (
            int(center_x),
            int(center_y)
        ),
        38,
        5
    )


# ============================================================
# PANEL
# ============================================================

def draw_panel(
    rect,
    border_color
):

    # Panel background
    pygame.draw.rect(
        screen,
        PANEL_COLOR,
        rect,
        border_radius=14
    )

    # Border
    pygame.draw.rect(
        screen,
        border_color,
        rect,
        width=2,
        border_radius=14
    )


# ============================================================
# TOP HUD
# ============================================================

def draw_top_hud():

    # ==========================================
    # SCORE
    # ==========================================

    draw_text(
        f"SCORE  {player_score:02d}",
        small_font,
        (55, 48),
        LIGHT_BLUE,
        False
    )

    # ==========================================
    # TITLE
    # ==========================================

    draw_soft_text(
        "TIC TAC TOE",
        title_font,
        (SCREEN_WIDTH // 2, 48),
        WHITE,
        NEON_CYAN
    )

    draw_text(
        "PRO",
        subtitle_font,
        (SCREEN_WIDTH // 2, 82),
        NEON_PINK
    )

    # ==========================================
    # TIMER
    # ==========================================

    elapsed = int(
        time.time() - round_start_time
    )

    minutes = elapsed // 60
    seconds = elapsed % 60

    timer_surface = small_font.render(
        f"TIME  {minutes:02d}:{seconds:02d}",
        True,
        LIGHT_BLUE
    )

    timer_rect = timer_surface.get_rect(
        topright=(SCREEN_WIDTH - 55, 48)
    )

    screen.blit(
        timer_surface,
        timer_rect
    )

# ============================================================
# PLAYER PANEL
# ============================================================

def draw_player_panel():

    rect = pygame.Rect(
        55,
        225,
        210,
        155
    )

    draw_panel(
        rect,
        NEON_PINK
    )

    draw_text(
        "PLAYER",
        section_font,
        (160, 255),
        WHITE
    )

    draw_soft_text(
        "X",
        symbol_font,
        (160, 310),
        NEON_PINK,
        NEON_PINK
    )

    draw_text(
        "YOU",
        small_font,
        (160, 350),
        MUTED_TEXT
    )


# ============================================================
# COMPUTER PANEL
# ============================================================

def draw_computer_panel():

    rect = pygame.Rect(
        55,
        400,
        210,
        155
    )

    draw_panel(
        rect,
        NEON_BLUE
    )

    draw_text(
        "COMPUTER",
        section_font,
        (160, 430),
        WHITE
    )

    draw_soft_text(
        "O",
        symbol_font,
        (160, 485),
        NEON_BLUE,
        NEON_BLUE
    )

    draw_text(
        "CPU",
        small_font,
        (160, 525),
        MUTED_TEXT
    )


# ============================================================
# STAGE PANEL
# ============================================================

def draw_stage_panel():

    rect = pygame.Rect(
        835,
        225,
        210,
        155
    )

    draw_panel(
        rect,
        NEON_PURPLE
    )

    # Difficulty title
    draw_text(
        "DIFFICULTY",
        section_font,
        (940, 255),
        WHITE
    )

    # Current difficulty
    difficulty_display = difficulty

    if difficulty == "EASY":

        difficulty_color = NEON_CYAN

    elif difficulty == "MEDIUM":

        difficulty_color = NEON_PURPLE

    else:

        difficulty_color = NEON_PINK

    draw_soft_text(
        difficulty_display,
        symbol_font,
        (940, 305),
        difficulty_color,
        difficulty_color
    )

    # Round information
    draw_text(
        f"ROUND {round_number}",
        small_font,
        (940, 345),
        MUTED_TEXT
    )

    # Keyboard controls
    draw_text(
        "1  EASY   2  MED   3  HARD",
        small_font,
        (940, 365),
        LIGHT_BLUE
    )

# ============================================================
# LIVES
# ============================================================

def draw_lives():

    draw_text(
        "LIVES",
        small_font,
        (940, 415),
        LIGHT_BLUE
    )

    for i in range(3):

        x = 900 + i * 40

        pygame.draw.circle(
            screen,
            NEON_PINK,
            (x, 450),
            9,
            2
        )


# ============================================================
# BOARD
# ============================================================

def draw_board():

    board_rect = pygame.Rect(
        board_x,
        board_y,
        BOARD_DISPLAY_SIZE,
        BOARD_DISPLAY_SIZE
    )

    # Board background
    pygame.draw.rect(
        screen,
        (4, 10, 32),
        board_rect,
        border_radius=18
    )

    # Board border
    pygame.draw.rect(
        screen,
        NEON_CYAN,
        board_rect,
        width=2,
        border_radius=18
    )

    # Mouse hover
    mouse_x, mouse_y = pygame.mouse.get_pos()

    if (
        board_x <= mouse_x < board_x + BOARD_DISPLAY_SIZE
        and
        board_y <= mouse_y < board_y + BOARD_DISPLAY_SIZE
        and
        not game_over
        and
        current_turn == PLAYER_X
    ):

        col = (
            mouse_x - board_x
        ) // display_cell_size

        row = (
            mouse_y - board_y
        ) // display_cell_size

        index = row * 3 + col

        if board[index] == "":

            hover_rect = pygame.Rect(
                board_x + col * display_cell_size + 5,
                board_y + row * display_cell_size + 5,
                display_cell_size - 10,
                display_cell_size - 10
            )

            pygame.draw.rect(
                screen,
                CELL_HOVER,
                hover_rect,
                border_radius=10
            )

    # Grid
    for i in range(1, 3):

        x = board_x + i * display_cell_size

        draw_neon_line(
            (x, board_y + 12),
            (
                x,
                board_y + BOARD_DISPLAY_SIZE - 12
            ),
            NEON_CYAN,
            2
        )

    for i in range(1, 3):

        y = board_y + i * display_cell_size

        draw_neon_line(
            (board_x + 12, y),
            (
                board_x + BOARD_DISPLAY_SIZE - 12,
                y
            ),
            NEON_CYAN,
            2
        )

    # Symbols
    for index, value in enumerate(board):

        if value == "":
            continue

        row = index // 3
        col = index % 3

        center_x = (
            board_x
            + col * display_cell_size
            + display_cell_size // 2
        )

        center_y = (
            board_y
            + row * display_cell_size
            + display_cell_size // 2
        )

        if value == PLAYER_X:

            draw_x(
                center_x,
                center_y,
                NEON_PINK
            )

        else:

            draw_o(
                center_x,
                center_y,
                NEON_BLUE
            )

    # Winning highlight
    if winning_cells:

        for index in winning_cells:

            row = index // 3
            col = index % 3

            rect = pygame.Rect(
                board_x + col * display_cell_size + 8,
                board_y + row * display_cell_size + 8,
                display_cell_size - 16,
                display_cell_size - 16
            )

            pygame.draw.rect(
                screen,
                NEON_PURPLE,
                rect,
                width=2,
                border_radius=10
            )


# ============================================================
# WIN CHECK
# ============================================================

def check_winner():

    combinations = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6],
    ]

    for combination in combinations:

        a, b, c = combination

        if (
            board[a] != ""
            and board[a] == board[b]
            and board[b] == board[c]
        ):

            return board[a], combination

    if "" not in board:

        return "DRAW", []

    return None, []


# ============================================================
# FINISH GAME
# ============================================================

def finish_game(
    result,
    cells
):

    global game_over
    global winner
    global winning_cells
    global player_score
    global computer_score

    game_over = True
    winner = result
    winning_cells = cells

    if result == PLAYER_X:

        player_score += 1

    elif result == PLAYER_O:

        computer_score += 1


# ============================================================
# PLAYER MOVE
# ============================================================

def player_move(index):

    global current_turn
    global computer_move_time

    if game_over:
        return

    if current_turn != PLAYER_X:
        return

    if board[index] != "":
        return

    board[index] = PLAYER_X

    result, cells = check_winner()

    if result:

        finish_game(
            result,
            cells
        )

        return

    current_turn = PLAYER_O

    computer_move_time = (
        pygame.time.get_ticks() + 550
    )


# ============================================================
# COMPUTER AI - MINIMAX
# ============================================================

def minimax(board_state, depth, is_maximizing):

    result, _ = check_winner_for_board(board_state)

    if result == PLAYER_O:
        return 10 - depth

    if result == PLAYER_X:
        return depth - 10

    if result == "DRAW":
        return 0

    empty_cells = [
        i
        for i, value in enumerate(board_state)
        if value == ""
    ]

    if is_maximizing:

        best_score = -float("inf")

        for move in empty_cells:

            board_state[move] = PLAYER_O

            score = minimax(
                board_state,
                depth + 1,
                False
            )

            board_state[move] = ""

            best_score = max(
                best_score,
                score
            )

        return best_score

    else:

        best_score = float("inf")

        for move in empty_cells:

            board_state[move] = PLAYER_X

            score = minimax(
                board_state,
                depth + 1,
                True
            )

            board_state[move] = ""

            best_score = min(
                best_score,
                score
            )

        return best_score


def check_winner_for_board(board_state):

    combinations = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6],
    ]

    for combination in combinations:

        a, b, c = combination

        if (
            board_state[a] != ""
            and board_state[a] == board_state[b]
            and board_state[b] == board_state[c]
        ):
            return board_state[a], combination

    if "" not in board_state:
        return "DRAW", []

    return None, []


def computer_move():

    global current_turn

    empty_cells = [
        i
        for i, value in enumerate(board)
        if value == ""
    ]

    if not empty_cells:
        return

    # ========================================================
    # EASY MODE
    # ========================================================

    if difficulty == "EASY":

        # Completely random move
        move = random.choice(empty_cells)

    # ========================================================
    # MEDIUM MODE
    # ========================================================

    elif difficulty == "MEDIUM":

        move = None

        # ----------------------------------------------------
        # 1. Try to WIN
        # ----------------------------------------------------

        for test_move in empty_cells:

            board[test_move] = PLAYER_O

            result, _ = check_winner()

            board[test_move] = ""

            if result == PLAYER_O:

                move = test_move
                break

        # ----------------------------------------------------
        # 2. Block PLAYER if about to win
        # ----------------------------------------------------

        if move is None:

            for test_move in empty_cells:

                board[test_move] = PLAYER_X

                result, _ = check_winner()

                board[test_move] = ""

                if result == PLAYER_X:

                    move = test_move
                    break

        # ----------------------------------------------------
        # 3. Otherwise random
        # ----------------------------------------------------

        if move is None:

            move = random.choice(empty_cells)

    # ========================================================
    # HARD MODE
    # ========================================================

    else:

        best_score = -float("inf")
        best_moves = []

        for test_move in empty_cells:

            board[test_move] = PLAYER_O

            score = minimax(
                board,
                0,
                False
            )

            board[test_move] = ""

            if score > best_score:

                best_score = score
                best_moves = [test_move]

            elif score == best_score:

                best_moves.append(test_move)

        move = random.choice(best_moves)

    # ========================================================
    # APPLY COMPUTER MOVE
    # ========================================================

    board[move] = PLAYER_O

    result, cells = check_winner()

    if result:

        finish_game(
            result,
            cells
        )

        return

    current_turn = PLAYER_X


def handle_board_click(position):

    mouse_x, mouse_y = position

    if not (
        board_x <= mouse_x <
        board_x + BOARD_DISPLAY_SIZE
    ):
        return

    if not (
        board_y <= mouse_y <
        board_y + BOARD_DISPLAY_SIZE
    ):
        return

    col = (
        mouse_x - board_x
    ) // display_cell_size

    row = (
        mouse_y - board_y
    ) // display_cell_size

    index = row * 3 + col

    player_move(index)


# ============================================================
# RESET
# ============================================================

def reset_round():

    global board
    global current_turn
    global round_number
    global game_over
    global winner
    global winning_cells
    global computer_move_time
    global round_start_time

    board = [""] * 9
    round_number += 1
    current_turn = PLAYER_X

    game_over = False
    winner = None
    winning_cells = []

    computer_move_time = None

    round_start_time = time.time()


# ============================================================
# BOTTOM STATUS
# ============================================================

def draw_status():

    panel = pygame.Rect(
        360,
        640,
        380,
        48
    )

    pygame.draw.rect(
        screen,
        PANEL_COLOR,
        panel,
        border_radius=12
    )

    pygame.draw.rect(
        screen,
        (20, 60, 90),
        panel,
        width=1,
        border_radius=12
    )

    if game_over:

        if winner == PLAYER_X:

            text = "YOU WIN  •  PRESS R"

            color = NEON_PINK

        elif winner == PLAYER_O:

            text = "COMPUTER WINS  •  PRESS R"

            color = NEON_BLUE

        else:

            text = "DRAW  •  PRESS R"

            color = NEON_PURPLE

    else:

        if current_turn == PLAYER_X:

            text = "YOUR TURN"

            color = NEON_PINK

        else:

            text = "COMPUTER THINKING..."

            color = NEON_BLUE

    draw_text(
        text,
        status_font,
        panel.center,
        color
    )


# ============================================================
# MAIN LOOP
# ============================================================

running = True

while running:

    # --------------------------------------------------------
    # EVENTS
    # --------------------------------------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                handle_board_click(
                    event.pos
                )

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                running = False

            elif event.key == pygame.K_r:

                reset_round()

            elif event.key == pygame.K_1:

                difficulty = "EASY"

            elif event.key == pygame.K_2:

                difficulty = "MEDIUM"

            elif event.key == pygame.K_3:

                difficulty = "HARD"

                reset_round()

    # --------------------------------------------------------
    # COMPUTER
    # --------------------------------------------------------

    if (
        not game_over
        and
        current_turn == PLAYER_O
        and
        computer_move_time is not None
        and
        pygame.time.get_ticks()
        >= computer_move_time
    ):

        computer_move()

        computer_move_time = None

    # --------------------------------------------------------
    # DRAW
    # --------------------------------------------------------

    draw_background()

    draw_top_hud()

    draw_player_panel()

    draw_computer_panel()

    draw_stage_panel()

    draw_lives()

    draw_board()

    draw_status()

    # --------------------------------------------------------
    # UPDATE
    # --------------------------------------------------------

    pygame.display.flip()

    clock.tick(FPS)


# ============================================================
# CLEANUP
# ============================================================

pygame.quit()
sys.exit()