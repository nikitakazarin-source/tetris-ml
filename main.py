import numpy as np
import random as rn
import pygame as pg
i=np.ones((4,1),dtype=int)
o=np.ones((2,2),dtype=int)
t=np.array(([1,1,1],[0,1,0]),dtype=int)
l=np.array(([1,0],[1,0],[1,1]),dtype=int)
l2=np.array(([0,1],[0,1],[1,1]),dtype=int)
s=np.array(([1,1,0],[0,1,1]),dtype=int)
s2=np.array(([0,1,1],[1,1,0]),dtype=int)
shapes={'T':t,'L':l,'L2':l2,'I':i,'O':o,'S':s,'S2':s2}
class TetrisEngine:
    def __init__(self,height=20,width=10):
        self.height=height
        self.width=width 
        self.reset()

    def reset(self):
        self.board = np.zeros((self.height, self.width), dtype=int)
        self.score = 0
        self.lines_cleared = 0
        self.game_over = False
        self.bag = []
        self._spawn_piece()
        return self._get_board_props(self.board)
    def _spawn_piece(self):
        if not self.bag:
            self.bag=list(shapes.keys())
            rn.shuffle(self.bag)
        current_fig_name=self.bag.pop()
        copy_shade=shapes[current_fig_name].copy()
        self.current_fig=copy_shade
        self.piece_y=0
        self.piece_x=self.width//2-self.current_fig.shape[1]//2
        if self.check_collision(self.current_fig,self.piece_x,self.piece_y):
            self.game_over=True
    def render_console(self):
        display=self.board.copy()
        height_fig=self.current_fig.shape[0]
        width_fig=self.current_fig.shape[1]
        display[self.piece_y:self.piece_y+height_fig,self.piece_x:self.piece_x+width_fig]+=self.current_fig*2
        return display
    def check_collision(self,piece,x,y):
        h=piece.shape[0]
        w=piece.shape[1]
        if x<0 or x+w>self.width or y+h>self.height:
            return True
        temp_board=self.board[y:y+h,x:x+w]+piece 
        if np.any(temp_board>1):
            return True 
        return False 
    def move (self,dx):
        if not self.game_over:
            if not self.check_collision(self.current_fig,self.piece_x+dx,self.piece_y):
                self.piece_x+=dx
        return
    def rotate(self):
        if not self.game_over:
            rotated_fig=np.rot90(self.current_fig)
            if not self.check_collision(rotated_fig,self.piece_x,self.piece_y):
                self.current_fig=rotated_fig
    def lock_piece_(self):            
        height_fig=self.current_fig.shape[0]
        width_fig=self.current_fig.shape[1]
        self.board[self.piece_y:self.piece_y+height_fig,self.piece_x:self.piece_x+width_fig]+=self.current_fig
        print(self.board)
    def step_down(self):
        if self.game_over:
            return

        if not self.check_collision(self.current_fig, self.piece_x, self.piece_y + 1):
            self.piece_y += 1
        else:
            self.lock_piece_()
            self._clear_lines()
            self._spawn_piece()
    def hard_drop(self):
        if self.game_over:
            return
        while not self.check_collision(self.current_fig,self.piece_x,self.piece_y+1):
            self.piece_y+=1
        self.step_down()
    def _clear_lines(self):
        full_rows=np.all(self.board,axis=1)
        num_cleard=np.sum(full_rows)
        if num_cleard>0:
            remaining_rows=self.board[~full_rows]
            iwannabetheboshi=np.zeros((num_cleard,self.width),dtype=int)
            self.board=np.vstack((iwannabetheboshi,remaining_rows))
            self.lines_cleared=num_cleard
            self.score+=(num_cleard**2)*100
    def step(self, action):
        prev_score = self.score

        if action == 0:
            self.move(-1)
            self.step_down()
        elif action == 1:
            self.move(1)
            self.step_down()
        elif action == 2:
            self.rotate()
            self.step_down()
        elif action == 3:
            self.step_down()
        elif action == 4:
            self.hard_drop()

        reward = float(self.score - prev_score)
        if self.game_over:
            reward -= 10.0

        state = self.render_console()
        return state, reward, self.game_over
    def _get_board_props(self, board):
        full_rows = np.all(board == 1, axis=1)
        lines_cleared = int(np.sum(full_rows))
        if lines_cleared > 0:
            remaining = board[~full_rows]
            empty_top = np.zeros((lines_cleared, self.width), dtype=int)
            board = np.vstack((empty_top, remaining))

        heights = []
        holes = 0
        for x in range(self.width):
            col = board[:, x]
            if np.any(col == 1):
                top_y = int(np.argmax(col == 1))
                heights.append(self.height - top_y)
                holes += int(np.sum(col[top_y:] == 0))
            else:
                heights.append(0)

        total_height = sum(heights)

        bumpiness = 0
        for i in range(self.width - 1):
            bumpiness += abs(heights[i] - heights[i + 1])

        return np.array([lines_cleared, holes, bumpiness, total_height], dtype=np.float32)

    def get_next_states(self):
        states = {}
        for rot in range(4):
            rotated_fig = np.rot90(self.current_fig, rot)
            h, w = rotated_fig.shape
            for x in range(self.width - w + 1):
                y = 0
                if self.check_collision(rotated_fig, x, y):
                    continue
                while not self.check_collision(rotated_fig, x, y + 1):
                    y += 1
                temp_board = self.board.copy()
                temp_board[y : y + h, x : x + w] += rotated_fig
                states[(x, rot)] = self._get_board_props(temp_board)
        return states

    def step_ai(self, action):
        x, rot = action
        self.current_fig = np.rot90(self.current_fig, rot)
        self.piece_x = x
        self.piece_y = 0

        if self.check_collision(self.current_fig, self.piece_x, self.piece_y):
            self.game_over = True
            return -10.0, True

        prev_lines = self.lines_cleared
        self.hard_drop()
        cleared_now = self.lines_cleared - prev_lines

        reward = 1.0 + (cleared_now ** 2) * 10.0
        if self.game_over:
            reward -= 10.0

        return reward, self.game_over



