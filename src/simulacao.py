import random

from minhastats import media

def simular_lancamentos_moeda(numero_de_lancamentos):
    caras_ate_agora = 0
    frequencias_ao_longo_do_tempo = []

    for i in range(1, numero_de_lancamentos + 1):
        resultado = random.choice(["cara", "coroa"])

        if resultado == "cara":
            caras_ate_agora = caras_ate_agora + 1

        frequencia_atual = caras_ate_agora / i
        frequencias_ao_longo_do_tempo.append(frequencia_atual)

    return frequencias_ao_longo_do_tempo

def simular_teorema_central_limite(populacao_de_dados, tamanho_da_amostra, numero_de_repeticoes):
    medias_das_amostras = []

    for i in range(numero_de_repeticoes):
        amostra = random.choices(populacao_de_dados, k=tamanho_da_amostra)
        media_da_amostra = media(amostra)
        medias_das_amostras.append(media_da_amostra)

    return medias_das_amostras