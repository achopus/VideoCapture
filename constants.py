import numpy as np

B = 64
S = 1024

S-= 2 * B


DEFINED_CORNERS = np.array([[0,     0],
                            [S,   0],
                            [S, S],
                            [0,   S]])

DEFINED_CORNERS += B

PAD = 2 * B

frame_width = S + 2 * B
frame_height = S + 2 * B
