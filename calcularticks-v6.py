import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Lista de odds regressivas
TICKS = [
    20, 19.5, 19, 18.5, 18, 17.5, 17, 16.5, 16, 15.5, 15, 14.5, 14, 13.5, 13, 12.5, 12, 11.5, 11, 10.5, 10,
    9.8, 9.6, 9.4, 9.2, 9, 8.8, 8.6, 8.4, 8.2, 8, 7.8, 7.6, 7.4, 7.2, 7, 6.8, 6.6, 6.4, 6.2, 6,
    5.9, 5.8, 5.7, 5.6, 5.5, 5.4, 5.3, 5.2, 5.1, 5, 4.9, 4.8, 4.7, 4.6, 4.5, 4.4, 4.3, 4.2, 4.1, 4,
    3.95, 3.9, 3.85, 3.8, 3.75, 3.7, 3.65, 3.6, 3.55, 3.5, 3.45, 3.4, 3.35, 3.3, 3.25, 3.2, 3.15, 3.1, 3.05, 3,
    2.98, 2.96, 2.94, 2.92, 2.9, 2.88, 2.86, 2.84, 2.82, 2.8, 2.78, 2.76, 2.74, 2.72, 2.7, 2.68, 2.66, 2.64, 2.62, 2.6,
    2.58, 2.56, 2.54, 2.52, 2.5, 2.48, 2.46, 2.44, 2.42, 2.4, 2.38, 2.36, 2.34, 2.32, 2.3, 2.28, 2.26, 2.24, 2.22, 2.2,
    2.18, 2.16, 2.14, 2.12, 2.1, 2.08, 2.06, 2.04, 2.02, 2,
    1.99, 1.98, 1.97, 1.96, 1.95, 1.94, 1.93, 1.92, 1.91, 1.9, 1.89, 1.88, 1.87, 1.86, 1.85, 1.84, 1.83, 1.82, 1.81, 1.8,
    1.79, 1.78, 1.77, 1.76, 1.75, 1.74, 1.73, 1.72, 1.71, 1.7, 1.69, 1.68, 1.67, 1.66, 1.65, 1.64, 1.63, 1.62, 1.61, 1.6,
    1.59, 1.58, 1.57, 1.56, 1.55, 1.54, 1.53, 1.52, 1.51, 1.5, 1.49, 1.48, 1.47, 1.46, 1.45, 1.44, 1.43, 1.42, 1.41, 1.4,
    1.39, 1.38, 1.37, 1.36, 1.35, 1.34, 1.33, 1.32, 1.31, 1.3, 1.29, 1.28, 1.27, 1.26, 1.25, 1.24, 1.23, 1.22, 1.21, 1.2,
    1.19, 1.18, 1.17, 1.16, 1.15, 1.14, 1.13, 1.12, 1.11, 1.1, 1.09, 1.08, 1.07, 1.06, 1.05, 1.04, 1.03, 1.02, 1.01
]

# Configuração da página Streamlit
st.set_page_config(page_title="Calculadora de Ticks por Minuto", layout="wide")

# Título do aplicativo
st.title("Calculadora de Ticks por Minuto - Under Limite")
st.write("Esta calculadora ajuda a prever a movimentação das odds no mercado de under limite.")

# Função para calcular ticks por minuto
def calcular_ticks_por_minuto(odd, tempo):
    return ((odd - 1) * 100) / tempo

# Função para encontrar a odd mais próxima na lista de ticks
def encontrar_odd_mais_proxima(odd):
    return min(TICKS, key=lambda x: abs(x - odd))

# Função para encontrar o índice da odd na lista de ticks
def encontrar_indice_odd(odd):
    odd_proxima = encontrar_odd_mais_proxima(odd)
    return TICKS.index(odd_proxima)

# Função para prever odd futura baseada no tick rate
def prever_odd(odd_atual, tempo_atual, tempo_futuro, acrescimos_ht=0, acrescimos_ft=0):
    # Ajustar o tempo considerando os acréscimos
    tempo_maximo = 90 + acrescimos_ft
    
    if tempo_atual <= 45:
        tempo_maximo_primeiro_tempo = 45 + acrescimos_ht
        if tempo_futuro <= tempo_maximo_primeiro_tempo:
            tempo_restante = tempo_futuro - tempo_atual
        else:
            tempo_restante = (tempo_maximo_primeiro_tempo - tempo_atual) + (tempo_futuro - 45)
    else:
        tempo_restante = tempo_futuro - tempo_atual
    
    # Verificar se o tempo futuro é válido
    if tempo_futuro > tempo_maximo or tempo_futuro <= tempo_atual:
        return None, None
    
    # Calcular ticks por minuto
    tick_rate = calcular_ticks_por_minuto(odd_atual, tempo_maximo - tempo_atual)
    
    # Calcular quantos ticks vão diminuir no período
    ticks_a_diminuir = tick_rate * tempo_restante / 100
    
    # Encontrar índice da odd atual na lista
    indice_atual = encontrar_indice_odd(odd_atual)
    
    # Calcular novo índice
    novo_indice = int(indice_atual + ticks_a_diminuir)
    
    # Garantir que o índice está dentro dos limites
    novo_indice = min(max(novo_indice, 0), len(TICKS) - 1)
    
    # Retornar a nova odd e o tick rate
    return TICKS[novo_indice], tick_rate

# Interface principal
tabs = st.tabs(["Calculadora", "Previsão por Blocos", "Visualização"])

with tabs[0]:
    st.header("Calculadora de Ticks por Minuto")
    
    col1, col2 = st.columns(2)
    
    with col1:
        odd_atual = st.number_input("Odd Atual", min_value=1.01, max_value=20.0, value=2.0, step=0.01, format="%.2f")
        tempo_atual = st.number_input("Tempo Atual (minutos)", min_value=0, max_value=90, value=10, step=1)
        acrescimos_ht = st.number_input("Acréscimos 1º Tempo (minutos)", min_value=0, max_value=15, value=2, step=1)
        acrescimos_ft = st.number_input("Acréscimos 2º Tempo (minutos)", min_value=0, max_value=15, value=5, step=1)
    
    with col2:
        # Identificar se estamos no primeiro ou segundo tempo
        periodo = "1º Tempo" if tempo_atual <= 45 else "2º Tempo"
        st.info(f"Período atual: {periodo}")
        
        # Calcular tick rate
        tempo_maximo = 90 + acrescimos_ft if tempo_atual > 45 else 45 + acrescimos_ht
        if tempo_atual <= 45 and tempo_maximo < tempo_atual:
            st.error("Erro: O tempo atual não pode ser maior que o tempo máximo do 1º tempo.")
        else:
            tick_rate = calcular_ticks_por_minuto(odd_atual, tempo_maximo - tempo_atual)
            st.metric("Taxa de Ticks por Minuto", f"{tick_rate:.4f}")
            
            # Encontrar índice na lista de ticks
            indice_odd = encontrar_indice_odd(odd_atual)
            odd_padronizada = TICKS[indice_odd]
            st.metric("Odd padronizada mais próxima", f"{odd_padronizada:.2f}")
            
            # Mostrar posição no ranking de ticks
            st.metric("Posição no ranking de ticks", f"{indice_odd + 1} de {len(TICKS)}")
    
    # Previsão para os próximos minutos
    st.subheader("Previsão para os próximos minutos")
    
    # Criar uma tabela de previsão
    previsoes = {}
    tempos_futuros = [tempo_atual + 5, tempo_atual + 10, tempo_atual + 15, 45, 60, 75, 90, 90 + acrescimos_ft]
    tempos_futuros = [t for t in tempos_futuros if t > tempo_atual and t <= (90 + acrescimos_ft)]
    
    if tempos_futuros:
        for tempo_futuro in tempos_futuros:
            nova_odd, tick_rate = prever_odd(odd_atual, tempo_atual, tempo_futuro, acrescimos_ht, acrescimos_ft)
            if nova_odd is not None:
                previsoes[tempo_futuro] = nova_odd
        
        # Criar DataFrame para exibição
        df_previsoes = pd.DataFrame({
            "Tempo (min)": list(previsoes.keys()),
            "Odd Prevista": list(previsoes.values())
        })
        
        st.table(df_previsoes.set_index("Tempo (min)"))
    else:
        st.warning("Não é possível fazer previsões para tempos futuros com base nos dados atuais.")

with tabs[1]:
    st.header("Previsão por Blocos de Tempo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        odd_atual_bloco = st.number_input("Odd Atual", min_value=1.01, max_value=20.0, value=2.0, step=0.01, format="%.2f", key="odd_bloco")
        tempo_atual_bloco = st.number_input("Tempo Atual (minutos)", min_value=0, max_value=90, value=10, step=1, key="tempo_bloco")
        acrescimos_ht_bloco = st.number_input("Acréscimos 1º Tempo (minutos)", min_value=0, max_value=15, value=2, step=1, key="ht_bloco")
        acrescimos_ft_bloco = st.number_input("Acréscimos 2º Tempo (minutos)", min_value=0, max_value=15, value=5, step=1, key="ft_bloco")
        
    # Botões para previsão em blocos de 5 minutos
    st.subheader("Selecione o tempo alvo para previsão")
    
    # Criar botões de 5 em 5 minutos de acordo com o tempo atual
    tempo_max = 90 + acrescimos_ft_bloco
    botoes_tempos = list(range(5, tempo_max + 1, 5))
    botoes_tempos = [t for t in botoes_tempos if t > tempo_atual_bloco]
    
    if not botoes_tempos:
        st.warning("Não há tempos futuros disponíveis para previsão.")
    else:
        # Organizar botões em linhas
        cols = st.columns(5)
        tempo_selecionado = None
        
        for i, tempo in enumerate(botoes_tempos):
            col_idx = i % 5
            if cols[col_idx].button(f"{tempo}'", key=f"btn_{tempo}"):
                tempo_selecionado = tempo
        
        if tempo_selecionado:
            nova_odd, tick_rate = prever_odd(odd_atual_bloco, tempo_atual_bloco, tempo_selecionado, acrescimos_ht_bloco, acrescimos_ft_bloco)
            
            if nova_odd is not None:
                st.success(f"Previsão para o minuto {tempo_selecionado}:")
                st.metric("Odd Prevista", f"{nova_odd:.2f}")
                st.metric("Taxa de Ticks", f"{tick_rate:.4f}")
            else:
                st.error("Não foi possível calcular a previsão para esse tempo.")

with tabs[2]:
    st.header("Visualização da Queda de Odds")
    
    col1, col2 = st.columns(2)
    
    with col1:
        odd_viz = st.number_input("Odd Atual", min_value=1.01, max_value=20.0, value=2.0, step=0.01, format="%.2f", key="odd_viz")
        tempo_viz = st.number_input("Tempo Atual (minutos)", min_value=0, max_value=90, value=10, step=1, key="tempo_viz")
        acrescimos_ht_viz = st.number_input("Acréscimos 1º Tempo (minutos)", min_value=0, max_value=15, value=2, step=1, key="ht_viz")
        acrescimos_ft_viz = st.number_input("Acréscimos 2º Tempo (minutos)", min_value=0, max_value=15, value=5, step=1, key="ft_viz")
    
    # Gerar tempos para visualização
    tempo_max_viz = 90 + acrescimos_ft_viz
    tempos_viz = list(range(tempo_viz, tempo_max_viz + 1))
    odds_previstas = []
    
    for t in tempos_viz:
        nova_odd, _ = prever_odd(odd_viz, tempo_viz, t, acrescimos_ht_viz, acrescimos_ft_viz)
        if nova_odd is not None:
            odds_previstas.append(nova_odd)
        else:
            odds_previstas.append(None)
    
    # Remover None values
    tempos_viz_clean = [tempos_viz[i] for i in range(len(tempos_viz)) if odds_previstas[i] is not None]
    odds_previstas_clean = [odd for odd in odds_previstas if odd is not None]
    
    if tempos_viz_clean and odds_previstas_clean:
        # Criar gráfico
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(tempos_viz_clean, odds_previstas_clean, marker='o', linestyle='-', color='blue')
        
        # Adicionar linha vertical no minuto 45
        if tempo_viz <= 45 and max(tempos_viz_clean) > 45:
            ax.axvline(x=45, color='red', linestyle='--', alpha=0.7)
            ax.text(45, max(odds_previstas_clean), 'Intervalo', rotation=90, verticalalignment='top')
        
        # Configurar gráfico
        ax.set_title('Previsão de Queda das Odds ao Longo do Tempo')
        ax.set_xlabel('Tempo (minutos)')
        ax.set_ylabel('Odd')
        ax.grid(True, alpha=0.3)
        
        # Ajustar limites do eixo y para melhor visualização
        max_odd = max(odds_previstas_clean)
        min_odd = min(odds_previstas_clean)
        y_margin = (max_odd - min_odd) * 0.1  # 10% de margem
        ax.set_ylim(max(1.0, min_odd - y_margin), max_odd + y_margin)
        
        # Mostrar gráfico no Streamlit
        st.pyplot(fig)
        
        # Tabela de dados para download
        df_viz = pd.DataFrame({
            "Tempo (min)": tempos_viz_clean,
            "Odd Prevista": odds_previstas_clean
        })
        
        st.subheader("Dados da Previsão")
        st.dataframe(df_viz)
        
        # Download dos dados
        csv = df_viz.to_csv(index=False)
        st.download_button(
            label="Download dos dados em CSV",
            data=csv,
            file_name="previsao_odds.csv",
            mime="text/csv",
        )
    else:
        st.warning("Não há dados suficientes para gerar a visualização.")

# Rodapé com informações
st.markdown("---")
st.write("Calculadora de Ticks por Minuto para mercado de Under Limite")
st.write("Fórmula utilizada: ((odd - 1)*100)/tempo restante")
