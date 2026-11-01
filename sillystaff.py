import numpy as np 
board=np.random.uniform(1,20,size=(5,5))
board[0][0]=1
board[0][2]=1
emptyboard=np.zeros((5,5))
b=np.vstack(board,emptyboard)
print(b)