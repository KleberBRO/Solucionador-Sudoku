# Funções de desenho e componentes visuais
import pygame
from constants import *

pygame.font.init()
FONT = pygame.font.SysFont("arial", 35)
UI_FONT = pygame.font.SysFont("arial", 20)



def draw_grid(screen: pygame.Surface):
    """Desenha a grade do jogo na tela."""
    for i in range(5):
        # A cada terceira linha, a espessura é maior
        thickness = 3 if i % 2 == 0 else 1
        
        # linhas horizontais
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (BOARD_SIZE, i * CELL_SIZE), thickness)
        # linhas verticais
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, BOARD_SIZE), thickness)
        
def draw_numbers(screen: pygame.Surface, board: list[list[int]]):
    """Desenha os números do tabuleiro na tela."""
    for i in range(4):
        for j in range(4):
            if board[i][j] != 0:
                text = FONT.render(str(board[i][j]), True, BLACK)
                #Cálculo da posição para centralizar o número na célula
                x = j * CELL_SIZE + (CELL_SIZE - text.get_width()) // 2
                y = i * CELL_SIZE + (CELL_SIZE - text.get_height()) // 2
                screen.blit(text, (x, y))
                
def draw_selection(screen: pygame.Surface, selected_cell: tuple[int, int] | None):
    """Desenha uma borda vermelha ao redor da célula selecionada."""
    if selected_cell:
        row, col = selected_cell
        # Desenha um retângulo vermelho ao redor da célula selecionada
        pygame.draw.rect(screen, RED, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)
        
def draw_highlight(screen: pygame.Surface, selected_cell: tuple[int, int] | None):
    """Destaca a linha, coluna e bloco 3x3 da célula selecionada."""
    if not selected_cell:
        return
    
    row, col = selected_cell
    
    # Destaca a linha
    pygame.draw.rect(screen, HIGHLIGHT, (0, row * CELL_SIZE, BOARD_SIZE, CELL_SIZE))
    
    # Destaca a coluna
    pygame.draw.rect(screen, HIGHLIGHT, (col * CELL_SIZE, 0, CELL_SIZE, BOARD_SIZE))
    
    # Destaca o bloco 2x2
    box_x = (col // 2) * 2 * CELL_SIZE
    box_y = (row // 2) * 2 * CELL_SIZE
    pygame.draw.rect(screen, HIGHLIGHT, (box_x, box_y, 2 * CELL_SIZE, 2 * CELL_SIZE))
    
def draw_algo_cursor(screen: pygame.Surface, algo_state: tuple[int, int, str, int] | None):
    """Desenha o feedback visual do algoritmo com base na ação atual."""
    if not algo_state:
        return
        
    row, col, action, num = algo_state
    
    # Define as cores baseadas no que o algoritmo está fazendo
    if action == "TENTANDO":
        color = BLUE       # Azul para tentativas
    elif action == "BACKTRACK":
        color = RED        # Vermelho para retrocesso
    else: # "COLOCADO"
        color = GREEN      # Verde para sucesso provisório
        
    # Desenha a borda da célula
    pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 5)
    
    # Se estiver apenas tentando, o número não está no tabuleiro ainda. Desenhamos ele provisoriamente.
    if action == "TENTANDO":
        text = FONT.render(str(num), True, color)
        x = col * CELL_SIZE + (CELL_SIZE - text.get_width()) // 2
        y = row * CELL_SIZE + (CELL_SIZE - text.get_height()) // 2
        screen.blit(text, (x, y))


def draw_all(screen: pygame.Surface, board: list[list[int]], selected_cell: tuple[int, int] | None, algo_state: tuple[int, int, str, int] | None):
    """Função central para atualizar o frame atual."""
    screen.fill(WHITE)
    draw_highlight(screen, selected_cell)
    draw_grid(screen)
    draw_numbers(screen, board)
    draw_selection(screen, selected_cell)
    draw_algo_cursor(screen, algo_state)

class Button:
    def __init__(self, x: int, y: int, width: int, height: int, text: str):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = GRAY
        self.text_surf = UI_FONT.render(self.text, True, BLACK)

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=5)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=5) # Borda
        
        # Centraliza o texto
        text_rect = self.text_surf.get_rect(center=self.rect.center)
        screen.blit(self.text_surf, text_rect)

    def update_text(self, new_text: str, new_color: tuple):
        self.text = new_text
        self.color = new_color
        self.text_surf = UI_FONT.render(self.text, True, BLACK)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Retorna True se o botão foi clicado."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False
    
class Slider:
    def __init__(self, x: int, y: int, width: int, height: int, min_val: int, max_val: int, start_val: int):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.val = start_val
        self.dragging = False
        
        # O 'handle' é o botão deslizante
        self.handle_radius = height
        self.update_handle_pos()

    def update_handle_pos(self):
        """Calcula a posição X do botão deslizante com base no valor atual."""
        ratio = (self.val - self.min_val) / (self.max_val - self.min_val)
        self.handle_x = self.rect.x + int(ratio * self.rect.width)
        self.handle_y = self.rect.centery

    def draw(self, screen: pygame.Surface):
        # Desenha a linha de fundo
        pygame.draw.rect(screen, GRAY, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 1)
        
        # Desenha o botão deslizante
        pygame.draw.circle(screen, BLACK, (self.handle_x, self.handle_y), self.handle_radius)
        
        # Exibe o valor atual acima do slider
        text_surf = UI_FONT.render(f"Delay: {self.val}ms", True, BLACK)
        screen.blit(text_surf, (self.rect.x + self.rect.width + 15, self.rect.y - 5))

    def handle_event(self, event: pygame.event.Event):
        """Lida com os cliques e o arrasto do mouse."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Verifica se clicou na área do slider
            click_rect = pygame.Rect(self.rect.x, self.rect.y - self.handle_radius, self.rect.width, self.handle_radius * 2)
            if click_rect.collidepoint(event.pos):
                self.dragging = True
                self._update_val_from_mouse(event.pos[0])
                
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
            
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self._update_val_from_mouse(event.pos[0])

    def _update_val_from_mouse(self, mouse_x: int):
        """Atualiza o valor baseado na posição do mouse no eixo X."""
        # Limita o mouse_x dentro dos limites do slider
        mouse_x = max(self.rect.x, min(mouse_x, self.rect.right))
        
        ratio = (mouse_x - self.rect.x) / self.rect.width
        self.val = int(self.min_val + ratio * (self.max_val - self.min_val))
        self.update_handle_pos()