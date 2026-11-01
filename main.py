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
        self.board=np.zeros((self.height,self.width),dtype=int) 
        self.score=0
        self.game_over=False
        self.bag=[]
        self._spawn_piece()
        self.lines_cleared=0
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



