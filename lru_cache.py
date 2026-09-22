"""
lru_cache.py
------------
A from-scratch Least Recently Used (LRU) Cache.

DESIGN
======
Two data structures work together so both get() and put() run in
O(1) average time:

1. A hash map (`self._map`): key -> node.  Gives O(1) lookup of any
   key without scanning anything.

2. A doubly linked list that keeps nodes ordered by recency:

       FRONT (most recently used) <-> ... <-> BACK (least recently used)

   A doubly linked list lets you splice a node out of the middle and
   re-insert it at the front in O(1), with no shifting of other
   elements (unlike a plain list/array).

Two permanent sentinel nodes (`self._front`, `self._back`) bookend the
real entries. They never hold data themselves -- they just give every
real node a guaranteed prev/next neighbor, so insert/remove code never
needs an "is the list empty?" special case.

WHY NOT collections.OrderedDict?
   OrderedDict.move_to_end() + popitem(last=False) would solve this in
   a handful of lines, but it just delegates the whole problem to a
   built-in that already *is* an LRU-ordered structure. Writing the
   linked list by hand is what actually demonstrates the O(1) design.

TIME COMPLEXITY
   get(key): O(1) average -- one dict lookup + O(1) list splice.
   put(key, value): O(1) average -- one dict lookup/insert + O(1)
                     splice, and eviction removes a known node (the
                     one before the back sentinel), not a search.

SPACE COMPLEXITY
   O(capacity) -- exactly one dict entry + one linked-list node per
   cached key, capped at `capacity` entries.
"""


class _Node:
    """A single cache entry, doubling as a linked-list node."""
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity: int):
        if not isinstance(capacity, int) or capacity <= 0:
            raise ValueError("capacity must be a positive integer")

        self.capacity = capacity
        self._map = {}  # key -> _Node

        # Sentinels bookend the chain: front.next ... back.prev
        self._front = _Node()  # most-recently-used side
        self._back = _Node()   # least-recently-used side
        self._front.next = self._back
        self._back.prev = self._front

    # ---------- internal helpers ----------
    def _detach(self, node: _Node) -> None:
        """Unlink a node from wherever it currently sits."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _push_front(self, node: _Node) -> None:
        """Insert a node right after the front sentinel (MRU slot)."""
        node.next = self._front.next
        node.prev = self._front
        self._front.next.prev = node
        self._front.next = node

    def _touch(self, node: _Node) -> None:
        """Mark a node as most recently used."""
        self._detach(node)
        self._push_front(node)

    # ---------- public API ----------
    def get(self, key):
        node = self._map.get(key)
        if node is None:
            return -1
        self._touch(node)
        return node.value

    def put(self, key, value) -> None:
        existing = self._map.get(key)
        if existing is not None:
            existing.value = value
            self._touch(existing)
            return

        if len(self._map) >= self.capacity:
            lru_node = self._back.prev       # node just before back sentinel
            self._detach(lru_node)
            del self._map[lru_node.key]

        new_node = _Node(key, value)
        self._map[key] = new_node
        self._push_front(new_node)

    # ---------- niceties ----------
    def __len__(self):
        return len(self._map)

    def __contains__(self, key):
        return key in self._map

    def __repr__(self):
        items = []
        node = self._front.next
        while node is not self._back:
            items.append(f"{node.key!r}: {node.value!r}")
            node = node.next
        return "LRUCache([" + ", ".join(items) + "])  # MRU -> LRU"
