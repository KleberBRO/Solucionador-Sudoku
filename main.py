import pygame
import sys
from constants import *
from interface import draw_all, Button, Slider
from core import e_valido

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku Solver")
    clock = pygame.time.Clock()

    test_board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    selected = None
    paused = True

    # Inicialização dos componentes de interface customizados
    btn_play_pause = Button(20, BOARD_SIZE + 15, 100, 30, "Iniciar")
    slider_speed = Slider(150, BOARD_SIZE + 25, 200, 10, min_val=0, max_val=500, start_val=100)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # --- EVENTOS DA INTERFACE (Botão e Slider) ---
            if btn_play_pause.handle_event(event):
                paused = not paused
                if paused:
                    btn_play_pause.update_text("Iniciar", GRAY)
                else:
                    btn_play_pause.update_text("Pausar", (100, 255, 100)) # Verde claro

            slider_speed.handle_event(event)
            
            # --- EVENTOS DO TABULEIRO ---
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                # Verifica se o clique ocorreu dentro da área do tabuleiro
                if pos[1] < BOARD_SIZE:
                    col = pos[0] // CELL_SIZE
                    row = pos[1] // CELL_SIZE
                    selected = (row, col)
                else:
                    # Desmarca se clicar fora da grade, mas não interfere com os botões
                    if not btn_play_pause.rect.collidepoint(pos):
                        selected = None

            elif event.type == pygame.KEYDOWN:
                if selected:
                    row, col = selected
                    if event.unicode.isdigit() and event.unicode != '0':
                        num = int(event.unicode)
                        if e_valido(test_board, num, (row, col)):
                            test_board[row][col] = num
                    elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE or event.unicode == '0':
                        test_board[row][col] = 0

        delay = slider_speed.val

        # --- RENDERIZAÇÃO ---
        draw_all(screen, test_board, selected)
        
        # Desenha os componentes de interface por cima
        btn_play_pause.draw(screen)
        slider_speed.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()