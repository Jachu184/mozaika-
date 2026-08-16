import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Mozaika 10x42", layout="centered")

ROWS, COLS = 42, 10
TOTAL_BLACK = 110

# 1. Inicjalizacja stanu mozaiki (0 = biały ⬜, 1 = czarny ⬛)
if "grid_array" not in st.session_state:
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
            
    st.session_state.grid_array = grid

st.title("🧩 Mozaika 10x42")

current_black = int(np.sum(st.session_state.grid_array))
current_white = (ROWS * COLS) - current_black

col1, col2 = st.columns(2)
col1.metric("⬛ Czarne", f"{current_black} / 110")
col2.metric("⬜ Białe", f"{current_white} / 310")

st.caption("Wybierz opcję z listy w komórce, aby zmienić jej kolor (⬛/⬜).")

# 2. Przygotowanie danych do wyświetlenia jako znaki
display_grid = np.where(st.session_state.grid_array == 1, "⬛", "⬜")
df_display = pd.DataFrame(display_grid, columns=[f"C{i+1}" for i in range(COLS)])

# 3. CSS zmniejszający komórki, by 10 kolumn idealnie weszło na ekran telefonu
st.markdown("""
    <style>
    /* Wymuszenie wąskich kolumn w tabeli */
    [data-testid="stDataFrame"] div[role="gridcell"] {
        padding: 0px !important;
        font-size: 14px !important;
        text-align: center !important;
    }
    [data-testid="stDataFrame"] {
        width: 100% !important;
    }
    </style>
""", unsafe_allow_html=True)

# 4. Edytowalna tabela ze składką wyboru koloru
column_config = {
    col: st.column_config.SelectboxColumn(
        label=col,
        options=["⬛", "⬜"],
        required=True,
        width="small"
    ) for col in df_display.columns
}

edited_df = st.data_editor(
    df_display,
    column_config=column_config,
    use_container_width=True,
    hide_index=True,
    height=1200,
    key="emoji_editor"
)

# 5. Aktualizacja stanu aplikacji
new_grid = np.where(edited_df.to_numpy() == "⬛", 1, 0)
if not np.array_equal(new_grid, st.session_state.grid_array):
    st.session_state.grid_array = new_grid
    st.rerun()
        
