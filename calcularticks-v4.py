import streamlit as st
import plotly.graph_objects as go

# Lista de ticks pré-definidos
TICKS = [20.0, 19.5, 19.0, 18.5, 18.0, 17.5, 17.0, 16.5, 16.0, 15.5, 15.0, 14.5, 14.0, 13.5, 13.0, 12.5, 12.0, 11.5,
         11.0, 10.5, 10.0, 9.8, 9.6, 9.4, 9.2, 9.0, 8.8, 8.6, 8.4, 8.2, 8.0, 7.8, 7.6, 7.4, 7.2, 7.0, 6.8, 6.6, 6.4,
         6.2, 6.0, 5.9, 5.8, 5.7, 5.6, 5.5, 5.4, 5.3, 5.2, 5.1, 5.0, 4.9, 4.8, 4.7, 4.6, 4.5, 4.4, 4.3, 4.2, 4.1, 4.0,
         3.95, 3.9, 3.85, 3.8, 3.75, 3.7, 3.65, 3.6, 3.55, 3.5, 3.45, 3.4, 3.35, 3.3, 3.25, 3.2, 3.15, 3.1, 3.05, 3.0,
         2.98, 2.96, 2.94, 2.92, 2.9, 2.88, 2.86, 2.84, 2.82, 2.8, 2.78, 2.76, 2.74, 2.72, 2.7, 2.68, 2.66, 2.64, 2.62,
         2.6, 2.58, 2.56, 2.54, 2.52, 2.5, 2.48, 2.46, 2.44, 2.42, 2.4, 2.38, 2.36, 2.34, 2.32, 2.3, 2.28, 2.26, 2.24,
         2.22, 2.2, 2.18, 2.16, 2.14, 2.12, 2.1, 2.08, 2.06, 2.04, 2.02, 2.0, 1.99, 1.98, 1.97, 1.96, 1.95, 1.94, 1.93,
         1.92, 1.91, 1.9, 1.89, 1.88, 1.87, 1.86, 1.85, 1.84, 1.83, 1.82, 1.81, 1.8, 1.79, 1.78, 1.77, 1.76, 1.75, 1.74,
         1.73, 1.72, 1.71, 1.7, 1.69, 1.68, 1.67, 1.66, 1.65, 1.64, 1.63, 1.62, 1.61, 1.6, 1.59, 1.58, 1.57, 1.56, 1.55,
         1.54, 1.53, 1.52, 1.51, 1.5, 1.49, 1.48, 1.47, 1.46, 1.45, 1.44, 1.43, 1.42, 1.41, 1.4, 1.39, 1.38, 1.37, 1.36,
         1.35, 1.34, 1.33, 1.32, 1.31, 1.3, 1.29, 1.28, 1.27, 1.26, 1.25, 1.24, 1.23, 1.22, 1.21, 1.2, 1.19, 1.18, 1.17,
         1.16, 1.15, 1.14, 1.13, 1.12, 1.11, 1.1, 1.09, 1.08, 1.07, 1.06, 1.05, 1.04, 1.03, 1.02, 1.01]

def calcular_previsao():
    current_odd = st.session_state.odd
    current_time = st.session_state.tempo
    acréscimos_ht = st.session_state.acrescimos_ht
    acréscimos_ft = st.session_state.acrescimos_ft

    # Determinar período e tempo restante
    periodo = "Primeiro Tempo" if current_time <= 45 else "Segundo Tempo"
    tempo_total = (45 + acréscimos_ht) if periodo == "Primeiro Tempo" else (90 + acréscimos_ft)
    tempo_restante = tempo_total - current_time

    # Calcular ticks por minuto
    ticks_por_minuto = ((current_odd - 1) * 100) / current_time if current_time > 0 else 0

    # Encontrar posição atual nos ticks
    idx = min(range(len(TICKS)), key=lambda i: abs(TICKS[i] - current_odd))
    ticks_restantes = len(TICKS) - idx - 1
    taxa_necessaria = ticks_restantes / tempo_restante if tempo_restante > 0 else 0

    # Gerar previsão
    previsao = []
    tempo_decorrido = 0
    while ticks_restantes > 0 and tempo_decorrido <= tempo_restante:
        minuto_atual = current_time + tempo_decorrido
        posicao = int(idx + (taxa_necessaria * tempo_decorrido))
        previsao.append((minuto_atual, TICKS[min(posicao, len(TICKS)-1)]))
        tempo_decorrido += 1

    return {
        "periodo": periodo,
        "ticks_por_minuto": ticks_por_minuto,
        "taxa_necessaria": taxa_necessaria,
        "previsao": previsao,
        "tempo_restante": tempo_restante,
        "odd_final": previsao[-1][1] if previsao else 1.01
    }

# Interface do app
st.title("Calculadora de Ticks para Mercados Regressivos")

with st.form(key='calculadora'):
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("Odd Atual", key="odd", min_value=1.01, max_value=20.0, step=0.01, format="%.2f")
        st.number_input("Tempo Atual (min)", key="tempo", min_value=0, max_value=90, step=1)
    with col2:
        st.number_input("Acréscimos HT", key="acrescimos_ht", min_value=0, max_value=10, step=1)
        st.number_input("Acréscimos FT", key="acrescimos_ft", min_value=0, max_value=10, step=1)
    
    if st.form_submit_button("Calcular"):
        resultados = calcular_previsao()

        # Exibir métricas
        st.subheader("Principais Métricas")
        cols = st.columns(3)
        cols[0].metric("Ticks/Min Atual", f"{resultados['ticks_por_minuto']:.2f}")
        cols[1].metric("Taxa Necessária", f"{resultados['taxa_necessaria']:.2f}/min")
        cols[2].metric("Odd Final Prevista", f"{resultados['odd_final']:.2f}")

        # Gráfico interativo
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=[p[0] for p in resultados['previsao']],
            y=[p[1] for p in resultados['previsao']],
            mode='lines+markers',
            name='Previsão'
        ))
        fig.update_layout(
            title=f"Trajetória da Odd - {resultados['periodo']}",
            xaxis_title="Minuto",
            yaxis_title="Odd",
            hovermode="x unified"
        )
        st.plotly_chart(fig)

        # Tabela de previsão
        st.subheader("Previsão Detalhada")
        st.dataframe(
            data=[{"Minuto": p[0], "Odd Prevista": p[1]} for p in resultados['previsao']],
            use_container_width=True,
            hide_index=True
        )
