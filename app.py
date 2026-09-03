import streamlit as st
import sys
import os
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import minhastats as ms

from dados import carregar_dados, variaveis_numericas, variaveis_categoricas, obter_serie_numerica
from simulacao import simular_lancamentos_moeda
from simulacao import simular_lancamentos_moeda, simular_teorema_central_limite

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