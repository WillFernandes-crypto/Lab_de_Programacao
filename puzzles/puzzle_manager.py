from .automata_puzzle import AutomataPuzzle
from .theory_puzzle import TheoryPuzzle
from .graphs_puzzle import GraphsPuzzle
from .aed_puzzle import create_random_aed_puzzle
import random
import pygame

class PuzzleManager:
    def __init__(self):
        self.puzzle_types = {
            'automata': AutomataPuzzle,
            'theory': TheoryPuzzle,
            'graphs': GraphsPuzzle,
            'aed': create_random_aed_puzzle
        }
        self.current_puzzle = None
        self.current_type = None
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 32)
        self.user_input = ""
    
    def create_puzzle(self, puzzle_type=None):
        """
        Cria um novo puzzle do tipo especificado ou aleatório
        
        Args:
            puzzle_type (str, optional): 'automata', 'theory', 'graphs' ou 'aed'
        """
        if puzzle_type is None:
            puzzle_type = random.choice(list(self.puzzle_types.keys()))
            
        if puzzle_type not in self.puzzle_types:
            raise ValueError(f"Tipo de puzzle inválido: {puzzle_type}")
            
        self.current_type = puzzle_type
        self.current_puzzle = self.puzzle_types[puzzle_type]()
        return self.current_puzzle
    
    def get_current_puzzle(self):
        """Retorna o puzzle atual"""
        return self.current_puzzle
    
    def get_puzzle_type(self):
        """Retorna o tipo do puzzle atual"""
        return self.current_type
    
    def check_completion(self):
        """Verifica se o puzzle atual foi completado"""
        if self.current_puzzle is None:
            return False
            
        if hasattr(self.current_puzzle, 'completed'):
            return self.current_puzzle.completed
        return False
    
    def handle_event(self, event):
        """
        Encaminha eventos para o puzzle atual
        
        Args:
            event: Evento do Pygame
        """
        if self.current_puzzle:
            # Gerencia o ESC
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.current_puzzle.escape_pressed = True
                return
                
            # Gerencia entrada do usuário
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if hasattr(self.current_puzzle, 'check_solution'):
                        self.current_puzzle.check_solution(self.user_input)
                elif event.key == pygame.K_BACKSPACE:
                    self.user_input = self.user_input[:-1]
                else:
                    self.user_input += event.unicode
    
    def update(self, delta_time):
        """
        Atualiza o puzzle atual
        
        Args:
            delta_time: Tempo desde o último frame
        """
        if not self.current_puzzle:
            return
            
        self.display_surface.fill('black')
        
        # Renderiza o texto do puzzle
        if hasattr(self.current_puzzle, 'get_puzzle_text'):
            text = self.current_puzzle.get_puzzle_text()
            y = 50
            for line in text.split('\n'):
                text_surf = self.font.render(line, True, (255, 255, 255))
                self.display_surface.blit(text_surf, (50, y))
                y += 40
        
        # Renderiza a entrada do usuário
        input_text = self.font.render(f"Sua resposta: {self.user_input}", True, (255, 255, 255))
        self.display_surface.blit(input_text, (50, y + 30))
