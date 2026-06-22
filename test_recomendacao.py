import unittest

from recomendacao import (
    recomendar_cold_start,
    recomendar_usuario_existente,
    top_k_recomendacoes,
)


class GrafoFake:
    def __init__(self):
        self.adjacencia = {
            "t01": [("t02", 0.2), ("t03", 0.9), ("t04", 0.5), ("t05", 0.7)],
            "t02": [("t03", 0.4), ("t06", 0.8)],
        }

    def obter_vizinhos(self, texto_id):
        return self.adjacencia.get(texto_id, [])


class RecomendacaoTest(unittest.TestCase):
    def test_top_k_recomendacoes_mantem_maiores_pesos(self):
        resultado = top_k_recomendacoes(GrafoFake(), "t01", 2)

        self.assertEqual(resultado, [(0.9, "t03"), (0.7, "t05")])

    def test_recomendar_usuario_existente_remove_textos_ja_lidos(self):
        usuario = {
            "usuario": "u01",
            "area_interesse": "Jurídico",
            "interacoes": [
                {"texto_id": "t01", "nota": 3},
                {"texto_id": "t02", "nota": 2},
            ],
        }
        textos = [
            {"id": "t01", "titulo": "Texto 1", "area": "A", "ano": 2024},
            {"id": "t02", "titulo": "Texto 2", "area": "A", "ano": 2024},
            {"id": "t03", "titulo": "Texto 3", "area": "A", "ano": 2024},
            {"id": "t04", "titulo": "Texto 4", "area": "A", "ano": 2024},
            {"id": "t05", "titulo": "Texto 5", "area": "A", "ano": 2024},
            {"id": "t06", "titulo": "Texto 6", "area": "B", "ano": 2023},
        ]

        resultado = recomendar_usuario_existente(GrafoFake(), usuario, textos, k=2)

        self.assertEqual([item["texto_id"] for item in resultado], ["t03", "t05"])

    def test_cold_start_filtra_por_area(self):
        textos = [
            {"id": "t01", "titulo": "Texto 1", "area": "Financeiro", "ano": 2024},
            {"id": "t02", "titulo": "Texto 2", "area": "Jurídico", "ano": 2024},
        ]
        interacoes = [
            {
                "usuario": "u01",
                "area_interesse": "Financeiro",
                "interacoes": [{"texto_id": "t01", "nota": 3}],
            }
        ]

        resultado = recomendar_cold_start("Financeiro", textos, interacoes, k=5)

        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]["texto_id"], "t01")


if __name__ == "__main__":
    unittest.main()
