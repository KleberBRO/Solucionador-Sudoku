from __future__ import annotations
from core import e_valido

def contar_valores_possiveis(tabuleiro: list[list[int]], pos: tuple[int, int]) -> int:
    count = 0
    for num in range(1, 5):
        if e_valido(tabuleiro, num, pos):
            count += 1
    return count

def encontrar_vazio_vmr(tabuleiro: list[list[int]]) -> tuple[int, int] | None:
    min_possibilidades = 5
    melhor_pos = None
    for i in range(4):
        for j in range(4):
            if tabuleiro[i][j] == 0:
                possibilidades = contar_valores_possiveis(tabuleiro, (i, j))
                if possibilidades < min_possibilidades:
                    min_possibilidades = possibilidades
                    melhor_pos = (i, j)
                    if min_possibilidades <= 0:
                        return melhor_pos
    return melhor_pos

def resolver_sudoku(tabuleiro: list[list[int]]):
    pos = encontrar_vazio_vmr(tabuleiro)
    
    if not pos:
        return True

    row, col = pos

    # Mostra qual célula o VMR escolheu e quantas opções ela tinha
    opcoes = contar_valores_possiveis(tabuleiro, pos)
    yield (row, col, "VMR_ESCOLHA", opcoes)

    for num in range(1, 5):
        yield (row, col, "TENTANDO", num)

        if e_valido(tabuleiro, num, (row, col)):
            tabuleiro[row][col] = num
            yield (row, col, "COLOCADO", num)
            
            if (yield from resolver_sudoku(tabuleiro)):
                return True
            
            tabuleiro[row][col] = 0
            yield (row, col, "BACKTRACK", 0)
        else:
            yield (row, col, "INVALIDO", num)

    return False