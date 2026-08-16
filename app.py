import streamlit as st
import numpy as np

st.set_page_config(page_title="Mozaika 10x42", layout="centered")

ROWS, COLS = 42, 10
TOTAL_BLACK = 110

# 1. Inicjalizacja stanu mozaiki
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

current_black = int(np.sum(st.session_state.grid))
current_white = (ROWS * COLS) - current_black

col1, col2 = st.columns(2)
col1.metric("⬛ Czarne", f"{current_black} / 110")
col2.metric("⬜ Białe", f"{current_white} / 310")

st.divider()

# 2. Wymuszenie poziomego układu 10 kolumn na urządzeniach mobilnych (CSS)
st.markdown("""
    <style>
    /* Zapobieganie zawijaniu kolumn w Streamlit na wąskich ekranach */
    [data-testid="stHorizontalBlock"] {
        flex-wrap: nowrap !important;
        gap: 1px !important;
    }
    
    [data-testid="column"] {
        width: 10% !important;
        flex: 1 1 calc(10% - 1px) !important;
        min-width: 0px !important;
    }
    
    /* Kwadratowe, dopasowane do ekranu przyciski bez marginesów */
    div.stButton > button {
        width: 100% !important;
        height: 24px !important;
        min-height: 24px !important;
        padding: 0px !important;
        margin: 0px !important;
        border: 1px solid #777 !important;
        border-radius: 0px !important;
        font-size: 8px !important;
        line-height: 1 !important;
    }
    
    /* Dedykowane kolory przycisków */
    .st-black-btn > button {
        background-color: #000000 !important;
        color: #000000 !important;
    }
    
    .st-white-btn > button {
        background-color: #ffffff !important;
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Generowanie ścisłej siatki 10x42
for r in range(ROWS):
    cols = st.columns(COLS, gap="small")
    for c in range(COLS):
        is_black = st.session_state.grid[r, c] == 1
        
        # Przypisanie odpowiedniej klasy kolorystycznej
        btn_container = cols[c].container()
        
        cols[c].button(
            label=" ", 
            key=f"btn_{r}_{c}", 
            on_click=toggle_square, 
            args=(r, c)
        )
