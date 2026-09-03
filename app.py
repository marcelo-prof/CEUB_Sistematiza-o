import streamlit as st
import sys
import os
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import numpy as np
import minhastats as ms

from dados import carregar_dados, variaveis_numericas, variaveis_categoricas, obter_serie_numerica
from simulacao import simular_lancamentos_moeda
from simulacao import simular_lancamentos_moeda, simular_teorema_central_limite
from distribuicoes import ajustar_normal, densidade_normal, ajustar_exponencial, densidade_exponencial

st.title("Laboratório Estatístico Interativo")
st.write("Base de Dados: municípios brasileiros — renda, PIB e população")

df = carregar_dados()

st.write(f"A Base de Dados tem {df.shape[0]} linhas e {df.shape[1]} colunas.")
st.dataframe(df.head(20))

nomes_das_colunas = list(variaveis_numericas.keys())
coluna_escolhida = st.selectbox("Escolha uma variável numérica:", nomes_das_colunas)

dados_da_coluna = obter_serie_numerica(df, coluna_escolhida)

media_calculada = ms.media(dados_da_coluna)
mediana_calculada = ms.mediana(dados_da_coluna)
dp_calculado = ms.desvio_padrao(dados_da_coluna, "amostral")

q1, q2, q3 = ms.quartis(dados_da_coluna)
moda_calculada = ms.moda(dados_da_coluna)
amplitude_calculada = ms.amplitude(dados_da_coluna)
cv_calculado = ms.coeficiente_variacao(dados_da_coluna, "amostral")

coluna1, coluna2, coluna3 = st.columns(3)

with coluna1:
    st.metric("Média", f"{media_calculada:.2f}")
    st.metric("Mediana", f"{mediana_calculada:.2f}")

with coluna2:
    st.metric("Desvio-padrão", f"{dp_calculado:.2f}")
    st.metric("Coeficiente de variação", f"{cv_calculado:.1f}%")

with coluna3:
    st.metric("Amplitude", f"{amplitude_calculada:.2f}")
    st.write("Moda:", moda_calculada)

st.write(f"Quartis: Q1 = {q1:.2f} | Q2 = {q2:.2f} | Q3 = {q3:.2f}")

st.subheader("Histograma")

figura, eixo = plt.subplots()
eixo.hist(dados_da_coluna, bins=30, color="steelblue", edgecolor="white")
eixo.set_xlabel(coluna_escolhida)
eixo.set_ylabel("Frequência")
eixo.set_title(f"Distribuição de {coluna_escolhida}")

st.pyplot(figura)

outliers_encontrados = ms.detectar_outliers(dados_da_coluna)

st.subheader("Detecção de Outliers")
st.write(f"Foram encontrados {len(outliers_encontrados)} outliers, de um total de {len(dados_da_coluna)} observações ({100*len(outliers_encontrados)/len(dados_da_coluna):.1f}%).")

if len(outliers_encontrados) > 0:
    st.write("Alguns exemplos de valores considerados outliers:")
    st.write(outliers_encontrados[:10])

assimetria_calculada = ms.assimetria(dados_da_coluna)

if assimetria_calculada > 0.5:
    interpretacao = "assimétrica à direita (cauda longa de valores altos)"
elif assimetria_calculada < -0.5:
    interpretacao = "assimétrica à esquerda (cauda longa de valores baixos)"
else:
    interpretacao = "aproximadamente simétrica"

st.write(f"Interpretação automática: a distribuição de `{coluna_escolhida}` é {interpretacao} (coeficiente de assimetria = {assimetria_calculada:.2f}).")

st.subheader("Estatística Descritiva - Variáveis Categóricas")

from dados import obter_serie_categorica

nomes_categoricas = list(variaveis_categoricas.keys())
coluna_cat_escolhida = st.selectbox("Escolha uma variável categórica:", nomes_categoricas)

dados_categoricos = obter_serie_categorica(df, coluna_cat_escolhida)
frequencias = ms.tabela_frequencias(dados_categoricos)

st.write("Tabela de frequências:")
st.write(frequencias)

categorias = list(frequencias.keys())
valores = list(frequencias.values())

st.subheader("Gráfico de barras")

figura3, eixo3 = plt.subplots()
eixo3.bar(categorias, valores, color="steelblue")
eixo3.set_xlabel(coluna_cat_escolhida)
eixo3.set_ylabel("Frequência")
eixo3.set_title(f"Distribuição de {coluna_cat_escolhida}")

plt.xticks(rotation=90)
st.pyplot(figura3)

st.subheader("Lei dos Grandes Números")

numero_lancamentos = st.slider("Número de lançamentos da moeda:", min_value=10, max_value=5000, value=100)

frequencias = simular_lancamentos_moeda(numero_lancamentos)

st.write(f"Frequência relativa de 'cara' após {numero_lancamentos} lançamentos: {frequencias[-1]:.4f}")

figura_lgn, eixo_lgn = plt.subplots()
eixo_lgn.plot(frequencias)
eixo_lgn.axhline(y=0.5, color="red", linestyle="--", label="Probabilidade teórica (0.5)")
eixo_lgn.set_xlabel("Número de lançamentos")
eixo_lgn.set_ylabel("Frequência relativa de 'cara'")
eixo_lgn.set_title("Lei dos Grandes Números")
eixo_lgn.legend()

st.pyplot(figura_lgn)

st.subheader("Teorema Central do Limite")

nomes_numericas_tcl = list(variaveis_numericas.keys())
coluna_tcl = st.selectbox("Escolha uma variável para o TCL:", nomes_numericas_tcl)

dados_populacao_tcl = obter_serie_numerica(df, coluna_tcl)

tamanho_amostra = st.slider("Tamanho de cada amostra:", min_value=2, max_value=200, value=30)
numero_repeticoes = st.slider("Número de repetições (quantas amostras sortear):", min_value=100, max_value=5000, value=1000)

medias_amostrais = simular_teorema_central_limite(dados_populacao_tcl, tamanho_amostra, numero_repeticoes)

coluna_esquerda, coluna_direita = st.columns(2)

with coluna_esquerda:
    st.write("Distribuição ORIGINAL (população completa):")
    figura_original, eixo_original = plt.subplots()
    eixo_original.hist(dados_populacao_tcl, bins=30, color="steelblue", edgecolor="white")
    eixo_original.set_title(f"{coluna_tcl} (original)")
    st.pyplot(figura_original)

with coluna_direita:
    st.write("Distribuição das MÉDIAS AMOSTRAIS:")
    figura_medias, eixo_medias = plt.subplots()
    eixo_medias.hist(medias_amostrais, bins=30, color="darkorange", edgecolor="white")
    eixo_medias.set_title(f"Médias de amostras (n={tamanho_amostra})")
    st.pyplot(figura_medias)

st.subheader("Distribuições Teóricas")

nomes_dist = list(variaveis_numericas.keys())
coluna_dist = st.selectbox("Escolha uma variável:", nomes_dist, key="selectbox_distribuicoes")

dados_dist = obter_serie_numerica(df, coluna_dist)

distribuicao_escolhida = st.radio("Distribuição teórica:", ["Normal", "Exponencial"])

figura_dist, eixo_dist = plt.subplots()
eixo_dist.hist(dados_dist, bins=40, density=True, color="steelblue", edgecolor="white", alpha=0.7, label="Dados reais")

pontos_x = np.linspace(min(dados_dist), max(dados_dist), 200)

if distribuicao_escolhida == "Normal":
    mu, sigma = ajustar_normal(dados_dist)
    pontos_y = [densidade_normal(x, mu, sigma) for x in pontos_x]
    st.write(f"Parâmetros estimados: μ (média) = {mu:.2f}, σ (desvio-padrão) = {sigma:.2f}")
else:
    taxa = ajustar_exponencial(dados_dist)
    pontos_y = [densidade_exponencial(x, taxa) for x in pontos_x]
    st.write(f"Parâmetro estimado: λ (taxa) = {taxa:.6f}")

eixo_dist.plot(pontos_x, pontos_y, color="red", linewidth=2, label=f"{distribuicao_escolhida} ajustada")
eixo_dist.set_title(f"{coluna_dist}: dados reais vs. {distribuicao_escolhida}")
eixo_dist.legend()

st.pyplot(figura_dist)

st.subheader("Correlação e Regressão Linear")

nomes_regressao = list(variaveis_numericas.keys())

coluna_x = st.selectbox("Variável X (independente):", nomes_regressao, key="select_x")
coluna_y = st.selectbox("Variável Y (dependente):", nomes_regressao, key="select_y", index=1)

dados_x = df[coluna_x].tolist()
dados_y = df[coluna_y].tolist()

b0, b1 = ms.regressao_linear(dados_x, dados_y)
r2 = ms.r_quadrado(dados_x, dados_y)
r = ms.correlacao(dados_x, dados_y)

st.write(f"Correlação de Pearson (r): {r:.4f}")
st.write(f"R² (coeficiente de determinação): {r2:.4f}")
st.write(f"Equação da reta: ŷ = {b0:.4f} + {b1:.4f} × x")

st.write(f"Interpretação: para cada unidade a mais em `{coluna_x}`, espera-se uma variação de **{b1:.4f}** em `{coluna_y}`, em média.")

st.subheader("Gráfico de dispersão com reta de regressão")

figura_regressao, eixo_regressao = plt.subplots()
eixo_regressao.scatter(dados_x, dados_y, alpha=0.3, s=10, color="steelblue", label="Municípios")

x_minimo = min(dados_x)
x_maximo = max(dados_x)
y_no_minimo = b0 + b1 * x_minimo
y_no_maximo = b0 + b1 * x_maximo

eixo_regressao.plot([x_minimo, x_maximo], [y_no_minimo, y_no_maximo], color="red", linewidth=2, label="Reta de regressão")

eixo_regressao.set_xlabel(coluna_x)
eixo_regressao.set_ylabel(coluna_y)
eixo_regressao.set_title(f"{coluna_y} em função de {coluna_x}")
eixo_regressao.legend()

st.pyplot(figura_regressao)

st.subheader("Predição interativa")

media_x = ms.media(dados_x)
valor_x_digitado = st.number_input(f"Digite um valor de {coluna_x}:", value=media_x)

valor_y_previsto = b0 + b1 * valor_x_digitado

st.write(f"Predição: para {coluna_x} = {valor_x_digitado:.2f}, o modelo prevê {coluna_y} ≈ {valor_y_previsto:.2f}")

st.warning(
    "Atenção: correlação não implica causalidade. O fato de duas variáveis "
    "estarem correlacionadas não significa necessariamente "
    "que uma causa a outra diretamente. Pode haver outros fatores em comum "
    "influenciando as duas (por exemplo, municípios maiores tendem a ter mais "
    "infraestrutura, comércio e serviços, o que afeta tanto população quanto PIB "
    "simultaneamente), ou a relação pode ser bem mais complexa do que uma simples reta."
)