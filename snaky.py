import tkinter as tk
import random
import pygame
from pygame.locals import *

class SnakeGame:
    def __init__(self, master, width=400, height=400, block_size=20):
        self.master = master
        self.master.title("Snake Game")
        self.width = width
        self.height = height
        self.block_size = block_size
        self.canvas = tk.Canvas(master, width=width, height=height, bg="black")
        self.canvas.pack()

        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.food = self.create_food()
        self.direction = "RIGHT"

        self.score = 0
        self.delay = 100
        self.speed_var = tk.StringVar()
        self.speed_var.set("Normal")

        self.game_over = False
        self.create_widgets()
        self.bind_keys()
        self.update()

    def create_widgets(self):
        self.speed_label = tk.Label(self.master, text="Speed:")
        self.speed_label.pack(side=tk.LEFT)

        speed_options = ["Slow", "Normal", "Fast"]
        speed_menu = tk.OptionMenu(self.master, self.speed_var, *speed_options)
        speed_menu.pack(side=tk.LEFT)

        restart_button = tk.Button(self.master, text="Restart", command=self.restart_game)
        restart_button.pack(side=tk.RIGHT)

    def bind_keys(self):
        self.master.bind("<Up>", lambda event: self.set_direction("UP"))
        self.master.bind("<Down>", lambda event: self.set_direction("DOWN"))
        self.master.bind("<Left>", lambda event: self.set_direction("LEFT"))
        self.master.bind("<Right>", lambda event: self.set_direction("RIGHT"))

    def set_direction(self, direction):
        opposites = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}
        if direction != opposites[self.direction]:
            self.direction = direction

    def create_food(self):
        x = random.randint(1, (self.width - self.block_size) // self.block_size) * self.block_size
        y = random.randint(1, (self.height - self.block_size) // self.block_size) * self.block_size
        return x, y

    def check_collision(self, x, y, items):
        return any([x == item[0] and y == item[1] for item in items])

    def update(self):
        if not self.game_over:
            self.move_snake()
            self.check_collision_with_food()
            self.check_collision_with_wall()
            self.check_collision_with_self()
            self.canvas.delete("all")
            self.draw_snake()
            self.draw_food()
            self.draw_score()
            self.draw_direction()
            self.master.after(self.delay, self.update)

    def move_snake(self):
        head = list(self.snake[0])

        if self.direction == "UP":
            head[1] -= self.block_size
        elif self.direction == "DOWN":
            head[1] += self.block_size
        elif self.direction == "LEFT":
            head[0] -= self.block_size
        elif self.direction == "RIGHT":
            head[0] += self.block_size

        self.snake.insert(0, tuple(head))
        if len(self.snake) > self.score + 1:
            self.snake.pop()

    def check_collision_with_food(self):
        if self.snake[0] == self.food:
            self.score += 1
            self.food = self.create_food()
            self.update_speed()

    def check_collision_with_wall(self):
        x, y = self.snake[0]
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            self.game_over = True

    def check_collision_with_self(self):
        if self.check_collision(*self.snake[0], self.snake[1:]):
            self.game_over = True

    def update_speed(self):
        speed_mapping = {"Slow": 150, "Normal": 100, "Fast": 50}
        self.delay = speed_mapping.get(self.speed_var.get(), 100)

    def draw_snake(self):
        for segment in self.snake:
            x, y = segment
            self.canvas.create_rectangle(x, y, x + self.block_size, y + self.block_size, fill="green")

    def draw_food(self):
        x, y = self.food
        self.canvas.create_oval(x, y, x + self.block_size, y + self.block_size, fill="red")

    def draw_score(self):
        self.canvas.create_text(10, 10, text=f"Score: {self.score}", anchor="nw", fill="white")

    def draw_direction(self):
        x, y = self.snake[0]
        direction_text = f"Direction: {self.direction}"
        self.canvas.create_text(x, y - 15, text=direction_text, anchor="nw", fill="white")

    def restart_game(self):
        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.food = self.create_food()
        self.direction = "RIGHT"
        self.score = 0
        self.delay = 100
        self.game_over = False


def main():
    root = tk.Tk()
    root.resizable(False, False)
    game = SnakeGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
