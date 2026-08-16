import streamlit as st
import numpy as np

st.set_page_config(page_title="Mozaika 10x42", layout="centered")

ROWS, COLS = 42, 10
TOTAL_BLACK = 110

# 1. Inicjalizacja stanu mozaiki (stały Seed gwarantuje jednorazowe wygenerowanie)
if "grid" not in st.session_state:
    np.random.seed(42)  # Zapewnia stały układ początkowy
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

# 2. Zmiana koloru wybranego pola po kliknięciu
if "cell" in st.query_params:
    try:
        r, c = map(int, st.query_params["cell"].split("_"))
        st.session_state.grid[r, c] = 1 - st.session_state.grid[r, c]
    except Exception:
        pass
    st.query_params.clear()
    st.rerun()

# Statystyki
current_black = int(np.sum(st.session_state.grid))
current_white = (ROWS * COLS) - current_black

st.markdown(f"### 🧩 Mozaika 10x42 | ⬛ {current_black} / 110 | ⬜ {current_white}")

# 3. Wygenerowanie siatki jako czysty obraz HTML/CSS
grid_flat = st.session_state.grid.flatten()
cells_html = ""

for idx, val in enumerate(grid_flat):
    r = idx // COLS
    c = idx % COLS
    bg_color = "#000000" if val == 1 else "#ffffff"
    cells_html += f'<a href="?cell={r}_{c}" target="_self" class="square" style="background-color: {bg_color};"></a>'

full_html = f"""
<style>
    .block-container {{
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
    }}
    
    .mosaic-grid {{
        display: grid;
        grid-template-columns: repeat(10, 1fr);
        width: 100%;
        max-width: 360px;
        margin: 0 auto;
        background-color: #888888;
        gap: 1px;
        border: 2px solid #333333;
    }}
    
    .square {{
        display: block;
        width: 100%;
        aspect-ratio: 1 / 1;
        box-sizing: border-box;
        -webkit-tap-highlight-color: transparent;
    }}
</style>

<div class="mosaic-grid">
    {cells_html}
</div>
"""

st.markdown(full_html, unsafe_allow_html=True)
        
