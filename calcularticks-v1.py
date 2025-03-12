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

# Função para calcular ticks por minuto
def calcular_ticks(odd, tempo):
    return ((odd - 1) * 100) / tempo

# Função para prever odds futuras
def prever_odds(odd_atual, tempo_atual, ticks, periodo="HT"):
    if periodo == "HT":
        tempo_final = 45
    else:
        tempo_final = 90
    
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
        previsoes.append({"Minuto": minuto, "Odd Prevista": odd_prevista})
    
    return previsoes

# Título do aplicativo
st.title("Calculadora de Ticks para Under Limite")
st.markdown("""
Esta calculadora ajuda a prever odds regressivas no mercado de under limite, onde as odds devem 
chegar a 1.01 no final de cada período (HT: minuto 45, FT: minuto 90).
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
            format="%.2f"
        )
        
        tempo_atual = st.number_input(
            f"Minuto atual ({min_tempo}-{max_tempo}):",
            min_value=min_tempo,
            max_value=max_tempo,
            value=min_tempo,
            step=1
        )
        
        calcular = st.form_submit_button("Calcular e Prever")

# Cálculos e visualizações
if calcular or 'calculos_realizados' in st.session_state:
    # Armazenar que os cálculos foram realizados
    st.session_state.calculos_realizados = True
    
    # Tempo final do período
    tempo_final = 45 if periodo_codigo == "HT" else 90
    
    # Tempo restante
    tempo_restante = tempo_final - tempo_atual
    
    # Calcular ticks por minuto
    ticks = calcular_ticks(odd_atual, tempo_restante)
    
    # Gerar previsões
    previsoes = prever_odds(odd_atual, tempo_atual, ticks, periodo_codigo)
    df_previsoes = pd.DataFrame(previsoes)
    
    # Coluna de resultados
    with col2:
        st.subheader("Resultados")
        
        # Métricas principais
        metricas_col1, metricas_col2, metricas_col3 = st.columns(3)
        
        with metricas_col1:
            st.metric("Ticks por Minuto", f"{ticks:.2f}")
        
        with metricas_col2:
            odd_final_prevista = max(df_previsoes.iloc[-1]["Odd Prevista"], 1.01)
            st.metric("Odd Final Prevista", f"{odd_final_prevista:.2f}")
        
        with metricas_col3:
            st.metric("Tempo Restante", f"{tempo_restante} min")
        
        # Gráfico de previsão
        st.subheader("Previsão de Odds")
        
        # Adicionar odd atual ao dataframe para o gráfico
        df_grafico = pd.DataFrame([{"Minuto": tempo_atual, "Odd Prevista": odd_atual}] + previsoes)
        
        # Criar gráfico com Altair
        chart = alt.Chart(df_grafico).mark_line(
            point=alt.OverlayMarkDef(color="red")
        ).encode(
            x=alt.X('Minuto:Q', title='Minuto'),
            y=alt.Y('Odd Prevista:Q', title='Odd', scale=alt.Scale(domain=[1, max(df_grafico["Odd Prevista"]) * 1.1])),
            tooltip=['Minuto', 'Odd Prevista']
        ).properties(
            width=600,
            height=400
        ).interactive()
        
        st.altair_chart(chart, use_container_width=True)
        
        # Tabela de previsões
        st.subheader("Tabela de Previsões")
        
        # Adicionar formatação à tabela
        df_display = df_previsoes.copy()
        df_display["Odd Prevista"] = df_display["Odd Prevista"].apply(lambda x: f"{x:.2f}")
        
        # Exibir tabela
        st.dataframe(df_display, use_container_width=True)

# Informações adicionais
with st.expander("Como usar esta calculadora"):
    st.markdown("""
    ### Como usar esta calculadora:
    
    1. Selecione o período (Primeiro Tempo ou Segundo Tempo)
    2. Insira a odd atual do mercado under limite
    3. Insira o minuto atual da partida
    4. Clique em "Calcular e Prever"
    
    ### Interpretação dos resultados:
    
    - **Ticks por Minuto**: Representa a velocidade de queda da odd, calculada pela fórmula: ((odd - 1)*100)/tempo_restante
    - **Odd Final Prevista**: A odd estimada para o final do período (minuto 45 ou 90)
    - **Tempo Restante**: Quantidade de minutos até o final do período
    
    ### Sobre odds regressivas:
    
    No mercado de under limite, as odds são regressivas, começando mais altas e caindo à medida que o jogo avança.
    Idealmente, elas devem chegar próximas a 1.01 no final de cada período (minuto 45 ou 90).
    """)
