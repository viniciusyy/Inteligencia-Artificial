# Framework básico de satisfação de restrições (backtracking)
class Restricao:
    def __init__(self, variaveis):
        self.variaveis = variaveis

    # verifica se a Restrição implementada está satisfeita
    # atribuicao é um dicionário cujas as chaves são as
    # variáveis e os valores, o valor do domínio atribuído
    def esta_satisfeita(self, atribuicao):
        return True

class SatisfacaoRestricoes:
    def __init__(self, variaveis, dominios):
        self.variaveis = variaveis  # Variáveis para serem restringidas
        self.dominios = dominios    # Domínio de cada variável
        self.restricoes = {}        # restrições por variável
        for variavel in self.variaveis:
            self.restricoes[variavel] = []
            if variavel not in self.dominios:
                raise LookupError("Cada variável precisa de um domínio")

    # Adiciona um objeto Restrição à lista de Restrições
    def adicionar_restricao(self, restricao):
        for variavel in restricao.variaveis:
            if variavel not in self.variaveis:
                raise LookupError(f"Variável {variavel} não foi definida previamente")
            else:
                self.restricoes[variavel].append(restricao)

    # Verifica se os valores associados nas variáveis
    # respeitam as todas as restrições
    def esta_consistente(self, variavel, atribuicao):
        for restricao in self.restricoes[variavel]:
            if not restricao.esta_satisfeita(atribuicao):
                return False
        return True

    def busca_backtracking(self, atribuicao = {}):
        # retorna sucesso quando todas as variáveis forem atribuídas
        if len(atribuicao) == len(self.variaveis):
            return atribuicao

        # pega todas as variáveis que ainda não foram atribuídas
        variaveis_nao_atribuida  = [v for v in self.variaveis if v not in atribuicao]
        # pega primeira variável não atribuída
        primeira_variavel = variaveis_nao_atribuida[0]
        for valor in self.dominios[primeira_variavel]:
            atribuicao_local = atribuicao.copy()
            atribuicao_local[primeira_variavel] = valor
            # estamos consistentes, seguir recursão
            if self.esta_consistente(primeira_variavel, atribuicao_local):
                resultado = self.busca_backtracking(atribuicao_local)
                # para o backtracking se não encontra todos os resultados
                if resultado is not None:
                    return resultado
        return None

# --- Definição das restrições específicas para o problema ---

# Restrição que garante que duas aulas não sejam agendadas no mesmo dia e mesmo período.
class RestricaoTimeslotUnico(Restricao):
    def __init__(self, var1, var2):
        super().__init__([var1, var2])
        self.var1 = var1
        self.var2 = var2

    def esta_satisfeita(self, atribuicao):
        # Se alguma das duas variáveis ainda não foi atribuída, não há conflito
        if self.var1 not in atribuicao or self.var2 not in atribuicao:
            return True
        val1 = atribuicao[self.var1]  # (dia, período, professor)
        val2 = atribuicao[self.var2]
        # Verifica se dia e período são iguais
        if val1[0] == val2[0] and val1[1] == val2[1]:
            return False
        return True

# Restrição global para garantir que nenhum professor ultrapasse o limite de 4 aulas por semana.
class RestricaoProfessorLimite(Restricao):
    def __init__(self, variaveis, professor_limite=4):
        # Essa restrição envolve todas as variáveis
        super().__init__(variaveis)
        self.professor_limite = professor_limite

    def esta_satisfeita(self, atribuicao):
        # Conta quantas vezes cada professor aparece na atribuição parcial
        contagem = {}
        for var, valor in atribuicao.items():
            # valor é uma tupla (dia, período, professor)
            prof = valor[2]
            contagem[prof] = contagem.get(prof, 0) + 1
            if contagem[prof] > self.professor_limite:
                return False
        return True

# Nova restrição para limitar o número de aulas por dia
class RestricaoMaxAulasPorDia(Restricao):
    def __init__(self, variaveis, max_por_dia):
        super().__init__(variaveis)
        self.max_por_dia = max_por_dia

    def esta_satisfeita(self, atribuicao):
        # Conta quantas aulas estão agendadas em cada dia
        contagem = {}
        for var, valor in atribuicao.items():
            # valor é uma tupla (dia, período, professor)
            dia = valor[0]
            contagem[dia] = contagem.get(dia, 0) + 1
            if contagem[dia] > self.max_por_dia:
                return False
        return True

# --- Definição do problema de escalonamento de aulas ---

def main():
    # Definição dos dados do problema
    dias = range(5)      # 0: Segunda, 1: Terça, 2: Quarta, 3: Quinta, 4: Sexta
    periodos = range(5)  # 0: 8h, 1: 9h, 2: 10h, 3: 11h, 4: 12h
    
    # Professores: 0 = Prof. A, 1 = Prof. B, 2 = Prof. C
    # Mapeamento das disciplinas que cada professor pode lecionar:
    # Prof. A: Matemática e Física; Prof. B: Matemática e Computação; Prof. C: Física e Computação.
    allowed_professores = {
        "Matematica": [0, 1],
        "Fisica": [0, 2],
        "Computacao": [1, 2]
    }
    
    # Cada disciplina deve ter um número exato de aulas:
    # Matemática: 3, Física: 2, Computação: 3
    # Vamos criar uma variável para cada aula obrigatória.
    variaveis = [
        "Matematica1", "Matematica2", "Matematica3",
        "Fisica1", "Fisica2",
        "Computacao1", "Computacao2", "Computacao3"
    ]
    
    # Mapeamento para saber qual disciplina está associada a cada variável
    disciplina_por_variavel = {
        "Matematica1": "Matematica", "Matematica2": "Matematica", "Matematica3": "Matematica",
        "Fisica1": "Fisica", "Fisica2": "Fisica",
        "Computacao1": "Computacao", "Computacao2": "Computacao", "Computacao3": "Computacao"
    }
    
    # Construindo os domínios: para cada variável, o domínio são as tuplas (dia, período, professor)
    # onde dia ∈ {0,...,4}, período ∈ {0,...,4} e professor pertence à lista permitida para a disciplina.
    dominios = {}
    for var in variaveis:
        disc = disciplina_por_variavel[var]
        dominios[var] = []
        for d in dias:
            for p in periodos:
                for prof in allowed_professores[disc]:
                    dominios[var].append((d, p, prof))
    
    # Instancia o solucionador de satisfação de restrições
    sr = SatisfacaoRestricoes(variaveis, dominios)
    
    # Adiciona a restrição de horário único para cada par de variáveis (duas aulas não podem ocorrer no mesmo dia e período)
    for i in range(len(variaveis)):
        for j in range(i + 1, len(variaveis)):
            sr.adicionar_restricao(RestricaoTimeslotUnico(variaveis[i], variaveis[j]))
    
    # Adiciona a restrição global de limite de aulas por professor (no máximo 4 aulas)
    sr.adicionar_restricao(RestricaoProfessorLimite(variaveis, professor_limite=4))
    
    # Adiciona a restrição para limitar o número de aulas por dia (por exemplo, no máximo 2 aulas por dia)
    sr.adicionar_restricao(RestricaoMaxAulasPorDia(variaveis, max_por_dia=2))
    
    # Busca a solução por backtracking
    solucao = sr.busca_backtracking()
    
    # Impressão dos resultados
    if solucao is None:
        print("Nenhuma solução encontrada.")
    else:
        # Cria uma estrutura para agrupar as aulas por (dia, período)
        agenda = {}
        for var, valor in solucao.items():
            dia, periodo, prof = valor
            agenda[(dia, periodo)] = (disciplina_por_variavel[var], prof)
        
        nomes_dias = {0: "Segunda", 1: "Terça", 2: "Quarta", 3: "Quinta", 4: "Sexta"}
        horarios = {0: "8h", 1: "9h", 2: "10h", 3: "11h", 4: "12h"}
        nomes_prof = {0: "Prof. A", 1: "Prof. B", 2: "Prof. C"}
        
        print("Cronograma de Aulas:")
        # Percorre os dias e períodos na ordem
        for d in dias:
            print(f"\n{nomes_dias[d]}:")
            for p in periodos:
                if (d, p) in agenda:
                    disc, prof = agenda[(d, p)]
                    print(f"  {horarios[p]}: {nomes_prof[prof]} - {disc}")
                else:
                    print(f"  {horarios[p]}: Sem aula")

if __name__ == "__main__":
    main()
