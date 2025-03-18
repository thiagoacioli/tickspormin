import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt

# Configuração da página
st.set_page_config(
    page_title="Calculadora de Ticks para Under Limite",
    page_icon="📉",
    layout="wide"
)

# Definir a ordem regressiva dos ticks
def get_ticks_ordem_regressiva():
    # Partes da ordem regressiva
    parte1 = [20 - i*0.5 for i in range(21)]  # 20 até 10 com step 0.5
    parte2 = [10 - i*0.2 for i in range(11)]  # 10 até 8 com step 0.2
    parte3 = [8 - i*0.2 for i in range(11)]   # 8 até 6 com step 0.2
    parte4 = [6 - i*0.1 for i in range(11)]   # 6 até 5 com step 0.1
    parte5 = [5 - i*0.1 for i in range(11)]   # 5 até 4 com step 0.1
    parte6 = [4 - i*0.05 for i in range(21)]  # 4 até 3 com step 0.05
    parte7 = [3 - i*0.02 for i in range(51)]  # 3 até 2 com step 0.02
    parte8 = [2 - i*0.01 for i in range(100)] # 2 até 1.01 com step 0.01
    
    # Juntar todas as partes
    ordem_regressiva = parte1 + parte2 + parte3 + parte4 + parte5 + parte6 + parte7 + parte8
    
    # Garantir que todos os valores estejam formatados com 2 casas decimais
    ordem_regressiva = [round(tick, 2) for tick in ordem_regressiva]
    
    # Garantir que o último valor seja 1.01
    if ordem_regressiva[-1] != 1.01:
        ordem_regressiva[-1] = 1.01
        
    return ordem_regressiva

# Obter a ordem regressiva de ticks
ORDEM_REGRESSIVA = get_ticks_ordem_regressiva()

# Função para encontrar o índice do tick mais próximo
def encontrar_tick_mais_proximo(valor):
    # Encontrar o índice do valor mais próximo na ordem regressiva
    idx = min(range(len(ORDEM_REGRESSIVA)), key=lambda i: abs(ORDEM_REGRESSIVA[i] - valor))
    return idx, ORDEM_REGRESSIVA[idx]

# Função para calcular ticks por minuto considerando o número de ticks
def calcular_ticks_por_numero(odd_inicial, odd_final, tempo):
    # Encontrar o índice do tick mais próximo para odd inicial e final
    idx_inicial, _ = encontrar_tick_mais_proximo(odd_inicial)
    idx_final, _ = encontrar_tick_mais_proximo(odd_final)
    
    # Calcular número de ticks a percorrer
    num_ticks = idx_final - idx_inicial
    
    # Calcular ticks por minuto
    return num_ticks / tempo

# Função para calcular ticks por minuto usando a fórmula tradicional
def calcular_ticks(odd, tempo):
    return ((odd - 1) * 100) / tempo

# Função para prever odds futuras usando a tabela de ordem regressiva
def prever_odds_tabeladas(odd_atual, tempo_atual, ticks_por_minuto, periodo="HT", acrescimos=0):
    if periodo == "HT":
        tempo_final = 45 + acrescimos
    else:
        tempo_final = 90 + acrescimos
    
    # Tempo restante
    tempo_restante = tempo_final - tempo_atual
    
    # Encontrar o índice inicial na ordem regressiva
    idx_inicial, odd_inicial_ajustado = encontrar_tick_mais_proximo(odd_atual)
    
    # Lista para armazenar previsões
    previsoes = []
    
    # Para cada minuto, calcular a odd prevista
    for t in range(1, tempo_restante + 1):
        minuto = tempo_atual + t
        
        # Calcular quantos ticks devem ser percorridos em t minutos
        ticks_percorridos = int(ticks_por_minuto * t)
        
        # Calcular o novo índice na ordem regressiva
        idx_novo = min(idx_inicial + ticks_percorridos, len(ORDEM_REGRESSIVA) - 1)
        
        # Obter a odd tabelada correspondente
        odd_prevista = ORDEM_REGRESSIVA[idx_novo]
        
        # Marcar os minutos de acréscimo
        if (periodo == "HT" and minuto > 45) or (periodo == "FT" and minuto > 90):
            tipo_minuto = "Acréscimo"
        else:
            tipo_minuto = "Regular"
            
        previsoes.append({
            "Minuto": minuto, 
            "Odd Prevista": odd_prevista,
            "Tipo": tipo_minuto,
            "Ticks Percorridos": ticks_percorridos
        })
    
    return previsoes

# Título do aplicativo
st.title("Calculadora de Ticks para Under Limite com Ordem Regressiva")
st.markdown("""
Esta calculadora ajuda a prever odds regressivas no mercado de under limite, considerando a ordem regressiva 
exata dos ticks e os acréscimos dados pelo árbitro no primeiro tempo (HT) e no segundo tempo (FT).
""")

# Layout em colunas
col1, col2 = st.columns([1, 2])

# Coluna de entrada de dados
with col1:
    st.subheader("Dados atuais")
    
    # Seleção do período
    periodo = st.radio("Período:", ["Primeiro Tempo (HT)", "Segundo Tempo (FT)"], horizontal=True)
    periodo_codigo = "HT" if periodo == "Primeiro Tempo (HT)" else "FT"
    
    # Range de tempo permitido baseado no período
    min_tempo = 0 if periodo_codigo == "HT" else 46
    max_tempo = 44 if periodo_codigo == "HT" else 89  # Um minuto antes do fim para permitir cálculos
    
    # Entrada de dados em um form
    with st.form(key="calculadora_form"):
        odd_atual = st.number_input(
            "Odd atual:",
            min_value=1.02,
            max_value=20.0,
            value=1.5,
            step=0.01,
            format="%.2f",
            help="Valor atual da odd no mercado de under limite"
        )
        
        tempo_atual = st.number_input(
            f"Minuto atual ({min_tempo}-{max_tempo}):",
            min_value=min_tempo,
            max_value=max_tempo,
            value=min_tempo,
            step=1,
            help="Minuto atual da partida"
        )
        
        # Campo para acréscimos
        acrescimos = st.number_input(
            "Acréscimos previstos (minutos):",
            min_value=0,
            max_value=15,
            value=3,
            step=1,
            help="Estimativa de acréscimos que serão dados pelo árbitro neste período"
        )
        
        # Opção para considerar odd no final com acréscimos
        considerar_acrescimos = st.checkbox(
            "Considerar acréscimos no cálculo de ticks",
            value=True,
            help="Se marcado, usa o tempo total (incluindo acréscimos) para calcular os ticks por minuto"
        )
        
        # Método de cálculo
        metodo_calculo = st.radio(
            "Método de cálculo:",
            ["Fórmula ((odd-1)*100)/tempo", "Tabela de Ticks Regressivos"],
            horizontal=True,
            help="Escolha entre o cálculo usando a fórmula tradicional ou a tabela de ticks regressivos exatos"
        )
        
        calcular = st.form_submit_button("Calcular e Prever")

# Cálculos e visualizações
if calcular or 'calculos_realizados' in st.session_state:
    # Armazenar que os cálculos foram realizados
    st.session_state.calculos_realizados = True
    
    # Tempo final do período sem acréscimos
    tempo_regulamentar = 45 if periodo_codigo == "HT" else 90
    
    # Tempo final com acréscimos
    tempo_final = tempo_regulamentar + acrescimos
    
    # Tempo restante (baseado na escolha do usuário)
    if considerar_acrescimos:
        tempo_restante_para_calculo = tempo_final - tempo_atual
        odd_final_alvo = 1.01  # Alvo para o final do período com acréscimos
    else:
        tempo_restante_para_calculo = tempo_regulamentar - tempo_atual
        # Achar o índice da odd atual na ordem regressiva
        idx_atual, _ = encontrar_tick_mais_proximo(odd_atual)
        # Calcular quantos ticks devem ser percorridos proporcionalmente até o final do tempo regulamentar
        proporcao = (tempo_regulamentar - tempo_atual) / (tempo_final - tempo_atual)
        idx_final = int(idx_atual + (len(ORDEM_REGRESSIVA) - 1 - idx_atual) * proporcao)
        odd_final_alvo = ORDEM_REGRESSIVA[min(idx_final, len(ORDEM_REGRESSIVA) - 1)]
    
    # Tempo restante total (sempre inclui acréscimos para exibição)
    tempo_restante_total = tempo_final - tempo_atual
    
    # Calcular ticks por minuto
    if metodo_calculo == "Fórmula ((odd-1)*100)/tempo":
        ticks = calcular_ticks(odd_atual, tempo_restante_para_calculo)
        previsoes = prever_odds_tabeladas(odd_atual, tempo_atual, ticks/5, periodo_codigo, acrescimos)
    else:  # Método usando tabela de ticks regressivos
        ticks = calcular_ticks_por_numero(odd_atual, odd_final_alvo, tempo_restante_para_calculo)
        previsoes = prever_odds_tabeladas(odd_atual, tempo_atual, ticks, periodo_codigo, acrescimos)
    
    df_previsoes = pd.DataFrame(previsoes)
    
    # Separar previsões para tempo regulamentar e acréscimos
    df_regulamentar = df_previsoes[df_previsoes["Tipo"] == "Regular"]
    df_acrescimos = df_previsoes[df_previsoes["Tipo"] == "Acréscimo"]
    
    # Coluna de resultados
    with col2:
        st.subheader("Resultados")
        
        # Métricas principais
        metricas_col1, metricas_col2, metricas_col3 = st.columns(3)
        
        with metricas_col1:
            if metodo_calculo == "Fórmula ((odd-1)*100)/tempo":
                st.metric("Ticks por Minuto (Fórmula)", f"{ticks:.2f}")
            else:
                st.metric("Ticks por Minuto (Tabela)", f"{ticks:.2f}")
        
        with metricas_col2:
            # Odd no final do tempo regulamentar
            if not df_regulamentar.empty:
                odd_regulamentar = df_regulamentar.iloc[-1]["Odd Prevista"]
                st.metric(f"Odd em {tempo_regulamentar}'", f"{odd_regulamentar:.2f}")
        
        with metricas_col3:
            # Odd no final com acréscimos
            odd_final_prevista = df_previsoes.iloc[-1]["Odd Prevista"]
            st.metric(f"Odd em {tempo_final}' (com acréscimos)", f"{odd_final_prevista:.2f}")
        
        # Gráfico de previsão
        st.subheader("Previsão de Odds")
        
        # Adicionar odd atual ao dataframe para o gráfico
        df_grafico = pd.DataFrame([{"Minuto": tempo_atual, "Odd Prevista": odd_atual, "Tipo": "Regular", "Ticks Percorridos": 0}] + previsoes)
        
        # Adicionar linha vertical para marcar o final do tempo regulamentar
        linha_final = pd.DataFrame([
            {"Minuto": tempo_regulamentar, "y": min(df_grafico["Odd Prevista"])},
            {"Minuto": tempo_regulamentar, "y": max(df_grafico["Odd Prevista"]) * 1.05}
        ])
        
        # Criar gráfico base com Altair
        base = alt.Chart(df_grafico).encode(
            x=alt.X('Minuto:Q', title='Minuto'),
            y=alt.Y('Odd Prevista:Q', title='Odd', scale=alt.Scale(domain=[1, max(df_grafico["Odd Prevista"]) * 1.1]))
        )
        
        # Linha principal para o tempo normal
        linha_normal = base.mark_line(color='blue').encode(
            color=alt.condition(
                alt.datum.Tipo == 'Regular',
                alt.value('blue'),
                alt.value('red')
            )
        )
        
        # Pontos
        pontos = base.mark_circle(size=60).encode(
            color=alt.condition(
                alt.datum.Tipo == 'Regular',
                alt.value('blue'),
                alt.value('red')
            ),
            tooltip=['Minuto', 'Odd Prevista', 'Tipo', 'Ticks Percorridos']
        )
        
        # Linha vertical para marcar o final do tempo regulamentar
        regra = alt.Chart(linha_final).mark_rule(strokeDash=[12, 6], color='gray').encode(
            x='Minuto:Q'
        )
        
        # Texto para marcar final do tempo regulamentar
        texto = alt.Chart(pd.DataFrame([{"Minuto": tempo_regulamentar - 2, "y": max(df_grafico["Odd Prevista"]) * 1.05, "text": "Fim do Tempo Regulamentar"}])).mark_text(
            align='right',
            fontSize=12,
            color='gray'
        ).encode(
            x='Minuto:Q',
            y='y:Q',
            text='text:N'
        )
        
        # Combinar todos os elementos
        chart = (linha_normal + pontos + regra + texto).properties(
            width=600,
            height=400
        ).interactive()
        
        st.altair_chart(chart, use_container_width=True)
        
        # Tabela de previsões
        tabs = st.tabs(["Todas Previsões", "Tempo Regulamentar", "Acréscimos"])
        
        with tabs[0]:
            st.dataframe(
                df_previsoes.style.format({"Odd Prevista": "{:.2f}", "Ticks Percorridos": "{:.0f}"}),
                use_container_width=True
            )
        
        with tabs[1]:
            if not df_regulamentar.empty:
                st.dataframe(
                    df_regulamentar.style.format({"Odd Prevista": "{:.2f}", "Ticks Percorridos": "{:.0f}"}),
                    use_container_width=True
                )
            else:
                st.info("Não há minutos restantes no tempo regulamentar.")
        
        with tabs[2]:
            if not df_acrescimos.empty:
                st.dataframe(
                    df_acrescimos.style.format({"Odd Prevista": "{:.2f}", "Ticks Percorridos": "{:.0f}"}),
                    use_container_width=True
                )
            else:
                st.info("Não há acréscimos previstos para este período.")

    # Exibir tabela de ordem regressiva
    with st.expander("Ver Tabela de Ordem Regressiva Completa"):
        # Criar DataFrame com índices e valores
        df_ordem = pd.DataFrame({
            "Índice": range(len(ORDEM_REGRESSIVA)),
            "Valor da Odd": ORDEM_REGRESSIVA
        })
        
        # Reorganizar em múltiplas colunas para melhor visualização
        num_colunas = 4
        colunas = st.columns(num_colunas)
        
        items_per_column = len(df_ordem) // num_colunas + 1
        
        for i in range(num_colunas):
            start_idx = i * items_per_column
            end_idx = min((i + 1) * items_per_column, len(df_ordem))
            
            if start_idx < len(df_ordem):
                with colunas[i]:
                    st.dataframe(
                        df_ordem.iloc[start_idx:end_idx],
                        hide_index=True,
                        use_container_width=True
                    )

# Informações adicionais
with st.expander("Como usar esta calculadora"):
    st.markdown("""
    ### Como usar esta calculadora:
    
    1. Selecione o período (Primeiro Tempo ou Segundo Tempo)
    2. Insira a odd atual do mercado under limite
    3. Insira o minuto atual da partida
    4. Informe quantos minutos de acréscimos você prevê que o árbitro dará
    5. Escolha se deseja incluir os acréscimos no cálculo da taxa de ticks
    6. Selecione o método de cálculo:
       - **Fórmula tradicional**: Usa a fórmula ((odd-1)*100)/tempo
       - **Tabela de Ticks Regressivos**: Usa a tabela exata de valores possíveis das odds
    7. Clique em "Calcular e Prever"
    
    ### Interpretação dos resultados:
    
    - **Ticks por Minuto**: Representa a velocidade de queda da odd
    - **Odd em 45'/90'**: A odd estimada para o final do tempo regulamentar
    - **Odd com acréscimos**: A odd estimada para o final do período incluindo acréscimos
    - **Ticks Percorridos**: O número de ticks exatos que serão percorridos até aquele minuto
    
    ### Sobre a tabela de ordem regressiva:
    
    A tabela de ordem regressiva contém os valores exatos em que as odds podem parar. Utilizando este 
    método, a calculadora prevê as odds com base nos valores exatos da tabela, em vez de usar valores 
    contínuos que podem não existir na prática.
    """)
