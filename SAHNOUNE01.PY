import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Pro")

GREEN = (0, 200, 0)
RED = (200, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BLOCK = 20
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 35)


class Snake:
    def __init__(self):
        self._body = [(100, 100)]
        self._direction = "RIGHT"

    # ===== Property =====
    @property
    def body(self):
        return self._body

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        directions = ["UP", "DOWN", "LEFT", "RIGHT"]
        if value in directions:
            self._direction = value

    def move(self):
        x, y = self._body[0]

        if self._direction == "UP":
            y -= BLOCK
        elif self._direction == "DOWN":
            y += BLOCK
        elif self._direction == "LEFT":
            x -= BLOCK
        elif self._direction == "RIGHT":
            x += BLOCK

        new_head = (x, y)
        self._body.insert(0, new_head)
        self._body.pop()

    def grow(self):
        self._body.append(self._body[-1])

    def draw(self):
        for segment in self._body:
            pygame.draw.rect(screen, GREEN, (segment[0], segment[1], BLOCK, BLOCK))


class Food:
    def __init__(self):
        self._position = self.random_pos()

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    def random_pos(self):
        return (random.randrange(0, WIDTH, BLOCK),
                random.randrange(0, HEIGHT, BLOCK))

    def draw(self):
        pygame.draw.rect(screen, RED, (self._position[0], self._position[1], BLOCK, BLOCK))


def draw_score(score):
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))


def game():
    snake = Snake()
    food = Food()
    score = 0

    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            snake.direction = "UP"
        elif keys[pygame.K_DOWN]:
            snake.direction = "DOWN"
        elif keys[pygame.K_LEFT]:
            snake.direction = "LEFT"
        elif keys[pygame.K_RIGHT]:
            snake.direction = "RIGHT"

        snake.move()

        # ===== اصطدام بالجدار =====
        head = snake.body[0]
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            print("Game Over 💀")
            running = False

        # ===== اصطدام بنفسه =====
        if head in snake.body[1:]:
            print("Game Over 💀")
            running = False

        # ===== أكل الطعام =====
        if head == food.position:
            snake.grow()
            food.position = food.random_pos()
            score += 1

        snake.draw()
        food.draw()
        draw_score(score)

        pygame.display.update()
        clock.tick(12)

    pygame.quit()


game()  
