import tkinter
from random import randrange

class GameOf2048State:
    def __init__(self, tile_values, score):
        self.tile_values = tile_values
        self.score = score
        self.valid_actions = self.get_valid_actions_2()
        
    def copy(self):
        result = GameOf2048State(self.tile_values, self.score)
        return result
        
    def get_score(self):
        return self.score
        
    def get_tile_values(self):
        return self.tile_values
        
    def get_valid_actions(self):
        return self.valid_actions
        
    def get_valid_actions_2(self):
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
            
        return valid_actions


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
        1024, 0, 16, 32,
        2048, 0, 8, 64,
        4096, 0, 2, 256,
        8192, 512, 4, 128,
    ],
    0
)
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
        print("Up")
    else:
        print("You can\'t")
    
def down_action(event = None):
    if "down" in current_state.get_valid_actions():
        print("Down")
    else:
        print("You can\'t")

def left_action(event = None):
    if "left" in current_state.get_valid_actions():
        print("Left")
    else:
        print("You can\'t")
    
def right_action(event = None):
    if "right" in current_state.get_valid_actions():
        print("Right")
    else:
        print("You can\'t")

window.bind('<Up>', up_action)
window.bind('<Down>', down_action)
window.bind('<Left>', left_action)
window.bind('<Right>', right_action)

update_display(current_state)

window.mainloop()