import streamlit as st
import numpy as np

st.set_page_config(page_title="Interaktywna Mozaika", layout="centered")

ROWS, COLS = 42, 10
TOTAL_BLACK = 110

# Inicjalizacja stanu mozaiki przy pierwszym uruchomieniu
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

def toggle_square(r, c):
    st.session_state.grid[r, c] = 1 - st.session_state.grid[r, c]

st.title("🧩 Mozaika 10x42")
st.write("Kliknij w kwadrat, aby zmienić jego kolor.")

current_black = int(np.sum(st.session_state.grid))
current_white = (ROWS * COLS) - current_black

col1, col2 = st.columns(2)
col1.metric("⬛ Czarne", f"{current_black} / 110")
col2.metric("⬜ Białe", f"{current_white} / 310")

st.divider()

# CSS dla ładnego wyglądu przycisków na telefonie
st.markdown("""
    <style>
    div.stButton > button {
        width: 100% !important;
        height: 26px !important;
        padding: 0px !important;
        margin: 0px !important;
        border: 1px solid #777 !important;
        border-radius: 2px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Wyświetlanie siatki
for r in range(ROWS):
    cols = st.columns(COLS, gap="small")
    for c in range(COLS):
        is_black = st.session_state.grid[r, c] == 1
        # Emojis reprezentujące kolor w nagłówku lub wyglądzie
        cols[c].button(
            label="⬛" if is_black else "⬜", 
            key=f"btn_{r}_{c}", 
            on_click=toggle_square, 
            args=(r, c)
      )
      
