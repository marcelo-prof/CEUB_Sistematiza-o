import math
import pandas as pd
import numpy as np 
import random

#limitar as casas decimais
def truncar_dados(dados, num: int):
    match num:
        case 0:
            return int(dados)
        case 1:
            return math.floor(dados * 10) / 10
        case 2:
            return math.floor(dados * 100) / 100
        case 3:
            return math.floor(dados * 1000) / 1000
        case _:
            return dados


def soma_total(dados):
    num = 0
    for i in dados:
        num += i
    return num
# -------------------------------------------------------------------- #
# medida de posição central
def media(dados):
    soma = 0
    for i in dados:
        soma = soma + i
    media_calculada = soma / len(dados)
    return float(media_calculada)


# medida de posição central
def mediana(dados):
    dados_ordenados = sorted(dados)
    n = len(dados_ordenados)

    if n % 2 == 0:
        valor_mediana = (dados_ordenados[n // 2 - 1] + dados_ordenados[n // 2]) / 2
    else:
        valor_mediana = dados_ordenados[n // 2]
    return float(valor_mediana)


# medida de posição central
def moda(dados):
    contagem = {}

    for i in dados:
        if i in contagem:
            contagem[i] = contagem[i] + 1
        else:
            contagem[i] = 1
    maior_frequencia = max(contagem.values())
    moda = []

    for chave, valor in contagem.items():
        if valor == maior_frequencia:
            moda.append(chave)
    return moda


# -------------------------------------------------------------------- #
# medida de dispersão
def amplitude(dados):
    valor_amplitude = max(dados) - min(dados)
    return valor_amplitude


# medida de dispersão
def variancia(dados: list, populacional: bool = True) -> float:
    m = media(dados)
    soma = sum((x - m) ** 2 for x in dados)
    if populacional:
        return soma / len(dados)
    else:
        return soma / (len(dados) - 1)


# medida de dispersão
def desvio_padrao(dados: list, populacional: bool = True) -> float:
    return math.sqrt(variancia(dados, populacional))



# medida de dispersão 
def coeficiente_variacao(dados: list, populacional: bool = True) -> float:
    dp = desvio_padrao(dados, populacional)
    m = media(dados)
    return (dp / m) * 100
# -------------------------------------------------------------------- #


# medida de posição
def percentil(dados, p):
    dados_ordenados = sorted(dados)
    n = len(dados_ordenados)

    posicao = (p / 100) * (n - 1)

    piso = math.floor(posicao)
    teto = math.ceil(posicao)

    if piso == teto:
        return float(dados_ordenados[int(piso)])
    fracao = posicao - piso
    return float(dados_ordenados[piso] + fracao * (dados_ordenados[teto] - dados_ordenados[piso]))


# medida de posição
def quartis(dados):
    q1 = float(percentil(dados, 25))
    q2 = float(mediana(dados))  # Reutilizando a função mediana
    q3 = float(percentil(dados, 75))
    
    return q1, q2, q3
# -------------------------------------------------------------------- #


# medida de associação
def covariancia(x: list, y: list, populacional: bool = True) -> float:
    mx = media(x)
    my = media(y)
    soma = 0

    for xi, yi in zip(x, y):
        soma = soma + (xi - mx) * (yi - my)

    if populacional:
        divisor = len(x)
    else:
        divisor = len(x) - 1
        
    return soma / divisor


# medida de associação
def correlacao(x, y):
    cov = covariancia(x, y, populacional=False)
    dpx = desvio_padrao(x, populacional=False)
    dpy = desvio_padrao(y, populacional=False)
    return cov / (dpx * dpy)
# -------------------------------------------------------------------- #


def detectar_outliers(dados):
    q1, q2, q3 = quartis(dados)

    iqr = q3 - q1

    limite_inferior = q1 - 1.5 * iqr
    limite_superior = q3 + 1.5 * iqr

    outliers = []

    for valor in dados:
        if valor < limite_inferior or valor > limite_superior:
            outliers.append(valor)
    return outliers


def tabela_frequencias(categorias):
    contagem = {}

    for categoria in categorias:
        if categoria in contagem:
            contagem[categoria] = contagem[categoria] + 1
        else:
            contagem[categoria] = 1
    return contagem


def assimetria(dados):
    m = media(dados)
    md = mediana(dados)
    dp = desvio_padrao(dados, False)

    return 3 * (m - md) / dp


def regressao_linear(x, y):
    cov = covariancia(x, y, False)
    var_x = variancia(x, False)

    b1 = cov / var_x
    b0 = media(y) - b1 * media(x)

    return b0, b1


def r_quadrado(x, y):
    r = correlacao(x, y)
    return r ** 2

# -------------------------------------------------------------------- #

def obter_serie_num(df, coluna):
    return df[coluna].dropna().astype(float).tolist()


def obter_serie_cat(df, coluna):
    return df[coluna].dropna().astype(str).tolist()


# -------------------------------------------------------------------- #

def densidade_normal(x, mu, sigma):
    parte1 = 1 / (sigma * math.sqrt(2 * math.pi))
    parte2 = math.exp(-((x - mu) ** 2) / (2 * sigma ** 2))
    return parte1 * parte2

def ajustar_normal(dados):
    mu = media(dados)
    sigma = desvio_padrao(dados, False)
    return mu, sigma

def densidade_exponencial(x, taxa_lambda):
    # Calcula a altura da curva Exponencial(lambda) no ponto x. 
    if x < 0:
        return 0
    return taxa_lambda * math.exp(-taxa_lambda * x)

def ajustar_exponencial(dados):
    m = media(dados)
    taxa_lambda = 1 / m
    return taxa_lambda

# -------------------------------------------------------------------- #


#simulação lançamento de moedas
def simular_lanca_moedas(numero_de_lancamentos):
    caras_ate_agora = 0
    frequencias_ao_longo_do_tempo = []

    for i in range(1, numero_de_lancamentos + 1):
        resultado = random.choice(["cara", "coroa"])

        if resultado == "cara":
            caras_ate_agora = caras_ate_agora + 1

        frequencia_atual = caras_ate_agora / i
        frequencias_ao_longo_do_tempo.append(frequencia_atual)

    return frequencias_ao_longo_do_tempo


# simulação teoria central do limite
def simular_tcl(populacao_de_dados, tamanho_da_amostra, numero_de_repeticoes):

    medias_das_amostras = []

    for i in range(numero_de_repeticoes):

        amostra = np.random.choice(
            populacao_de_dados,
            size=tamanho_da_amostra,
            replace=True
        )

        media_da_amostra = media(amostra)

        medias_das_amostras.append(media_da_amostra)

    return medias_das_amostras