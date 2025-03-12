import streamlit as st
import pandas as pd
import numpy as np

# Configuração da página
st.set_page_config(
    page_title="Calculadora de Ticks - Odds Under",
    page_icon="⚽",
    layout="centered"
)

# Funções para cálculos
def calcular_ticks(odd_atual, tempo_atual, periodo_final=45):
    """
    Calcula ticks por minuto para odds regressivas de under
    A odd deve chegar a 1.01 no final do período (45 ou 90 min)
    """
    # Quanto a odd precisa diminuir até o final do período
    diferenca_odd = odd_atual - 1.01
    
    # Quanto tempo resta até o final do período
    tempo_restante = periodo_final - tempo_atual
    
    # Se não há tempo restante, não podemos calcular ticks
    if tempo_restante <= 0:
        return 0
    
    # Ticks por minuto para atingir 1.01 no final do período
    ticks = (diferenca_odd * 100) / tempo_restante
    
    return ticks

def prever_odds_futuras(odd_atual, ticks, tempo_atual, minutos_futuros):
    """
    Prevê odds futuras com base nos ticks por minuto (para odds regressivas)
    """
    odds_previstas = {}
    
    for minuto in minutos_futuros:
        # Quanto tempo passou desde a odd atual
        tempo_passado = minuto - tempo_atual
        
        # Redução na odd baseada nos ticks
        reducao = (ticks * tempo_passado) / 100
        
        # Nova odd prevista (regressiva)
        odd_prevista = max(1.01, odd_atual - reducao)
        
        odds_previstas[minuto] = odd_prevista
        
    return odds_previstas

# Título e descrição
st.title("⚽ Calculadora de Ticks - Odds Under")
st.markdown("""
Esta calculadora está otimizada para odds de under, que são regressivas e tendem a 1.01 
ao final de cada período (45 min para HT e 90 min para FT).
""")

# Layout em colunas para os inputs
col1, col2 = st.columns(2)

with col1:
    odd_atual = st.number_input(
        "Odd Atual:",
        min_value=1.01,
        max_value=10.0,
        value=1.5,
        step=0.01,
        format="%.2f",
        help="Insira a odd atual de under (maior que 1.01)"
    )

with col2:
    tempo_atual = st.number_input(
        "Tempo Atual (minutos):",
        min_value=0,
        max_value=90,
        value=15,
        step=1,
        help="Insira o tempo atual da partida (0-90 minutos)"
    )

# Determinar se é primeiro ou segundo tempo
if tempo_atual <= 45:
    periodo = "Primeiro Tempo (HT)"
    periodo_final = 45
else:
    periodo = "Segundo Tempo (FT)"
    periodo_final = 90

st.info(f"Período atual: **{periodo}** | O valor da odd deve chegar a **1.01** no minuto **{periodo_final}**")

# Cálculo dos ticks por minuto
if st.button("Calcular Ticks e Prever Odds Futuras"):
    # Verificar se há tempo suficiente para o cálculo
    if tempo_atual >= periodo_final:
        st.warning(f"O tempo atual já atingiu ou ultrapassou o final do período ({periodo_final} min).")
    else:
        # Calcular ticks
        ticks = calcular_ticks(odd_atual, tempo_atual, periodo_final)
        
        # Exibir resultado dos ticks
        st.success(f"**Ticks por minuto: {ticks:.2f}**")
        
        # Determinar próximos minutos para previsão
        if tempo_atual < 45:
            # Primeiro tempo - até 45 min
            proximos_minutos = list(range(tempo_atual + 5, 46, 5))
        else:
            # Segundo tempo - até 90 min
            proximos_minutos = list(range(tempo_atual + 5, 91, 5))
        
        if not proximos_minutos:
            st.warning("Não há minutos futuros disponíveis para previsão neste período.")
        else:
            # Prever odds futuras
            odds_previstas = prever_odds_futuras(odd_atual, ticks, tempo_atual, proximos_minutos)
            
            # Criar DataFrame para exibição
            df_previsao = pd.DataFrame({
                "Minuto": proximos_minutos,
                "Odd Prevista": [round(odds_previstas[min], 2) for min in proximos_minutos]
            })
            
            # Adicionar linha para o final do período sempre mostrando 1.01
            df_final = pd.DataFrame({
                "Minuto": [periodo_final],
                "Odd Prevista": [1.01]
            })
            
            df_completo = pd.concat([df_previsao, df_final]).sort_values("Minuto")
            
            # Exibir tabela de previsão
            st.subheader("Previsão de Odds Futuras")
            st.dataframe(df_completo, hide_index=True)
            
            # Exibir dados em formato de tabela HTML para melhor visualização
            st.subheader("Tabela de Referência")
            
            # Criar tabela HTML
            html_table = """
            <table style="width:100%; border-collapse: collapse; text-align: center;">
                <tr style="background-color: #f2f2f2;">
                    <th style="padding: 8px; border: 1px solid #ddd;">Minuto</th>
                    <th style="padding: 8px; border: 1px solid #ddd;">Odd Prevista</th>
                </tr>
            """
            
            # Adicionar linha para o tempo atual
            html_table += f"""
                <tr style="background-color: #e6f7ff;">
                    <td style="padding: 8px; border: 1px solid #ddd;"><strong>{tempo_atual}</strong></td>
                    <td style="padding: 8px; border: 1px solid #ddd;"><strong>{odd_atual:.2f}</strong></td>
                </tr>
            """
            
            # Adicionar linhas para cada previsão
            for minuto in proximos_minutos:
                html_table += f"""
                    <tr>
                        <td style="padding: 8px; border: 1px solid #ddd;">{minuto}</td>
                        <td style="padding: 8px; border: 1px solid #ddd;">{odds_previstas[minuto]:.2f}</td>
                    </tr>
                """
            
            # Adicionar linha para o final do período
            html_table += f"""
                <tr style="background-color: #e6ffe6;">
                    <td style="padding: 8px; border: 1px solid #ddd;"><strong>{periodo_final}</strong></td>
                    <td style="padding: 8px; border: 1px solid #ddd;"><strong>1.01</strong></td>
                </tr>
            """
            
            html_table += "</table>"
            
            st.markdown(html_table, unsafe_allow_html=True)

# Explicação da fórmula
with st.expander("Como funcionam os cálculos para odds de under?"):
    st.markdown("""
    ### Lógica das odds de under
    
    As odds de under são regressivas, ou seja, diminuem com o tempo e tendem a 1.01 no final do período (45 min para primeiro tempo e 90 min para segundo tempo).
    
    ### Fórmula para calcular Ticks por Minuto
    
    ```
    Diferença de odd = odd atual - 1.01
    Tempo restante = final do período - tempo atual
    Ticks por Minuto = (diferença de odd * 100) / tempo restante
    ```
    
    ### Fórmula para prever Odds Futuras
    
    ```
    Tempo passado = minuto futuro - tempo atual
    Redução na odd = (ticks * tempo passado) / 100
    Odd Prevista = odd atual - redução (nunca menor que 1.01)
    ```
    
    ### Exemplo:
    Se a odd atual é 1.5 aos 15 minutos do primeiro tempo:
    - Diferença de odd = 1.5 - 1.01 = 0.49
    - Tempo restante = 45 - 15 = 30 minutos
    - Ticks = (0.49 * 100) / 30 = 1.63 ticks por minuto
    - Odd prevista para o minuto 30: 1.5 - ((1.63 * 15) / 100) = 1.26
    """)

# Informações adicionais
st.caption("Este aplicativo é uma ferramenta de previsão para odds de under e simula a tendência natural dessas odds de atingirem 1.01 ao final de cada período.")
