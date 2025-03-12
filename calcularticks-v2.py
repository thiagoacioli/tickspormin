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

stoppage_time = st.number_input('Acréscimos (minutos):',
                               min_value=0,
                               max_value=15,
                               value=0,
                               step=1,
                               help='Tempo adicional determinado pelo árbitro')

# Configura tempo máximo
base_max_time = 45 if half == 'Primeiro Tempo (HT)' else 90
adjusted_max_time = base_max_time + stoppage_time

current_time = st.number_input('Minuto atual:', 
                              min_value=0, 
                              max_value=adjusted_max_time, 
                              value=0, 
                              step=1)

remaining_time = adjusted_max_time - current_time

if remaining_time <= 0:
    st.error('⛔ O tempo atual não pode ser maior ou igual ao tempo máximo ajustado!')
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
        
        for minute in range(current_time + 1, adjusted_max_time + 1):
            delta = minute - current_time
            predicted_odd = odd - (ticks / 100) * delta
            predicted_odd = max(round(predicted_odd, 2), 1.01)
            
            # Formatação do minuto com acréscimos
            if minute > base_max_time:
                display_minute = f"{base_max_time}+{minute - base_max_time}"
            else:
                display_minute = str(minute)
                
            predictions.append((display_minute, predicted_odd))

        # Mostra em formato de tabela
        df = pd.DataFrame(predictions, columns=['Minuto', 'Odd Prevista'])
        st.table(df.style.format({'Odd Prevista': '{:.2f}'}))
