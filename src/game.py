import os
import pygame
import numpy as np
from bot import Bot
from utils import game_over

class TicTacToe:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((600,600))
        pygame.display.set_caption('TicTacToe')
        # Set default directory
        current_working_directory = os.getcwd()
        if not os.path.exists(current_working_directory):
            os.makedirs(current_working_directory)
        self._default_directory = os.path.abspath(os.path.join(current_working_directory, ".."))
        self.board = pygame.image.load(f'{self._default_directory}/images/board.png')
        self.x_icon = pygame.image.load(f'{self._default_directory}/images/x.png')
        self.o_icon = pygame.image.load(f'{self._default_directory}/images/o.png')
        self.my_font = pygame.font.SysFont('Comic Sans MS', 30)
        self.square_size = self.board.get_width()/3
        self.bot = Bot()
        self.set_defaults()
    
    def set_defaults(self):
        self.screen.fill('white')
        text_choose_player = self.my_font.render("Choose player:", True, (0, 0, 0), 'white')
        text_player_1 = self.my_font.render("Player 1", True, (0, 0, 0), 'white')
        text_player_2 = self.my_font.render("Player 2", True, (0, 0, 0), 'white')
        self.button_rect_1 = pygame.Rect(125, 275, 105, 40)
        self.button_rect_2 = pygame.Rect(375, 275, 105, 40)
        self.screen.blit(text_choose_player, (205, 125))
        self.screen.blit(text_player_1, self.button_rect_1)
        self.screen.blit(text_player_2, self.button_rect_2)
        self.game_state = np.full((3,3), None)
        self.round_started = False
        self.game_over = False
        self.player_turn = 1
    
    def start_round(self, player_1):
        self.round_started = True
        self.screen.fill('white')
        self.screen.blit(self.board, (0, 0))
        if not player_1:
            self.bot.set_player(1, 0)
            self.make_move(self.bot.choose_square(self.game_state))
        else:
            self.bot.set_player(0, 1)
    
    def square_is_free(self, square):
        return self.game_state[square] == None

    def draw_player_icon(self, square):
        if self.player_turn == 1:
            icon = self.x_icon
        else:
            icon = self.o_icon
        self.screen.blit(icon, (10 + square[1] * self.square_size, 10 + square[0] * self.square_size))

    def make_move(self, square):
        self.game_state[square] = self.player_turn
        self.draw_player_icon(square)
        game_is_over, winner = game_over(self.game_state)
        if game_is_over:
            if winner != None:
                text_surface = self.my_font.render(f"Player {1 if winner == 1 else 2} wins!", False, (0, 0, 0), 'white')
                self.screen.blit(text_surface, (210, 275))
                self.game_over = True
            else:
                text_surface = self.my_font.render(f"Draw!", False, (0, 0, 0), 'white')
                self.screen.blit(text_surface, (263, 275))
                self.game_over = True
        # Switch player's turn
        if self.player_turn == 1:
            self.player_turn = 0
        else:
            self.player_turn = 1

    def convert_mouse_pos_to_square(self, mouse_pos):
        return (int(np.ceil(mouse_pos[1]/self.square_size) - 1), int(np.ceil(mouse_pos[0]/self.square_size) - 1))

    def run(self):
        isRunning = True
        while isRunning:
            pygame.display.flip()

            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        isRunning = False
                    
                    case pygame.MOUSEBUTTONDOWN:
                        if not self.round_started:
                            if self.button_rect_1.collidepoint(event.pos):
                                self.start_round(True)
                            if self.button_rect_2.collidepoint(event.pos):
                                self.start_round(False)

                        elif not self.game_over:
                            square = self.convert_mouse_pos_to_square(pygame.mouse.get_pos())
                            if self.square_is_free(square):
                                self.make_move(square)
                                if not self.game_over:
                                    self.make_move(self.bot.choose_square(self.game_state))
                        else:
                            self.set_defaults()
        pygame.quit()