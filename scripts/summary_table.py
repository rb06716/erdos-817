#!/usr/bin/env python3
"""Summary table: exact values / upper bounds for g_3(n), Korsky's bandwidth lower bound b_n, ratios."""
import math
T = [1]
def trinom(m):  # central trinomial coefficient [x^m](1+x+x^2)^m
    return sum(math.comb(m, k) * math.comb(m - k, k) for k in range(m // 2 + 1))
T = [trinom(m) for m in range(20)]
def b(n): return (T[n] - 1) // 2 + sum(T[:n])
exact = {1: 1, 2: 3, 3: 8, 4: 22, 5: 60, 6: 168, 7: 474}
upper = {8: 1368, 9: 3974, 10: 11578, 11: 34088, 12: 100422}
print('| n | g_3(n) | b_n (Korsky) | g - b_n | g/3^n | g*sqrt(n)/3^n | previous upper bound |')
print('| --- | --- | --- | --- | --- | --- | --- |')
prev = None
for n in range(1, 13):
    g = exact.get(n, upper.get(n)); tag = '' if n in exact else '<= '
    pb = '' if n <= 6 else ('504 = 3*168' if n == 7 else '%d = (168/729)*3^n' % (168 * 3 ** (n - 6)))
    print('| %d | %s%d | %d | %s%d | %s%.4f | %s%.4f | %s |' % (n, tag, g, b(n), tag, g - b(n), tag, g / 3 ** n, tag, g * math.sqrt(n) / 3 ** n, pb))
print('central trinomial T_0..T_12 =', T[:13])
