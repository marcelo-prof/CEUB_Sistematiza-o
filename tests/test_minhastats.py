import sys
import os
import math

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import minhastats as ms
import numpy as np

from scipy import stats

def test_media():
    dados = [10, 20, 30, 40]

    resultado_meu = ms.media(dados)
    resultado_numpy = np.mean(dados)

    assert math.isclose(resultado_meu, resultado_numpy)

def test_mediana():
    dados = [10, 20, 30, 40]

    resultado_meu = ms.mediana(dados)
    resultado_numpy = np.median(dados)

    assert math.isclose(resultado_meu, resultado_numpy)

def test_variancia_amostral():
    dados = [10, 20, 30, 40]

    resultado_meu = ms.variancia(dados, "amostral")
    resultado_numpy = np.var(dados, ddof=1)

    assert math.isclose(resultado_meu, resultado_numpy)

def test_variancia_populacional():
    dados = [10, 20, 30, 40]

    resultado_meu = ms.variancia(dados, "populacional")
    resultado_numpy = np.var(dados, ddof=0)

    assert math.isclose(resultado_meu, resultado_numpy)

def test_desvio_padrao():
    dados = [10, 20, 30, 40]

    resultado_meu = ms.desvio_padrao(dados, "amostral")
    resultado_numpy = np.std(dados, ddof=1)
    
    assert math.isclose(resultado_meu, resultado_numpy)

def test_amplitude():
    dados = [10, 20, 30, 40]

    resultado_meu = ms.amplitude(dados)
    resultado_numpy = np.max(dados) - np.min(dados)

    assert math.isclose(resultado_meu, resultado_numpy)

def test_percentil_25():
    dados = [10, 20, 30, 40, 50]

    resultado_meu = ms.percentil(dados, 25)
    resultado_numpy = np.percentile(dados, 25)

    assert math.isclose(resultado_meu, resultado_numpy)

def test_percentil_75():
    dados = [10, 20, 30, 40, 50]

    resultado_meu = ms.percentil(dados, 75)
    resultado_numpy = np.percentile(dados, 75)

    assert math.isclose(resultado_meu, resultado_numpy)

def test_coeficiente_variacao():
    dados = [10, 20, 30, 40]

    resultado_meu = ms.coeficiente_variacao(dados, "amostral")
    resultado_numpy = (np.std(dados, ddof=1) / abs(np.mean(dados))) * 100

    assert math.isclose(resultado_meu, resultado_numpy)

def test_moda():
    dados = [1, 1, 2, 2, 3]

    resultado_meu = ms.moda(dados)

    assert resultado_meu == [1, 2]

def test_covariancia():
    x = [10, 20, 30, 40]
    y = [1000, 1500, 1300, 2000]

    resultado_meu = ms.covariancia(x, y, "amostral")
    resultado_numpy = np.cov(x, y, ddof=1)[0][1]

    assert math.isclose(resultado_meu, resultado_numpy)

def test_correlacao():
    x = [10, 20, 30, 40]
    y = [1000, 1500, 1300, 2000]

    resultado_meu = ms.correlacao(x, y)
    resultado_scipy, _ = stats.pearsonr(x, y)

    assert math.isclose(resultado_meu, resultado_scipy)