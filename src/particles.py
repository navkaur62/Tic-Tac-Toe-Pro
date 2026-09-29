import random
import math
import pygame


class Particle:
    """A single visual particle."""

    def __init__(self, x, y, color):
        self.x = x
        self.y = y

        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(1.5, 4.5)

        self.velocity_x = math.cos(angle) * speed
        self.velocity_y = math.sin(angle) * speed

        self.color = color
        self.radius = random.randint(2, 5)
        self.life = random.randint(350, 700)
        self.max_life = self.life

    def update(self, dt):
        """Update particle position and lifetime."""

        self.x += self.velocity_x * (dt / 16.67)
        self.y += self.velocity_y * (dt / 16.67)

        self.velocity_y += 0.08 * (dt / 16.67)

        self.life -= dt

        return self.life > 0

    def draw(self, screen):
        """Draw the particle with fading alpha."""

        if self.life <= 0:
            return

        alpha = max(0, min(255, int(
            255 * (self.life / self.max_life)
        )))

        surface = pygame.Surface(
            (self.radius * 2 + 4, self.radius * 2 + 4),
            pygame.SRCALPHA
        )

        pygame.draw.circle(
            surface,
            (*self.color, alpha),
            (
                self.radius + 2,
                self.radius + 2
            ),
            self.radius
        )

        screen.blit(
            surface,
            (
                int(self.x - self.radius - 2),
                int(self.y - self.radius - 2)
            )
        )


class ParticleSystem:
    """Manage all game particles."""

    def __init__(self):
        self.particles = []

    def emit(self, x, y, color, count=12):
        """Create particles at a position."""

        for _ in range(count):
            self.particles.append(
                Particle(x, y, color)
            )

    def update(self, dt):
        """Update and remove expired particles."""

        alive_particles = []

        for particle in self.particles:
            if particle.update(dt):
                alive_particles.append(particle)

        self.particles = alive_particles

    def draw(self, screen):
        """Draw all active particles."""

        for particle in self.particles:
            particle.draw(screen)

    def clear(self):
        """Remove all particles."""

        self.particles.clear()

    def is_active(self):
        """Return whether particles are currently active."""

        return len(self.particles) > 0