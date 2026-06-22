from dataclasses import asdict, dataclass
import random


@dataclass
class Tile:
    tile_id: int
    target_row: int
    target_col: int
    row: int
    col: int
    rotation: int = 0


class Board:
    def __init__(self, size=3, rotation_mode=False):
        if size not in (3, 4, 5):
            raise ValueError("size must be 3, 4, or 5")
        self.size = size
        self.rotation_mode = rotation_mode
        self.grid = []
        self.blank_pos = (size - 1, size - 1)
        self.reset()

    def reset(self):
        self.grid = []
        for row in range(self.size):
            line = []
            for col in range(self.size):
                if row == self.size - 1 and col == self.size - 1:
                    line.append(None)
                else:
                    tile_id = row * self.size + col
                    line.append(Tile(tile_id, row, col, row, col, 0))
            self.grid.append(line)
        self.blank_pos = (self.size - 1, self.size - 1)

    def snapshot(self):
        return {
            "size": self.size,
            "rotation_mode": self.rotation_mode,
            "blank_pos": list(self.blank_pos),
            "grid": [[asdict(tile) if tile else None for tile in row] for row in self.grid],
        }

    def load_snapshot(self, snapshot):
        self.size = int(snapshot["size"])
        self.rotation_mode = bool(snapshot.get("rotation_mode", False))
        self.blank_pos = tuple(snapshot["blank_pos"])
        self.grid = [[Tile(**tile) if tile else None for tile in row] for row in snapshot["grid"]]

    def in_bounds(self, row, col):
        return 0 <= row < self.size and 0 <= col < self.size

    def is_adjacent_to_blank(self, row, col):
        br, bc = self.blank_pos
        return abs(row - br) + abs(col - bc) == 1

    def legal_moves(self):
        br, bc = self.blank_pos
        candidates = [(br - 1, bc), (br + 1, bc), (br, bc - 1), (br, bc + 1)]
        return [(r, c) for r, c in candidates if self.in_bounds(r, c) and self.grid[r][c] is not None]

    def move(self, row, col):
        if not self.in_bounds(row, col):
            return False
        tile = self.grid[row][col]
        if tile is None or not self.is_adjacent_to_blank(row, col):
            return False
        br, bc = self.blank_pos
        self.grid[br][bc] = tile
        self.grid[row][col] = None
        tile.row, tile.col = br, bc
        self.blank_pos = (row, col)
        return True

    def shuffle(self, moves=None, seed=None):
        rng = random.Random(seed) if seed is not None else random
        count = moves if moves is not None else self.size * self.size * 24
        previous_blank = None
        performed = []
        for _ in range(count):
            legal = self.legal_moves()
            if previous_blank in legal and len(legal) > 1:
                legal.remove(previous_blank)
            row, col = rng.choice(legal)
            tile = self.grid[row][col]
            old_blank = self.blank_pos
            self.move(row, col)
            performed.append({"tile_id": tile.tile_id, "from": [row, col], "to": list(old_blank)})
            previous_blank = old_blank
        if self.is_solved():
            row, col = rng.choice(self.legal_moves())
            tile = self.grid[row][col]
            old_blank = self.blank_pos
            self.move(row, col)
            performed.append({"tile_id": tile.tile_id, "from": [row, col], "to": list(old_blank)})
        return performed

    def is_solved(self):
        for row in range(self.size):
            for col in range(self.size):
                tile = self.grid[row][col]
                if row == self.size - 1 and col == self.size - 1:
                    if tile is not None:
                        return False
                    continue
                if tile is None or tile.target_row != row or tile.target_col != col:
                    return False
                if self.rotation_mode and tile.rotation % 360 != 0:
                    return False
        return True

    def flat_ids(self):
        return [tile.tile_id if tile else None for row in self.grid for tile in row]

    def inversion_count(self):
        ids = [item for item in self.flat_ids() if item is not None]
        return sum(1 for i, left in enumerate(ids) for right in ids[i + 1 :] if left > right)

    def is_solvable(self):
        inversions = self.inversion_count()
        if self.size % 2 == 1:
            return inversions % 2 == 0
        blank_row_from_bottom = self.size - self.blank_pos[0]
        return (blank_row_from_bottom % 2 == 0) != (inversions % 2 == 0)

    def manhattan_distance(self):
        total = 0
        for row in self.grid:
            for tile in row:
                if tile:
                    total += abs(tile.row - tile.target_row) + abs(tile.col - tile.target_col)
        return total
