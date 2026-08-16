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

# 2. Przechwycenie kliknięcia z komunikatu JavaScript
if "last_clicked" in st.session_state and st.session_state.last_clicked:
    r, c = st.session_state.last_clicked
    st.session_state.grid[r, c] = 1 - st.session_state.grid[r, c]
    st.session_state.last_clicked = None

st.title("🧩 Mozaika 10x42")

current_black = int(np.sum(st.session_state.grid))
current_white = (ROWS * COLS) - current_black

col1, col2 = st.columns(2)
col1.metric("⬛ Czarne", f"{current_black} / 110")
col2.metric("⬜ Białe", f"{current_white} / 310")

st.divider()

# 3. Wygenerowanie siatki w czystym HTML/CSS z natywną obsługą dotyku
grid_data = st.session_state.grid.tolist()

html_code = f"""
<!DOCTYPE html>
<html>
<head>
<style>
    body {{
        margin: 0;
        padding: 0;
        display: flex;
        justify-content: center;
        background-color: transparent;
        user-select: none;
    }}
    .grid-container {{
        display: grid;
        grid-template-columns: repeat({COLS}, 1fr);
        width: 100%;
        max-width: 360px;
        border: 2px solid #333;
        background-color: #777;
        gap: 1px;
    }}
    .cell {{
        width: 100%;
        padding-top: 100%; /* Wymuszenie idealnego kwadratu */
        position: relative;
        cursor: pointer;
    }}
    .cell-inner {{
        position: absolute;
        top: 0; left: 0; bottom: 0; right: 0;
    }}
    .black {{ background-color: #000000; }}
    .white {{ background-color: #ffffff; }}
</style>
</head>
<body>

<div class="grid-container" id="mosaic">
</div>

<script>
    const gridData = {grid_data};
    const container = document.getElementById('mosaic');

    gridData.forEach((row, rIdx) => {{
        row.forEach((val, cIdx) => {{
            const cell = document.createElement('div');
            cell.className = 'cell';
            
            const inner = document.createElement('div');
            inner.className = 'cell-inner ' + (val === 1 ? 'black' : 'white');
            cell.appendChild(inner);

            // Obsługa kliknięcia/dotknięcia palcem
            cell.addEventListener('click', () => {{
                // Wysyłamy informację do Streamlita
                window.parent.postMessage({{
                    type: 'streamlit:setComponentValue',
                    value: [rIdx, cIdx]
                }}, '*');
            }});

            container.appendChild(cell);
        }});
    }});
</script>

</body>
</html>
"""

# Renderowanie interaktywnej mozaiki
component_value = st.components.v1.html(html_code, height=1350)

# Jeśli kliknięto w pole, zapisz dane i odśwież
if component_value:
    st.session_state.last_clicked = component_value
    st.rerun()
        
