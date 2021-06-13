from random import choice, random

class GameOf2048State:
    def __init__(self, tile_values, score):
        self.tile_values = tile_values
        self.score = score
        self.update_valid_actions()
        
    def copy(self):
        result = GameOf2048State(self.tile_values.copy(), self.score)
        return result
        
    def get_score(self):
        return self.score
        
    def get_tile_values(self):
        return self.tile_values.copy()
        
    def get_valid_actions(self):
        return self.valid_actions.copy()
        
    def update_valid_actions(self):
        valid_actions = []
        # tvwd: tile_values_with_dummy
        # Check up
        """
        tvwd = [0 for _ in range(4)] + self.tile_values
        if any([tvwd[i + 4] == tvwd[i] and twd[i + 4] != 0 for i in range(16)]):
            valid_actions.append("up")
        """
        if any([
                (
                    self.tile_values[i] != 0
                    and (
                        self.tile_values[i - 4] == 0
                        or self.tile_values[i - 4] == self.tile_values[i]
                    )
                )
                for i in range(4, 16)
        ]):
            valid_actions.append("up")
            
        # Check down
        if any([
                (
                    self.tile_values[i] != 0
                    and (
                        self.tile_values[i + 4] == 0
                        or self.tile_values[i + 4] == self.tile_values[i]
                    )
                )
                for i in range(0, 12)
        ]):
            valid_actions.append("down")
            
        # Check left
        """
        tvwd =  [0 if i % 5 == 0 else self.tile_values[i - (i // 5) - 1] for i in range(20)]
        if any([tvwd[i] == tvwd[i - 1] for i in range(20) if i % 5 != 0]):
            valid_actions.append("left")
        """
        if any([
                (
                    self.tile_values[i] != 0
                    and (
                        self.tile_values[i - 1] == 0
                        or self.tile_values[i - 1] == self.tile_values[i]
                    )
                )
                for i in range(0, 16) if i % 4 != 0
        ]):
            valid_actions.append("left")
        
        # Check right
        if any([
                (
                    self.tile_values[i] != 0
                    and (
                        self.tile_values[i + 1] == 0
                        or self.tile_values[i + 1] == self.tile_values[i]
                    )
                )
                for i in range(0, 16) if i % 4 != 3
        ]):
            valid_actions.append("right")

        self.valid_actions = valid_actions.copy()
        
    def align_up(self):
        def move_zero_tiles():
            # Identify move_distance
            empty_tile_in_col = [0, 0, 0, 0]
            move_distance = [0 for _ in range(16)]
            for i in range(0, 16):
                if self.tile_values[i] == 0:
                    empty_tile_in_col[i % 4] += 1
                else:
                    move_distance[i] = empty_tile_in_col[i % 4]
        
            # Execute movement
            for i in range(4, 16):
                if move_distance[i] > 0:
                    self.tile_values[i - 4 * move_distance[i]] = self.tile_values[i]
                    self.tile_values[i] = 0
        
        
        move_zero_tiles()
        
        # Joining same tile
        for i in range(12):
            if self.tile_values[i] == self.tile_values[i + 4]:
                self.tile_values[i] *= 2
                self.score += self.tile_values[i]
                self.tile_values[i + 4] = 0
        
        move_zero_tiles()
        
        self.update_valid_actions()

    def align_down(self):
        def move_zero_tiles():
            # Identify move_distance
            empty_tile_in_col = [0, 0, 0, 0]
            move_distance = [0 for _ in range(16)]
            for i in range(15, -1, -1):
                if self.tile_values[i] == 0:
                    empty_tile_in_col[i % 4] += 1
                else:
                    move_distance[i] = empty_tile_in_col[i % 4]
        
            # Execute movement
            for i in range(12, -1, -1):
                if move_distance[i] > 0:
                    self.tile_values[i + 4 * move_distance[i]] = self.tile_values[i]
                    self.tile_values[i] = 0
        
        move_zero_tiles()
        
        for i in range(15, 3, -1):
            if self.tile_values[i] == self.tile_values[i - 4]:
                self.tile_values[i] *= 2
                self.score += self.tile_values[i]
                self.tile_values[i - 4] = 0
                
        move_zero_tiles()
        
        self.update_valid_actions()

    def align_left(self):
        def move_zero_tiles():
            # Identify move_distance
            move_distance = [0 for _ in range(16)]
            for r in range(4):
                empty_tile_in_row = 0
                for c in range(4):
                    if self.tile_values[4 * r + c] == 0:
                        empty_tile_in_row += 1
                    else:
                        move_distance[4 * r + c] = empty_tile_in_row
        
            # Execute movement
            for i in range(16):
                if i % 4 != 0:
                    if move_distance[i] > 0:
                        self.tile_values[i - move_distance[i]] = self.tile_values[i]
                        self.tile_values[i] = 0
        
        move_zero_tiles()
        
        for i in range(16):
            if i % 4 != 3:
                if self.tile_values[i] == self.tile_values[i + 1]:
                    self.tile_values[i] *= 2
                    self.score += self.tile_values[i]
                    self.tile_values[i + 1] = 0
                
        move_zero_tiles()
        
        self.update_valid_actions()

    def align_right(self):
        def move_zero_tiles():
            # Identify move_distance
            move_distance = [0 for _ in range(16)]
            for r in range(4):
                empty_tile_in_row = 0
                for c in range(3, -1, -1):
                    if self.tile_values[4 * r + c] == 0:
                        empty_tile_in_row += 1
                    else:
                        move_distance[4 * r + c] = empty_tile_in_row
        
            # Execute movement
            for i in range(15, -1, -1):
                if i % 4 != 3:
                    if move_distance[i] > 0:
                        self.tile_values[i + move_distance[i]] = self.tile_values[i]
                        self.tile_values[i] = 0
        
        move_zero_tiles()
        
        for i in range(15, 0, -1): # i == 0 tidak digunakan
            if i % 4 != 0:
                if self.tile_values[i] == self.tile_values[i - 1]:
                    self.tile_values[i] *= 2
                    self.score += self.tile_values[i]
                    self.tile_values[i - 1] = 0
                
        move_zero_tiles()
        
        self.update_valid_actions()
        
    def get_empty_tile_indexes(self):
        return [i for i in range(16) if self.tile_values[i] == 0]
        
    def put_random_tile(self):
        self.tile_values[choice(self.get_empty_tile_indexes())] = 2 if random() < 0.8 else 4
        self.update_valid_actions()
        
    def has_2048_tile(self):
        return 2048 in self.tile_values
        
    def put_tile(self, value, idx):
        self.tile_values[idx] = value
        
    def render(self):
        for row in range(4):
            for col in range(4):
                print(" {: >6}".format(self.tile_values[4 * row + col]), end = "")
            print()