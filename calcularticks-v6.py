import streamlit as st
import pandas as pd
import time

def calculate_ticks_per_minute(odd, time_val):
    if time_val == 0:
        return 0.0  # Evitar divisão por zero no início do jogo
    return ((odd - 1) * 100) / time_val

def predict_odds(current_odd, current_time, extra_time_ht, extra_time_ft, period_selection, include_extra_time):
    predictions = []
    
    # Definir o tempo final de cada período com base na seleção 'include_extra_time'
    if include_extra_time:
        time_end_ht = 45 + extra_time_ht
        time_end_ft = 90 + extra_time_ft
    else:
        time_end_ht = 45
        time_end_ft = 90

    # Determinar o tempo final relevante com base na seleção de período
    if period_selection == '1º Tempo':
        target_time = time_end_ht
    else: # '2º Tempo'
        target_time = time_end_ft

    # Se o tempo atual já passou do tempo alvo, não há previsão regressiva
    if current_time >= target_time:
        return pd.DataFrame({'Minuto': [], 'Odd Prevista': []})

    # Calcular a taxa de queda por tick para atingir 1.01 no tempo alvo
    total_ticks_to_fall = (current_odd - 1.01) * 100
    time_remaining = target_time - current_time

    if time_remaining <= 0:
        return pd.DataFrame({"Minuto": [], "Odd Prevista": []})

    projected_ticks_per_minute = total_ticks_to_fall / time_remaining

    # Prever odds para os próximos minutos até o target_time
    # Aumentar o range para cobrir até o final do jogo + acréscimos
    for minute_offset in range(1, (target_time - current_time) + 1): 
        future_time = current_time + minute_offset
        
        if future_time > target_time:
            predicted_odd = 1.01
        else:
            ticks_fallen = projected_ticks_per_minute * minute_offset
            predicted_odd = current_odd - (ticks_fallen / 100)
            
            if predicted_odd < 1.01:
                predicted_odd = 1.01

        predictions.append({'Minuto': future_time, 'Odd Prevista': predicted_odd})

    return pd.DataFrame(predictions)

# Função para aplicar estilos às células da tabela
def highlight_odds_ranges(s):
    # Cores com 10% de opacidade
    red_bg = 'background-color: rgba(255, 0, 0, 0.10)'
    yellow_bg = 'background-color: rgba(255, 255, 0, 0.10)'
    green_bg = 'background-color: rgba(0, 255, 0, 0.10)'
    no_bg = ''

    df_styled = pd.DataFrame(no_bg, index=s.index, columns=s.columns)

    for col in s.columns:
        if col == 'Odd Prevista':
            for idx, odd_val in s[col].items():
                # Certificar-se de que odd_val é um float para comparação
                try:
                    odd_val_float = float(odd_val)
                except ValueError:
                    # Se a conversão falhar, pode ser um valor formatado ou NaN, tratar como 0.0 ou ignorar
                    odd_val_float = 0.0 

                # Faixa lenta (vermelha)
                if (odd_val_float >= 4.0) or \
                   (3.0 <= odd_val_float <= 3.5) or \
                   (2.0 <= odd_val_float <= 2.3) or \
                   (1.01 <= odd_val_float <= 1.30):
                    df_styled.loc[idx, col] = red_bg
                # Faixa média (amarela)
                elif (3.5 < odd_val_float < 4.0) or \
                     (1.70 <= odd_val_float < 1.80) or \
                     (1.30 < odd_val_float < 1.50):
                    df_styled.loc[idx, col] = yellow_bg
                # Faixa rápida (verde)
                elif (2.3 < odd_val_float < 3.0) or \
                     (1.80 <= odd_val_float < 2.0) or \
                     (1.50 <= odd_val_float < 1.70):
                    df_styled.loc[idx, col] = green_bg
    return df_styled

def highlight_every_5_minutes(row):
    if row['Minuto'] % 5 == 0:
        return ['background-color: #24145A; color: white'] * len(row) # Cor roxa para o fundo, texto branco
    return [''] * len(row)

st.set_page_config(layout='wide', page_title='Calculadora de Ticks por Minuto')

st.title('⚽ Calculadora de Ticks por Minuto (Under Limite)')
st.markdown('--- ')

st.sidebar.header('Parâmetros de Entrada')

current_odd = st.sidebar.number_input(
    'Odd Atual (ex: 1.80)', 
    min_value=1.01, 
    value=1.80, 
    step=0.01,
    format='%.2f'
)

period_selection = st.sidebar.radio(
    'Período do Jogo',
    ('1º Tempo', '2º Tempo'),
    key='period_radio'
)

# Definir o range do slider de tempo com base na seleção do período
min_time_slider = 0
max_time_slider = 90
default_time_slider_value = 30 # Valor padrão para o 1º tempo

if period_selection == '1º Tempo':
    min_time_slider = 0
    max_time_slider = 45
    default_time_slider_value = 30
elif period_selection == '2º Tempo':
    min_time_slider = 45
    max_time_slider = 90
    default_time_slider_value = 60 # Um valor razoável para o 2º tempo

# Reset current_time_input if period changes to ensure it's within the new range
# This logic ensures the slider value is reset when the period radio button changes
if 'last_period_selection' not in st.session_state or st.session_state.last_period_selection != period_selection:
    st.session_state.current_time_input = default_time_slider_value
    st.session_state.last_period_selection = period_selection
    # Also reset simulated time if period changes
    st.session_state.simulated_time = st.session_state.current_time_input
    st.session_state.simulation_running = False

# Update current_time_input in session state when slider changes
st.session_state.current_time_input = st.sidebar.slider(
    'Tempo Atual do Jogo (minutos)', 
    min_value=min_time_slider, 
    max_value=max_time_slider, 
    value=st.session_state.current_time_input, # Use session state value
    key='time_slider'
)

include_extra_time = st.sidebar.checkbox(
    'Incluir Acréscimos no Cálculo da Taxa de Ticks',
    value=True, # Por padrão, incluir acréscimos
    help='Se marcado, a odd chegará a 1.01 no final dos acréscimos. Se desmarcado, no final do tempo regulamentar.'
)

# Campo único de acréscimos condicionado ao período selecionado
extra_time_value = st.sidebar.number_input(
    f'Acréscimos para o {period_selection} (minutos)', 
    min_value=0, 
    value=0, 
    step=1,
    disabled=(not include_extra_time)
)

extra_time_ht = 0
extra_time_ft = 0

if include_extra_time:
    if period_selection == '1º Tempo':
        extra_time_ht = extra_time_value
    else:
        extra_time_ft = extra_time_value

st.markdown('## Resultados')

# Placeholder para a tabela de previsões
predictions_placeholder = st.empty()

# Cronômetro no sidebar
st.sidebar.markdown('--- ')
st.sidebar.header('Simulação de Cronômetro')

# Initialize simulation state
if 'simulation_running' not in st.session_state:
    st.session_state.simulation_running = False

if 'simulated_time' not in st.session_state:
    st.session_state.simulated_time = st.session_state.current_time_input

# Buttons for simulation control
col1, col2 = st.sidebar.columns(2)
start_button = col1.button('Iniciar Simulação')
pause_button = col2.button('Pausar Simulação')

if start_button:
    st.session_state.simulation_running = True
    st.session_state.simulated_time = st.session_state.current_time_input

if pause_button:
    st.session_state.simulation_running = False

# Display simulated time in sidebar
simulated_time_display = st.sidebar.empty()
if st.session_state.simulation_running:
    simulated_time_display.metric(label="Tempo Simulado", value=f"{st.session_state.simulated_time} min")

# Main logic for displaying results and running simulation
current_display_time = st.session_state.simulated_time if st.session_state.simulation_running else st.session_state.current_time_input

# Calculate and display initial results or current simulation step
ticks_per_minute = calculate_ticks_per_minute(current_odd, current_display_time)
st.metric(label='Ticks por Minuto', value=f'{ticks_per_minute:.2f}')

st.markdown('### Previsão de Odds Futuras')

if current_display_time == 0:
    predictions_placeholder.warning('Não é possível prever a odd futura com o tempo atual em 0. Por favor, insira um tempo maior que 0.')
else:
    odd_predictions_df = predict_odds(current_odd, current_display_time, extra_time_ht, extra_time_ft, period_selection, include_extra_time)
    if not odd_predictions_df.empty:
        # Certificar-se de que a coluna 'Odd Prevista' é numérica antes de aplicar estilos
        # A conversão para numérico deve ser feita aqui, antes de passar para as funções de estilo
        odd_predictions_df['Odd Prevista'] = pd.to_numeric(odd_predictions_df['Odd Prevista'], errors='coerce')
        styled_df = odd_predictions_df.style.apply(highlight_every_5_minutes, axis=1).apply(highlight_odds_ranges, axis=None)
        # Formatar 'Odd Prevista' para 2 casas decimais APÓS a estilização
        styled_df = styled_df.format({'Odd Prevista': "{:.2f}"})
        predictions_placeholder.dataframe(styled_df, width='stretch')
    else:
        predictions_placeholder.info('Não foi possível gerar previsões de odds futuras com os parâmetros fornecidos (tempo atual >= tempo alvo).')

# Simulation loop
if st.session_state.simulation_running:
    # Determine simulation end time
    if period_selection == '1º Tempo':
        simulation_end_time = 45 + (extra_time_ht if include_extra_time else 0)
    else:
        simulation_end_time = 90 + (extra_time_ft if include_extra_time else 0)

    # Ensure simulation doesn't go past actual game end + FT extra time
    max_game_time = 90 + extra_time_ft # Use the FT extra time for overall max
    if simulation_end_time > max_game_time:
        simulation_end_time = max_game_time

    while st.session_state.simulated_time < simulation_end_time and st.session_state.simulation_running:
        st.session_state.simulated_time += 1
        # Update the displayed simulated time in the sidebar
        simulated_time_display.metric(label="Tempo Simulado", value=f"{st.session_state.simulated_time} min")
        # Rerun the app to update display
        time.sleep(60) # Simulate 1 minute real time for 1 minute game time
        st.rerun() 

    if st.session_state.simulated_time >= simulation_end_time:
        st.session_state.simulation_running = False
        st.sidebar.write('Simulação concluída.')

st.markdown('--- ')
st.markdown('**Observação**: Esta calculadora ajuda a prever odds regressivas no mercado de under limite, considerando também os acréscimos dados pelo árbitro no primeiro tempo (HT) e no segundo tempo (FT).')
