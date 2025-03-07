import streamlit as st
import pandas as pd
import numpy as np

# Configuração da página
st.set_page_config(
    page_title="Calculadora de Ticks por Minuto",
    page_icon="🧮",
    layout="centered"
)

# Título do aplicativo
st.title("Calculadora de Ticks por Minuto")
st.markdown("Calcule os ticks por minuto com base na odd e no tempo.")

# Criando o formulário de entrada
with st.form(key="calculadora_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        odd = st.number_input(
            "Odd atual:",
            min_value=1.01,
            value=2.0,
            step=0.01,
            format="%.2f",
            help="Insira a odd atual (deve ser maior que 1)"
        )
    
    with col2:
        tempo = st.number_input(
            "Tempo (em minutos):",
            min_value=0.1,
            value=1.0,
            step=0.1,
            format="%.1f",
            help="Insira o tempo em minutos"
        )
    
    calcular = st.form_submit_button("Calcular")

# Cálculo e exibição do resultado
if calcular or 'calcular' in st.session_state:
    st.session_state.calcular = True
    
    # Cálculo usando a fórmula: odd - 1 * 100 / tempo
    ticks_por_minuto = (odd - 1) * 100 / tempo
    
    # Exibir resultado em um card destacado
    st.success(f"Resultado: **{ticks_por_minuto:.2f}** ticks por minuto")
    
    # Tabela de simulação para diferentes valores de odd
    st.subheader("Simulação para diferentes odds:")
    
    # Criar range de odds para simulação
    odds_simulacao = np.arange(max(1.1, odd-0.5), odd+0.5, 0.1)
    
    # Calcular ticks para cada odd
    resultados = []
    for odd_sim in odds_simulacao:
        ticks = (odd_sim - 1) * 100 / tempo
        resultados.append({
            "Odd": f"{odd_sim:.2f}",
            "Ticks por Minuto": f"{ticks:.2f}"
        })
    
    # Exibir tabela de resultados
    df = pd.DataFrame(resultados)
    st.dataframe(df, hide_index=True)

# Informações adicionais
with st.expander("Sobre a fórmula"):
    st.markdown("""
    A fórmula utilizada para calcular os ticks por minuto é:
    
    **Ticks por Minuto = (odd - 1) * 100 / tempo**
    
    Onde:
    - odd é o valor atual da cotação
    - tempo é o valor em minutos
    """)
