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

Enquanto o grafo projetado da Pessoa 1 nao estiver pronto, `main.py` usa `grafo_textos = None` e demonstra o cold start.

Para rodar os testes:

```bash
python -m unittest
```
