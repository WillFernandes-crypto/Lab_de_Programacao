import pygame
import sys
from puzzles.aed_puzzle import create_random_aed_puzzle

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Teste - Puzzle de AED")

def main():
    puzzle = create_random_aed_puzzle()
    font = pygame.font.Font(None, 32)
    user_input = ""
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if puzzle.check_solution(user_input):
                        print("Correto!")
                    else:
                        print("Incorreto!")
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.key == pygame.K_SPACE:
                    puzzle = create_random_aed_puzzle()
                    user_input = ""
                else:
                    user_input += event.unicode
        
        screen.fill((0, 0, 0))
        
        # Renderiza o texto do puzzle
        text = font.render(puzzle.get_puzzle_text(), True, (255, 255, 255))
        screen.blit(text, (50, 50))
        
        # Renderiza a entrada do usuário
        input_text = font.render(f"Sua resposta: {user_input}", True, (255, 255, 255))
        screen.blit(input_text, (50, 150))
        
        pygame.display.flip()

if __name__ == "__main__":
    main()