import streamlit as st
import pandas as pd

st.title('Calculadora de Ticks por Minuto ⚽📈')

# Inputs do usuário
odd = st.number_input('Odd atual:', 
                     min_value=1.01, 
                     max_value=1000.0, 
                     step=0.01, 
                     value=2.0)

half = st.radio('Selecione o período:', 
               ('Primeiro Tempo (HT)', 'Segundo Tempo'))

# Configura tempo máximo
max_time = 45 if half == 'Primeiro Tempo (HT)' else 90
current_time = st.number_input('Minuto atual:', 
                              min_value=0, 
                              max_value=max_time, 
                              value=0, 
                              step=1)

remaining_time = max_time - current_time

if remaining_time <= 0:
    st.error('⛔ O tempo atual não pode ser maior ou igual ao tempo máximo do período!')
else:
    if odd <= 1.01:
        st.error('⛔ A odd já é 1.01 ou menor!')
    else:
        # Cálculo dos ticks
        ticks = ((odd - 1.01) * 100) / remaining_time
        st.metric(label="**Ticks por minuto**", value=f"{ticks:.2f}")

        # Previsão das odds
        st.subheader('Previsão das Odds 📉')
        predictions = []
        
        for minute in range(current_time + 1, max_time + 1):
            delta = minute - current_time
            predicted_odd = odd - (ticks / 100) * delta
            predicted_odd = max(round(predicted_odd, 2), 1.01)
            predictions.append((minute, predicted_odd))

        # Mostra em formato de tabela
        df = pd.DataFrame(predictions, columns=['Minuto', 'Odd Prevista'])
        st.table(df.style.format({'Odd Prevista': '{:.2f}'}))
