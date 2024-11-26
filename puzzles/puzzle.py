import pygame
from utils.settings import *
from utils.sprites import *

class State(pygame.sprite.Sprite):
    def __init__(self, pos, groups, is_initial=False, is_final=False):
        super().__init__(groups)
        # Visual
        self.radius = 30
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=pos)
        
        # Estado
        self.is_initial = is_initial
        self.is_final = is_final
        self.transitions = {}  # {simbolo: estado_destino}
        self.selected = False
        
        self.draw_state()
    
    def draw_state(self):
        # Desenha círculo principal
        pygame.draw.circle(self.image, 'white', (self.radius, self.radius), self.radius, 2)
        
        # Se for estado final, desenha círculo interno
        if self.is_final:
            pygame.draw.circle(self.image, 'white', (self.radius, self.radius), self.radius - 5, 2)
            
        # Se for estado inicial, desenha seta
        if self.is_initial:
            start_pos = (0, self.radius)
            end_pos = (self.radius - 10, self.radius)
            pygame.draw.line(self.image, 'white', start_pos, end_pos, 2)
            # Desenha ponta da seta
            pygame.draw.polygon(self.image, 'white', [
                (end_pos[0], end_pos[1]),
                (end_pos[0] - 10, end_pos[1] - 5),
                (end_pos[0] - 10, end_pos[1] + 5)
            ])

class Transition:
    def __init__(self, from_state, to_state, symbol):
        self.from_state = from_state
        self.to_state = to_state
        self.symbol = symbol

class AutomataPuzzle:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = pygame.sprite.Group()
        self.states = pygame.sprite.Group()
        self.selected_state = None
        self.transitions = []
        self.font = pygame.font.Font(None, 36)
        
        # Estados do puzzle
        self.completed = False
        self.escape_pressed = False
        
        # Linguagem alvo
        self.target_language = "Construa um autômato que aceite palavras com 'ab'"
        self.alphabet = ['a', 'b']
        
        # Criar estados iniciais
        self.create_initial_states()
        
        self.creating_transition = False
        self.transition_start = None
        
    def create_initial_states(self):
        # Cria estado inicial
        initial_state = State(
            pos=(200, SCREEN_HEIGHT//2),
            groups=[self.all_sprites, self.states],
            is_initial=True
        )
        
        # Cria estado final
        final_state = State(
            pos=(600, SCREEN_HEIGHT//2),
            groups=[self.all_sprites, self.states],
            is_final=True
        )
        
    def draw_instructions(self):
        # Desenha instruções do puzzle
        instructions = [
            self.target_language,
            "Clique esquerdo: selecionar/conectar estados",
            "Clique direito: cancelar seleção",
            "ESC: sair do puzzle",
            "ENTER: verificar solução"
        ]
        
        for i, text in enumerate(instructions):
            text_surf = self.font.render(text, True, 'white')
            text_rect = text_surf.get_rect(topleft=(50, 50 + i * 40))
            self.display_surface.blit(text_surf, text_rect)
            
        if self.transition_start:
            text_surf = self.font.render('Selecione o estado de destino', True, 'yellow')
            text_rect = text_surf.get_rect(topleft=(50, SCREEN_HEIGHT - 100))
            self.display_surface.blit(text_surf, text_rect)
            
    def handle_event(self, event):
        """Gerencia eventos do puzzle"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Botão esquerdo
                # Verifica colisão com estados
                mouse_pos = pygame.mouse.get_pos()
                for state in self.states:
                    if state.rect.collidepoint(mouse_pos):
                        if not self.transition_start:
                            self.transition_start = state
                        else:
                            # Cria transição
                            self.create_transition(self.transition_start, state)
                            self.transition_start = None
                        break
                        
            elif event.button == 3:  # Botão direito
                self.transition_start = None
                
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.escape_pressed = True
            elif event.key == pygame.K_RETURN:
                self.check_solution()
                
    def create_transition(self, from_state, to_state):
        """Cria uma transição entre dois estados"""
        # Por enquanto, usa 'a' como símbolo padrão
        # Você pode implementar uma caixa de diálogo para escolher o símbolo
        symbol = 'a'
        self.transitions.append(Transition(from_state, to_state, symbol))
        from_state.transitions[symbol] = to_state
        
    def draw_transitions(self):
        for transition in self.transitions:
            start_pos = transition.from_state.rect.center
            end_pos = transition.to_state.rect.center
            
            # Desenha linha
            pygame.draw.line(self.display_surface, 'white', start_pos, end_pos, 2)
            
            # Desenha símbolo da transição
            mid_pos = ((start_pos[0] + end_pos[0])//2, (start_pos[1] + end_pos[1])//2)
            text_surf = self.font.render(transition.symbol, True, 'yellow')
            text_rect = text_surf.get_rect(center=mid_pos)
            self.display_surface.blit(text_surf, text_rect)
    
    def check_solution(self):
        """Verifica se o autômato aceita a linguagem correta"""
        # Exemplo: verifica se existe um caminho de 'a' para 'b'
        initial_state = next((state for state in self.states if state.is_initial), None)
        if not initial_state:
            return
            
        # Verifica se existe um caminho ab
        if 'a' in initial_state.transitions:
            state_after_a = initial_state.transitions['a']
            if 'b' in state_after_a.transitions:
                final_state = state_after_a.transitions['b']
                if final_state.is_final:
                    self.completed = True
                    print("Puzzle completado!")
    
    def run(self, delta_time):
        if self.escape_pressed:
            return
            
        self.display_surface.fill('black')
        self.draw_transitions()
        self.all_sprites.update(delta_time)
        self.all_sprites.draw(self.display_surface)
        self.draw_instructions()
        
        # Desenha linha temporária durante a criação de transição
        if self.transition_start:
            mouse_pos = pygame.mouse.get_pos()
            pygame.draw.line(self.display_surface, 'yellow', 
                           self.transition_start.rect.center, mouse_pos, 2)
