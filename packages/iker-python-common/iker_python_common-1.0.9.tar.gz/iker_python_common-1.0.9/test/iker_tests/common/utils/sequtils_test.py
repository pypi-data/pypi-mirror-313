import unittest

import ddt

from iker.common.utils.sequtils import batch_yield
from iker.common.utils.sequtils import chunk, chunk_between, chunk_with_key, merge_chunks
from iker.common.utils.sequtils import deduped, grouped
from iker.common.utils.sequtils import head, init, last, tail
from iker.common.utils.sequtils import seq


@ddt.ddt
class SeqUtilsTest(unittest.TestCase):

    @ddt.data(([1], 1), ([1, 2], 1))
    @ddt.unpack
    def test_head(self, data, expect):
        self.assertEqual(expect, head(data))

    def test_head__empty(self):
        self.assertRaises(Exception, head, [])

    def test_head__none(self):
        self.assertRaises(Exception, head, None)

    @ddt.data(([1], 1), ([1, 2], 2))
    @ddt.unpack
    def test_last(self, data, expect):
        self.assertEqual(expect, last(data))

    def test_last__empty(self):
        self.assertRaises(Exception, last, [])

    def test_last__none(self):
        self.assertRaises(Exception, last, None)

    @ddt.data(([1], []), ([1, 2], [1]), ([1, 2, 3], [1, 2]))
    @ddt.unpack
    def test_init(self, data, expect):
        self.assertEqual(expect, init(data))

    def test_init__empty(self):
        self.assertEqual([], init([]))

    def test_init__none(self):
        self.assertRaises(Exception, init, None)

    @ddt.data(([1], []), ([1, 2], [2]), ([1, 2, 3], [2, 3]))
    @ddt.unpack
    def test_tail(self, data, expect):
        self.assertEqual(expect, tail(data))

    def test_tail__empty(self):
        self.assertEqual([], tail([]))

    def test_tail__none(self):
        self.assertRaises(Exception, tail, None)

    @ddt.data(
        (None, lambda x: x, []),
        ([], lambda x: x, []),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: x,
            [
                (0, [0]),
                (1, [1]),
                (2, [2]),
                (3, [3]),
                (4, [4]),
                (5, [5]),
                (6, [6]),
                (7, [7]),
                (8, [8]),
                (9, [9]),
                (10, [10]),
                (11, [11]),
                (12, [12]),
                (13, [13]),
                (14, [14]),
                (15, [15]),
                (16, [16]),
                (17, [17]),
                (18, [18]),
                (19, [19]),
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: x % 5,
            [
                (0, [0, 5, 10, 15]),
                (1, [1, 6, 11, 16]),
                (2, [2, 7, 12, 17]),
                (3, [3, 8, 13, 18]),
                (4, [4, 9, 14, 19]),
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: x % 2,
            [
                (0, [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]),
                (1, [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]),
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: None,
            [(None, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19])],
        ),
        (
            [[0] * 5, [1] * 5, [2] * 4, [3] * 4, [4] * 3, [5] * 3],
            lambda x: len(x),
            [
                (5, [[0, 0, 0, 0, 0], [1, 1, 1, 1, 1]]),
                (4, [[2, 2, 2, 2], [3, 3, 3, 3]]),
                (3, [[4, 4, 4], [5, 5, 5]]),
            ],
        ),
    )
    @ddt.unpack
    def test_grouped(self, data, key_func, expect):
        self.assertEqual(expect, grouped(data, key_func=key_func))

    @ddt.data(
        (None, lambda x: x, []),
        ([], lambda x: x, []),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: x,
            [
                [0],
                [1],
                [2],
                [3],
                [4],
                [5],
                [6],
                [7],
                [8],
                [9],
                [10],
                [11],
                [12],
                [13],
                [14],
                [15],
                [16],
                [17],
                [18],
                [19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: x % 5,
            [
                [0, 5, 10, 15],
                [1, 6, 11, 16],
                [2, 7, 12, 17],
                [3, 8, 13, 18],
                [4, 9, 14, 19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: x % 2,
            [
                [0, 2, 4, 6, 8, 10, 12, 14, 16, 18],
                [1, 3, 5, 7, 9, 11, 13, 15, 17, 19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: None,
            [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]],
        ),
        (
            [[0] * 5, [1] * 5, [2] * 4, [3] * 4, [4] * 3, [5] * 3],
            lambda x: len(x),
            [
                [[0, 0, 0, 0, 0], [1, 1, 1, 1, 1]],
                [[2, 2, 2, 2], [3, 3, 3, 3]],
                [[4, 4, 4], [5, 5, 5]],
            ],
        ),
    )
    @ddt.unpack
    def test_grouped__values_only(self, data, key_func, expect):
        self.assertEqual(expect, grouped(data, key_func=key_func, values_only=True))

    @ddt.data(
        (None, lambda x: x, []),
        ([], lambda x, y: x == y, []),
        ([0, 0, 0, 0, 0], lambda x, y: x == y, [0]),
        ([None, None, None], lambda x, y: x == y, [None]),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: x == y,
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
        ),
        (
            [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 3, 3, 3, 2, 2, 2, 1, 1, 1, 0, 0, 0],
            lambda x, y: x == y,
            [0, 1, 2, 3, 4, 3, 2, 1, 0],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: abs(x - y) < 2,
            [0, 2, 4, 6, 8, 10, 12, 14, 16, 18],
        ),
    )
    @ddt.unpack
    def test_deduped(self, data, comp_func, expect):
        self.assertEqual(expect, deduped(data, comp_func=comp_func))

    @ddt.data(
        ([], 1, []),
        ([1], 1, [[1]]),
        ([1], 2, [[1]]),
        ([1, 2, 3, 4, 5], 2, [[1, 2], [3, 4], [5]]),
        ([1, 2, 3, 4, 5, 6], 2, [[1, 2], [3, 4], [5, 6]]),
        ([1, 2, 3, 4, 5, 6], 3, [[1, 2, 3], [4, 5, 6]]),
        ([[1, 2, 3], [4, 5, 6]], 1, [[[1, 2, 3]], [[4, 5, 6]]]),
        ([[1, 2, 3], [4, 5, 6]], 2, [[[1, 2, 3], [4, 5, 6]]]),
    )
    @ddt.unpack
    def test_batch_yield(self, data, batch_size, expect):
        self.assertEqual(expect, list(batch_yield(data, batch_size)))

    @ddt.data(
        (None, lambda x: x, []),
        ([], lambda x, y: True, []),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: True,
            [
                [0],
                [1],
                [2],
                [3],
                [4],
                [5],
                [6],
                [7],
                [8],
                [9],
                [10],
                [11],
                [12],
                [13],
                [14],
                [15],
                [16],
                [17],
                [18],
                [19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: abs(head(x) - y) > 4,
            [
                [0, 1, 2, 3, 4],
                [5, 6, 7, 8, 9],
                [10, 11, 12, 13, 14],
                [15, 16, 17, 18, 19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: abs(last(x) - y) > 1,
            [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: last(x) % 2 == 0,
            [
                [0],
                [1, 2],
                [3, 4],
                [5, 6],
                [7, 8],
                [9, 10],
                [11, 12],
                [13, 14],
                [15, 16],
                [17, 18],
                [19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: last(x) % 2 == 1,
            [
                [0, 1],
                [2, 3],
                [4, 5],
                [6, 7],
                [8, 9],
                [10, 11],
                [12, 13],
                [14, 15],
                [16, 17],
                [18, 19],
            ],
        ),
    )
    @ddt.unpack
    def test_chunk(self, data, chunk_func, expect):
        self.assertEqual(expect, chunk(data, chunk_func=chunk_func))

    @ddt.data(
        (None, lambda x: x, []),
        ([], lambda x, y: True, []),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: True,
            [
                [0, 1],
                [1, 2],
                [2, 3],
                [3, 4],
                [4, 5],
                [5, 6],
                [6, 7],
                [7, 8],
                [8, 9],
                [9, 10],
                [10, 11],
                [11, 12],
                [12, 13],
                [13, 14],
                [14, 15],
                [15, 16],
                [16, 17],
                [17, 18],
                [18, 19],
                [19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: abs(head(x) - y) > 4,
            [
                [0, 1, 2, 3, 4, 5],
                [5, 6, 7, 8, 9, 10],
                [10, 11, 12, 13, 14, 15],
                [15, 16, 17, 18, 19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: abs(last(x) - y) > 1,
            [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: last(x) % 2 == 0,
            [
                [0, 1],
                [1, 2, 3],
                [3, 4, 5],
                [5, 6, 7],
                [7, 8, 9],
                [9, 10, 11],
                [11, 12, 13],
                [13, 14, 15],
                [15, 16, 17],
                [17, 18, 19],
                [19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: last(x) % 2 == 1,
            [
                [0, 1, 2],
                [2, 3, 4],
                [4, 5, 6],
                [6, 7, 8],
                [8, 9, 10],
                [10, 11, 12],
                [12, 13, 14],
                [14, 15, 16],
                [16, 17, 18],
                [18, 19],
            ],
        ),
    )
    @ddt.unpack
    def test_chunk__exclusive_end(self, data, chunk_func, expect):
        self.assertEqual(expect, chunk(data, chunk_func=chunk_func, exclusive_end=True))

    @ddt.data(
        (None, lambda x: x, []),
        ([], lambda x, y: True, []),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: True,
            [
                [0],
                [1],
                [2],
                [3],
                [4],
                [5],
                [6],
                [7],
                [8],
                [9],
                [10],
                [11],
                [12],
                [13],
                [14],
                [15],
                [16],
                [17],
                [18],
                [19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: abs(x - y) > 1,
            [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: x % 2 == 0,
            [
                [0],
                [1, 2],
                [3, 4],
                [5, 6],
                [7, 8],
                [9, 10],
                [11, 12],
                [13, 14],
                [15, 16],
                [17, 18],
                [19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: x % 2 == 1,
            [
                [0, 1],
                [2, 3],
                [4, 5],
                [6, 7],
                [8, 9],
                [10, 11],
                [12, 13],
                [14, 15],
                [16, 17],
                [18, 19],
            ],
        ),
    )
    @ddt.unpack
    def test_chunk_between(self, data, chunk_func, expect):
        self.assertEqual(expect, chunk_between(data, chunk_func=chunk_func))

    @ddt.data(
        (None, lambda x: x, []),
        ([], lambda x, y: True, []),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: True,
            [
                [0, 1],
                [1, 2],
                [2, 3],
                [3, 4],
                [4, 5],
                [5, 6],
                [6, 7],
                [7, 8],
                [8, 9],
                [9, 10],
                [10, 11],
                [11, 12],
                [12, 13],
                [13, 14],
                [14, 15],
                [15, 16],
                [16, 17],
                [17, 18],
                [18, 19],
                [19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: abs(x - y) > 1,
            [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: x % 2 == 0,
            [
                [0, 1],
                [1, 2, 3],
                [3, 4, 5],
                [5, 6, 7],
                [7, 8, 9],
                [9, 10, 11],
                [11, 12, 13],
                [13, 14, 15],
                [15, 16, 17],
                [17, 18, 19],
                [19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: x % 2 == 1,
            [
                [0, 1, 2],
                [2, 3, 4],
                [4, 5, 6],
                [6, 7, 8],
                [8, 9, 10],
                [10, 11, 12],
                [12, 13, 14],
                [14, 15, 16],
                [16, 17, 18],
                [18, 19],
            ],
        ),
    )
    @ddt.unpack
    def test_chunk_between__exclusive_end(self, data, chunk_func, expect):
        self.assertEqual(expect, chunk_between(data, chunk_func=chunk_func, exclusive_end=True))

    @ddt.data(
        (None, lambda x: x, []),
        ([], lambda x: True, []),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: x,
            [
                [0],
                [1],
                [2],
                [3],
                [4],
                [5],
                [6],
                [7],
                [8],
                [9],
                [10],
                [11],
                [12],
                [13],
                [14],
                [15],
                [16],
                [17],
                [18],
                [19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: True,
            [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: (x + 1) // 2,
            [
                [0],
                [1, 2],
                [3, 4],
                [5, 6],
                [7, 8],
                [9, 10],
                [11, 12],
                [13, 14],
                [15, 16],
                [17, 18],
                [19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: x // 2,
            [
                [0, 1],
                [2, 3],
                [4, 5],
                [6, 7],
                [8, 9],
                [10, 11],
                [12, 13],
                [14, 15],
                [16, 17],
                [18, 19],
            ],
        ),
    )
    @ddt.unpack
    def test_chunk_with_key(self, data, key_func, expect):
        self.assertEqual(expect, chunk_with_key(data, key_func=key_func))

    @ddt.data(
        (None, lambda x: x, []),
        ([], lambda x: True, []),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: x,
            [
                [0, 1],
                [1, 2],
                [2, 3],
                [3, 4],
                [4, 5],
                [5, 6],
                [6, 7],
                [7, 8],
                [8, 9],
                [9, 10],
                [10, 11],
                [11, 12],
                [12, 13],
                [13, 14],
                [14, 15],
                [15, 16],
                [16, 17],
                [17, 18],
                [18, 19],
                [19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: True,
            [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: (x + 1) // 2,
            [
                [0, 1],
                [1, 2, 3],
                [3, 4, 5],
                [5, 6, 7],
                [7, 8, 9],
                [9, 10, 11],
                [11, 12, 13],
                [13, 14, 15],
                [15, 16, 17],
                [17, 18, 19],
                [19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: x // 2,
            [
                [0, 1, 2],
                [2, 3, 4],
                [4, 5, 6],
                [6, 7, 8],
                [8, 9, 10],
                [10, 11, 12],
                [12, 13, 14],
                [14, 15, 16],
                [16, 17, 18],
                [18, 19],
            ],
        ),
    )
    @ddt.unpack
    def test_chunk_with_key__exclusive_key(self, data, key_func, expect):
        self.assertEqual(expect, chunk_with_key(data, key_func=key_func, exclusive_end=True))

    @ddt.data(
        (None, lambda x: x, []),
        ([], lambda x, y: True, []),
        (
            [
                [0],
                [1],
                [2],
                [3],
                [4],
                [5],
                [6],
                [7],
                [8],
                [9],
                [10],
                [11],
                [12],
                [13],
                [14],
                [15],
                [16],
                [17],
                [18],
                [19],
            ],
            lambda x, y: True,
            [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]],
        ),
        (
            [
                [0, 1, 2, 3, 4],
                [5, 6, 7, 8, 9],
                [10, 11, 12, 13, 14],
                [15, 16, 17, 18, 19],
            ],
            lambda x, y: abs(head(x) - head(y)) < 10,
            [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]],
        ),
        (
            [
                [0, 1, 2, 3, 4],
                [5, 6, 7, 8, 9],
                [10, 11, 12, 13, 14],
                [15, 16, 17, 18, 19],
            ],
            lambda x, y: last(x) % 10 == 4,
            [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]],
        ),
    )
    @ddt.unpack
    def test_merge_chunks(self, data, merge_func, expect):
        self.assertEqual(expect, merge_chunks(data, merge_func=merge_func))

    @ddt.data(
        (None, lambda x: x, []),
        ([], lambda x, y: True, []),
        (
            [
                [0, 1],
                [1, 2],
                [2, 3],
                [3, 4],
                [4, 5],
                [5, 6],
                [6, 7],
                [7, 8],
                [8, 9],
                [9, 10],
                [10, 11],
                [11, 12],
                [12, 13],
                [13, 14],
                [14, 15],
                [15, 16],
                [16, 17],
                [17, 18],
                [18, 19],
                [19],
            ],
            lambda x, y: True,
            [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]],
        ),
        (
            [
                [0, 1, 2, 3, 4, 5],
                [5, 6, 7, 8, 9, 10],
                [10, 11, 12, 13, 14, 15],
                [15, 16, 17, 18, 19],
            ],
            lambda x, y: abs(head(x) - head(y)) < 10,
            [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]],
        ),
        (
            [
                [0, 1, 2, 3, 4, 5],
                [5, 6, 7, 8, 9, 10],
                [10, 11, 12, 13, 14, 15],
                [15, 16, 17, 18, 19],
            ],
            lambda x, y: last(init(x)) % 10 == 4,
            [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]],
        ),
    )
    @ddt.unpack
    def test_merge_chunks__drop_exclusive_end(self, data, merge_func, expect):
        self.assertEqual(expect, merge_chunks(data, merge_func=merge_func, drop_exclusive_end=True))

    @ddt.data(
        ([0], 0, [0]),
        ([1, 2, 3, 4, 5], 0, [1]),
        ([1, 2, 3, 4, 5], -1, [5]),
        ([1, 2, 3, 4, 5], slice(None, 1), [1]),
        ([1, 2, 3, 4, 5], slice(1, None), [2, 3, 4, 5]),
        ([1, 2, 3, 4, 5], slice(None, -1), [1, 2, 3, 4]),
        ([1, 2, 3, 4, 5], slice(-1, None), [5]),
        ([1, 2, 3, 4, 5], slice(1, -1), [2, 3, 4]),
        ([1, 2, 3, 4, 5], slice(1, -1, 2), [2, 4]),
    )
    @ddt.unpack
    def test_seq_builtin_getitem(self, data, item, expect):
        actual = seq(data)[item]
        self.assertEqual(actual.data, expect)

    @ddt.data(
        ([], 0),
        ([0], 1),
        ([1, 2, 3, 4, 5], 5),
    )
    @ddt.unpack
    def test_seq_builtin_len(self, data, expect):
        actual = len(seq(data))
        self.assertEqual(actual, expect)

    @ddt.data(
        ([], 0, False),
        ([0], 0, True),
        ([0], -1, False),
        ([1, 2, 3, 4, 5], 0, False),
        ([1, 2, 3, 4, 5], 1, True),
        ([1, 2, 3, 4, 5], -1, False),
    )
    @ddt.unpack
    def test_seq_builtin_contains(self, data, item, expect):
        actual = item in seq(data)
        self.assertEqual(actual, expect)

    @ddt.data(
        ([], []),
        ([0], [0]),
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),
    )
    @ddt.unpack
    def test_seq_builtin_iter(self, data, expect):
        actual = list(x for x in seq(data))
        self.assertEqual(actual, expect)

    @ddt.data(
        ([], []),
        ([0], [0]),
        ([1, 2, 3, 4, 5], [5, 4, 3, 2, 1]),
    )
    @ddt.unpack
    def test_seq_builtin_reversed(self, data, expect):
        actual = list(x for x in reversed(seq(data)))
        self.assertEqual(actual, expect)

    @ddt.data(
        ([], 0, 0),
        ([0], 0, 1),
        ([0], -1, 0),
        ([0, 0, 0], 0, 3),
        ([0, 0, 0], -1, 0),
        ([1, 2, 3, 4, 5], 0, 0),
        ([1, 2, 3, 4, 5], 1, 1),
        ([1, 2, 3, 4, 5], -1, 0),
    )
    @ddt.unpack
    def test_seq_count(self, data, item, expect):
        actual = seq(data).count(item)
        self.assertEqual(actual, expect)

    @ddt.data(
        ([], lambda x: True, 0),
        ([0], lambda x: True, 1),
        ([0], lambda x: False, 0),
        ([0], lambda x: x % 2 == 0, 1),
        ([0], lambda x: x % 2 == 1, 0),
        ([0, 0, 0], lambda x: True, 3),
        ([0, 0, 0], lambda x: False, 0),
        ([0, 0, 0], lambda x: x % 2 == 0, 3),
        ([0, 0, 0], lambda x: x % 2 == 1, 0),
        ([1, 2, 3, 4, 5], lambda x: x % 2 == 0, 2),
        ([1, 2, 3, 4, 5], lambda x: x % 2 == 1, 3),
        ([1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5], lambda x: x % 2 == 0, 6),
        ([1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5], lambda x: x % 2 == 1, 9),
    )
    @ddt.unpack
    def test_seq_count_if(self, data, func, expect):
        actual = seq(data).count_if(func)
        self.assertEqual(actual, expect)

    @ddt.data(
        ([], 0, lambda x, y: x, []),
        ([], None, lambda x, y: x, []),
        ([0], 1, lambda x, y: x + y, [1]),
        ([1, 2, 3, 4, 5], 1, lambda x, y: x + y, [2, 4, 7, 11, 16]),
        ([1, 2, 3, 4, 5], 1, lambda x, y: x * y, [1, 2, 6, 24, 120]),
        ([1, 2, 3, 4, 5], 0, lambda x, y: x * 10 + y, [1, 12, 123, 1234, 12345]),
    )
    @ddt.unpack
    def test_seq_scan_left(self, data, zero, func, expect):
        actual = seq(data).scan_left(zero, func)
        self.assertEqual(actual.data, expect)

    @ddt.data(
        ([], 0, lambda x, y: x, []),
        ([], None, lambda x, y: x, []),
        ([0], 1, lambda x, y: x + y, [1]),
        ([1, 2, 3, 4, 5], 1, lambda x, y: x + y, [16, 15, 13, 10, 6]),
        ([1, 2, 3, 4, 5], 1, lambda x, y: x * y, [120, 120, 60, 20, 5]),
        ([1, 2, 3, 4, 5], 0, lambda x, y: x * 10 + y, [54321, 5432, 543, 54, 5]),
    )
    @ddt.unpack
    def test_seq_scan_right(self, data, zero, func, expect):
        actual = seq(data).scan_right(zero, func)
        self.assertEqual(actual.data, expect)

    @ddt.data(
        ([], lambda x: x, []),
        ([0], lambda x: x, [0]),
        ([1, 2, 3, 4, 5], lambda x: x * 2, [2, 4, 6, 8, 10]),
        ([1, 2, 3, 4, 5], lambda x: x ** 2, [1, 4, 9, 16, 25]),
    )
    @ddt.unpack
    def test_seq_map(self, data, func, expect):
        actual = seq(data).map(func)
        self.assertEqual(actual.data, expect)

    @ddt.data(
        ([], 0, lambda x, y: x, [0]),
        ([], None, lambda x, y: x, []),
        ([0], 1, lambda x, y: x + y, [1]),
        ([1, 2, 3, 4, 5], 1, lambda x, y: x + y, [16]),
        ([1, 2, 3, 4, 5], 1, lambda x, y: x * y, [120]),
        ([1, 2, 3, 4, 5], 0, lambda x, y: x * 10 + y, [12345]),
    )
    @ddt.unpack
    def test_seq_fold_left(self, data, zero, func, expect):
        actual = seq(data).fold_left(zero, func)
        self.assertEqual(actual.data, expect)

    @ddt.data(
        ([], 0, lambda x, y: x, [0]),
        ([0], 1, lambda x, y: x + y, [1]),
        ([1, 2, 3, 4, 5], 1, lambda x, y: x + y, [16]),
        ([1, 2, 3, 4, 5], 1, lambda x, y: x * y, [120]),
        ([1, 2, 3, 4, 5], 0, lambda x, y: x * 10 + y, [54321]),
    )
    @ddt.unpack
    def test_seq_fold_right(self, data, zero, func, expect):
        actual = seq(data).fold_right(zero, func)
        self.assertEqual(actual.data, expect)

    @ddt.data(
        ([], lambda x, y: x, []),
        ([0], lambda x, y: x + y, [0]),
        ([1, 2, 3, 4, 5], lambda x, y: x + y, [15]),
        ([1, 2, 3, 4, 5], lambda x, y: y, [5]),
    )
    @ddt.unpack
    def test_seq_reduce(self, data, func, expect):
        actual = seq(data).reduce(func)
        self.assertEqual(actual.data, expect)

    @ddt.data(
        ([], None, []),
        ([0], None, [0]),
        ([1, 2, 3, 4, 5], None, [5]),
        ([1, 2, 3, 4, 5], lambda x, y: True, [1]),
        ([1, 2, 3, 4, 5], lambda x, y: False, [5]),
    )
    @ddt.unpack
    def test_seq_max(self, data, func, expect):
        actual = seq(data).max(func)
        self.assertEqual(actual.data, expect)

    @ddt.data(
        ([], None, []),
        ([0], None, [0]),
        ([1, 2, 3, 4, 5], None, [1]),
        ([1, 2, 3, 4, 5], lambda x, y: True, [1]),
        ([1, 2, 3, 4, 5], lambda x, y: False, [5]),
    )
    @ddt.unpack
    def test_seq_min(self, data, func, expect):
        actual = seq(data).min(func)
        self.assertEqual(actual.data, expect)

    @ddt.data(
        ([], lambda x: x % 2, []),
        ([0], lambda x: x % 2, [(0, [0])]),
        ([1, 2, 3, 4, 5], lambda x: x % 2, [(0, [2, 4]), (1, [1, 3, 5])]),
        ([1, 2, 3, 4, 5], lambda x: x * 2, [(2, [1]), (4, [2]), (6, [3]), (8, [4]), (10, [5])]),
    )
    @ddt.unpack
    def test_seq_group(self, data, func, expect):
        actual = seq(data).group(func)
        self.assertEqual(actual.data, expect)

    @ddt.data(
        ([], []),
        ([(0, "")], [0]),
        ([(1, "a"), (2, "b"), (3, "c"), (4, "d"), (5, "e")], [1, 2, 3, 4, 5]),
    )
    @ddt.unpack
    def test_seq_keys(self, data, expect):
        actual = seq(data).keys()
        self.assertEqual(actual.data, expect)

    @ddt.data(
        ([], []),
        ([(0, "")], [""]),
        ([(1, "a"), (2, "b"), (3, "c"), (4, "d"), (5, "e")], ["a", "b", "c", "d", "e"]),
    )
    @ddt.unpack
    def test_seq_values(self, data, expect):
        actual = seq(data).values()
        self.assertEqual(actual.data, expect)

    @ddt.data(
        ([], []),
        ([(0, "")], [("", 0)]),
        ([(1, "a"), (2, "b"), (3, "c"), (4, "d"), (5, "e")], [("a", 1), ("b", 2), ("c", 3), ("d", 4), ("e", 5)]),
    )
    @ddt.unpack
    def test_seq_swap(self, data, expect):
        actual = seq(data).swap()
        self.assertEqual(actual.data, expect)

    @ddt.data(
        ([], []),
        ([[]], []),
        ([[0]], [0]),
        ([[1, 2, 3, 4, 5]], [1, 2, 3, 4, 5]),
        ([[], [1], [2], [3], [4], [5], []], [1, 2, 3, 4, 5]),
        ([[], [1, 2, 3, 4, 5], []], [1, 2, 3, 4, 5]),
    )
    @ddt.unpack
    def test_seq_flatten(self, data, expect):
        actual = seq(data).flatten()
        self.assertEqual(actual.data, expect)

    @ddt.data(
        ([], [], []),
        ([0], [], []),
        ([], [0], []),
        ([0], [0], [(0, 0)]),
        ([0, 0], [0], [(0, 0)]),
        ([0], [0, 0], [(0, 0)]),
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]),
        ([1, 2, 3, 4, 5], [5, 4, 3, 2, 1], [(1, 5), (2, 4), (3, 3), (4, 2), (5, 1)]),
        ([1, 2, 3, 4, 5], ["a", "b", "c", "d", "e"], [(1, "a"), (2, "b"), (3, "c"), (4, "d"), (5, "e")]),
        (["a", "b", "c", "d", "e"], [1, 2, 3, 4, 5], [("a", 1), ("b", 2), ("c", 3), ("d", 4), ("e", 5)]),
    )
    @ddt.unpack
    def test_seq_zip(self, a, b, expect):
        actual = seq(a).zip(seq(b))
        self.assertEqual(actual.data, expect)

    @ddt.data(
        ([], [], 0, []),
        ([0], [], None, [(0, None)]),
        ([0], [], 1, [(0, 1)]),
        ([], [0], None, [(None, 0)]),
        ([], [0], 1, [(1, 0)]),
        ([0], [0], 0, [(0, 0)]),
        ([0, 0], [0], None, [(0, 0), (0, None)]),
        ([0, 0], [0], 1, [(0, 0), (0, 1)]),
        ([0], [0, 0], None, [(0, 0), (None, 0)]),
        ([0], [0, 0], 1, [(0, 0), (1, 0)]),
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], None, [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]),
        ([1, 2, 3, 4, 5], [5, 4, 3, 2, 1], None, [(1, 5), (2, 4), (3, 3), (4, 2), (5, 1)]),
        ([1, 2, 3, 4, 5, 6, 7], [1, 2, 3, 4, 5], 0, [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 0), (7, 0)]),
        ([1, 2, 3, 4, 5, 6, 7], [5, 4, 3, 2, 1], 0, [(1, 5), (2, 4), (3, 3), (4, 2), (5, 1), (6, 0), (7, 0)]),
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6, 7], 0, [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (0, 6), (0, 7)]),
        ([1, 2, 3, 4, 5], [7, 6, 5, 4, 3, 2, 1], 0, [(1, 7), (2, 6), (3, 5), (4, 4), (5, 3), (0, 2), (0, 1)]),
        ([1, 2, 3, 4, 5], ["a", "b", "c", "d", "e"], None, [(1, "a"), (2, "b"), (3, "c"), (4, "d"), (5, "e")]),
        (["a", "b", "c", "d", "e"], [1, 2, 3, 4, 5], None, [("a", 1), ("b", 2), ("c", 3), ("d", 4), ("e", 5)]),
        (
            [1, 2, 3, 4, 5],
            ["a", "b", "c", "d", "e", "f", "g"],
            0,
            [(1, "a"), (2, "b"), (3, "c"), (4, "d"), (5, "e"), (0, "f"), (0, "g")],
        ),
        (
            [1, 2, 3, 4, 5],
            ["a", "b", "c", "d", "e", "f", "g"],
            "-",
            [(1, "a"), (2, "b"), (3, "c"), (4, "d"), (5, "e"), ("-", "f"), ("-", "g")],
        ),
        (
            [1, 2, 3, 4, 5, 6, 7],
            ["a", "b", "c", "d", "e"],
            "-",
            [(1, "a"), (2, "b"), (3, "c"), (4, "d"), (5, "e"), (6, "-"), (7, "-")],
        ),
        (
            [1, 2, 3, 4, 5, 6, 7],
            ["a", "b", "c", "d", "e"],
            0,
            [(1, "a"), (2, "b"), (3, "c"), (4, "d"), (5, "e"), (6, 0), (7, 0)],
        ),
    )
    @ddt.unpack
    def test_seq_zip_fill(self, a, b, fill, expect):
        actual = seq(a).zip_fill(seq(b), fill)
        self.assertEqual(actual.data, expect)
