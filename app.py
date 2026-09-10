import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import openpyxl
import csv
import os
import src.minhastats as ms
import src.funcoes_graficos as graf



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
        
            # valores e exibir
#            st.write(df[coluna_categorica].value_counts())
#            st.write(df[coluna_categorica].value_counts(normalize=True) * 100)            
            freq_abs = df[coluna_categorica].value_counts()
            freq_rel = df[coluna_categorica].value_counts(normalize=True) * 100
            st.subheader("Frequência Absoluta")
            st.write(freq_abs)
            st.subheader("Frequência Relativa")
            st.write(freq_rel.round(2))
            valores_categoricos = df[coluna_categorica].dropna().tolist()
            categorico = True

        if categorico:
            
            # gráficos
            tab_grafico1, tab_grafico2, tab_grafico3, tab_grafico4 = st.tabs([
                "Histograma",
                "Gráfico de Pizza",
                "Grafico de Barras",
                "Diagrama de pontos"
                ])

            
            # Aba 1 — Histograma           
            with tab_grafico1:
                graf1 = graf.grafico_histograma(valores_categoricos)
                st.pyplot(graf1)
                
            
            # Aba 2 - Gráfico de Pizza
            with tab_grafico2:
                graf2 = graf.grafico_pizza_categorico(valores_categoricos)
                st.pyplot(graf2)
            
            # Aba 3 - Grafico de Barras                                 
            with tab_grafico3:
                graf3 = graf.grafico_barras_categorico(valores_categoricos, titulo=f"Distribuição de {coluna_categorica}")

                st.pyplot(graf3)
                
            # Aba 4 - Grafico de Pontos
            with tab_grafico4:
                graf4 = graf.grafico_pontos_categorico(valores_categoricos)
                st.pyplot(graf4)
                
        
        # estatística para dados numéricos
        else:
            valores = df[coluna_numerica].dropna().tolist()
            escolha = st.radio(
                "Selecione o tipo de estatística:",
                ["Medidas de Posição", "Medidas de Dispersão", "Medidas de Associação", "Distribuição Teórica", "Teoria Central do Limite", "Lei dos Grandes Números", "Outliers"]
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
            
            # valores e exibir
            elif escolha == "Medidas de Dispersão":
                st.subheader("Medidas de Dispersão")
                st.write("Total de Inferências:", len(valores))
                st.write("Soma Total: ", sum(valores))
                st.write("Valor mínimo: ", min(valores))
                st.write("Valor máximo: ", max(valores))
                st.write("Amplitude:", ms.amplitude(valores))
            ##################
                
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

            
            # teoria central do limite
            elif escolha == "Teoria Central do Limite":

                st.subheader("Teorema Central do Limite")

                coluna_tcl = coluna_numerica

                dados_populacao_tcl = ms.obter_serie_num(df, coluna_numerica)

                tamanho_amostra = st.slider("Tamanho de cada amostra:", min_value=2, max_value=500, value=100)
                numero_repeticoes = st.slider("Número de repetições:", min_value=100, max_value=5000, value=1000)
                medias_amostrais = ms.simular_tcl(dados_populacao_tcl, tamanho_amostra, numero_repeticoes)
                media_populacao = ms.media(dados_populacao_tcl)
                media_das_amostras = ms.media(medias_amostrais)
                coluna_esquerda, coluna_direita = st.columns(2)

                
                # distribuição original
                with coluna_esquerda:
                    
                    st.write("Distribuição ORIGINAL (população completa):")
                    figura_original, eixo_original = plt.subplots()
                    eixo_original.hist(dados_populacao_tcl, bins=30, color="steelblue", edgecolor="white")
                    eixo_original.axvline(media_populacao, color="red", linestyle="--", linewidth=2, label=f"Média = {media_populacao:.2f}")
                    eixo_original.set_title(f"{coluna_tcl} (original)")
                    eixo_original.set_xlabel("Valor")
                    eixo_original.set_ylabel("Frequência")
                    eixo_original.legend()
                    st.pyplot(figura_original)


                    # distribuição das médias
                    with coluna_direita:
                        st.write("Distribuição das MÉDIAS AMOSTRAIS:")
                        figura_medias, eixo_medias = plt.subplots()
                        eixo_medias.hist(medias_amostrais, bins=30, color="darkorange", edgecolor="white")
                        eixo_medias.axvline(media_populacao, color="red", linestyle="--", linewidth=2, label=f"Média população = {media_populacao:.2f}")
                        eixo_medias.axvline(media_das_amostras, color="black", linestyle="--", linewidth=2, label=f"Média das amostras = {media_das_amostras:.2f}")
                        eixo_medias.set_title(f"Médias de amostras (n={tamanho_amostra})")
                        eixo_medias.set_xlabel("Média amostral")
                        eixo_medias.set_ylabel("Frequência")

                        eixo_medias.legend()

                        st.pyplot(figura_medias)


            # distribuição teórica    
            elif escolha == "Distribuição Teórica":
                nomes_dist = valores
                coluna_dist = coluna_selecao
                dados_dist = ms.obter_serie_num(df, coluna_dist)
                distribuicao_escolhida = st.radio("Distribuição teórica:", ["Normal", "Exponencial"])

                figura_dist, eixo_dist = plt.subplots()
                eixo_dist.hist(dados_dist, bins=40, density=True, color="steelblue", edgecolor="white", alpha=0.7, label="Dados reais")

                pontos_x = np.linspace(min(dados_dist), max(dados_dist), 200)

                if distribuicao_escolhida == "Normal":
                    mu, sigma = ms.ajustar_normal(dados_dist)
                    pontos_y = [ms.densidade_normal(x, mu, sigma) for x in pontos_x]
                    st.write(f"Parâmetros estimados: μ (média) = {mu:.2f}, σ (desvio-padrão) = {sigma:.2f}")
                else:
                    taxa = ms.ajustar_exponencial(dados_dist)
                    pontos_y = [ms.densidade_exponencial(x, taxa) for x in pontos_x]
                    st.write(f"Parâmetro estimado: λ (taxa) = {taxa:.6f}")

                eixo_dist.plot(pontos_x, pontos_y, color="red", linewidth=2, label=f"{distribuicao_escolhida} ajustada")
                eixo_dist.set_title(f"{coluna_dist}: dados reais vs. {distribuicao_escolhida}")
                eixo_dist.legend()
                st.pyplot(figura_dist)

            # outliers            
            elif escolha == "Outliers":
                outliers_encontrados = ms.detectar_outliers(valores)
                st.subheader("Detecção de Outliers")
                st.write(f"Foram encontrados {len(outliers_encontrados)} outliers, de um total de {len(valores)} observações ({100*len(outliers_encontrados)/len(valores):.1f}%).")
                
                if len(outliers_encontrados) > 0:
                    st.write("Alguns exemplos de valores considerados outliers:")
                    st.write(outliers_encontrados[:10])
                    assimetria_calculada = ms.assimetria(valores)

                    if assimetria_calculada > 0.5:
                        interpretacao = "assimétrica à direita (cauda longa de valores altos)"
                    
                    elif assimetria_calculada < -0.5:
                        interpretacao = "assimétrica à esquerda (cauda longa de valores baixos)"
                    
                    else:
                        interpretacao = "aproximadamente simétrica"

                st.write(f"Interpretação automática: a distribuição de `{coluna_numerica}` é {interpretacao} (coeficiente de assimetria = {assimetria_calculada:.2f}).")

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
                    st.subheader("Correlação e Regressão Linear")

                    nomes_regressao = valores

                    coluna_x = coluna_numerica
                    coluna_y = outra_coluna

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

                    st.write(f"Predição: para {coluna_x} = {valor_x_digitado:.2f}, o modelo preve {coluna_y} ≈ {valor_y_previsto:.2f}")
    
                    st.warning(
                        "Atenção: correlação não implica causalidade. O fato de duas variáveis "
                        "estarem correlacionadas não significa necessariamente "
                        "que uma causa a outra diretamente. Pode haver outros fatores em comum "
                    )
                
                
                else: 
                    st.error("Escolha uma coluna diferente/válida")

            
            #Lei dos Grandes Números
            else: 
                    st.subheader("Lei dos Grandes Números")

                    numero_lancamentos = st.slider("Número de lançamentos da moeda:", min_value=10, max_value=5000, value=100)

                    frequencias = ms.simular_lanca_moedas(numero_lancamentos)

                    st.write(f"Frequência relativa de 'cara' após {numero_lancamentos} lançamentos: {frequencias[-1]:.4f}")

                    figura_lgn, eixo_lgn = plt.subplots()
                    eixo_lgn.plot(frequencias)
                    eixo_lgn.axhline(y=0.5, color="red", linestyle="--", label="Probabilidade teórica (0.5)")
                    eixo_lgn.set_xlabel("Número de lançamentos")
                    eixo_lgn.set_ylabel("Frequência relativa de 'cara'")
                    eixo_lgn.set_title("Lei dos Grandes Números")
                    eixo_lgn.legend()

                    st.pyplot(figura_lgn)


#-----------------------------------------------------------#

                    
                    
                    
                    
                    
                    
                    
# --------------------------------------------------------------------------- #
# graficos
            if coluna_numerica and escolha not in ["Medidas de Associação", "Distribuição Teórica", "Teoria Central do Limite", "Outliers", "Lei dos Grandes Números"]: 
                
                valores = df[coluna_numerica].dropna().tolist() 
                
                tab_grafico5, tab_grafico6, tab_grafico7 = st.tabs([
                    "Medidas posição",
                    "Box Plot (Diagrama de Caixa)",
                    "Histograma"
                    ])

                # Aba 1 — Medidas de Posição               
                with tab_grafico5:
                    
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
                with tab_grafico6:    
                    
                    graf6 = graf.grafico_boxplot(valores)
                    st.pyplot(graf6)


                # Aba 3 - Histograma
                with tab_grafico7:              
                    
                    graf7 = graf.grafico_histograma(valores, bins=15)
                    st.pyplot(graf7)
# --------------------------------------------------------------------------- #

    st.success("SISTEMATIZAÇÃO realizada pelos estudantes: Erik, Marcelo, Nadiely, Ulysses e Valentine")
                