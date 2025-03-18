import streamlit as st
import pandas as pd

st.title('Calculadora de Ticks para Mercado Under Limite ⚽📉')

# Lista pré-definida de ticks (convertendo vírgulas para pontos)
predefined_ticks = """
20
19,5
19
18,5
18
17,5
17
16,5
16
15,5
15
14,5
14
13,5
13
12,5
12
11,5
11
10,5
10
9,8
9,6
9,4
9,2
9
8,8
8,6
8,4
8,2
8
7,8
7,6
7,4
7,2
7
6,8
6,6
6,4
6,2
6
5,9
5,8
5,7
5,6
5,5
5,4
5,3
5,2
5,1
5
4,9
4,8
4,7
4,6
4,5
4,4
4,3
4,2
4,1
4
3,95
3,9
3,85
3,8
3,75
3,7
3,65
3,6
3,55
3,5
3,45
3,4
3,35
3,3
3,25
3,2
3,15
3,1
3,05
3
2,98
2,96
2,94
2,92
2,9
2,88
2,86
2,84
2,82
2,8
2,78
2,76
2,74
2,72
2,7
2,68
2,66
2,64
2,62
2,6
2,58
2,56
2,54
2,52
2,5
2,48
2,46
2,44
2,42
2,4
2,38
2,36
2,34
2,32
2,3
2,28
2,26
2,24
2,22
2,2
2,18
2,16
2,14
2,12
2,1
2,08
2,06
2,04
2,02
2
1,99
1,98
1,97
1,96
1,95
1,94
1,93
1,92
1,91
1,9
1,89
1,88
1,87
1,86
1,85
1,84
1,83
1,82
1,81
1,8
1,79
1,78
1,77
1,76
1,75
1,74
1,73
1,72
1,71
1,7
1,69
1,68
1,67
1,66
1,65
1,64
1,63
1,62
1,61
1,6
1,59
1,58
1,57
1,56
1,55
1,54
1,53
1,52
1,51
1,5
1,49
1,48
1,47
1,46
1,45
1,44
1,43
1,42
1,41
1,4
1,39
1,38
1,37
1,36
1,35
1,34
1,33
1,32
1,31
1,3
1,29
1,28
1,27
1,26
1,25
1,24
1,23
1,22
1,21
1,2
1,19
1,18
1,17
1,16
1,15
1,14
1,13
1,12
1,11
1,1
1,09
1,08
1,07
1,06
1,05
1,04
1,03
1,02
1,01
"""

# Processar a lista de ticks
sorted_ticks = sorted([float(tick.strip().replace(',', '.')) for tick in predefined_ticks.strip().split('\n')], reverse=True)

def encontrar_tick(predicted_odd):
    for tick in sorted_ticks:
        if tick <= predicted_odd:
            return tick
    return 1.01

# Entradas do usuário
odd = st.number_input('Odd atual:', 
                     min_value=1.01, 
                     max_value=1000.0, 
                     step=0.01, 
                     value=2.0,
                     format="%.2f")

half = st.radio('Selecione o período:', 
               ('Primeiro Tempo (HT)', 'Segundo Tempo (FT)'))

# Configurar acréscimos
if half == 'Primeiro Tempo (HT)':
    acréscimos = st.number_input('Acréscimos no HT (minutos):',
                                min_value=0,
                                max_value=15,
                                value=0)
else:
    acréscimos = st.number_input('Acréscimos no FT (minutos):',
                                min_value=0,
                                max_value=15,
                                value=0)

# Configurar tempo máximo
base_time = 45 if half == 'Primeiro Tempo (HT)' else 90
tempo_maximo = base_time + acréscimos

tempo_atual = st.number_input('Minuto atual:', 
                             min_value=0, 
                             max_value=tempo_maximo, 
                             value=0)

tempo_restante = tempo_maximo - tempo_atual

if tempo_restante <= 0:
    st.error('⛔ Tempo atual inválido para o período selecionado!')
elif odd <= 1.01:
    st.error('⛔ A odd já atingiu o valor mínimo!')
else:
    # Cálculo do tick rate
    tick_rate = ((odd - 1.01) * 100) / tempo_restante
    st.metric(label="**Ticks por minuto necessários**", value=f"{tick_rate:.2f}")

    # Previsão das odds
    st.subheader('Previsão Minuto a Minuto 📅')
    previsões = []
    
    for minuto in range(tempo_atual + 1, tempo_maximo + 1):
        delta = minuto - tempo_atual
        odd_prevista = odd - (tick_rate / 100) * delta
        odd_prevista = max(odd_prevista, 1.01)
        odd_ajustada = encontrar_tick(odd_prevista)
        
        # Formatar minutos com acréscimos
        if half == 'Primeiro Tempo (HT)' and minuto > 45:
            minuto_formatado = f"45+{minuto - 45}"
        elif half == 'Segundo Tempo (FT)' and minuto > 90:
            minuto_formatado = f"90+{minuto - 90}"
        else:
            minuto_formatado = str(minuto)
            
        previsões.append((minuto_formatado, odd_ajustada))

    # Criar tabela
    df = pd.DataFrame(previsões, columns=['Minuto', 'Odd Prevista'])
    st.table(df.style.format({'Odd Prevista': '{:.2f}'}))
