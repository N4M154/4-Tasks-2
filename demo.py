"""
demo.py
-------
Runs the exact example from the assignment sheet and prints real,
live output from LRUCache -- nothing here is hand-typed.
"""

from lru_cache import LRUCache


def show(expr, result=None):
    if result is None:
        print(f">>> {expr}")
    else:
        print(f">>> {expr}\n{result}")


print("=== Assignment example ===\n")

print(">>> cache = LRUCache(2)")
cache = LRUCache(2)

print(">>> cache.put('A', 10)")
cache.put("A", 10)

print(">>> cache.put('B', 20)")
cache.put("B", 20)

print(f">>> cache.get('A')\n{cache.get('A')}   # expected 10")

print(">>> cache.put('C', 30)   # capacity=2 is full -> evicts 'B' (LRU)")
cache.put("C", 30)

print(f">>> cache.get('B')\n{cache.get('B')}   # expected -1 (evicted)")
print(f">>> cache.get('C')\n{cache.get('C')}   # expected 30")
print(f">>> cache.get('A')\n{cache.get('A')}   # expected 10")

print("\n=== A couple of extra edge cases ===\n")

print(">>> cache2 = LRUCache(1)")
cache2 = LRUCache(1)
cache2.put("X", 1)
print(f">>> cache2.get('X')\n{cache2.get('X')}   # expected 1")
cache2.put("Y", 2)  # evicts X immediately, capacity is 1
print(f">>> cache2.get('X')\n{cache2.get('X')}   # expected -1")
print(f">>> cache2.get('Y')\n{cache2.get('Y')}   # expected 2")

print("\n>>> cache.put('A', 999)   # update existing key + refresh recency")
cache.put("A", 999)
print(f">>> cache.get('A')\n{cache.get('A')}   # expected 999")

try:
    LRUCache(0)
except ValueError as e:
    print(f"\n>>> LRUCache(0) -> raised ValueError: {e}")
