"""
demo.py
-------
Runs the exact example from the assignment sheet and prints real,
live output from Cache -- nothing here is hand-typed or edited.
"""

from cache import Cache

print('cache = Cache(2)')
cache = Cache(2)

print('cache.put("A", 10)')
cache.put("A", 10)

print('cache.put("B", 20)')
cache.put("B", 20)

print(f'cache.get("A")      -> {cache.get("A")}')

print('cache.put("C", 30)')
cache.put("C", 30)

print(f'cache.get("B")      -> {cache.get("B")}')
print(f'cache.get("C")      -> {cache.get("C")}')
print(f'cache.get("A")      -> {cache.get("A")}')