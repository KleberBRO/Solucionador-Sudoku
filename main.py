from __future__ import annotations
import pygame
import sys
from constants import *
from interface import draw_all, Button, Slider, gerar_texto_log
from core import e_valido
from solucionador import resolver_sudoku

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku Solver 4x4")
    clock = pygame.time.Clock()
    log_mensagens = []
    MAX_LOG_LINES = 10

    test_board = [
        [0, 2, 0, 0],
        [0, 0, 3, 0],
        [0, 0, 0, 1],
        [4, 0, 0, 0]
    ]

    selected = None
    paused = True
    
    # Variáveis de controle para o algoritmo (yield) e tempo
    solver_generator = None
    last_update_time = pygame.time.get_ticks()
    current_algo_state = None  # (row, col, action, num)

    btn_play_pause = Button(20, BOARD_SIZE + 35, 100, 30, "Iniciar")
    slider_speed = Slider(150, BOARD_SIZE + 45, 200, 10, min_val=0, max_val=1000, start_val=100)

    running = True
    while running:
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Controle do botão Iniciar/Pausar
            if btn_play_pause.handle_event(event):
                paused = not paused
                if paused:
                    btn_play_pause.update_text("Iniciar", GRAY)
                else:
                    btn_play_pause.update_text("Pausar", (100, 255, 100))
                    # Inicia o gerador do solucionador caso ainda não exista
                    if solver_generator is None:
                        solver_generator = resolver_sudoku(test_board)

            slider_speed.handle_event(event)
            
            # Interação com a grade e teclado
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if pos[1] < BOARD_SIZE:
                    col = pos[0] // CELL_SIZE
                    row = pos[1] // CELL_SIZE
                    selected = (row, col)
                else:
                    if not btn_play_pause.rect.collidepoint(pos):
                        selected = None

            elif event.type == pygame.KEYDOWN:
                if selected:
                    row, col = selected
                    if event.unicode in ['1', '2', '3', '4']:
                        num = int(event.unicode)
                        if e_valido(test_board, num, (row, col)):
                            test_board[row][col] = num
                    elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE or event.unicode == '0':
                        test_board[row][col] = 0

        delay = slider_speed.val

        # Lógica central: Executa o próximo passo do algoritmo baseado no delay do slider
        if not paused and solver_generator:
            if current_time - last_update_time > delay:
                try:
                    current_algo_state = next(solver_generator)
                    last_update_time = current_time
                    msg = gerar_texto_log(current_algo_state)
                    if msg:
                        log_mensagens.append(msg)
                        if len(log_mensagens) > MAX_LOG_LINES:
                            log_mensagens.pop(0)
                            
                except StopIteration:
                    # O algoritmo terminou (encontrou solução ou falhou)
                    solver_generator = None
                    paused = True
                    current_algo_state = None
                    btn_play_pause.update_text("Concluído", GRAY)

        # Renderização
        draw_all(screen, test_board, selected, current_algo_state, log_mensagens)
        btn_play_pause.draw(screen)
        slider_speed.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()