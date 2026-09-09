import math
import numpy as np
import scipy.stats as stats
import src.minhastats as ms

#from src.minhastats import  media, mediana, moda, amplitude, variancia, desvio_padrao, coeficiente_variacao, percentil, quartis, covariancia, correlacao


dados = [1, 2, 3, 4, 5]
x = [2, 4, 6, 8]
y = [1, 3, 5, 7]

print("=== Testes manuais ===")

# Média
print("Média:", ms.media(dados), " | NumPy:", np.mean(dados))

# Mediana
print("Mediana:", ms.mediana(dados), " | NumPy:", np.median(dados))

# Moda
print("Moda:", ms.moda(dados), " | SciPy:", stats.mode(dados, keepdims=True).mode)

# Amplitude
print("Amplitude:", ms.amplitude(dados), " | NumPy:", np.ptp(dados))

# Variância
print("Variância populacional:", ms.variancia(dados, True), " | NumPy:", np.var(dados, ddof=0))
print("Variância amostral:", ms.variancia(dados, False), " | NumPy:", np.var(dados, ddof=1))

# Desvio padrão
print("Desvio padrão populacional:", ms.desvio_padrao(dados, True), " | NumPy:", np.std(dados, ddof=0))
print("Desvio padrão amostral:", ms.desvio_padrao(dados, False), " | NumPy:", np.std(dados, ddof=1))

# Coeficiente de variação
print("Coeficiente de variação:", ms.coeficiente_variacao(dados, False), " | NumPy:", (np.std(dados, ddof=1)/np.mean(dados))*100)

# Percentis e quartis
for p in [25, 50, 75]:
    print(f"Percentil {p}:", ms.percentil(dados, p), " | NumPy:", np.percentile(dados, p))

q1, q2, q3 = ms.quartis(dados)
np_q1, np_q2, np_q3 = np.percentile(dados, [25, 50, 75])
print("Quartis:", (q1, q2, q3), " | NumPy:", (np_q1, np_q2, np_q3))

# Covariância
print("Covariância populacional:", ms.covariancia(x, y, True), " | NumPy:", np.cov(x, y, ddof=0)[0,1])
print("Covariância amostral:", ms.covariancia(x, y, False), " | NumPy:", np.cov(x, y, ddof=1)[0,1])

# Correlação
print("Correlação:", ms.correlacao(x, y), " | SciPy:", stats.pearsonr(x, y)[0])
