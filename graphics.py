import pygame
import torch
from main import TetrisEngine
from train import DQNAgent

CELL_SIZE = 30
WIDTH = 300
HIGHT = 600

game = TetrisEngine()
agent = DQNAgent()

agent.model.load_state_dict(torch.load("best_tetris_model.pth"))
agent.model.eval()
agent.epsilon = 0.0

pygame.init()
screen = pygame.display.set_mode((WIDTH, HIGHT))
clock = pygame.time.Clock()

def draw_board():
    screen.fill((20, 20, 20))
    grid = game.render_console()
    for y in range(game.height):
        for x in range(game.width):
            val = grid[y, x]
            if val > 0:
                color = (200, 200, 200) if val == 1 else (0, 255, 255)
                pygame.draw.rect(
                    screen,
                    color,
                    (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1)
                )
    pygame.display.set_caption(f"Score: {game.score} | Lines: {game.lines_cleared}")
    pygame.display.flip()

running = True
while not game.game_over and running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    next_states = game.get_next_states()
    if not next_states:
        break

    action = agent.select_action(next_states)
    x, rot = action

    game.current_fig = game.current_fig.copy()
    for _ in range(rot):
        game.current_fig = game.current_fig.T[::-1]
    game.piece_x = x
    game.piece_y = 0

    draw_board()
    pygame.time.delay(80)

    game.hard_drop()
    draw_board()
    clock.tick(15)

pygame.quit()
print(f"Итоговый счет ИИ: {game.score} | Сожжено линий: {game.lines_cleared}")