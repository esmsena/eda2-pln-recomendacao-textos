from recomendacao import carregar_json, recomendar
from grafo import construir_grafo_bipartido, gerar_projecao_texto_texto
from pln_modulo import ProcessadorTexto


def imprimir_recomendacoes(titulo, recomendacoes):
    print(titulo)
    print("-" * len(titulo))

    for posicao, item in enumerate(recomendacoes, start=1):
        print(
            f"{posicao}. {item['texto_id']} - {item['titulo']} "
            f"({item['area']}, {item['ano']}) | pontuacao: {item['pontuacao']}"
        )


def construir_grafo_projetado(textos, caminho_interacoes, alpha=0.4):
    processador = ProcessadorTexto(textos)
    vetores_tfidf = processador.calcular_tfidf()
    grafo_bipartido = construir_grafo_bipartido(caminho_interacoes)
    return gerar_projecao_texto_texto(grafo_bipartido, vetores_tfidf, alpha=alpha)


def main():
    textos = carregar_json("dados/textos.json")
    interacoes = carregar_json("dados/interacoes.json")

    grafo_textos = construir_grafo_projetado(textos, "dados/interacoes.json", alpha=0.4)

    recomendacoes_usuario_existente = recomendar(
        grafo_textos=grafo_textos,
        usuario_id="u01",
        textos=textos,
        interacoes=interacoes,
        k=5,
    )
    imprimir_recomendacoes(
        "Recomendacoes para usuario existente", recomendacoes_usuario_existente
    )

    print()

    recomendacoes_usuario_novo = recomendar(
        grafo_textos=grafo_textos,
        usuario_id="u99",
        textos=textos,
        interacoes=interacoes,
        k=5,
        area_interesse="Financeiro",
    )
    imprimir_recomendacoes("Cold start para usuario novo", recomendacoes_usuario_novo)


if __name__ == "__main__":
    main()
