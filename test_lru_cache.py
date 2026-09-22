"""
test_lru_cache.py
------------------
Unit tests for Cache. Run with:  python3 -m unittest -v
"""

import unittest
from cache import Cache


class TestCache(unittest.TestCase):

    def test_basic_get_put(self):
        c = Cache(2)
        c.put("A", 10)
        c.put("B", 20)
        self.assertEqual(c.get("A"), 10)

    def test_eviction_on_overflow(self):
        c = Cache(2)
        c.put("A", 10)
        c.put("B", 20)
        c.get("A")          # A becomes most recently used
        c.put("C", 30)       # capacity full -> evicts B (least recently used)
        self.assertEqual(c.get("B"), -1)
        self.assertEqual(c.get("C"), 30)
        self.assertEqual(c.get("A"), 10)

    def test_missing_key_returns_negative_one(self):
        c = Cache(3)
        self.assertEqual(c.get("nope"), -1)

    def test_update_existing_key_refreshes_recency(self):
        c = Cache(2)
        c.put("A", 1)
        c.put("B", 2)
        c.put("A", 100)      # update -> A is now most recently used
        c.put("C", 3)         # evicts B, not A
        self.assertEqual(c.get("A"), 100)
        self.assertEqual(c.get("B"), -1)
        self.assertEqual(c.get("C"), 3)

    def test_capacity_one(self):
        c = Cache(1)
        c.put("X", 1)
        c.put("Y", 2)         # immediately evicts X
        self.assertEqual(c.get("X"), -1)
        self.assertEqual(c.get("Y"), 2)

    def test_invalid_capacity_raises(self):
        with self.assertRaises(ValueError):
            Cache(0)
        with self.assertRaises(ValueError):
            Cache(-5)

    def test_len_and_contains(self):
        c = Cache(2)
        c.put("A", 1)
        self.assertIn("A", c)
        self.assertEqual(len(c), 1)
        c.put("B", 2)
        c.put("C", 3)  # evicts A
        self.assertNotIn("A", c)
        self.assertEqual(len(c), 2)


if __name__ == "__main__":
    unittest.main()