import numpy as np

DEFINED_CORNERS = np.array([[ 400,   50],
                            [1350,   50],
                            [1350, 1000],
                            [ 400, 1000]])


y0 = 50
y1 = 1000
x0 = 400
x1 = 1350
B = 50
frame_width = (x1 - x0) + 2 * B
frame_height = (y1 - y0) + 2 * B