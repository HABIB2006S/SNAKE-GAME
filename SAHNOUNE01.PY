
import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 400
BLOCK = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake OOP Advanced")

clock = pygame.time.Clock()

GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# ===================== SNAKE CLASS =====================
class Snake:
    def __init__(self):
        self._body = [(100, 100), (80, 100), (60, 100)]
        self._direction = "RIGHT"

    # ===== GETTER =====
    @property
    def body(self):
        return self._body

    @property
    def head(self):
        return self._body[0]

    @property
    def direction(self):
        return self._direction

    # ===== SETTER (مع حماية) =====
    @direction.setter
    def direction(self, value):
        opposite = {
            "UP": "DOWN",
            "DOWN": "UP",
            "LEFT": "RIGHT",
            "RIGHT": "LEFT"
        }

        # منع الرجوع للخلف مباشرة
        if value != opposite.get(self._direction):
            self._direction = value

    # ===== MOVE =====
    def move(self):
        x, y = self.head

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

    # ===== GROW =====
    def grow(self):
        self._body.append(self._body[-1])

    # ===== DRAW =====
    def draw(self, screen):
        for block in self._body:
            pygame.draw.rect(screen, GREEN, (*block, BLOCK, BLOCK))

    # ===== COLLISION SELF =====
    def check_self_collision(self):
        return self.head in self._body[1:]


# ===================== FOOD CLASS =====================
class Food:
    def __init__(self):
        self._position = self._random_pos()

    # GETTER
    @property
    def position(self):
        return self._position

    # SETTER (إعادة توليد الطعام)
    @position.setter
    def position(self, value):
        self._position = value

    def _random_pos(self):
        return (
            random.randint(0, WIDTH // BLOCK - 1) * BLOCK,
            random.randint(0, HEIGHT // BLOCK - 1) * BLOCK
        )

    def respawn(self):
        self._position = self._random_pos()

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (*self._position, BLOCK, BLOCK))


# ===================== GAME CLASS =====================
class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.running = True

    # ===== GETTER SCORE =====
    @property
    def score_value(self):
        return self._score

    # ===== SETTER SCORE =====
    @score_value.setter
    def score_value(self, value):
        if value >= 0:
            self._score = value

    def update(self):
        self.snake.move()

        # تصادم مع الطعام
        if self.snake.head == self.food.position:
            self.snake.grow()
            self.food.respawn()
            self.score += 10

        # تصادم مع الجدار
        x, y = self.snake.head
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            self.running = False

        # تصادم مع النفس
        if self.snake.check_self_collision():
            self.running = False

    def draw(self):
        screen.fill(BLACK)
        self.snake.draw(screen)
        self.food.draw(screen)

        text = pygame.font.SysFont(None, 30).render(
            f"Score: {self.score}", True, WHITE
        )
        screen.blit(text, (10, 10))

        pygame.display.update()

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.direction = "UP"
                elif event.key == pygame.K_DOWN:
                    self.snake.direction = "DOWN"
                elif event.key == pygame.K_LEFT:
                    self.snake.direction = "LEFT"
                elif event.key == pygame.K_RIGHT:
                    self.snake.direction = "RIGHT"


# ===================== MAIN LOOP =====================
game = Game()

while game.running:
    game.handle_keys()
    game.update()
    game.draw()
    clock.tick(10)

pygame.quit()