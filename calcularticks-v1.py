import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Configuração da página
st.set_page_config(
    page_title="Calculadora de Ticks por Minuto - Futebol",
    page_icon="⚽",
    layout="centered"
)

# Funções para cálculos
def calcular_ticks(odd, tempo):
    """Calcula ticks por minuto usando a fórmula: ((odd - 1)*100)/tempo"""
    return ((odd - 1) * 100) / tempo

def prever_odds_futuras(odd_atual, tempo_atual, ticks, minutos_futuros):
    """Prevê odds futuras com base nos ticks por minuto"""
    odds_previstas = {}
    
    for minuto in minutos_futuros:
        # A fórmula inversa para encontrar a odd: odd = (ticks * tempo / 100) + 1
        odd_prevista = (ticks * minuto / 100) + 1
        odds_previstas[minuto] = odd_prevista
        
    return odds_previstas

# Título e descrição
st.title("⚽ Calculadora de Ticks por Minuto - Futebol")
st.markdown("""
Esta calculadora permite estimar os ticks por minuto com base na odd atual e no tempo de jogo,
e prever as odds futuras para os próximos minutos da partida.
""")

# Layout em colunas para os inputs
col1, col2 = st.columns(2)

with col1:
    odd_atual = st.number_input(
        "Odd Atual:",
        min_value=1.01,
        value=2.0,
        step=0.01,
        format="%.2f",
        help="Insira a odd atual (maior que 1)"
    )

with col2:
    tempo_atual = st.number_input(
        "Tempo Atual (minutos):",
        min_value=1,
        max_value=90,
        value=15,
        step=1,
        help="Insira o tempo atual da partida (1-90 minutos)"
    )

# Determinar se é primeiro ou segundo tempo
if tempo_atual <= 45:
    periodo = "Primeiro Tempo (HT)"
    tempo_max = 45
else:
    periodo = "Segundo Tempo"
    tempo_max = 90

st.info(f"Período atual: **{periodo}** | Tempo máximo: **{tempo_max}** minutos")

# Cálculo dos ticks por minuto
if st.button("Calcular Ticks e Prever Odds Futuras"):
    # Calcular ticks
    ticks = calcular_ticks(odd_atual, tempo_atual)
    
    # Exibir resultado dos ticks
    st.success(f"**Ticks por minuto: {ticks:.2f}**")
    
    # Determinar próximos minutos para previsão
    if tempo_atual <= 45:
        # Primeiro tempo
        proximos_minutos = list(range(tempo_atual + 5, 46, 5))
    else:
        # Segundo tempo
        proximos_minutos = list(range(tempo_atual + 5, 91, 5))
    
    if not proximos_minutos:  # Se estiver no final do jogo
        st.warning("Não há minutos futuros disponíveis para previsão neste período.")
    else:
        # Prever odds futuras
        odds_previstas = prever_odds_futuras(odd_atual, tempo_atual, ticks, proximos_minutos)
        
        # Criar DataFrame para exibição
        df_previsao = pd.DataFrame({
            "Minuto": proximos_minutos,
            "Odd Prevista": [round(odds_previstas[min], 2) for min in proximos_minutos]
        })
        
        # Exibir tabela de previsão
        st.subheader("Previsão de Odds Futuras")
        st.dataframe(df_previsao, hide_index=True)
        
        # Criar gráfico de previsão
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # Adicionar ponto atual
        ax.scatter(tempo_atual, odd_atual, color='red', s=100, zorder=5, label='Odd Atual')
        
        # Plotar linha de projeção
        todos_minutos = [tempo_atual] + proximos_minutos
        todas_odds = [odd_atual] + [odds_previstas[min] for min in proximos_minutos]
        ax.plot(todos_minutos, todas_odds, marker='o', linestyle='-', color='blue')
        
        # Configurar gráfico
        ax.set_xlabel('Minuto da Partida')
        ax.set_ylabel('Odd')
        ax.set_title('Projeção de Odds ao Longo do Tempo')
        ax.grid(True)
        ax.legend()
        
        # Exibir gráfico
        st.pyplot(fig)

# Explicação da fórmula
with st.expander("Como funcionam os cálculos?"):
    st.markdown("""
    ### Fórmula para calcular Ticks por Minuto
    
    ```
    Ticks por Minuto = ((odd - 1) * 100) / tempo
    ```
    
    ### Fórmula para prever Odds Futuras
    
    ```
    Odd Prevista = (ticks * tempo_futuro / 100) + 1
    ```
    
    ### Exemplo:
    Se a odd atual é 2.0 aos 10 minutos de jogo:
    - Ticks = ((2.0 - 1) * 100) / 10 = 10 ticks por minuto
    - Odd prevista para o minuto 20: (10 * 20 / 100) + 1 = 3.0
    """)

# Informações adicionais
st.caption("Este aplicativo é uma ferramenta de previsão e não garante resultados em eventos reais.")
