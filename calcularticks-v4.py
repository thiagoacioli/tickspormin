import streamlit as st

# Lista completa de ticks regressivos (já convertidos para float)
ticks = [
    20.0, 19.5, 19.0, 18.5, 18.0, 17.5, 17.0, 16.5, 16.0, 15.5,
    15.0, 14.5, 14.0, 13.5, 13.0, 12.5, 12.0, 11.5, 11.0, 10.5,
    10.0, 9.8, 9.6, 9.4, 9.2, 9.0, 8.8, 8.6, 8.4, 8.2,
    8.0, 7.8, 7.6, 7.4, 7.2, 7.0, 6.8, 6.6, 6.4, 6.2,
    6.0, 5.9, 5.8, 5.7, 5.6, 5.5, 5.4, 5.3, 5.2, 5.1,
    5.0, 4.9, 4.8, 4.7, 4.6, 4.5, 4.4, 4.3, 4.2, 4.1,
    4.0, 3.95, 3.9, 3.85, 3.8, 3.75, 3.7, 3.65, 3.6, 3.55,
    3.5, 3.45, 3.4, 3.35, 3.3, 3.25, 3.2, 3.15, 3.1, 3.05,
    3.0, 2.98, 2.96, 2.94, 2.92, 2.9, 2.88, 2.86, 2.84, 2.82,
    2.8, 2.78, 2.76, 2.74, 2.72, 2.7, 2.68, 2.66, 2.64, 2.62,
    2.6, 2.58, 2.56, 2.54, 2.52, 2.5, 2.48, 2.46, 2.44, 2.42,
    2.4, 2.38, 2.36, 2.34, 2.32, 2.3, 2.28, 2.26, 2.24, 2.22,
    2.2, 2.18, 2.16, 2.14, 2.12, 2.1, 2.08, 2.06, 2.04, 2.02,
    2.0, 1.99, 1.98, 1.97, 1.96, 1.95, 1.94, 1.93, 1.92, 1.91,
    1.9, 1.89, 1.88, 1.87, 1.86, 1.85, 1.84, 1.83, 1.82, 1.81,
    1.8, 1.79, 1.78, 1.77, 1.76, 1.75, 1.74, 1.73, 1.72, 1.71,
    1.7, 1.69, 1.68, 1.67, 1.66, 1.65, 1.64, 1.63, 1.62, 1.61,
    1.6, 1.59, 1.58, 1.57, 1.56, 1.55, 1.54, 1.53, 1.52, 1.51,
    1.5, 1.49, 1.48, 1.47, 1.46, 1.45, 1.44, 1.43, 1.42, 1.41,
    1.4, 1.39, 1.38, 1.37, 1.36, 1.35, 1.34, 1.33, 1.32, 1.31,
    1.3, 1.29, 1.28, 1.27, 1.26, 1.25, 1.24, 1.23, 1.22, 1.21,
    1.2, 1.19, 1.18, 1.17, 1.16, 1.15, 1.14, 1.13, 1.12, 1.11,
    1.1, 1.09, 1.08, 1.07, 1.06, 1.05, 1.04, 1.03, 1.02, 1.01
]

def main():
    st.title("Calculadora de Ticks - Mercado Under")
    
    # Inputs principais
    col1, col2 = st.columns(2)
    with col1:
        odd = st.number_input("Odd Atual", min_value=1.01, max_value=20.0, step=0.01, format="%.2f")
    with col2:
        tempo = st.number_input("Minuto Atual", min_value=0, max_value=90, step=1)
    
    # Acréscimos
    st.subheader("Configuração de Acréscimos")
    ac_ht = st.number_input("Acréscimos no HT", min_value=0, max_value=10, step=1)
    ac_ft = st.number_input("Acréscimos no FT", min_value=0, max_value=10, step=1)
    
    # Cálculo do tempo total
    if tempo <= 45:
        periodo = "Primeiro Tempo"
        tempo_total = 45 + ac_ht
    else:
        periodo = "Segundo Tempo"
        tempo_total = 45 + ac_ft
    
    # Cálculo do tick rate
    tick_rate = ((odd - 1) * 100) / tempo_total if tempo_total > 0 else 0
    
    # Encontrar posição atual nos ticks
    try:
        index_atual = ticks.index(odd)
    except ValueError:
        # Encontra o tick mais próximo se não houver correspondência exata
        index_atual = min(range(len(ticks)), key=lambda i: abs(ticks[i] - odd))
    
    # Previsão para os próximos minutos
    st.subheader("Previsão de Odds Futuras")
    minutos_restantes = (tempo_total - tempo) if tempo <=45 else (tempo_total - (tempo - 45))
    
    previsoes = []
    for minuto in range(1, minutos_restantes + 1):
        novo_index = index_atual - (tick_rate * minuto)
        novo_index = max(0, min(int(round(novo_index)), len(ticks)-1))
        previsoes.append((minuto + tempo, ticks[novo_index]))
    
    # Exibição em tabela
    st.write(f"**Tick Rate Calculado:** {tick_rate:.2f} ticks/minuto")
    st.write("**Projeção:**")
    
    for minuto, odd_projetada in previsoes:
        st.write(f"- Minuto {minuto}: `{odd_projetada:.2f}`")

if __name__ == "__main__":
    main()
import streamlit as st
import plotly.express as px
import pandas as pd

# [...] (Lista de ticks mantida igual do código anterior)

def main():
    st.title("Calculadora de Ticks - Mercado Under")
    
    # Inputs principais (mantido igual)
    col1, col2 = st.columns(2)
    with col1:
        odd = st.number_input("Odd Atual", min_value=1.01, max_value=20.0, step=0.01, format="%.2f")
    with col2:
        tempo = st.number_input("Minuto Atual", min_value=0, max_value=90, step=1)
    
    # [...] (Seção de acréscimos mantida igual)
    
    # Cálculos principais (mantidos iguais)
    # [...] (Código de cálculo do tick_rate e previsoes)
    
    # ========= NOVOS ELEMENTOS =========
    st.markdown("---")
    
    # Métricas principais em cards
    st.subheader("Principais Indicadores")
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Ticks por Minuto", f"{tick_rate:.2f}", delta_color="off", border=True)
    with m2:
        odd_final = previsoes[-1][1] if previsoes else odd
        st.metric("Odd Final Prevista", f"{odd_final:.2f}", border=True)
    with m3:
        tempo_restante = minutos_restantes
        st.metric("Tempo Restante", f"{tempo_restante} min", border=True)
    
    # Gráfico interativo de tendência
    st.subheader("Trajetória das Odds Previstas")
    
    # Criar DataFrame para o Plotly
    df = pd.DataFrame(previsoes, columns=["Minuto", "Odd"])
    
    # Plotar gráfico de linha interativo
    fig = px.line(
        df,
        x="Minuto",
        y="Odd",
        markers=True,
        title="Projeção Temporal das Odds",
        labels={"Odd": "Valor da Odd", "Minuto": "Minuto do Jogo"}
    )
    
    # Personalizar layout
    fig.update_layout(
        hovermode="x unified",
        xaxis_range=[df['Minuto'].min()-1, df['Minuto'].max()+1],
        yaxis_range=[df['Odd'].min()-0.5, df['Odd'].max()+0.5],
        template="plotly_white"
    )
    
    # Adicionar linha de referência atual
    fig.add_vline(
        x=tempo,
        line_dash="dot",
        annotation_text="Momento Atual",
        line_color="red"
    )
    
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
