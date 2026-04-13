import tkinter as tk
import random
import os

WIDTH = 400
HEIGHT = 400
SIZE = 20
SPEED = 150

SCORE_FILE = "highscore.txt"

class Snake:
    def __init__(self):
        self.body = [(100, 100)]
        self.direction = "RIGHT"
        self.grow_flag = False

    def move(self):
        x, y = self.body[0]

        if self.direction == "UP":
            y -= SIZE
        elif self.direction == "DOWN":
            y += SIZE
        elif self.direction == "LEFT":
            x -= SIZE
        elif self.direction == "RIGHT":
            x += SIZE

        new_head = (x, y)
        self.body.insert(0, new_head)

        if not self.grow_flag:
            self.body.pop()
        else:
            self.grow_flag = False

    def grow(self):
        self.grow_flag = True

    def check_collision(self):
        x, y = self.body[0]
        return x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT or (x, y) in self.body[1:]


class Food:
    def __init__(self):
        self.respawn()

    def respawn(self):
        self.position = (
            random.randint(0, (WIDTH-SIZE)//SIZE) * SIZE,
            random.randint(0, (HEIGHT-SIZE)//SIZE) * SIZE
        )


class Game:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()

        self.speed = SPEED
        self.load_high_score()

        # ✅ التحكم بالكيبورد
        self.root.bind("<Up>", lambda e: self.set_dir("UP"))
        self.root.bind("<Down>", lambda e: self.set_dir("DOWN"))
        self.root.bind("<Left>", lambda e: self.set_dir("LEFT"))
        self.root.bind("<Right>", lambda e: self.set_dir("RIGHT"))
        self.root.bind("r", lambda e: self.restart())

        self.restart()

    def load_high_score(self):
        if os.path.exists(SCORE_FILE):
            with open(SCORE_FILE, "r") as f:
                self.high_score = int(f.read())
        else:
            self.high_score = 0

    def save_high_score(self):
        with open(SCORE_FILE, "w") as f:
            f.write(str(self.high_score))

    def restart(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.running = True
        self.update()

    def set_dir(self, direction):
        opposite = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}
        if direction != opposite.get(self.snake.direction):
            self.snake.direction = direction

    def update(self):
        if not self.running:
            self.canvas.create_text(WIDTH/2, HEIGHT/2, fill="white",
                                    text="GAME OVER\nPress R to Restart")
            if self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score()
            return

        self.snake.move()

        if self.snake.body[0] == self.food.position:
            self.snake.grow()
            self.food.respawn()
            self.score += 1

        if self.snake.check_collision():
            self.running = False

        self.draw()
        self.root.after(self.speed, self.update)

    def draw(self):
        self.canvas.delete("all")

        for x, y in self.snake.body:
            self.canvas.create_rectangle(x, y, x+SIZE, y+SIZE, fill="green")

        fx, fy = self.food.position
        self.canvas.create_rectangle(fx, fy, fx+SIZE, fy+SIZE, fill="red")

        self.canvas.create_text(
            100, 10,
            fill="white",
            text=f"Score: {self.score} | High: {self.high_score}"
        )


root = tk.Tk()
root.title("Snake PC 🐍🎮")
game = Game(root)
root.mainloop()