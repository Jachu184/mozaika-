import streamlit as st
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Mozaika 10x42", layout="centered")

ROWS, COLS = 42, 10
TOTAL_BLACK = 110

# 1. Inicjalizacja stanu mozaiki (rozproszona siatka)
if "grid" not in st.session_state:
    indices = [(r, c) for r in range(ROWS) for c in range(COLS)]
    grid = np.zeros((ROWS, COLS), dtype=int)
    np.random.shuffle(indices)
    
    placed = 0
    for r, c in indices:
        if placed == TOTAL_BLACK:
            break
        has_neighbor = False
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr, nc] == 1:
                has_neighbor = True
                break
        if not has_neighbor:
            grid[r, c] = 1
            placed += 1
            
    st.session_state.grid = grid

st.title("🧩 Mozaika 10x42")

current_black = int(np.sum(st.session_state.grid))
current_white = (ROWS * COLS) - current_black

col1, col2 = st.columns(2)
col1.metric("⬛ Czarne", f"{current_black} / 110")
col2.metric("⬜ Białe", f"{current_white} / 310")

st.divider()

# 2. Tworzenie interaktywnej mozaiki Plotly
fig = px.imshow(
    st.session_state.grid,
    color_continuous_scale=[[0, 'white'], [1, 'black']],
    aspect="equal"
)

# Ukrywanie osi, dodanie siatki oddzielającej kwadraty
fig.update_xaxes(showticklabels=False, showgrid=True, gridwidth=1, gridcolor='gray', dtick=1)
fig.update_yaxes(showticklabels=False, showgrid=True, gridwidth=1, gridcolor='gray', dtick=1)

fig.update_layout(
    coloraxis_showscale=False,
    margin=dict(l=5, r=5, t=5, b=5),
    height=1100,
    dragmode=False
)

# 3. Wyświetlenie obrazu i przechwycenie kliknięcia na telefonie
selected_point = st.plotly_chart(
    fig, 
    use_container_width=True, 
    on_select="rerun", 
    selection_mode="points"
)

# 4. Obsługa zmiany koloru po kliknięciu
if selected_point and "selection" in selected_point and "points" in selected_point["selection"]:
    points = selected_point["selection"]["points"]
    if len(points) > 0:
        pt = points[0]
        r, c = pt["y"], pt["x"]
        
        # Zmiana stanu wybranego pola
        st.session_state.grid[r, c] = 1 - st.session_state.grid[r, c]
        st.rerun()
