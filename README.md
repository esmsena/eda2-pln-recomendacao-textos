# Sistema de Recomendação de Textos

Trabalho de EDA2 utilizando:

- Grafos
- PLN
- Python

## Integrantes

- Esther Sena
- Allan Kelvin Dias
- Yasmim de Souza
- Yves Gustavo Ribeiro
- Nicole Jovita

## Objetivo

Construir um sistema de recomendação de textos baseado em um grafo bipartido usuário-texto.

## Estruturas de Dados

- Grafo bipartido
- Heap
- Hash Table

## Algoritmos

- Busca em largura (BFS)
- Similaridade de cosseno
- Projeção texto-texto

## Como executar

python main.py

## Parte da Pessoa 3

A parte de heap e recomendacao final esta em `recomendacao.py`.

- `top_k_recomendacoes(grafo_textos, texto_origem, k)`: usa min-heap para manter os K vizinhos com maiores pesos de um texto no grafo projetado.
- `recomendar_usuario_existente(...)`: usa o historico do usuario e o grafo texto-texto recebido da Pessoa 1 para gerar recomendacoes.
- `recomendar_cold_start(...)`: quando nao existe historico ou o grafo ainda nao foi entregue, filtra textos pela area de interesse e ranqueia pelos mais bem avaliados.
- `recomendar(...)`: funcao principal que escolhe entre recomendacao por grafo e cold start.

O arquivo `main.py` ja integra os modulos das outras pessoas:

1. carrega `dados/textos.json`;
2. gera os vetores TF-IDF com `ProcessadorTexto`;
3. constroi o grafo bipartido com `construir_grafo_bipartido`;
4. gera o grafo projetado texto-texto com `gerar_projecao_texto_texto`;
5. chama `recomendar(...)` para usuario existente e para cold start.

Se o grafo projetado nao for informado, `recomendar(...)` ainda consegue usar o cold start por area de interesse.

Para rodar os testes:

```bash
python -m unittest
```
