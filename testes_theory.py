import pygame
import sys
from puzzles.theory_puzzle import TheoryPuzzle

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Teste - Puzzle de Teoria")

def main():
    theory = TheoryPuzzle()
    question, options, correct = theory.get_random_puzzle()
    font = pygame.font.Font(None, 32)
    selected_option = None
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                    selected_option = int(event.unicode) - 1
                    if selected_option == correct:
                        print("Correto!")
                    else:
                        print("Incorreto!")
                if event.key == pygame.K_SPACE:
                    question, options, correct = theory.get_random_puzzle()
                    selected_option = None
        
        screen.fill((0, 0, 0))
        y = 50
        
        # Renderiza a questão
        for line in question.split('\n'):
            text = font.render(line, True, (255, 255, 255))
            screen.blit(text, (50, y))
            y += 40
        
        # Renderiza as opções
        for i, option in enumerate(options):
            color = (0, 255, 0) if selected_option == i else (255, 255, 255)
            text = font.render(f"{i+1}. {option}", True, color)
            screen.blit(text, (50, y))
            y += 40
        
        pygame.display.flip()

if __name__ == "__main__":
    main()