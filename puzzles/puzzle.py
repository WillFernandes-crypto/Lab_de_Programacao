import pygame
from utils.settings import *
from utils.sprites import *
import math

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
        self.transitions = []
        self.font = pygame.font.Font(None, 36)
        
        # Estados do puzzle
        self.completed = False
        self.escape_pressed = False
        self.transition_start = None
        self.current_symbol = None  # Para armazenar o símbolo atual
        
        # Mensagens de feedback
        self.message = ""
        self.message_timer = 0
        
        # Criar estados iniciais
        self.create_initial_states()
        
    def create_initial_states(self):
        # Estado inicial (q0)
        self.q0 = State(
            pos=(200, SCREEN_HEIGHT//2),
            groups=[self.all_sprites, self.states],
            is_initial=True
        )
        
        # Estado intermediário (q1)
        self.q1 = State(
            pos=(400, SCREEN_HEIGHT//2),
            groups=[self.all_sprites, self.states]
        )
        
        # Estado final (q2)
        self.q2 = State(
            pos=(600, SCREEN_HEIGHT//2),
            groups=[self.all_sprites, self.states],
            is_final=True
        )
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Botão esquerdo
                mouse_pos = pygame.mouse.get_pos()
                for state in self.states:
                    if state.rect.collidepoint(mouse_pos):
                        if not self.transition_start:
                            self.transition_start = state
                            self.show_message("Selecione o símbolo (a/b)")
                        elif self.current_symbol:  # Só cria transição se tiver um símbolo
                            # Cria a transição com o símbolo selecionado
                            if self.create_transition(self.transition_start, state, self.current_symbol):
                                self.show_message(f"Transição '{self.current_symbol}' criada!")
                            # Reseta o estado
                            self.transition_start = None
                            self.current_symbol = None
                        break
                        
            elif event.button == 3:  # Botão direito
                self.transition_start = None
                self.current_symbol = None
                self.show_message("Seleção cancelada")
                
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.escape_pressed = True
            elif event.key == pygame.K_RETURN:
                self.check_solution()
            elif self.transition_start and event.key in [pygame.K_a, pygame.K_b]:
                self.current_symbol = pygame.key.name(event.key)
                self.show_message(f"Símbolo '{self.current_symbol}' selecionado. Agora selecione o estado de destino")
    
    def create_transition(self, from_state, to_state, symbol):
        # Verifica se já existe uma transição com esse símbolo
        if symbol in from_state.transitions:
            self.show_message("Já existe uma transição com esse símbolo!")
            return False
            
        self.transitions.append(Transition(from_state, to_state, symbol))
        from_state.transitions[symbol] = to_state
        return True
        
    def show_message(self, text):
        self.message = text
        self.message_timer = 60  # Frames que a mensagem ficará visível
        
    def check_solution(self):
        """Verifica se o autômato aceita a linguagem L = {ab}"""
        # Verifica se existe um caminho q0 -a-> q1 -b-> q2
        try:
            # Deve começar do estado inicial
            if 'a' in self.q0.transitions:
                state_after_a = self.q0.transitions['a']
                if 'b' in state_after_a.transitions:
                    final_state = state_after_a.transitions['b']
                    if final_state.is_final:
                        self.completed = True
                        self.show_message("Puzzle completado! Pressione ESC para sair")
                        return
            
            self.show_message("Solução incorreta. Tente novamente!")
        except AttributeError:
            self.show_message("Construa o autômato completo!")
    
    def draw_instructions(self):
        instructions = [
            "Construa um autômato que aceite a palavra 'ab'",
            "Clique esquerdo: selecionar estado",
            "Teclas a/b: definir símbolo da transição",
            "Clique direito: cancelar seleção",
            "ENTER: verificar solução",
            "ESC: sair do puzzle"
        ]
        
        for i, text in enumerate(instructions):
            text_surf = self.font.render(text, True, 'white')
            text_rect = text_surf.get_rect(topleft=(50, 50 + i * 40))
            self.display_surface.blit(text_surf, text_rect)
            
        # Desenha mensagem de feedback
        if self.message and self.message_timer > 0:
            text_surf = self.font.render(self.message, True, 'yellow')
            text_rect = text_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 100))
            self.display_surface.blit(text_surf, text_rect)
            self.message_timer -= 1
    
    def draw_transitions(self):
        for transition in self.transitions:
            start_pos = transition.from_state.rect.center
            end_pos = transition.to_state.rect.center
            
            # Calcula o ponto médio para o texto e a seta
            mid_x = (start_pos[0] + end_pos[0]) // 2
            mid_y = (start_pos[1] + end_pos[1]) // 2
            mid_pos = (mid_x, mid_y)
            
            # Desenha a linha
            pygame.draw.line(self.display_surface, 'white', start_pos, end_pos, 2)
            
            # Desenha a ponta da seta
            angle = math.atan2(end_pos[1] - start_pos[1], end_pos[0] - start_pos[0])
            arrow_size = 20
            arrow_angle = math.pi / 6  # 30 graus
            
            # Calcula os pontos da ponta da seta
            arrow_p1 = (end_pos[0] - arrow_size * math.cos(angle - arrow_angle),
                       end_pos[1] - arrow_size * math.sin(angle - arrow_angle))
            arrow_p2 = (end_pos[0] - arrow_size * math.cos(angle + arrow_angle),
                       end_pos[1] - arrow_size * math.sin(angle + arrow_angle))
            
            # Desenha a ponta da seta
            pygame.draw.polygon(self.display_surface, 'white', 
                              [end_pos, arrow_p1, arrow_p2])
            
            # Desenha o símbolo da transição
            text_surf = self.font.render(transition.symbol, True, 'yellow')
            text_rect = text_surf.get_rect(center=mid_pos)
            self.display_surface.blit(text_surf, text_rect)
    
    def run(self, delta_time):
        if self.escape_pressed:
            return
            
        self.display_surface.fill('black')
        
        # Desenha linha temporária durante a criação de transição
        if self.transition_start and self.current_symbol:
            mouse_pos = pygame.mouse.get_pos()
            pygame.draw.line(self.display_surface, 'yellow', 
                           self.transition_start.rect.center, mouse_pos, 2)
        
        self.draw_transitions()
        self.all_sprites.update(delta_time)
        self.all_sprites.draw(self.display_surface)
        self.draw_instructions()
