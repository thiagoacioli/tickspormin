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
