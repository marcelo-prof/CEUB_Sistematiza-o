import math

def media(dados):
    
    soma = 0
    for i in dados:
        soma = soma + i
    
    media_calculada = soma / len(dados)
    return media_calculada

def mediana(dados):
    dados_ordenados = sorted(dados)
    n = len(dados_ordenados)

    if n % 2 == 0:
        valor_mediana = (dados_ordenados[n // 2 - 1] + dados_ordenados[n // 2]) / 2
    else:
        valor_mediana = dados_ordenados[n // 2]

    return valor_mediana

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

def amplitude(dados):
    valor_amplitude = max(dados) - min(dados)

    return valor_amplitude

def variancia(dados, tipo):
    m = media(dados)
    
    soma_quadrados = 0

    for i in dados:
        soma_quadrados = soma_quadrados + (i - m) ** 2
    
    if tipo == "populacional":
        divisor = len(dados)
    else:
        divisor = len(dados) - 1
    
    return soma_quadrados / divisor

def desvio_padrao(dados, tipo):
    v = variancia(dados, tipo)

    return math.sqrt(v)

def percentil(dados, p):
    dados_ordenados = sorted(dados)
    n = len(dados_ordenados)

    posicao = (p / 100) * (n - 1)

    piso = math.floor(posicao)
    teto = math.ceil(posicao)

    if piso == teto:
        return dados_ordenados[int(piso)]
    
    fracao = posicao - piso
    return dados_ordenados[piso] + fracao * (dados_ordenados[teto] - dados_ordenados[piso])

def quartis(dados):
    q1 = percentil(dados, 25)
    q2 = percentil(dados, 50)
    q3 = percentil(dados, 75)

    return q1, q2, q3

def coeficiente_variacao(dados, tipo):
    dp = desvio_padrao(dados, tipo)
    m = media(dados)

    return (dp / m) * 100

def covariancia(x, y, tipo):
    mx = media(x)
    my = media(y)

    soma = 0

    for xi, yi in zip(x, y):
        soma = soma + (xi - mx) * (yi - my)
    
    if tipo == "populacional":
        divisor = len(x)
    else:
        divisor = len(x) - 1
    
    return soma / divisor

def correlacao_pearson(x, y):
    cov = covariancia(x, y, "amostral")
    dpx = desvio_padrao(x, "amostral")
    dpy = desvio_padrao(y, "amostral")

    return cov / (dpx * dpy)