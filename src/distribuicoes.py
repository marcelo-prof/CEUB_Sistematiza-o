import math
from minhastats import media, desvio_padrao

def densidade_normal(x, mu, sigma):
    parte1 = 1 / (sigma * math.sqrt(2 * math.pi))
    parte2 = math.exp(-((x - mu) ** 2) / (2 * sigma ** 2))
    return parte1 * parte2

def ajustar_normal(dados):
    mu = media(dados)
    sigma = desvio_padrao(dados, "amostral")
    return mu, sigma

def densidade_exponencial(x, taxa_lambda):
    """Calcula a altura da curva Exponencial(lambda) no ponto x."""
    if x < 0:
        return 0
    return taxa_lambda * math.exp(-taxa_lambda * x)

def ajustar_exponencial(dados):
    m = media(dados)
    taxa_lambda = 1 / m
    return taxa_lambda
