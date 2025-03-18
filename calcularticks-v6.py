import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Definir os valores da escala de odds regressiva
odds_regressivas = [
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

def calcular_ticks_por_minuto(odd, tempo):
    """Calcula os ticks por minuto com base na odd atual e tempo"""
    return ((odd - 1) * 100) / tempo

def encontrar_odd_mais_proxima(odd):
    """Encontra o valor mais próximo na lista de odds regressivas"""
    return min(odds_regressivas, key=lambda x: abs(x - odd))

def encontrar_indice_odd(odd):
    """Encontra o índice da odd mais próxima na lista de odds regressivas"""
    odd_proxima = encontrar_odd_mais_proxima(odd)
    return odds_regressivas.index(odd_proxima)

def prever_odd_para_tempo_alvo(odd_atual, tempo_atual, ticks_por_minuto, tempo_alvo):
    """Prevê a odd para um tempo específico do jogo"""
    # Verifica se o tempo alvo é depois do tempo atual
    if tempo_alvo <= tempo_atual:
        return odd_atual
    
    # Calcula quantos minutos no futuro
    minutos_futuros = tempo_alvo - tempo_atual
    
    # Calcula quantos ticks serão movidos nesse tempo
    ticks_a_mover = ticks_por_minuto * minutos_futuros
    
    # Encontra o índice atual na escala de odds
    indice_atual = encontrar_indice_odd(odd_atual)
    
    # Calcula o novo índice
    novo_indice = min(len(odds_regressivas) - 1, int(indice_atual + ticks_a_mover))
    
    # Retorna a odd prevista
    if 0 <= novo_indice < len(odds_regressivas):
        return odds_regressivas[novo_indice]
    elif novo_indice >= len(odds_regressivas):
        return 1.01  # Retorna o valor mínimo se ultrapassar
    else:
        return odd_atual  # Mantém a odd atual se o índice for negativo

def calcular_tempo_restante(tempo, periodo):
    """Calcula o tempo restante no período atual"""
    if periodo == "HT":
        return 45 - tempo
    else:  # FT
        return 90 - tempo

def criar_tabela_previsoes(odd_atual, tempo_atual, periodo, ticks_por_minuto):
    """Cria uma tabela com previsões de odds para tempos específicos do jogo"""
    # Determinar o tempo máximo
    if periodo == "HT":
        tempo_maximo = 45
    else:
        tempo_maximo = 90
    
    # Criar intervalos de 5 em 5 minutos
    if periodo == "HT":
        # Para primeiro tempo, criar intervalos de 5 em 5 até 45
        intervalos = list(range(max(tempo_atual + 5, 5), 46, 5))
    else:
        # Para segundo tempo, criar intervalos de 5 em 5 a partir de 50 até 90
        intervalos = list(range(max(tempo_atual + 5, 50), 91, 5))
    
    # Criar dados da tabela
    dados = []
    for tempo_jogo in intervalos:
        if tempo_jogo > tempo_atual:  # Só prever para o futuro
            odd_prevista = prever_odd_para_tempo_alvo(odd_atual, tempo_atual, ticks_por_minuto, tempo_jogo)
            dados.append({
                "Minuto do Jogo": tempo_jogo,
                "Odd Prevista": odd_prevista
            })
    
    return pd.DataFrame(dados)

# Configurar o aplicativo Streamlit
st.set_page_config(page_title="Calculadora de Ticks - Under Limite", layout="wide")

st.title("Calculadora de Ticks por Minuto - Under Limite")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Dados Atuais")
    
    # Seleção do período
    periodo = st.radio("Período", ["HT", "FT"], horizontal=True)
    
    # Entradas do usuário
    if periodo == "HT":
        tempo = st.number_input("Tempo Atual (minutos)", min_value=0, max_value=45, value=10, step=1)
    else:
        tempo = st.number_input("Tempo Atual (minutos)", min_value=46, max_value=90, value=60, step=1)
    
    odd = st.number_input("Odd Atual", min_value=1.01, max_value=20.0, value=3.0, step=0.01, format="%.2f")
    
    # Cálculo dos ticks por minuto
    ticks_por_minuto = calcular_ticks_por_minuto(odd, tempo)
    
    st.metric("Ticks por Minuto", f"{ticks_por_minuto:.2f}")
    
    # Tempo restante
    tempo_restante = calcular_tempo_restante(tempo, periodo)
    st.metric("Tempo Restante", f"{tempo_restante} minutos")
    
    # Odd mais próxima na escala
    odd_proxima = encontrar_odd_mais_proxima(odd)
    st.metric("Odd mais próxima na escala", f"{odd_proxima:.2f}")
    
    # Posição na escala de odds
    indice_odd = encontrar_indice_odd(odd)
    st.metric("Posição na escala de odds", f"{indice_odd} / {len(odds_regressivas)}")

with col2:
    st.subheader("Previsão de Odds para Minutos Específicos")
    
    st.markdown("**Selecione um minuto para ver a previsão da odd:**")
    
    # Determinar os botões a serem mostrados com base no período e tempo atual
    if periodo == "HT":
        # Para primeiro tempo, botões de 5 em 5 até 45
        tempos_possiveis = [t for t in range(5, 46, 5) if t > tempo]
    else:
        # Para segundo tempo, botões de 5 em 5 de 50 até 90
        tempos_possiveis = [t for t in range(50, 91, 5) if t > tempo]
    
    # Criar grade de botões
    # Determinar quantos botões por linha
    botoes_por_linha = 6
    
    # Criar linhas necessárias
    for i in range(0, len(tempos_possiveis), botoes_por_linha):
        cols = st.columns(botoes_por_linha)
        # Adicionar botões a esta linha
        for j in range(botoes_por_linha):
            idx = i + j
            if idx < len(tempos_possiveis):
                tempo_alvo = tempos_possiveis[idx]
                if cols[j].button(f"{tempo_alvo}'", key=f"btn_{tempo_alvo}"):
                    odd_prevista = prever_odd_para_tempo_alvo(odd, tempo, ticks_por_minuto, tempo_alvo)
                    st.success(f"No minuto {tempo_alvo}, a odd prevista é: **{odd_prevista:.2f}**")
    
    # Tabela completa de previsões
    st.markdown("### Tabela de Previsões")
    tabela_previsoes = criar_tabela_previsoes(odd, tempo, periodo, ticks_por_minuto)
    
    if not tabela_previsoes.empty:
        st.dataframe(tabela_previsoes, hide_index=True)
        
        # Criar gráfico de previsão
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Dados para o gráfico
        tempos_jogo = [tempo] + tabela_previsoes["Minuto do Jogo"].tolist()
        odds_previstas = [odd] + tabela_previsoes["Odd Prevista"].tolist()
        
        # Plot
        plt.plot(tempos_jogo, odds_previstas, 'o-', color='blue')
        plt.xlabel('Minuto do Jogo')
        plt.ylabel('Odd Prevista')
        plt.title('Projeção das Odds ao Longo do Tempo')
        plt.grid(True)
        
        # Adiciona linha para odd mínima (1.01)
        plt.axhline(y=1.01, color='r', linestyle='--', alpha=0.7)
        
        # Definir limites do eixo y
        plt.ylim(max(0.9, min(odds_previstas) - 0.2), max(odds_previstas) + 0.5)
        
        st.pyplot(fig)
    else:
        st.info("Não há previsões disponíveis para o tempo restante.")

# Mostrar explicação do funcionamento
with st.expander("Como funciona a calculadora?"):
    st.markdown("""
    ### Funcionamento da Calculadora de Ticks por Minuto

    1. **Fórmula utilizada**: `((odd - 1) * 100) / tempo`
    2. **Períodos**:
       - HT: Do minuto 0 ao 45
       - FT: Do minuto 46 ao 90
    3. **Escala de Odds**: A calculadora usa uma escala regressiva padronizada de odds que vai de 20.0 até 1.01
    4. **Previsão**: Baseada no ritmo atual de ticks por minuto, a calculadora prevê em qual odd o mercado estará nos minutos específicos do jogo

    **Observação**: Este app é uma ferramenta de auxílio para análise de tendências nas odds do mercado under limite, onde as odds são regressivas e tendem a 1.01 no final de cada período.
    """)
