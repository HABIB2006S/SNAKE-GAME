import pygame
import random

pygame.init()

# حجم الشاشة
WIDTH, HEIGHT = 600, 400
BLOCK = 20  # حجم كل مربع (جزء من الأفعى)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake OOP Advanced")

clock = pygame.time.Clock()

# ألوان
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# ===================== SNAKE CLASS =====================
class Snake:
    def __init__(self):
        # جسم الأفعى (كل عنصر هو جزء من الجسم)
        self._body = [(100, 100), (80, 100), (60, 100)]
        # الاتجاه تاع الحركة
        self._direction = "RIGHT"

    # ===== GETTER =====
    # نجيب الجسم
    @property
    def body(self):
        return self._body

    # نجيب الرأس
    @property
    def head(self):
        return self._body[0]

    # نجيب الاتجاه
    @property
    def direction(self):
        return self._direction

    # ===== SETTER =====
    # نبدل الاتجاه لكن بطريقة محمية
    @direction.setter
    def direction(self, value):
        # باش ما يرجعش للخلف مباشرة (bug)
        opposite = {
            "UP": "DOWN",
            "DOWN": "UP",
            "LEFT": "RIGHT",
            "RIGHT": "LEFT"
        }

        # إذا ماكانش عكس الاتجاه الحالي، نبدلو
        if value != opposite.get(self._direction):
            self._direction = value

    # ===== MOVE =====
    def move(self):
        x, y = self.head  # ناخذو رأس الأفعى

        # نحركو حسب الاتجاه
        if self._direction == "UP":
            y -= BLOCK
        elif self._direction == "DOWN":
            y += BLOCK
        elif self._direction == "LEFT":
            x -= BLOCK
        elif self._direction == "RIGHT":
            x += BLOCK

        # نضيفو رأس جديد
        new_head = (x, y)
        self._body.insert(0, new_head)

        # نحيدو آخر جزء باش تبقى نفس الطول
        self._body.pop()

    # ===== GROW =====
    def grow(self):
        # كي تاكل تزيد قطعة في الجسم
        self._body.append(self._body[-1])

    # ===== DRAW =====
    def draw(self, screen):
        # نرسمو كل أجزاء الأفعى
        for block in self._body:
            pygame.draw.rect(screen, GREEN, (*block, BLOCK, BLOCK))

    # ===== SELF COLLISION =====
    def check_self_collision(self):
        # إذا الرأس لمس الجسم تاعو = خسارة
        return self.head in self._body[1:]


# ===================== FOOD CLASS =====================
class Food:
    def __init__(self):
        # نحدد مكان عشوائي للأكل
        self._position = self._random_pos()

    # نجيب مكان الأكل
    @property
    def position(self):
        return self._position

    # نبدل مكان الأكل (setter)
    @position.setter
    def position(self, value):
        self._position = value

    # توليد مكان عشوائي
    def _random_pos(self):
        return (
            random.randint(0, WIDTH // BLOCK - 1) * BLOCK,
            random.randint(0, HEIGHT // BLOCK - 1) * BLOCK
        )

    # نرجعو نولدوه من جديد كي تاكله الأفعى
    def respawn(self):
        self._position = self._random_pos()

    # رسم الأكل
    def draw(self, screen):
        pygame.draw.rect(screen, RED, (*self._position, BLOCK, BLOCK))


# ===================== GAME CLASS =====================
class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.running = True

    # ===== SCORE (getter) =====
    @property
    def score_value(self):
        return self._score

    # ===== SCORE (setter) =====
    @score_value.setter
    def score_value(self, value):
        if value >= 0:
            self._score = value

    def update(self):
        # نحركو الأفعى
        self.snake.move()

        # إذا كلات الأكل
        if self.snake.head == self.food.position:
            self.snake.grow()      # تكبر الأفعى
            self.food.respawn()    # نبدلو الأكل
            self.score += 10      # نزيدو النقاط

        # تصادم مع الحيط
        x, y = self.snake.head
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            self.running = False  # game over

        # تصادم مع روحها
        if self.snake.check_self_collision():
            self.running = False

    def draw(self):
        # نملو الشاشة بالأسود
        screen.fill(BLACK)

        # نرسمو الأفعى والأكل
        self.snake.draw(screen)
        self.food.draw(screen)

        # نعرضو السكور
        text = pygame.font.SysFont(None, 30).render(
            f"Score: {self.score}", True, WHITE
        )
        screen.blit(text, (10, 10))

        pygame.display.update()

    def handle_keys(self):
        # قراءة الكلافيي
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                # تغيير الاتجاه حسب السهم
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
    game.handle_keys()  # نشوفو الأزرار
    game.update()       # نحدثو اللعبة
    game.draw()         # نرسمو الشاشة
    clock.tick(10)      # سرعة اللعبة

pygame.quit()