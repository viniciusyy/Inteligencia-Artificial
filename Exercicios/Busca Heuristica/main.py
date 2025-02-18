from labirinto import Labirinto
from dijkstra import dijkstra
from a_estrela import a_estrela
from no import no_caminho, vertice_caminho

def main():
    print("=== Fugir do Labirinto com Dijkstra ===")
    problema = Labirinto()
    estados_visitados, no_solucao = dijkstra(problema)
    if no_solucao is None:
        print("Não houve solução para o problema")
    else:
        movimentos = vertice_caminho(no_solucao)
        caminho_estados = no_caminho(no_solucao)
        print("Movimentos (arestas):", movimentos)
        print("Caminho de estados:", caminho_estados)
    print("Total de estados visitados:", estados_visitados)
    print("Estado final:")
    print(problema.imprimir(no_solucao) if no_solucao is not None else "Sem solução")

    print("\n" + "="*40 + "\n")

    print("=== Fugir do Labirinto com A* ===")
    problema2 = Labirinto()
    estados_visitados, no_solucao = a_estrela(problema2)
    if no_solucao is None:
        print("Não houve solução para o problema")
    else:
        movimentos = vertice_caminho(no_solucao)
        caminho_estados = no_caminho(no_solucao)
        print("Movimentos (arestas):", movimentos)
        print("Caminho de estados:", caminho_estados)
    print("Total de estados visitados:", estados_visitados)
    print("Estado final:")
    print(problema2.imprimir(no_solucao) if no_solucao is not None else "Sem solução")

if __name__ == "__main__":
    main()
