import matplotlib.pyplot as plt

# grafico de barras
def grafico_barras_categorico(valores, titulo="Distribuição de Categorias"):

    categorias = {}

    for v in valores:
        categorias[v] = categorias.get(v, 0) + 1

    fig, ax = plt.subplots()

    ax.bar(categorias.keys(), categorias.values(), color="skyblue", edgecolor="black")
    ax.set_title(titulo)
    ax.set_xlabel("Categorias")
    ax.set_ylabel("Frequência")

    plt.xticks(rotation=45)

    fig.tight_layout()

    return fig


# grafico de pizza
def grafico_pizza_categorico(valores, titulo="Proporção de Categorias"):
    categorias = {}
    for v in valores:
        categorias[v] = categorias.get(v, 0) + 1

    fig, ax = plt.subplots()
    ax.pie(categorias.values(), labels=categorias.keys(), autopct="%1.1f%%", startangle=90)
    ax.set_title(titulo)

    return fig


# grafico de pontos
def grafico_pontos_categorico(valores, titulo="Gráfico de Pontos - Categorias"):
    # Conta as ocorrências
    categorias = {}
    for v in valores:
        categorias[v] = categorias.get(v, 0) + 1

    # Cria figura
    fig, ax = plt.subplots()
    ax.scatter(list(categorias.keys()), list(categorias.values()), color="red", s=100)

    # Configurações
    ax.set_title(titulo)
    ax.set_xlabel("Categorias")
    ax.set_ylabel("Frequência")
    plt.xticks(rotation=45)

    return fig


# grafico histograma
def grafico_histograma(valores, bins=10):
    fig, ax = plt.subplots()
    ax.hist(valores, bins=bins, edgecolor="black", alpha=0.7)
    ax.set_title("Histograma")                
    ax.set_xlabel("Valores")                
    ax.set_ylabel("Frequência")           
    
    return fig


# grafico boxplot
def grafico_boxplot(valores):                  
    fig, ax = plt.subplots()                  
    ax.boxplot(valores)                  
    ax.set_title("Boxplot")                 
    ax.set_xlabel("Dados")                 
    ax.set_ylabel("Valores")
               
    return fig
