import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import openpyxl
import csv
import os
import src.minhastats as ms



st.title("Laboratório Estatístico Interativo")

arquivo = st.file_uploader(
    "Carregue seu dataset",
    type=["csv", "xlsx", "json"]
)

if arquivo is not None:

    nome_arquivo = arquivo.name.lower()
    extensao = os.path.splitext(nome_arquivo)[1]

    # leitura e identificação do arquivo    
    try:

        # CSV
        if extensao == ".csv":
            # lê uma amostra para tentar detectar o separador
            sample = arquivo.read(4096).decode("utf-8", errors="ignore")
            arquivo.seek(0)

            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
                sep_detectado = dialect.delimiter

            except csv.Error:
                # caso o Sniffer não consiga detectar
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

        # não foi possível ler o arquivo
        else:
            st.error("Formato de arquivo não suportado.")
            df = None

        # resultado
        if df is not None:

            st.success(
                f"Arquivo lido com sucesso! "
                f"Número de colunas: {df.shape[1]}"
            )

            st.write("Pré-visualização dos dados:")
            st.dataframe(df.head())

    # arquivo não suportado
    except Exception as e:

        st.error(f"Não foi possível ler o arquivo: {e}")
# --------------------------------------------------------------------------- #

    #COLOCAR UMA OPCAO VAZIA#
    # escolha da coluna    
    coluna_selecao = st.selectbox("Escolha uma coluna:", df.select_dtypes(include=["number", "object"]).columns)

    
    # verifica o tipo de dados da coluna    
    if coluna_selecao:

        #se a coluna escolhida foi de dados númericos   
        if pd.api.types.is_numeric_dtype(df[coluna_selecao]): 
            coluna_numerica = coluna_selecao
            st.success("coluna composta por dados númericos")
            valores = df[coluna_numerica].dropna().tolist()
            categorico = False
            
        #se a coluna escolhida foi dados categóricos
        else:
            coluna_categorica = coluna_selecao
            st.success("coluna composta por dados categóricos")
            st.write(df[coluna_categorica].value_counts()) 
            categorico = True
            


        # estatística para dados numéricos
        if not categorico:
            valores = df[coluna_numerica].dropna().tolist()
            escolha = st.radio(
                "Selecione o tipo de estatística:",
                ["Medidas de Posição", "Medidas de Dispersão", "Medidas de Associação"]
            )
            # estatística para as medidas de posição central
            if escolha == "Medidas de Posição":
                st.subheader("Medidas de Posição")
                st.write("Total de inferências:", len(valores))
                st.write("Soma Total: ", sum(valores))
                st.write("Média de: ", ms.media(valores))
                st.write("Mediana: ", ms.mediana(valores))
                st.write("Moda: ", ms.moda(valores))
                st.write("Quartis: ", ms.quartis(valores))
                p = st.slider("Escolha o percentil :", min_value=0, max_value=100, value=10, step=1)
                st.write(f"Percentil {p}:", ms.percentil(valores, p))
                st.write("Percentil 90: ", ms.percentil(valores, 90))
            
            # estatística para as medidas de dispersão
            elif escolha == "Medidas de Dispersão":
                st.subheader("Medidas de Dispersão")
                st.write("Total de Inferências:", len(valores))
                st.write("Soma Total: ", sum(valores))
                st.write("Valor mínimo: ", min(valores))
                st.write("Valor máximo: ", max(valores))
                st.write("Amplitude:", ms.amplitude(valores))
                
                # conferir se trata de dados populacionais ou dados amostrais
                dados_pop = st.toggle("DADOS POPULACIONAIS")
                
                    # dados populacionais
                if dados_pop:
                    st.write("Variância populacional:", ms.variancia(valores, dados_pop))
                    st.write("Desvio Padrão populacional:", ms.desvio_padrao(valores, dados_pop))
                    st.write("Coeficiente de Variação:", ms.coeficiente_variacao(valores, dados_pop))

                    # dados amostrais
                else:
                    st.write("Variância amostral:", ms.variancia(valores, dados_pop))
                    st.write("Desvio Padrão amostral:", ms.desvio_padrao(valores, dados_pop))
                    st.write("Coeficiente de Variação:", ms.coeficiente_variacao(valores, dados_pop))

            # estatística para as medidas de dispersão
            elif escolha == "Medidas de Associação":
                
                st.subheader("Medidas de Associação")
                outra_coluna = st.selectbox("Escolha outra coluna numérica:", df.select_dtypes(include="number").columns)

                #escolher outra coluna que seja diferente da primeira escolhida
                if outra_coluna and outra_coluna != coluna_numerica:

                    # conferir se trata de dados populacionais ou dados amostrais
                    dados_pop2 = st.toggle("DADOS POPULACIONAIS")
                    
                    #dado populacional
                    if dados_pop2:    
                        valores2 = df[outra_coluna].dropna().tolist()
                        st.write("Covariância populacional: ", ms.covariancia(valores, valores2, dados_pop2))
                    
                    # dado amostral
                    else:
                        valores2 = df[outra_coluna].dropna().tolist()
                        st.write("Covariância amostral: ", ms.covariancia(valores, valores2, dados_pop2))
               
                    st.write("Correlação de Pearson:", ms.correlacao(valores, valores2))
                
                else: 
                    st.error("Escolha uma coluna diferente/válida")
# --------------------------------------------------------------------------- #
# graficos
            if coluna_numerica: valores = df[coluna_numerica].dropna().tolist()    
            
            tab_grafico1, tab_grafico2, tab_grafico3 = st.tabs([
                "Medidas posição",
                "Box Plot (Diagrama de Caixa)",
                "Histograma"
                ])

# Aba 1 — Medidas de Posição               
            with tab_grafico1:
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
            with tab_grafico2:
                def grafico_boxplot(valores):
                    fig, ax = plt.subplots()
                    ax.boxplot(valores)
                    ax.set_title("Boxplot")
                    ax.set_xlabel("Dados")
                    ax.set_ylabel("Valores")
                    
                    return fig

                st.pyplot(grafico_boxplot(valores))


# Aba 3 - Histograma
            with tab_grafico3:
                def grafico_histograma(valores, bins=10):
                    fig, ax = plt.subplots()
                    ax.hist(valores, bins=bins, edgecolor="black", alpha=0.7)
                    ax.set_title("Histograma")
                    ax.set_xlabel("Valores")
                    ax.set_ylabel("Frequência")

                    return fig
                    
                st.pyplot(grafico_histograma(valores, bins=15))

# Aba 4 - 