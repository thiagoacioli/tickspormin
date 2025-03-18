import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Definir a lista de ticks em ordem decrescente
ticks = [
    20, 19.5, 19, 18.5, 18, 17.5, 17, 16.5, 16, 15.5, 15, 14.5, 14, 13.5, 13, 12.5, 
    12, 11.5, 11, 10.5, 10, 9.8, 9.6, 9.4, 9.2, 9, 8.8, 8.6, 8.4, 8.2, 8, 7.8, 7.6, 
    7.4, 7.2, 7, 6.8, 6.6, 6.4, 6.2, 6, 5.9, 5.8, 5.7, 5.6, 5.5, 5.4, 5.3, 5.2, 5.1, 
    5, 4.9, 4.8, 4.7, 4.6, 4.5, 4.4, 4.3, 4.2, 4.1, 4, 3.95, 3.9, 3.85, 3.8, 3.75, 
    3.7, 3.65, 3.6, 3.55, 3.5, 3.45, 3.4, 3.35, 3.3, 3.25, 3.2, 3.15, 3.1, 3.05, 3, 
    2.98, 2.96, 2.94, 2.92, 2.9, 2.88, 2.86, 2.84, 2.82, 2.8, 2.78, 2.76, 2.74, 2.72, 
    2.7, 2.68, 2.66, 2.64, 2.62, 2.6, 2.58, 2.56, 2.54, 2.52, 2.5, 2.48, 2.46, 2.44, 
    2.42, 2.4, 2.38, 2.36, 2.34, 2.32, 2.3, 2.28, 2.26, 2.24, 2.22, 2.2, 2.18, 2.16, 
    2.14, 2.12, 2.1, 2.08, 2.06, 2.04, 2.02, 2, 1.99, 1.98, 1.97, 1.96, 1.95, 1.94, 
    1.93, 1.92, 1.91, 1.9, 1.89, 1.88, 1.87, 1.86, 1.85, 1.84, 1.83, 1.82, 1.81, 1.8, 
    1.79, 1.78, 1.77, 1.76, 1.75, 1.74, 1.73, 1.72, 1.71, 1.7, 1.69, 1.68, 1.67, 1.66, 
    1.65, 1.64, 1.63, 1.62, 1.61, 1.6, 1.59, 1.58, 1.57, 1.56, 1.55, 1.54, 1.53, 1.52, 
    1.51, 1.5, 1.49, 1.48, 1.47, 1.46, 1.45, 1.44, 1.43, 1.42, 1.41, 1.4, 1.39, 1.38, 
    1.37, 1.36, 1.35, 1.34, 1.33, 1.32, 1.31, 1.3, 1.29, 1.28, 1.27, 1.26, 1.25, 1.24, 
    1.23, 1.22, 1.21, 1.2, 1.19, 1.18, 1.17, 1.16, 1.15, 1.14, 1.13, 1.12, 1.11, 1.1, 
    1.09, 1.08, 1.07, 1.06, 1.05, 1.04, 1.03, 1.02, 1.01
]

# Função para calcular ticks por minuto
def calcular_ticks_por_minuto(odd, tempo):
    return ((odd - 1) * 100) / tempo

# Função para encontrar a odd mais próxima na lista de ticks
def encontrar_odd_proxima(odd_valor):
    # Encontrar o índice da odd mais próxima na lista
    idx = min(range(len(ticks)), key=lambda i: abs(ticks[i] - odd_valor))
    return ticks[idx], idx

# Função para prever odds futuras baseadas no ritmo atual
def prever_odds_futuras(odd_atual, tempo_atual, acrescimos_ht, acrescimos_ft, periodo):
    odd_proxima, idx_atual = encontrar_odd_proxima(odd_atual)
    ticks_por_minuto = calcular_ticks_por_minuto(odd_atual, tempo_atual)
    
    # Definir o tempo máximo baseado no período
    if periodo == "Primeiro Tempo (HT)":
        tempo_max = 45 + acrescimos_ht
    else:  # Segundo Tempo (FT)
        tempo_max = 90 + acrescimos_ft
    
    # Calcular quantos minutos faltam
    if periodo == "Primeiro Tempo (HT)":
        minutos_restantes = tempo_max - tempo_atual
    else:
        minutos_restantes = tempo_max - tempo_atual
    
    # Calcular quantos ticks serão consumidos no tempo restante
    ticks_restantes = ticks_por_minuto * minutos_restantes
    
    # Estimar o índice final baseado nos ticks restantes
    idx_estimado = min(len(ticks) - 1, int(idx_atual + ticks_restantes))
    
    # Criar lista de tempos futuros e odds previstas
    tempos_futuros = []
    odds_previstas = []
    indices_previstos = []
    
    # Adicionar previsões para cada minuto futuro
    for minuto_adicional in range(1, int(minutos_restantes) + 1):
        tempo_futuro = tempo_atual + minuto_adicional
        
        # Calcular ticks acumulados até este minuto
        ticks_acumulados = ticks_por_minuto * minuto_adicional
        
        # Calcular índice previsto
        idx_previsto = min(len(ticks) - 1, int(idx_atual + ticks_acumulados))
        
        # Adicionar às listas
        tempos_futuros.append(tempo_futuro)
        odds_previstas.append(ticks[idx_previsto])
        indices_previstos.append(idx_previsto)
    
    return tempos_futuros, odds_previstas, indices_previstos

# Configuração da página Streamlit
st.set_page_config(page_title="Calculadora de Ticks por Minuto", layout="wide")

# Título do aplicativo
st.title("Calculadora de Ticks por Minuto - Mercado Under Limite")
st.markdown("### Previsão de Odds para Apostas")

# Criar layout com colunas
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Entrada de Dados")
    
    # Seleção do período do jogo
    periodo = st.radio("Selecione o período do jogo:", 
                      ["Primeiro Tempo (HT)", "Segundo Tempo (FT)"])
    
    # Input para a odd atual
    odd_atual = st.number_input("Odd Atual:", 
                                min_value=1.01, 
                                max_value=20.0, 
                                value=2.0, 
                                step=0.01,
                                format="%.2f")
    
    # Input para o tempo atual
    if periodo == "Primeiro Tempo (HT)":
        tempo_atual = st.slider("Tempo Atual (minutos):", 
                               min_value=1, 
                               max_value=45, 
                               value=15)
    else:
        tempo_atual = st.slider("Tempo Atual (minutos):", 
                               min_value=46, 
                               max_value=90, 
                               value=60)
    
    # Input para acréscimos
    acrescimos_ht = st.number_input("Acréscimos no Primeiro Tempo (minutos):", 
                                   min_value=0, 
                                   max_value=15, 
                                   value=2)
    
    acrescimos_ft = st.number_input("Acréscimos no Segundo Tempo (minutos):", 
                                   min_value=0, 
                                   max_value=15, 
                                   value=5)
    
    # Botão para calcular
    calcular = st.button("Calcular Ticks por Minuto")

# Exibição de resultados
with col2:
    if calcular:
        st.subheader("Resultados")
        
        # Encontrar a odd mais próxima na lista de ticks
        odd_proxima, idx_atual = encontrar_odd_proxima(odd_atual)
        
        # Calcular ticks por minuto
        tpm = calcular_ticks_por_minuto(odd_atual, tempo_atual)
        
        # Exibir resultados
        st.markdown(f"**Odd fornecida:** {odd_atual:.2f}")
        st.markdown(f"**Odd mais próxima na tabela:** {odd_proxima:.2f}")
        st.markdown(f"**Tempo atual:** {tempo_atual} minutos")
        st.markdown(f"**Ticks por minuto:** {tpm:.4f}")
        
        # Prever odds futuras
        tempos_futuros, odds_previstas, indices_previstos = prever_odds_futuras(
            odd_atual, tempo_atual, acrescimos_ht, acrescimos_ft, periodo
        )
        
        # Criar dataframe com previsões
        if len(tempos_futuros) > 0:
            df_previsao = pd.DataFrame({
                "Minuto": tempos_futuros,
                "Odd Prevista": odds_previstas
            })
            
            # Exibir tabela de previsão
            st.subheader("Previsão de Odds Futuras")
            st.dataframe(df_previsao.style.format({"Odd Prevista": "{:.2f}"}))
            
            # Criar gráfico
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(df_previsao["Minuto"], df_previsao["Odd Prevista"], 
                   marker='o', linestyle='-', color='blue')
            ax.set_title("Previsão de Odds x Tempo")
            ax.set_xlabel("Minuto")
            ax.set_ylabel("Odd")
            ax.grid(True)
            
            # Adicionar linha para o valor atual
            ax.axhline(y=odd_atual, color='r', linestyle='--', alpha=0.7)
            ax.axvline(x=tempo_atual, color='r', linestyle='--', alpha=0.7)
            
            # Ajustar limites do eixo y para melhor visualização
            y_min = max(1.0, min(odds_previstas) * 0.9)
            y_max = max(odds_previstas) * 1.1
            ax.set_ylim(y_min, y_max)
            
            # Exibir gráfico
            st.pyplot(fig)
            
        else:
            st.warning("Não foi possível calcular previsões futuras.")

# Informações adicionais
st.markdown("---")
st.markdown("""
### Como usar esta calculadora:
1. Selecione o período do jogo (Primeiro ou Segundo Tempo)
2. Insira a odd atual do mercado under
3. Defina o tempo atual em minutos
4. Configure os acréscimos esperados para ambos os tempos
5. Clique em "Calcular Ticks por Minuto"

A calculadora mostrará a taxa de ticks por minuto e fará previsões de como a odd deve se comportar nos minutos restantes.
""")
