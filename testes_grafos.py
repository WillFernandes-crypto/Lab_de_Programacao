import pygame
import sys
from puzzles.graphs_puzzle import GraphsPuzzle

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Teste - Puzzle de Grafos")

def render_text(screen, text, font, start_y, max_width=700):
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        test_surface = font.render(test_line, True, (255, 255, 255))
        
        if test_surface.get_width() > max_width:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(word)
        else:
            current_line.append(word)
    
    if current_line:
        lines.append(' '.join(current_line))
    
    y = start_y
    for line in lines:
        text_surface = font.render(line, True, (255, 255, 255))
        screen.blit(text_surface, (50, y))
        y += 30
    
    return y

def main():
    graphs = GraphsPuzzle()
    font = pygame.font.Font(None, 32)
    user_input = ""
    question, answer = graphs.get_random_puzzle()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print("Resposta correta:", answer)
                    print("Sua resposta:", user_input)
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.key == pygame.K_SPACE:
                    question, answer = graphs.get_random_puzzle()
                    user_input = ""
                else:
                    user_input += event.unicode
        
        screen.fill((0, 0, 0))
        
        # Renderiza a questão
        y = render_text(screen, question, font, 50)
        
        # Renderiza a entrada do usuário
        input_text = f"Sua resposta: {user_input}"
        text_surface = font.render(input_text, True, (255, 255, 255))
        screen.blit(text_surface, (50, y + 30))
        
        pygame.display.flip()

if __name__ == "__main__":
    main()