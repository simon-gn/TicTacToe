import numpy as np

def game_over(game_state):
    for i in range(3):
        if np.all(game_state[i] == 1) or np.all(game_state[:, i] == 1):
            return True, 1
        if np.all(game_state[i] == 0) or np.all(game_state[:, i] == 0):
            return True, 0
    if np.all(np.diag(game_state) == 1) or np.all(np.diag(np.fliplr(game_state)) == 1):
        return True, 1
    if np.all(np.diag(game_state) == 0) or np.all(np.diag(np.fliplr(game_state)) == 0):
        return True, 0
    if not np.any(np.equal(game_state, None)):
        return True, None
    return False, None