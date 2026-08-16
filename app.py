import streamlit as st
import numpy as np

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

# Zmiana koloru pola
if "click_event" in st.session_state and st.session_state.click_event:
    try:
        r, c = map(int, st.session_state.click_event.split("_"))
        st.session_state.grid[r, c] = 1 - st.session_state.grid[r, c]
        st.session_state.click_event = None
    except:
        pass

st.title("🧩 Mozaika 10x42")

current_black = int(np.sum(st.session_state.grid))
current_white = (ROWS * COLS) - current_black

col1, col2 = st.columns(2)
col1.metric("⬛ Czarne", f"{current_black} / 110")
col2.metric("⬜ Białe", f"{current_white} / 310")

st.divider()

# 2. Generowanie obrazu mozaiki jako interaktywnej siatki SVG
cell_size = 30
width = COLS * cell_size
height = ROWS * cell_size

svg_cells = []
for r in range(ROWS):
    for c in range(COLS):
        color = "#000000" if st.session_state.grid[r, c] == 1 else "#ffffff"
        x = c * cell_size
        y = r * cell_size
        svg_cells.append(
            f'<rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" '
            f'fill="{color}" stroke="#777777" stroke-width="1" '
            f'onclick="window.parent.postMessage({{type: \'streamlit:setComponentValue\', value: \'{r}_{c}\'}}, \'*\')" '
            f'style="cursor: pointer;"/>'
        )

svg_code = f'''
<div style="display: flex; justify-content: center; width: 100%;">
    <svg width="100%" viewBox="0 0 {width} {height}" style="max-width: 350px; height: auto; border: 2px solid #333;">
        {"".join(svg_cells)}
    </svg>
</div>
'''

# 3. Wyświetlenie siatki dokładnie jak na grafice
st.components.v1.html(
    f'''
    <div id="svg-container">
        {svg_code}
    </div>
    <script>
    const rects = document.querySelectorAll('rect');
    rects.forEach(rect => {{
        rect.addEventListener('click', (e) => {{
            const id = e.target.getAttribute('onclick').match(/'([^']+)'/)[1];
            window.parent.postMessage({{
                isStreamlit: true,
                type: "streamlit:setComponentValue",
                value: id
            }}, "*");
        }});
    }});
    </script>
    ''',
    height=1300
    )
