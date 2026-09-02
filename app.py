import streamlit as st
import sys
import os
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import minhastats as ms

from dados import carregar_dados, variaveis_numericas, variaveis_categoricas, obter_serie_numerica

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
st.write("Mediana:", mediana_calculada)
st.write("Desvio-padrão (amostral):", dp_calculado)

st.subheader("Histograma")

figura, eixo = plt.subplots()
eixo.hist(dados_da_coluna, bins=30, color="steelblue", edgecolor="white")
eixo.set_xlabel(coluna_escolhida)
eixo.set_ylabel("Frequência")
eixo.set_title(f"Distribuição de {coluna_escolhida}")

st.pyplot(figura)

outliers_encontrados = ms.detectar_outliers(dados_da_coluna)

st.subheader("Detecção de Outliers")
st.write(f"Foram encontrados **{len(outliers_encontrados)}** outliers, de um total de {len(dados_da_coluna)} observações ({100*len(outliers_encontrados)/len(dados_da_coluna):.1f}%).")

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

st.header("Estatística Descritiva — Variáveis Categóricas")

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