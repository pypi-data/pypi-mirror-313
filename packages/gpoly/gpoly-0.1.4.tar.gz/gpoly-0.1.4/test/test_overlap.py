import numpy as np
import copy

a = np.array([[0, 0, 1],
              [0, 1, 1],
              [0, 0, 1]])

b = np.array([[0, 0, 0],
              [0, 1, 0],
              [1, 1, 1]])

c = np.array([[1, 0, 0],
              [1, 1, 0],
              [1, 0, 0]])

masks = [a, b, c]

# overlapping
overlaps = []
for i, maski in enumerate(masks):
    for j, maskj in enumerate(masks):
        if not maski.astype(bool) is maskj.astype(bool):
            if j > i:
                overlap = maski.astype(bool) & maskj.astype(bool)
                if overlap.any():
                    overlaps.append((i, j, overlap))

for overlap in overlaps:
    masks[overlap[1]][overlap[-1]] = 0
