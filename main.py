import numpy as np
import random as rn
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

        pass
    def reset(self):
        self.board=np.zeros((self.height,self.width),dtype=int)
        self.score=0
        self.game_over=False
        self.bag=[]
        self._spawn_piece()
        pass
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
        display[self.piece_y:self.piece_y+height_fig,self.piece_x:self.piece_x+width_fig]+=self.current_fig
        print(display)
    def check_collision(self,piece,x,y):
        h=piece.shape[0]
        w=piece.shape[1]
        if x<0 or x+w>self.width or y+h>self.height:
            return True
        temp_board=self.board[y:y+h,x:x+w]+piece 
        if np.any(temp_board>1):
            return True 
        return False 







game=TetrisEngine()
game.render_console()