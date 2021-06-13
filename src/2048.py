import tkinter
from time import sleep
from GameOf2048State import GameOf2048State
from bot import ai_think

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

DEPTH = 5

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
        
action_func = {
    "up": up_action,
    "down": down_action,
    "left": left_action,
    "right": right_action
}

# window.bind('<Up>', up_action)
# window.bind('<Down>', down_action)
# window.bind('<Left>', left_action)
# window.bind('<Right>', right_action)

def start(event = None):
    print("Thinking ....")
    solution = ai_think(current_state, DEPTH)
    print(solution)
    action_func[solution]()
    if len(current_state.get_valid_actions()) > 0:
        window.after(500, start)

# window.bind('<Up>', start)

update_display(current_state)

window.after(500, start)
window.mainloop()