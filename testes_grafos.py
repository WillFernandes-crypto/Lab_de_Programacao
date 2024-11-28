import pygame
import sys
from puzzles.graphs_puzzle import GraphsPuzzle

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Teste - Puzzle de Grafos")

def main():
    graphs = GraphsPuzzle()
    font = pygame.font.Font(None, 32)
    user_input = ""
    question, answer = graphs.minimum_spanning_tree_puzzle()
    
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
                    question, answer = graphs.minimum_spanning_tree_puzzle()
                    user_input = ""
                else:
                    user_input += event.unicode
        
        screen.fill((0, 0, 0))
        
        # Renderiza a questão
        y = 50
        for line in question.split('\n'):
            text = font.render(line, True, (255, 255, 255))
            screen.blit(text, (50, y))
            y += 30
        
        # Renderiza a entrada do usuário
        input_text = font.render(f"Sua resposta: {user_input}", True, (255, 255, 255))
        screen.blit(input_text, (50, y + 30))
        
        pygame.display.flip()

if __name__ == "__main__":
    main()