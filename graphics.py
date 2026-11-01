import numpy as np
import random as rn
import pygame
from main import TetrisEngine

game = TetrisEngine()
fall_timer = 0
CELL_SIZE = 30
HIGHT = 600
WIDTH = 300

pygame.init()
screen = pygame.display.set_mode((WIDTH, HIGHT))
pygame.display.set_caption("My Tetris AI Project")
clock = pygame.time.Clock()

running = True
while not game.game_over and running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Выходим из главного цикла при нажатии на крестик
            
        if event.type == pygame.KEYDOWN:
            # Исправлено: event.key вместо pygame.event.key
            if event.key == pygame.K_LEFT:
                game.move(-1)
            if event.key == pygame.K_RIGHT:
                game.move(1)
            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_DOWN:
                game.step_down()
            if event.key == pygame.K_SPACE:
                game.hard_drop()

    fall_timer += 1
    if fall_timer >= 30:
        game.step_down()
        fall_timer = 0

    screen.fill((20, 20, 20))
    grid = game.render_console()  # Важно: в main.py этот метод должен делать return display!

    for y in range(game.height):
        for x in range(game.width):
            val = grid[y, x]
            if val > 0:
                if val == 1:
                    color = (200, 200, 200)  # Светло-серый для упавших блоков
                else:
                    color = (0, 255, 255)    # Голубой для падающей фигуры (если умножал на 2)
                
                # Рисуем квадратик 29x29 пикселей (оставляя 1 пиксель для сетки)
                pygame.draw.rect(
                    screen, 
                    color, 
                    (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1)
                )

    # Показываем нарисованный кадр на экране и держим 60 FPS
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
print(f"Игра окончена! Твой счет: {game.score}, сожжено линий: {game.lines_cleared}")