class No:
    def __init__(self, estado, no_pai=None, aresta=None, custo=0.0, heuristica=0.0):
        self.estado = estado          # Para o labirinto, estado é uma tupla (linha, coluna)
        self.no_pai = no_pai
        self.aresta = aresta          # Indica o movimento realizado ("⬆️", "⬇️", "⬅️" ou "➡️")
        self.custo = custo
        self.heuristica = heuristica

    def __repr__(self):
        return str(self.estado)

    def __lt__(self, outro):
        return (self.custo + self.heuristica) < (outro.custo + outro.heuristica)

def no_caminho(no):
    """
    Retorna a sequência de estados do nó inicial até o nó atual.
    """
    caminho = [no.estado]
    while no.no_pai is not None:
        caminho.append(no.estado)
        no = no.no_pai
    caminho.reverse()
    return caminho

def vertice_caminho(no):
    """
    Retorna a sequência de movimentos (arestas) para alcançar o nó atual.
    """
    caminho = []
    while no.no_pai is not None:
        if no.aresta is not None:
            caminho.append(no.aresta)
        no = no.no_pai
    caminho.reverse()
    return caminho
