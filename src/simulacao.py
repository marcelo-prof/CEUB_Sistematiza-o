import random


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

if __name__ == "__main__":
    resultado = simular_lancamentos_moeda(1000)
    print("Frequência após 10 lançamentos:", resultado[9])
    print("Frequência após 1000 lançamentos:", resultado[999])