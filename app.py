import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import csv
import os
import minhastats as ms



st.title("Laboratório Estatístico Interativo")

arquivo = st.file_uploader(
    "Carregue seu dataset",
    type=["csv", "xlsx", "json"]
)

if arquivo is not None:

    nome_arquivo = arquivo.name.lower()
    extensao = os.path.splitext(nome_arquivo)[1]

    try:

        # CSV
        if extensao == ".csv":
            # Lê uma amostra para tentar detectar o separador
            sample = arquivo.read(4096).decode("utf-8", errors="ignore")
            arquivo.seek(0)

            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
                sep_detectado = dialect.delimiter

            except csv.Error:
                # Caso o Sniffer não consiga detectar
                # tenta os separadores mais comuns
                st.warning(
                    "Não foi possível detectar automaticamente "
                    "o separador. Tentando ';'."
                )
                sep_detectado = ";"

            arquivo.seek(0)

            df = pd.read_csv(arquivo, sep=sep_detectado, encoding="utf-8")

        # Excel
        elif extensao == ".xlsx":df = pd.read_excel(arquivo)

        # JSON
        elif extensao == ".json":df = pd.read_json(arquivo)

        else:
            st.error("Formato de arquivo não suportado.")
            df = None

        # Resultado
        if df is not None:

            st.success(
                f"Arquivo lido com sucesso! "
                f"Número de colunas: {df.shape[1]}"
            )

            st.write("Pré-visualização dos dados:")
            st.dataframe(df.head())

    except Exception as e:

        st.error(f"Não foi possível ler o arquivo: {e}")
# --------------------------------------------------------------------------- #
        
# Escolha da coluna
    coluna = st.selectbox("Escolha uma coluna:", df.select_dtypes(include="number").columns)
    if coluna:
# Verifica o tipo de dados da coluna
    
        if pd.api.types.is_numeric_dtype(df[coluna]): #coluna contêm dados quantitativos
            valores = df[coluna].dropna().tolist()
            categorico = False
        else: # coluna contêm dados qualitativos
            st.write(df[coluna].value_counts()) 
            categorico = True
            st.alert("coluna composta por dados categóricos")


# Menu de escolha do tipo de estatística
        if coluna:
            valores = df[coluna].dropna().tolist()
            escolha = st.radio(
                "Selecione o tipo de estatística:",
                ["Medidas de Posição", "Medidas de Dispersão", "Medidas de Associação"]
            )

            if escolha == "Medidas de Posição":
                st.subheader("Medidas de Posição")
                st.write("Total de inferências:", len(valores))
                st.write("Média de: ", ms.media(valores))
                st.write("Mediana: ", ms.mediana(valores))
                st.write("Moda: ", ms.moda(valores))
                st.write("Quartis: ", ms.quartis(valores))
                p = st.slider("Escolha o percentil :", min_value=0, max_value=100, value=10, step=1)
                st.write(f"Percentil {p}:", ms.percentil(valores, p))
                st.write("Percentil 90: ", ms.percentil(valores, 90))
          
            elif escolha == "Medidas de Dispersão":
                st.subheader("Medidas de Dispersão")
                st.write("Amplitude:", ms.amplitude(valores))
                st.write("Variância amostral:", ms.variancia(valores, False)) # Padrao Amostral
                st.write("Desvio Padrão amostral:", ms.desvio_padrao(valores, False)) # Padrao Amostral
                st.write("Coeficiente de Variação:", ms.coeficiente_variacao(valores, False)) # Padrao Amostral

            elif escolha == "Medidas de Associação":
                st.subheader("Medidas de Associação")
                outra_coluna = st.selectbox("Escolha outra coluna numérica:", df.select_dtypes(include="number").columns)
                if outra_coluna and outra_coluna != coluna:
                    valores2 = df[outra_coluna].dropna().tolist()
                    st.write("Covariância:", ms.covariancia(valores, valores2, False)) # Padrao Amostral
                    st.write("Correlação de Pearson:", ms.correlacao(valores, valores2))

#            elif escolha == "Distribuições":
#                st.subheader("Distribuições")
#                x = st.slider("Escolha um valor para calcular PDF/PMF", min_value=min(valores), max_value=max(valores))
#                st.write("Normal PDF:", ms.normal_pdf(x, mu=ms.media(valores), sigma=ms.desvio_padrao(valores)))
#               st.write("Poisson PMF (λ=media):", ms.poisson_pmf(x, lam=ms.media(valores)))


# --------------------------------------------------------------------------- #
# graficos
            if coluna: valores = df[coluna].dropna().tolist()    
            
            tab_medida_posicao1, tab_medida_posicao2, tab_medida_posicao3, tab_medida_posicao4 = st.tabs([
                "Medidas posição",
                "Box Plot (Diagrama de Caixa)",
                "Histograma",
                "Barras com Linha de Média"
                ])

# Aba 1 — Medidas de Posição               
            with tab_medida_posicao1:
                    st.subheader("Medidas de Posição")
                    m = ms.media(valores)
                    med = ms.mediana(valores)
                    mod = ms.moda(valores)

                    fig, ax = plt.subplots()
                    ax.hist(valores, bins=10, edgecolor="black", alpha=0.7)
                    ax.axvline(m, color="red", linestyle="--", label=f"Média: {m:.2f}")
                    ax.axvline(med, color="blue", linestyle="--", label=f"Mediana: {med:.2f}")
                    for mo in mod:
                        ax.axvline(mo, color="green", linestyle="--", label=f"Moda: {mo}")
                    ax.set_title("Distribuição dos dados e medidas de posição")
                    ax.set_xlabel("Valores")
                    ax.set_ylabel("Frequência")
                    ax.legend()
                    
                    st.pyplot(fig)
            
# Aba 2 — BoxPlot               
            with tab_medida_posicao2:
                def grafico_boxplot(valores):
                    fig, ax = plt.subplots()
                    ax.boxplot(valores)
                    ax.set_title("Boxplot")
                    ax.set_xlabel("Dados")
                    ax.set_ylabel("Valores")
                    
                    return fig

                st.pyplot(grafico_boxplot(valores))


# Aba 3 - Histograma
            with tab_medida_posicao3:
                def grafico_histograma(valores, bins=10):
                    fig, ax = plt.subplots()
                    ax.hist(valores, bins=bins, edgecolor="black", alpha=0.7)
                    ax.set_title("Histograma")
                    ax.set_xlabel("Valores")
                    ax.set_ylabel("Frequência")

                    return fig
                    
                st.pyplot(grafico_histograma(valores, bins=15))

# Aba 4 - 