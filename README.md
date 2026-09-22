# LRU Cache (Python)

A Least Recently Used (LRU) cache implemented from scratch — no
`collections.OrderedDict`, no third-party libraries. Supports:

- `LRUCache(capacity)`
- `get(key)` → value, or `-1` if not present
- `put(key, value)` → insert or update

## Data structures used, and why

The cache combines **two** structures so both operations stay O(1):

1. **Hash map** (`dict`): `key -> node`. Gives instant (O(1)) lookup
   of any key — no scanning.
2. **Doubly linked list**: keeps every entry ordered by recency,
   from most-recently-used (front) to least-recently-used (back).
   A doubly linked list is the key trick — because each node knows
   its `prev` and `next`, you can cut a node out of the middle of the
   list and drop it back in at the front in O(1), with no shifting of
   other elements the way an array/Python list would require.

Two permanent **sentinel nodes** (`_front`, `_back`) bookend the real
entries. They hold no data — they just guarantee every real node has
a neighbor on both sides, so insert/remove code never needs to
special-case an empty or single-item list.

### Why not `OrderedDict`?

`OrderedDict.move_to_end()` + `popitem(last=False)` would solve this
in a handful of lines — but that's outsourcing the entire problem to
a built-in that's already an LRU-ordered structure. Building the
linked list by hand is what actually shows the underlying design.

## How LRU ordering is maintained

- On `get(key)`: if found, the node is unlinked from its current spot
  and re-inserted at the front (`_touch`) — that's what "most
  recently used" means here.
- On `put(key, value)`:
  - If the key already exists, update its value and `_touch` it (same
    as get — an update counts as a use).
  - If it's a new key and the cache is **full**, the node just before
    the back sentinel (`_back.prev`) is the least-recently-used entry
    — it's detached and removed from the dict in O(1) (no search
    needed, we always know exactly where it is).
  - The new node is inserted at the front and added to the dict.

## Complexity

| Operation | Time (avg) | Why                                                                                     |
| --------- | ---------- | --------------------------------------------------------------------------------------- |
| `get`     | O(1)       | one dict lookup + O(1) list splice                                                      |
| `put`     | O(1)       | one dict lookup/insert + O(1) splice; eviction removes a known node, not a searched one |

**Space:** O(capacity) — exactly one dict entry + one linked-list node
per cached item, capped at `capacity`.

## How to run

Requires Python 3.7+, no dependencies.

```bash
# Run the example/demo (prints live output, matches the assignment example)
python demo.py

# Run the unit test suite
python -m unittest -v
```

### Files

- `lru_cache.py` — the `LRUCache` implementation
- `demo.py` — runs the assignment's example scenario + a couple of
  edge cases, printing real output
- `test_lru_cache.py` — unit tests (7 cases: basic ops, eviction,
  missing keys, update-refreshes-recency, capacity=1, invalid
  capacity, `len`/`in`)

### Claude AI tool

### Code generation prompts

```text
Write a Python LRU cache implementation from scratch using a hash map and doubly linked list. It must support get(key), put(key, value), and eviction of the least recently used item when capacity is reached. Return only the final Python code.

Create a clean Python class for an LRU cache with O(1) get and put operations. Include docstrings, proper edge-case handling, and a simple example usage.

Generate unit tests for an LRU cache covering normal use, key updates, eviction, missing keys, and capacity=1. Use Python's unittest framework.
```

### Bug-fix prompts

```text
Review this LRU cache implementation and fix any logic errors. Keep the same API and complexity, but correct the eviction, recency, and update behavior. Explain each fix briefly.

This Python LRU cache is failing certain tests. Find the bug, fix it, and provide the corrected code with a short explanation of why the issue happened.

Debug this LRU cache implementation and make it pass edge-case tests for invalid capacity, duplicate updates, and eviction ordering.
```

### Refactor prompts

```text
Refactor this LRU cache code to be cleaner and easier to understand without changing its behavior or O(1) performance.

Improve the structure of this Python LRU cache by simplifying methods, reducing duplication, and making the linked-list logic clearer.
```
