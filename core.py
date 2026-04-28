# regras do jogo (validação, busca de vazios)

def encontrar_vazio(tabuleiro: list[list[int]]) -> tuple[int, int] | None:
    """Retorna a posição (linha, coluna) da primeira célula vazia (0)."""
    for i in range(9):
        for j in range(9):
            if tabuleiro[i][j] == 0:
                return (i, j)
    return None

def e_valido(tabuleiro: list[list[int]], num: int, pos: tuple[int, int]) -> bool:
    """Verifica se a inserção de 'num' na 'pos' é válida pelas regras do Sudoku."""
    row, col = pos
    
    # Verificar linha
    for j in range(9):
        if tabuleiro[row][j] == num and col != j:
            return False

    # Verificar coluna
    for i in range(9):
        if tabuleiro[i][col] == num and row != i:
            return False

    # Verificar bloco 3x3
    box_x = col // 3
    box_y = row // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if tabuleiro[i][j] == num and (i, j) != pos:
                return False

    return True