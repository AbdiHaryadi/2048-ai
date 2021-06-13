import tkinter
from random import randrange, choice, random

class GameOf2048State:
    def __init__(self, tile_values, score):
        self.tile_values = tile_values
        self.score = score
        self.update_valid_actions()
        
    def copy(self):
        result = GameOf2048State(self.tile_values, self.score)
        return result
        
    def get_score(self):
        return self.score
        
    def get_tile_values(self):
        return self.tile_values
        
    def get_valid_actions(self):
        return self.valid_actions
        
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


window = tkinter.Tk()

window.title("2048")
canvas = tkinter.Canvas(window, width = 640, height = 480)

# Create a background
canvas.create_rectangle(0, 0, 640, 480, fill = "#edf4fa", width = 0)

border_width = 5
rectangles = []
texts = []
current_state = GameOf2048State(
    [
        0, 0, 0, 0,
        0, 0, 0, 0,
        0, 0, 0, 0,
        0, 0, 0, 0
    ],
    0
)
current_state.put_random_tile()
current_state.put_random_tile()

colors = { # From https://colorpalettes.net/color-palette-3666/
    0: "#cdd4ca",
    2: "#ffd66c",
    4: "#f2be54",
    8: "#daa63c",
    16: "#9fc6cc",
    32: "#87aeb4",
    64: "#6f969c",
    128: "#2d569c",
    256: "#153e74",
    512: "#00265c",
    1024: "#313235",
    2048: "#191a1d",
    4096: "#010205",
    8192: "black",
    16384: "black",
    32768: "black",
    65536: "black"
}

current_tile_values = current_state.get_tile_values()

for row in range(4):
    for col in range(4):
        current_value = current_tile_values[row * 4 + col]
    
        rectangles.append(
            canvas.create_rectangle(
                120 * col + border_width,
                120 * row + border_width,
                120 * (col + 1) - border_width,
                120 * (row + 1) - border_width,
                fill=colors[current_value],
                width=0
            )
        )
        
        texts.append(
            canvas.create_text(
                60 + 120 * col,
                60 + 120 * row,
                fill="white" if current_value != 0 else colors[current_value],
                font="Arial 20",
                text=str(current_value)
            )
        )
        
# Create score
canvas.create_text(560, 60, fill = "black", font="Arial 20", text="Skor:")
score_obj = canvas.create_text(560, 100, fill = "black", font="Arial 20", text="")
canvas.itemconfig(score_obj, text = str(current_state.get_score()))

def update_display(state):
    current_tile_values = state.get_tile_values()
    for row in range(4):
        for col in range(4):
            current_value = current_tile_values[row * 4 + col]
            canvas.itemconfig(rectangles[row * 4 + col], fill = colors[current_value])
            canvas.itemconfig(
                texts[row * 4 + col],
                fill = "white" if current_value != 0 else colors[current_value],
                text=str(current_value)
            )
            
    canvas.itemconfig(score_obj, text = str(state.get_score()))

canvas.pack()

def up_action(event = None):
    if "up" in current_state.get_valid_actions():
        current_state.align_up()
        current_state.put_random_tile()
        update_display(current_state)
    else:
        print("You can\'t")
    
def down_action(event = None):
    if "down" in current_state.get_valid_actions():
        current_state.align_down()
        current_state.put_random_tile()
        update_display(current_state)
    else:
        print("You can\'t")

def left_action(event = None):
    if "left" in current_state.get_valid_actions():
        current_state.align_left()
        current_state.put_random_tile()
        update_display(current_state)
    else:
        print("You can\'t")
    
def right_action(event = None):
    if "right" in current_state.get_valid_actions():
        current_state.align_right()
        current_state.put_random_tile()
        update_display(current_state)
    else:
        print("You can\'t")

window.bind('<Up>', up_action)
window.bind('<Down>', down_action)
window.bind('<Left>', left_action)
window.bind('<Right>', right_action)

update_display(current_state)

window.mainloop()