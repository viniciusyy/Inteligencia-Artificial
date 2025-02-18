class Visitados:
    def __init__(self):
        self.visitados = set()

    def adicionar(self, no):
        # Como o estado do labirinto é uma tupla (imutável), podemos adicioná-lo diretamente.
        self.visitados.add(no.estado)

    def foi_visitado(self, no):
        return no.estado in self.visitados

    def tamanho(self):
        return len(self.visitados)
