from fila_prioridade import FilaPrioridade
from visitados import Visitados

def a_estrela(problema):
    no = problema.iniciar()

    fila = FilaPrioridade()
    fila.push(0, no)

    visitados = Visitados()
    visitados.adicionar(no)

    while not fila.esta_vazio():
        no = fila.pop()
        visitados.adicionar(no)

        # Teste objetivo: chegou ao objetivo?
        if problema.testar_objetivo(no):
            return (visitados.tamanho(), no)

        # Geração dos nós sucessores
        nos_sucessores = problema.gerar_sucessores(no)
        for no_sucessor in nos_sucessores:
            if not visitados.foi_visitado(no_sucessor):
                no_sucessor.custo = no.custo + problema.custo(no, no_sucessor)
                no_sucessor.heuristica = problema.heuristica(no_sucessor)
                prioridade = no_sucessor.custo + no_sucessor.heuristica
                fila.push(prioridade, no_sucessor)

    return (visitados.tamanho(), None)
