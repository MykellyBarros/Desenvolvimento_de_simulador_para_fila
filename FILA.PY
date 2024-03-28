import random

# Função principal para simular a fila
def simular_fila(numero_aleatorios, numero_servidores, max_pessoas_fila):
    # Parâmetros do gerador de números pseudoaleatórios
    a = 1664525  # Parâmetro multiplicativo do LCG
    c = 1013904223  # Parâmetro aditivo do LCG
    M = 2**32  # Módulo do LCG
    seed = 12345  # Valor inicial da semente
    previous = seed  # Inicialização da semente

    # Função para gerar números pseudoaleatórios normalizados entre 0 e 1
    def NextRandom():
        nonlocal previous
        previous = (a * previous + c) % M  # Atualização da semente usando o LCG
        return previous / M  # Retorna o valor normalizado entre 0 e 1

    # Função para simular o evento de chegada
    def CHEGADA(tempo_atual, proximo_evento_chegada):
        nonlocal fila, numero_total_clientes

        # Atualiza o estado da fila
        fila.append(tempo_atual)

        # Gera o próximo evento de chegada
        proximo_evento_chegada += random.uniform(2, 5)  # Gera um intervalo de chegada entre 2 e 5 unidades de tempo

        return proximo_evento_chegada  # Retorna o próximo evento de chegada

    # Função para simular o evento de saída
    def SAIDA(tempo_atual):
        nonlocal fila, tempo_total_clientes_no_sistema, numero_total_clientes

        # Remove o cliente que está sendo atendido
        tempo_cliente_na_fila = fila.pop(0)  # Remove o primeiro cliente da fila
        tempo_total_clientes_no_sistema += tempo_atual - tempo_cliente_na_fila  # Calcula o tempo que o cliente passou no sistema
        numero_total_clientes += 1  # Incrementa o número total de clientes atendidos

    # Inicialização dos parâmetros da simulação
    tempo_atual = 0  # Tempo atual da simulação
    fila = []  # Fila de espera para os clientes
    numero_total_clientes = 0  # Número total de clientes atendidos
    tempo_total_clientes_no_sistema = 0  # Tempo total que os clientes passaram no sistema
    proximo_evento_chegada = 2.0  # Próximo evento de chegada ocorre no tempo 2.0
    proximo_evento_saida = float('inf')  # Inicialmente não há eventos de saída agendados

    # Laço de repetição para simular a fila
    for _ in range(numero_aleatorios):
        # Determinar o próximo evento (chegada ou saída)
        if proximo_evento_chegada < proximo_evento_saida:
            tempo_atual = proximo_evento_chegada
            proximo_evento_chegada = CHEGADA(tempo_atual, proximo_evento_chegada)  # Simula o evento de chegada
            
            if len(fila) == 1:  # Se a fila estava vazia, agendar a saída do cliente
                proximo_evento_saida = tempo_atual + random.uniform(3, 5)  # Gera um tempo de saída para o cliente
        else:
            tempo_atual = proximo_evento_saida
            SAIDA(tempo_atual)  # Simula o evento de saída

            if len(fila) > 0:  # Se ainda há clientes na fila, agendar a saída do próximo cliente
                proximo_evento_saida = tempo_atual + random.uniform(3, 5)  # Gera um tempo de saída para o próximo cliente
            else:
                proximo_evento_saida = float('inf')  # Se a fila estiver vazia, não há eventos de saída agendados

            if len(fila) >= max_pessoas_fila:  # Verifica se a fila atingiu o número máximo de pessoas
                fila.pop()  # Remove o último cliente da fila

    # Cálculo dos índices de desempenho
    tempo_global_simulacao = tempo_atual
    vazao = numero_total_clientes / tempo_global_simulacao  # Calcula a vazão do sistema
    utilizacao = tempo_total_clientes_no_sistema / (tempo_global_simulacao * numero_servidores)  # Calcula a utilização do sistema
    populacao_media = sum(len(fila) for tempo_na_fila in fila) / len(fila) if fila else 0  # Calcula a população média na fila
    tempo_medio_resposta = tempo_total_clientes_no_sistema / numero_total_clientes if numero_total_clientes else 0  # Calcula o tempo médio de resposta

    # Retorna os índices de desempenho calculados
    return numero_total_clientes, tempo_global_simulacao, vazao, utilizacao, populacao_media, tempo_medio_resposta

# Parâmetros da simulação
# numero_aleatorios = 100000  # Número de eventos a serem simulados
# numero_servidores = 1  # Número de servidores no sistema
# max_pessoas_fila = 10  # Número máximo de pessoas na fila

# Realiza a simulação
resultados_simulacao = simular_fila(100000, 1, 5) #G/G/1/5

# Exibição dos resultados
print(f"\n-----------------------------------")
print("Resultados da simulação1:")
print(f"Número total de clientes atendidos: {resultados_simulacao[0]}")
print(f"Tempo global da simulação: {resultados_simulacao[1]}")
print(f"Vazão: {resultados_simulacao[2]}")
print(f"Utilização: {resultados_simulacao[3]}")
print(f"População média: {resultados_simulacao[4]}")
print(f"Tempo médio de resposta: {resultados_simulacao[5]}")
print(f"\n-----------------------------------")
resultados_simulacao2 = simular_fila(100000, 2, 5) #G/G/2/5
print("Resultados da simulação2:")
print(f"Número total de clientes atendidos: {resultados_simulacao2[0]}")
print(f"Tempo global da simulação: {resultados_simulacao2[1]}")
print(f"Vazão: {resultados_simulacao2[2]}")
print(f"Utilização: {resultados_simulacao2[3]}")
print(f"População média: {resultados_simulacao2[4]}")
print(f"Tempo médio de resposta: {resultados_simulacao2[5]}")