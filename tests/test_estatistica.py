import math
import numpy as np
import scipy.stats as stats
import src.minhastats as ms

#from minhastats import media, mediana, moda, amplitude, variancia, desvio_padrao, coeficiente_variacao, percentil, quartis, covariancia, correlacao


# testes automatizados com tolerância númerica documentada
# (rtol=1e-8) 

def test_media():
    dados = [1, 2, 3, 4, 5]
    assert math.isclose(ms.media(dados), np.mean(dados), rel_tol=1e-8)

def test_mediana():
    dados = [1, 2, 3, 4, 5]
    assert math.isclose(ms.mediana(dados), np.median(dados), rel_tol=1e-8)

def test_moda():
    dados = [1, 2, 2, 3, 3, 3, 4]
    assert set(ms.moda(dados)) == set(stats.mode(dados, keepdims=True).mode)

def test_amplitude():
    dados = [10, 20, 30, 40]
    assert math.isclose(ms.amplitude(dados), np.ptp(dados), rel_tol=1e-8)

def test_variancia_populacional():
    dados = [1, 2, 3, 4, 5]
    populacional = True
    assert math.isclose(ms.variancia(dados, populacional), np.var(dados, ddof=0), rel_tol=1e-8)

def test_variancia_amostral():
    dados = [1, 2, 3, 4, 5]
    populacional = False
    assert math.isclose(ms.variancia(dados, populacional), np.var(dados, ddof=1), rel_tol=1e-8)

def test_desvio_padrao_populacional():
    dados = [1, 2, 3, 4, 5]
    populacional = True
    assert math.isclose(ms.desvio_padrao(dados, populacional), np.std(dados, ddof=0), rel_tol=1e-8)

def test_desvio_padrao_amostral():
    dados = [1, 2, 3, 4, 5]
    populacional = False
    assert math.isclose(ms.desvio_padrao(dados, populacional), np.std(dados, ddof=1), rel_tol=1e-8)

def test_coeficiente_variacao():
    dados = [10, 20, 30, 40, 50]
    esperado = (np.std(dados, ddof=1) / np.mean(dados)) * 100
    populacional = False
    assert math.isclose(ms.coeficiente_variacao(dados, populacional), esperado, rel_tol=1e-8)

def test_percentil():
    dados = [15, 20, 35, 40, 50]
    for p in [25, 50, 75]:
        assert math.isclose(ms.percentil(dados, p), np.percentile(dados, p), rel_tol=1e-8)

def test_quartis():
    dados = [15, 20, 35, 40, 50]
    q1, q2, q3 = ms.quartis(dados)
    np_q1, np_q2, np_q3 = np.percentile(dados, [25, 50, 75])
    assert math.isclose(q1, np_q1, rel_tol=1e-8)
    assert math.isclose(q2, np_q2, rel_tol=1e-8)
    assert math.isclose(q3, np_q3, rel_tol=1e-8)

def test_covariancia_amostral():
    x = [2, 4, 6, 8]
    y = [1, 3, 5, 7]
    populacional = False
    assert math.isclose(ms.covariancia(x, y, populacional), np.cov(x, y, ddof=1)[0,1], rel_tol=1e-8)

def test_covariancia_populacional():
    x = [2, 4, 6, 8]
    y = [1, 3, 5, 7]
    populacional = True
    assert math.isclose(ms.covariancia(x, y, populacional), np.cov(x, y, ddof=0)[0,1], rel_tol=1e-8)

def test_correlacao():
    x = [2, 4, 6, 8]
    y = [1, 3, 5, 7]
    assert math.isclose(ms.correlacao(x, y), stats.pearsonr(x, y)[0], rel_tol=1e-8)