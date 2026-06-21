from recomendacao import carregar_json, recomendar


def imprimir_recomendacoes(titulo, recomendacoes):
    print(titulo)
    print("-" * len(titulo))

    for posicao, item in enumerate(recomendacoes, start=1):
        print(
            f"{posicao}. {item['texto_id']} - {item['titulo']} "
            f"({item['area']}, {item['ano']}) | pontuacao: {item['pontuacao']}"
        )


def main():
    textos = carregar_json("dados/textos.json")
    interacoes = carregar_json("dados/interacoes.json")

    # O grafo projetado ainda sera entregue pela Pessoa 1.
    # Enquanto isso, passar None aciona a recomendacao por area.
    grafo_textos = None

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
