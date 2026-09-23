"""
offset_recursion.py -- greedy first-hole continuation of the known extremal chains (starting from the n = 3, 5,
6, 7 optima). It prints the upper bounds obtained by always taking the least admissible hole. Constructions only.
"""
from hole_dp import first_hole
import sys
starts = {3: ([1, 3], 8), 5: ([1, 3, 8, 22], 60), 6: ([4, 6, 9, 23, 61], 168), 6.5: ([2, 6, 9, 23, 61], 168), 7: ([8, 9, 15, 27, 65, 172], 474)}
for key, (B, M) in starts.items():
    n = len(B) + 1
    line = f'start n={n} B={B} M={M}:'
    B = list(B)
    for step in range(3 if key < 7 else 5):
        B = sorted(B + [M]); n += 1
        M2, ok = first_hole(B)
        if not ok:
            line += f' | n={n}: B violates (i)'; break
        M = M2
        line += f' | n={n}: M={M}'
    print(line, flush=True)
