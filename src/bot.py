from GameOf2048State import GameOf2048State
from random import shuffle

action_func = {
    "up": GameOf2048State.align_up,
    "down": GameOf2048State.align_down,
    "left": GameOf2048State.align_left,
    "right": GameOf2048State.align_right
}

def ai_think(state, depth):
    best_solution = expectiminimax(state, depth)
    return best_solution
    
def heuristic_function(state):
    def heuristic_with_weight(state):
        tv = state.get_tile_values()
        score = 0
        for row in range(4):
            for col in range(4):
                score += tv[row * 4 + col] / (2 ** (row + col))
        return score
    
    # return score
    return heuristic_with_weight(state) + len(state.get_empty_tile_indexes())
            
def expectiminimax(state, depth):
    # Dari sisi pemain
    possible_solutions = state.get_valid_actions()
    shuffle(possible_solutions)
    max_value = -999999
    best_solution = None
    for solution in possible_solutions:
        next_state = state.copy()
        action_func[solution](next_state)
        current_value = min_search(
            next_state,
            depth - 1
        )
        
        if current_value > max_value:
            max_value = current_value
            best_solution = solution
    
    assert best_solution != None
    return best_solution
    
def min_search(state, depth):
    # Dari sisi penaruh ubin
    possible_empty_idx = state.get_empty_tile_indexes()
    if len(possible_empty_idx) == 0: # Base 1, I have no idea why this exists
        return heuristic_function(state)
    elif depth <= 0: # Base 2
        return heuristic_function(state)
    else:
        possible_solutions = (
            [(2, i, 0.8) for i in possible_empty_idx] + [(4, i, 0.2) for i in possible_empty_idx]
        )
        
        min_value = 0
        
        for tile, idx, probability in possible_solutions:
            next_state = state.copy()
            next_state.put_tile(tile, idx)
            min_value += max_search(
                next_state,
                depth - 1
            ) * probability
                
        return min_value / len(possible_empty_idx)
        
def max_search(state,  depth):
    # Dari sisi pemain
    possible_solutions = state.get_valid_actions()
    if len(possible_solutions) == 0: # Base 1
        return -900000 - depth
    elif depth <= 0: # Base 2
        return heuristic_function(state)
    else:
        max_value = -999999
        solution_idx = 0
        while solution_idx < len(possible_solutions):
            next_state = state.copy()
            action_func[possible_solutions[solution_idx]](next_state)
            max_value = max(max_value, min_search(
                next_state,
                depth - 1
            ))
            
            solution_idx += 1
        
        return max_value