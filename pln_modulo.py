import math
import re
from collections import Counter, defaultdict

class ProcessadorTexto:
    def __init__(self, textos):
        self.textos = textos
        # Stopwords básicas em português
        self.stopwords = {"a", "o", "de", "que", "e", "do", "da", "em", "um", "para", "é", "com", "não", "uma", "os", "no", "se", "na", "por", "mais", "as", "dos", "como", "mas", "foi", "ao", "que"}
        self.indice_invertido = defaultdict(set)
        self._construir_indice()

    def limpar_texto(self, texto):
        # Remove caracteres especiais e coloca em minúsculo
        texto = re.sub(r'[^\w\s]', '', texto.lower())
        palavras = texto.split()
        return [p for p in palavras if p not in self.stopwords]

    def _construir_indice(self):
        for item in self.textos:
            palavras = self.limpar_texto(item['texto'])
            for palavra in set(palavras):
                self.indice_invertido[palavra].add(item['id'])

    def calcular_tfidf(self):
        num_docs = len(self.textos)
        vetores_tfidf = {}
        
        # Contagem de documentos por termo (DF)
        df = Counter()
        for item in self.textos:
            palavras = set(self.limpar_texto(item['texto']))
            for p in palavras:
                df[p] += 1
        
        # Cálculo TF-IDF
        for item in self.textos:
            palavras = self.limpar_texto(item['texto'])
            total_palavras = len(palavras)
            tf = Counter(palavras)
            
            vetor = {}
            for palavra, contagem in tf.items():
                # tf * idf
                tfidf = (contagem / total_palavras) * math.log(num_docs / df[palavra])
                vetor[palavra] = tfidf
            vetores_tfidf[item['id']] = vetor
        return vetores_tfidf

def similaridade_cosseno(vetor_a, vetor_b):
    interseccao = set(vetor_a.keys()) & set(vetor_b.keys())
    produto_escalar = sum(vetor_a[p] * vetor_b[p] for p in interseccao)
    
    norma_a = math.sqrt(sum(val**2 for val in vetor_a.values()))
    norma_b = math.sqrt(sum(val**2 for val in vetor_b.values()))
    
    if norma_a == 0 or norma_b == 0: return 0.0
    return produto_escalar / (norma_a * norma_b)