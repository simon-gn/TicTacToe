import numpy as np
from utils import game_over

class Bot:    
    def set_player(self, bot, player):
        self.bot = bot
        self.player = player

    def choose_square(self, game_state):
        return self.minimax(game_state, -np.inf, np.inf, True)[1]

    def minimax(self, game_state, alpha, beta, is_maximizing):
        position = game_state.copy()
        free_squares_indices = np.where(position == None)
        free_squares = list(zip(free_squares_indices[0], free_squares_indices[1]))
        game_is_over, winner = game_over(position)
        if game_is_over:
            if winner == self.bot:
                return 1, None
            if winner == self.player:
                return -1, None
            if winner == None:
                return 0, None
        
        if is_maximizing:
            max_score = -np.inf
            for square in free_squares:
                position[square] = self.bot
                score = self.minimax(position, alpha, beta, False)[0]
                if score > max_score:
                    max_score = score
                    best_move = square
                position[square] = None
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            return max_score, best_move
        
        else:
            min_score = np.inf
            for square in free_squares:
                position[square] = self.player
                score = self.minimax(position, alpha, beta, True)[0]
                min_score = min(min_score, score)
                position[square] = None
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return min_score, None