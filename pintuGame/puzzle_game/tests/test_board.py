import unittest

from src.board import Board


class BoardTests(unittest.TestCase):
    def test_initial_board_is_solved_with_blank_last(self):
        board = Board(3)
        self.assertTrue(board.is_solved())
        self.assertIsNone(board.grid[2][2])
        tile = board.grid[0][0]
        self.assertEqual(tile.tile_id, 0)
        self.assertEqual((tile.target_row, tile.target_col, tile.row, tile.col, tile.rotation), (0, 0, 0, 0, 0))

    def test_only_adjacent_tile_moves(self):
        board = Board(3)
        before = board.snapshot()
        self.assertFalse(board.move(0, 0))
        self.assertEqual(board.snapshot(), before)
        self.assertFalse(board.move(2, 2))
        self.assertEqual(board.snapshot(), before)
        self.assertTrue(board.move(2, 1))
        self.assertEqual(board.blank_pos, (2, 1))

    def test_legal_moves_from_solved(self):
        board = Board(4)
        self.assertEqual(set(board.legal_moves()), {(2, 3), (3, 2)})

    def test_shuffle_is_solvable_and_not_solved(self):
        for size in (3, 4, 5):
            board = Board(size)
            moves = board.shuffle(80, seed=42)
            self.assertGreaterEqual(len(moves), 80)
            self.assertTrue(board.is_solvable())
            self.assertFalse(board.is_solved())

    def test_snapshot_roundtrip(self):
        board = Board(3)
        board.shuffle(20, seed=7)
        snapshot = board.snapshot()
        restored = Board(3)
        restored.load_snapshot(snapshot)
        self.assertEqual(restored.snapshot(), snapshot)


if __name__ == "__main__":
    unittest.main()
