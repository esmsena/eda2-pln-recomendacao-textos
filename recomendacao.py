import heapq
import json
from collections import defaultdict


def carregar_json(caminho):
    with open(caminho, encoding="utf-8") as arquivo:
        return json.load(arquivo)


def top_k_recomendacoes(grafo_textos, texto_origem, k):
    """Mantem os K vizinhos mais fortes de um texto usando min-heap."""
    heap = []

    for vizinho, peso in obter_vizinhos(grafo_textos, texto_origem):
        item = (peso, vizinho)

        if len(heap) < k:
            heapq.heappush(heap, item)
        elif peso > heap[0][0]:
            heapq.heapreplace(heap, item)

    return sorted(heap, reverse=True)


def recomendar_usuario_existente(grafo_textos, usuario, textos, k=5, nota_minima=2):
    """
    Recomenda textos usando o grafo projetado texto-texto recebido da Pessoa 1.

    A pontuacao final soma as similaridades dos vizinhos dos textos ja avaliados
    pelo usuario. A nota dada pelo usuario entra como peso adicional.
    """
    textos_por_id = indexar_textos(textos)
    textos_lidos = {interacao["texto_id"] for interacao in usuario["interacoes"]}
    pontuacoes = defaultdict(float)

    for interacao in usuario["interacoes"]:
        texto_origem = interacao["texto_id"]
        nota = interacao.get("nota", 0)

        if nota < nota_minima:
            continue

        for vizinho, peso in obter_vizinhos(grafo_textos, texto_origem):
            if vizinho not in textos_lidos:
                pontuacoes[vizinho] += peso * nota

    melhores = top_k_pontuacoes(
        ((pontuacao, texto_id) for texto_id, pontuacao in pontuacoes.items()), k
    )
    return formatar_recomendacoes(melhores, textos_por_id)


def recomendar_cold_start(area_interesse, textos, interacoes, k=5, excluir_ids=None):
    """
    Recomenda para usuario sem historico.

    Enquanto o indice invertido nao existir, filtra pela area de interesse e
    ranqueia pelos textos mais bem avaliados no conjunto de interacoes.
    """
    estatisticas = calcular_estatisticas_avaliacoes(interacoes)
    candidatos = []
    excluir_ids = excluir_ids or set()

    for texto in textos:
        if texto["area"].lower() != area_interesse.lower():
            continue

        texto_id = texto["id"]
        if texto_id in excluir_ids:
            continue

        media, quantidade = estatisticas.get(texto_id, (0, 0))
        pontuacao = (media, quantidade, texto.get("ano", 0))
        candidatos.append((pontuacao, texto_id))

    melhores = top_k_pontuacoes(candidatos, k)
    textos_por_id = indexar_textos(textos)

    recomendacoes = []
    for pontuacao, texto_id in melhores:
        texto = textos_por_id[texto_id]
        media, quantidade = estatisticas.get(texto_id, (0, 0))
        recomendacoes.append(
            {
                "texto_id": texto_id,
                "titulo": texto["titulo"],
                "area": texto["area"],
                "ano": texto["ano"],
                "nota_media": round(media, 2),
                "quantidade_avaliacoes": quantidade,
                "pontuacao": round(media, 4),
            }
        )

    return recomendacoes


def recomendar(grafo_textos, usuario_id, textos, interacoes, k=5, area_interesse=None):
    """
    Fluxo principal da Pessoa 3.

    Se houver usuario e grafo, usa o historico no grafo projetado. Se o usuario
    nao existir, ou se o grafo ainda nao chegou, usa a estrategia de cold start.
    """
    usuario = buscar_usuario(interacoes, usuario_id)

    if usuario is not None and grafo_textos is not None:
        recomendacoes = recomendar_usuario_existente(grafo_textos, usuario, textos, k)
        if recomendacoes:
            return recomendacoes

    area = area_interesse
    if area is None and usuario is not None:
        area = usuario["area_interesse"]

    if area is None:
        raise ValueError("Informe area_interesse para recomendar um usuario novo.")

    excluir_ids = set()
    if usuario is not None:
        excluir_ids = {interacao["texto_id"] for interacao in usuario["interacoes"]}

    return recomendar_cold_start(area, textos, interacoes, k, excluir_ids)


def obter_vizinhos(grafo_textos, texto_origem):
    """
    Aceita formatos comuns para facilitar a integracao com a Pessoa 1:
    - grafo.adjacencia["t01"] = [("t02", 0.8), ...]
    - grafo.adjacencia["t01"] = {"t02": 0.8, ...}
    - grafo["t01"] = [("t02", 0.8), ...]
    """
    adjacencia = getattr(grafo_textos, "adjacencia", grafo_textos)
    vizinhos = adjacencia.get(texto_origem, [])

    if isinstance(vizinhos, dict):
        return vizinhos.items()

    return vizinhos


def top_k_pontuacoes(itens, k):
    heap = []

    for pontuacao, texto_id in itens:
        item = (pontuacao, texto_id)

        if len(heap) < k:
            heapq.heappush(heap, item)
        elif pontuacao > heap[0][0]:
            heapq.heapreplace(heap, item)

    return sorted(heap, reverse=True)


def buscar_usuario(interacoes, usuario_id):
    for usuario in interacoes:
        if usuario["usuario"] == usuario_id:
            return usuario

    return None


def indexar_textos(textos):
    return {texto["id"]: texto for texto in textos}


def calcular_estatisticas_avaliacoes(interacoes):
    somas = defaultdict(int)
    quantidades = defaultdict(int)

    for usuario in interacoes:
        for interacao in usuario["interacoes"]:
            texto_id = interacao["texto_id"]
            somas[texto_id] += interacao.get("nota", 0)
            quantidades[texto_id] += 1

    estatisticas = {}
    for texto_id, soma in somas.items():
        quantidade = quantidades[texto_id]
        estatisticas[texto_id] = (soma / quantidade, quantidade)

    return estatisticas


def formatar_recomendacoes(melhores, textos_por_id):
    recomendacoes = []

    for pontuacao, texto_id in melhores:
        texto = textos_por_id.get(texto_id, {})
        recomendacoes.append(
            {
                "texto_id": texto_id,
                "titulo": texto.get("titulo", "Titulo nao encontrado"),
                "area": texto.get("area", "Area nao encontrada"),
                "ano": texto.get("ano"),
                "pontuacao": round(pontuacao, 4),
            }
        )

    return recomendacoes
