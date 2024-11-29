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
        self.text_y_position = 50
        
        # Inicializando atributos que faltavam
        self.display_surface = pygame.display.get_surface()
        self.user_input = ""
        self.font = pygame.font.Font(None, 36)
    
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
        if self.current_puzzle and hasattr(self.current_puzzle, 'handle_event'):
            self.current_puzzle.handle_event(event)
    
    def update(self, delta_time):
        """Atualiza e renderiza o puzzle atual"""
        if self.current_puzzle:
            self.display_surface.fill((0, 0, 0))  # Fundo preto
            
            # Renderiza o texto do puzzle
            question_text = self.current_puzzle.get_puzzle_text()
            y = self.text_y_position
            
            # Quebra o texto em linhas se necessário
            for line in question_text.split('\n'):
                text = self.font.render(line, True, (255, 255, 255))
                self.display_surface.blit(text, (50, y))
                y += 30
            
            # Renderiza a entrada do usuário
            input_text = self.font.render(f"Sua resposta: {self.user_input}", True, (255, 255, 255))
            self.display_surface.blit(input_text, (50, y + 30))
