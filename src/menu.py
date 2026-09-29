import math
import pygame


class MenuButton:
    """Animated rounded button used by the main menu."""

    def __init__(self, rect, text, font):
        self.base_rect = pygame.Rect(rect)
        self.rect = self.base_rect.copy()
        self.text = text
        self.font = font

        self.hovered = False
        self.hover_progress = 0.0
        self.scale = 1.0

    def update(self, mouse_pos, dt):
        self.hovered = self.base_rect.collidepoint(mouse_pos)

        target = 1.0 if self.hovered else 0.0
        speed = dt / 120.0

        if self.hover_progress < target:
            self.hover_progress = min(
                target,
                self.hover_progress + speed
            )
        else:
            self.hover_progress = max(
                target,
                self.hover_progress - speed
            )

        self.scale = 1.0 + (0.025 * self.hover_progress)

        width = int(self.base_rect.width * self.scale)
        height = int(self.base_rect.height * self.scale)

        self.rect = pygame.Rect(
            0,
            0,
            width,
            height
        )
        self.rect.center = self.base_rect.center

    def draw(self, surface):
        # Shadow
        shadow_rect = self.rect.move(0, 6)

        pygame.draw.rect(
            surface,
            (8, 12, 22),
            shadow_rect,
            border_radius=16
        )

        # Main button
        button_color = (
            35 + int(15 * self.hover_progress),
            42 + int(18 * self.hover_progress),
            62 + int(20 * self.hover_progress),
        )

        pygame.draw.rect(
            surface,
            button_color,
            self.rect,
            border_radius=16
        )

        # Border
        border_color = (
            80 + int(80 * self.hover_progress),
            95 + int(75 * self.hover_progress),
            130 + int(80 * self.hover_progress),
        )

        pygame.draw.rect(
            surface,
            border_color,
            self.rect,
            width=2,
            border_radius=16
        )

        # Text
        text_surface = self.font.render(
            self.text,
            True,
            (235, 240, 255)
        )

        text_rect = text_surface.get_rect(
            center=self.rect.center
        )

        surface.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


class MainMenu:
    """Professional animated main menu."""

    PLAY = "play"
    SETTINGS = "settings"
    STATISTICS = "statistics"
    EXIT = "exit"

    def __init__(self, screen):
        self.screen = screen

        self.width = screen.get_width()
        self.height = screen.get_height()

        self.title_font = pygame.font.SysFont(
            "arial",
            58,
            bold=True
        )

        self.subtitle_font = pygame.font.SysFont(
            "arial",
            21
        )

        self.button_font = pygame.font.SysFont(
            "arial",
            25,
            bold=True
        )

        self.footer_font = pygame.font.SysFont(
            "arial",
            16
        )

        center_x = self.width // 2

        button_width = 300
        button_height = 58
        gap = 16

        start_y = 300

        self.buttons = [
            MenuButton(
                (
                    center_x - button_width // 2,
                    start_y,
                    button_width,
                    button_height
                ),
                "PLAY GAME",
                self.button_font
            ),
            MenuButton(
                (
                    center_x - button_width // 2,
                    start_y + (button_height + gap),
                    button_width,
                    button_height
                ),
                "SETTINGS",
                self.button_font
            ),
            MenuButton(
                (
                    center_x - button_width // 2,
                    start_y + 2 * (button_height + gap),
                    button_width,
                    button_height
                ),
                "STATISTICS",
                self.button_font
            ),
            MenuButton(
                (
                    center_x - button_width // 2,
                    start_y + 3 * (button_height + gap),
                    button_width,
                    button_height
                ),
                "EXIT",
                self.button_font
            ),
        ]

        self.pulse_time = 0.0

        # Decorative board marks
        self.decorations = [
            ("X", 90, 150, 0.25),
            ("O", self.width - 100, 190, 0.0),
            ("X", 120, self.height - 150, 1.2),
            ("O", self.width - 120, self.height - 120, 0.7),
        ]

    def update(self, dt):
        self.pulse_time += dt

        mouse_pos = pygame.mouse.get_pos()

        for button in self.buttons:
            button.update(mouse_pos, dt)

    def draw_background(self):
        """Draw dark vertical gradient."""

        for y in range(self.height):
            ratio = y / max(1, self.height)

            color = (
                int(10 + 10 * ratio),
                int(14 + 12 * ratio),
                int(28 + 20 * ratio)
            )

            pygame.draw.line(
                self.screen,
                color,
                (0, y),
                (self.width, y)
            )

        # Soft decorative circles
        pulse = (
            math.sin(self.pulse_time * 0.002)
            + 1
        ) / 2

        circles = [
            (
                self.width // 2,
                160,
                150 + int(15 * pulse)
            ),
            (
                100,
                100,
                80
            ),
            (
                self.width - 80,
                self.height - 100,
                100
            ),
        ]

        for x, y, radius in circles:
            glow_surface = pygame.Surface(
                (radius * 2, radius * 2),
                pygame.SRCALPHA
            )

            pygame.draw.circle(
                glow_surface,
                (70, 90, 150, 18),
                (radius, radius),
                radius
            )

            self.screen.blit(
                glow_surface,
                (x - radius, y - radius)
            )

    def draw_decorations(self):
        """Draw floating X/O symbols."""

        for mark, x, y, phase in self.decorations:
            offset = math.sin(
                self.pulse_time * 0.002 + phase
            ) * 5

            font = pygame.font.SysFont(
                "arial",
                52,
                bold=True
            )

            if mark == "X":
                color = (105, 170, 255)
            else:
                color = (255, 125, 180)

            surface = font.render(
                mark,
                True,
                color
            )

            rect = surface.get_rect(
                center=(x, y + offset)
            )

            self.screen.blit(surface, rect)

    def draw(self):
        self.draw_background()
        self.draw_decorations()

        # Title
        title = self.title_font.render(
            "TIC-TAC-TOE PRO",
            True,
            (240, 244, 255)
        )

        title_rect = title.get_rect(
            center=(self.width // 2, 115)
        )

        self.screen.blit(title, title_rect)

        # Subtitle
        subtitle = self.subtitle_font.render(
            "Ultimate Strategy Game",
            True,
            (150, 165, 195)
        )

        subtitle_rect = subtitle.get_rect(
            center=(self.width // 2, 165)
        )

        self.screen.blit(
            subtitle,
            subtitle_rect
        )

        # Decorative divider
        divider_width = 170

        pygame.draw.line(
            self.screen,
            (75, 95, 135),
            (
                self.width // 2 - divider_width // 2,
                205
            ),
            (
                self.width // 2 + divider_width // 2,
                205
            ),
            2
        )

        # Buttons
        for button in self.buttons:
            button.draw(self.screen)

        # Footer
        footer = self.footer_font.render(
            "1 / 2 / 3  •  Difficulty     |     ESC  •  Back",
            True,
            (105, 115, 140)
        )

        footer_rect = footer.get_rect(
            center=(self.width // 2, self.height - 35)
        )

        self.screen.blit(
            footer,
            footer_rect
        )

    def handle_event(self, event):
        """Return the selected menu action."""

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos

                for button, action in zip(
                    self.buttons,
                    [
                        self.PLAY,
                        self.SETTINGS,
                        self.STATISTICS,
                        self.EXIT,
                    ]
                ):
                    if button.is_clicked(mouse_pos):
                        return action

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return self.PLAY

            if event.key == pygame.K_ESCAPE:
                return self.EXIT

        return None