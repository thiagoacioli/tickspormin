import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt

# Configuração da página
st.set_page_config(
    page_title="Calculadora",
    page_icon="📉",
    layout="wide"
)

# Função para calcular ticks por minuto
def calcular_ticks(odd, tempo):
    return ((odd - 1) * 100) / tempo

# Função para prever odds futuras
def prever_odds(odd_atual, tempo_atual, ticks, periodo="HT", acrescimos=0):
    if periodo == "HT":
        tempo_final = 45 + acrescimos
    else:
        tempo_final = 90 + acrescimos
    
    # Tempo restante
    tempo_restante = tempo_final - tempo_atual
    
    # Lista para armazenar previsões
    previsoes = []
    
    # Calcula odds para cada minuto restante
    for t in range(1, tempo_restante + 1):
        minuto = tempo_atual + t
        # Quanto a odd deve cair em t minutos baseado no tick atual
        queda = (ticks * t) / 100
        odd_prevista = max(odd_atual - queda, 1.01)
        
        # Marcar os minutos de acréscimo
        if (periodo == "HT" and minuto > 45) or (periodo == "FT" and minuto > 90):
            tipo_minuto = "Acréscimo"
        else:
            tipo_minuto = "Regular"
            
        previsoes.append({
            "Minuto": minuto, 
            "Odd Prevista": odd_prevista,
            "Tipo": tipo_minuto
        })
    
    return previsoes

# Título do aplicativo
st.title("Calculadora de Ticks para Under Limite com Acréscimos")
st.markdown("""
Esta calculadora ajuda a prever odds regressivas no mercado de under limite, considerando também
os acréscimos dados pelo árbitro no primeiro tempo (HT) e no segundo tempo (FT).
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
            max_value=10.0,
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
    else:
        tempo_restante_para_calculo = tempo_regulamentar - tempo_atual
    
    # Tempo restante total (sempre inclui acréscimos para exibição)
    tempo_restante_total = tempo_final - tempo_atual
    
    # Calcular ticks por minuto
    ticks = calcular_ticks(odd_atual, tempo_restante_para_calculo)
    
    # Gerar previsões (sempre incluindo acréscimos na previsão)
    previsoes = prever_odds(odd_atual, tempo_atual, ticks, periodo_codigo, acrescimos)
    df_previsoes = pd.DataFrame(previsoes)
    
    # Separar previsões para tempo regulamentar e acréscimos
    df_regulamentar = df_previsoes[df_previsoes["Tipo"] == "Regular"]
    df_acrescimos = df_previsoes[df_previsoes["Tipo"] == "Acréscimo"]
    
    # Coluna de resultados
    with col2:
        st.subheader("Resultados")
        
        # Métricas principais
        metricas_col1, metricas_col2, metricas_col3, metricas_col4 = st.columns(4)
        
        with metricas_col1:
            st.metric("Ticks por Minuto", f"{ticks:.2f}")
        
        with metricas_col2:
            # Odd no final do tempo regulamentar
            if not df_regulamentar.empty:
                odd_regulamentar = df_regulamentar.iloc[-1]["Odd Prevista"]
                st.metric(f"Odd em {tempo_regulamentar}'", f"{odd_regulamentar:.2f}")
        
        with metricas_col3:
            # Odd no final com acréscimos
            odd_final_prevista = df_previsoes.iloc[-1]["Odd Prevista"]
            st.metric(f"Odd em {tempo_final}' (com acréscimos)", f"{odd_final_prevista:.2f}")
        
        with metricas_col4:
            st.metric("Tempo Restante Total", f"{tempo_restante_total} min")
        
        # Gráfico de previsão
        st.subheader("Previsão de Odds")
        
        # Adicionar odd atual ao dataframe para o gráfico
        df_grafico = pd.DataFrame([{"Minuto": tempo_atual, "Odd Prevista": odd_atual, "Tipo": "Regular"}] + previsoes)
        
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
            tooltip=['Minuto', 'Odd Prevista', 'Tipo']
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
                df_previsoes.style.format({"Odd Prevista": "{:.2f}"}),
                use_container_width=True
            )
        
        with tabs[1]:
            if not df_regulamentar.empty:
                st.dataframe(
                    df_regulamentar.style.format({"Odd Prevista": "{:.2f}"}),
                    use_container_width=True
                )
            else:
                st.info("Não há minutos restantes no tempo regulamentar.")
        
        with tabs[2]:
            if not df_acrescimos.empty:
                st.dataframe(
                    df_acrescimos.style.format({"Odd Prevista": "{:.2f}"}),
                    use_container_width=True
                )
            else:
                st.info("Não há acréscimos previstos para este período.")

# Informações adicionais
with st.expander("Como usar esta calculadora"):
    st.markdown("""
    ### Como usar esta calculadora:
    
    1. Selecione o período (Primeiro Tempo ou Segundo Tempo)
    2. Insira a odd atual do mercado under limite
    3. Insira o minuto atual da partida
    4. Informe quantos minutos de acréscimos você prevê que o árbitro dará
    5. Escolha se deseja incluir os acréscimos no cálculo da taxa de ticks:
       - Se marcado: calcula considerando que a odd chegará a 1.01 até o final dos acréscimos
       - Se desmarcado: calcula considerando que a odd chegará a 1.01 até o final do tempo regulamentar
    6. Clique em "Calcular e Prever"
    
    ### Interpretação dos resultados:
    
    - **Ticks por Minuto**: Representa a velocidade de queda da odd
    - **Odd em 45'/90'**: A odd estimada para o final do tempo regulamentar
    - **Odd com acréscimos**: A odd estimada para o final do período incluindo acréscimos
    - **Tempo Restante Total**: Quantidade de minutos até o final do período com acréscimos
    
    ### O gráfico:
    
    - **Linha azul**: Previsão durante o tempo regulamentar
    - **Linha vermelha**: Previsão durante os acréscimos
    - **Linha vertical tracejada**: Marca o final do tempo regulamentar
    """)
