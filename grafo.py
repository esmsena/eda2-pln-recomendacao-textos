import json
from pln_modulo import ProcessadorTexto, similaridade_cosseno

class Grafo:
    def __init__(self):
        # Estrutura de Lista de Adjacência implementada na mão
        # vertice -> lista de [vizinho, peso]
        self.adjacencia = {}

    def adicionar_vertice(self, v):
        if v not in self.adjacencia:
            self.adjacencia[v] = []

    def adicionar_aresta(self, u, v, peso):
        # Como o grafo é não-direcionado, adicionamos o caminho de ida e volta
        self.adicionar_vertice(u)
        self.adicionar_vertice(v)
        
        # Evita duplicar arestas, atualizando o peso se já existir
        for aresta in self.adjacencia[u]:
            if aresta[0] == v:
                aresta[1] = peso
                break
        else:
            self.adjacencia[u].append([v, peso])

        for aresta in self.adjacencia[v]:
            if aresta[0] == u:
                aresta[1] = peso
                break
        else:
            self.adjacencia[v].append([u, peso])

    def obter_vizinhos(self, v):
        return self.adjacencia.get(v, [])


def construir_grafo_bipartido(caminho_interacoes):
    """
    Passo 2: Lê o JSON e monta o grafo bipartido (Usuário -> Redação)
    Pesos baseados na nota: 1 (leitura), 2 (avaliação), 3 (favorito)
    """
    grafo_bipartido = Grafo()
    
    with open(caminho_interacoes, 'r', encoding='utf-8') as f:
        dados_usuarios = json.load(f)
        
    for user_data in dados_usuarios:
        usuario_id = user_data['usuario']
        grafo_bipartido.adicionar_vertice(usuario_id)
        
        for interacao in user_data['interacoes']:
            texto_id = interacao['texto_id']
            peso = interacao['nota'] # Nota 1, 2 ou 3 do JSON
            
            # Conecta Usuário <-> Redação
            grafo_bipartido.adicionar_aresta(usuario_id, texto_id, peso)
            
    return grafo_bipartido


def gerar_projecao_texto_texto(grafo_bipartido, vetores_tfidf, alpha=0.5):
    """
    Passo 3: Gera a projeção Texto-Texto combinando:
    1. Coocorrência (Usuários que leram os mesmos dois textos)
    2. Similaridade de Cosseno (PLN)
    Formula do Peso Final = alpha * Coocorrência_Normalizada + (1 - alpha) * Similaridade_Cosseno
    """
    grafo_textos = Grafo()
    
    # 1. Identificar todas as redações presentes no sistema
    todas_redacoes = [v for v in grafo_bipartido.adjacencia.keys() if v.startswith('t')]
    
    # Inicializa todas as redações como vértices isolados na projeção
    for t in todas_redacoes:
        grafo_textos.adicionar_vertice(t)
        
    # 2. Comparar par a par de redações para calcular o peso da projeção
    for i in range(len(todas_redacoes)):
        for j in range(i + 1, len(todas_redacoes)):
            tA = todas_redacoes[i]
            tB = todas_redacoes[j]
            
            # --- Fator 1: Coocorrência de Usuários ---
            # Encontra usuários que interagiram com ambos os textos
            usuarios_tA = {vizinho[0] for vizinho in grafo_bipartido.obter_vizinhos(tA)}
            usuarios_tB = {vizinho[0] for vizinho in grafo_bipartido.obter_vizinhos(tB)}
            usuarios_em_comum = usuarios_tA & usuarios_tB
            
            coocorrencia = len(usuarios_em_comum)
            
            # --- Fator 2: Similaridade Semântica (PLN da Pessoa 2) ---
            sim_cosseno = 0.0
            if tA in vetores_tfidf and tB in vetores_tfidf:
                sim_cosseno = similaridade_cosseno(vetores_tfidf[tA], vetores_tfidf[tB])
            
            # Se houver alguma relação (ou leram juntos ou o texto é parecido)
            if coocorrencia > 0 or sim_cosseno > 0.0:
                # Normalização simples da coocorrência (evita que o peso exploda se muitos lerem)
                # Como temos 12 usuários no máximo, dividimos por 5.0 como fator de escala (teto em 1.0)
                coocorrencia_norm = min(coocorrencia / 5.0, 1.0)
                
                # Peso Final Ponderado (Combinação Híbrida)
                peso_final = (alpha * coocorrencia_norm) + ((1 - alpha) * sim_cosseno)
                
                # Cria a aresta na projeção apenas se o peso for relevante
                if peso_final > 0.01:
                    grafo_textos.adicionar_aresta(tA, tB, round(peso_final, 4))
                    
    return grafo_textos


# --- Área de Teste Local ---
if __name__ == "__main__":
    print("=== Testando Módulo de Grafos ===")
    
    # 1. Carrega textos para alimentar o módulo de PLN da Pessoa 2
    with open('dados/textos.json', 'r', encoding='utf-8') as f:
        dados_textos = json.load(f)
        
    # 2. Executa o código da Pessoa 2 para obter os vetores TF-IDF
    processador = ProcessadorTexto(dados_textos)
    vetores_tfidf = processador.calcular_tfidf()
    
    # 3. Constrói o seu Grafo Bipartido
    g_bipartido = construir_grafo_bipartido('dados/interacoes.json')
    print(f"Grafo Bipartido criado com {len(g_bipartido.adjacencia)} vértices totais.")
    
    # Teste rápido: Ver vizinhos do usuário u01
    print("Interações do u01:", g_bipartido.obter_vizinhos('u01'))
    
    # 4. Gera a Projeção Texto-Texto que a Pessoa 3 vai usar
    g_projetado = gerar_projecao_texto_texto(g_bipartido, vetores_tfidf, alpha=0.4)
    print(f"Grafo Projetado (Texto-Texto) criado com sucesso.")
    
    # Ver conexões da redação t03 (Inteligência Artificial no Judiciário)
    print("\nConexões geradas para a redação t03 (Top 3 exemplos):")
    conexoes_t03 = g_projetado.obter_vizinhos('t03')
    for vizinho, peso in conexoes_t03[:3]:
        print(f" -> Conectado com {vizinho} | Peso Combinado: {peso}")