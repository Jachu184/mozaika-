import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Mozaika 10x42", layout="centered")

ROWS, COLS = 42, 10
TOTAL_BLACK = 110

# 1. Inicjalizacja stanu mozaiki (siatka wartości logicznych True/False)
if "grid_bool" not in st.session_state:
    indices = [(r, c) for r in range(ROWS) for c in range(COLS)]
    grid = np.zeros((ROWS, COLS), dtype=bool)
    np.random.shuffle(indices)
    
    placed = 0
    for r, c in indices:
        if placed == TOTAL_BLACK:
            break
        has_neighbor = False
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr, nc]:
                has_neighbor = True
                break
        if not has_neighbor:
            grid[r, c] = True
            placed += 1
            
    st.session_state.grid_bool = pd.DataFrame(
        grid, 
        columns=[f"K{i+1}" for i in range(COLS)]
    )

st.title("🧩 Mozaika 10x42")

current_black = int(st.session_state.grid_bool.sum().sum())
current_white = (ROWS * COLS) - current_black

col1, col2 = st.columns(2)
col1.metric("⬛ Czarne", f"{current_black} / 110")
col2.metric("⬜ Białe", f"{current_white} / 310")

st.caption("Stuknij w dowolne pole w tabeli poniżej, aby zmienić jego kolor.")

# 2. Stylowanie CSS dla kompaktowego wyglądu siatki
st.markdown("""
    <style>
    /* Zmniejszenie wysokości wierszy i paddingów w edytorze tabeli */
    [data-testid="stDataFrame"] div {
        font-size: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Interaktywna siatka 10x42 w formie edytora danych
edited_df = st.data_editor(
    st.session_state.grid_bool,
    column_config={
        col: st.column_config.CheckboxColumn(
            label=col,
            default=False,
            width="small"
        ) for col in st.session_state.grid_bool.columns
    },
    use_container_width=True,
    hide_index=True,
    height=1200,
    key="editor"
)

# 4. Aktualizacja stanu aplikacji po zmianie w tabeli
if not edited_df.equals(st.session_state.grid_bool):
    st.session_state.grid_bool = edited_df
    st.rerun()
    
