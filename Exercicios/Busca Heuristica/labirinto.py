# labirinto.py

import numpy as np
from no import No

class Labirinto:
    def __init__(self):
        self.labirinto = np.array([
            ['A', 'A', '.', '#', '.', '.', '.', 'R'],
            ['.', 'A', 'A', '.', '.', 'AM', '#', '.'],
            ['#', '.', 'A', '#', '.', 'AM', '#', '#'],
            ['.', '#', '.', 'A', 'A', 'A', 'A', 'A'],
            ['.', '.', '.', '.', 'A', '.', '.', '.'],
            ['.', 'AM', '.', '.', 'A', '#', '.', '.'],
            ['.', 'AM', '.', '.', '.', 'A', '#', '.'],
            ['I', '.', '.', '.', '#', '.', 'A', '.']
        ])
        # Define quais símbolos representam células acessíveis.
        # Consideramos acessíveis: 'A', '.', 'AM', 'I' (inicial) e 'R' (objetivo)
        self.acessiveis = {'A', '.', 'AM', 'I', 'R'}

        # Identifica a posição inicial (onde está 'I') e o objetivo (onde está 'R')
        self.start = self.__encontrar_posicao('I')
        self.goal  = self.__encontrar_posicao('R')

    def __encontrar_posicao(self, simbolo):
        linhas, colunas = self.labirinto.shape
        for i in range(linhas):
            for j in range(colunas):
                if self.labirinto[i, j] == simbolo:
                    return (i, j)
        return None

    def iniciar(self):
        # Retorna o nó inicial baseado na posição do 'I'
        return No(self.start)

    def testar_objetivo(self, no):
        # O objetivo é atingir a posição onde está 'R'
        return no.estado == self.goal

    def gerar_sucessores(self, no):
        sucessores = []
        r, c = no.estado
        # Define os movimentos possíveis: (nome, (delta linha, delta coluna))
        movimentos = [
            ("⬆️", (-1, 0)),
            ("⬇️", (1, 0)),
            ("⬅️", (0, -1)),
            ("➡️", (0, 1))
        ]
        for mov, (dr, dc) in movimentos:
            novo_r, novo_c = r + dr, c + dc
            if self.__is_valid(novo_r, novo_c):
                novo_estado = (novo_r, novo_c)
                sucessor = No(novo_estado, no, mov)
                sucessores.append(sucessor)
        return sucessores

    def __is_valid(self, r, c):
        linhas, colunas = self.labirinto.shape
        if 0 <= r < linhas and 0 <= c < colunas:
            # Se a célula estiver no conjunto de acessíveis, é válida.
            if self.labirinto[r, c] in self.acessiveis:
                return True
        return False

    def custo(self, no, no_destino):
        # Custo fixo para cada movimento
        return 1

    def heuristica(self, no):
        # Distância de Manhattan entre o estado atual e o objetivo
        r, c = no.estado
        gr, gc = self.goal
        return abs(r - gr) + abs(c - gc)

    def imprimir(self, no):
        """
        Imprime o labirinto destacando a posição atual (marcada com 'X').
        As paredes permanecem como '#' e as demais células são exibidas conforme o array.
        """
        lab = self.labirinto.copy()
        r, c = no.estado
        # Cria uma cópia para não alterar o original
        lab_str = ""
        linhas, colunas = lab.shape
        for i in range(linhas):
            linha = ""
            for j in range(colunas):
                if (i, j) == (r, c):
                    linha += " X ".ljust(4)
                else:
                    linha += f" {lab[i, j]} ".ljust(4)
            lab_str += linha + "\n"
        return lab_str
