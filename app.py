import streamlit as st
import numpy as np

st.set_page_config(page_title="Mozaika 10x42", layout="centered")

ROWS, COLS = 42, 10
TOTAL_BLACK = 110

# 1. Tworzenie stałej siatki początkowej (tylko raz)
if "grid" not in st.session_state:
    np.random.seed(42)
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

# 2. Aktualizacja macierzy, jeśli przyszła zmiana z JS
if "last_toggle" in st.session_state and st.session_state.last_toggle:
    r, c = st.session_state.last_toggle
    st.session_state.grid[r, c] = 1 - st.session_state.grid[r, c]
    st.session_state.last_toggle = None

st.title("🧩 Mozaika 10x42")

current_black = int(np.sum(st.session_state.grid))
current_white = (ROWS * COLS) - current_black

col1, col2 = st.columns(2)
col1.metric("⬛ Czarne", f"{current_black} / 110")
col2.metric("⬜ Białe", f"{current_white} / 310")

st.divider()

# 3. Interaktywna aplikacja w czystym HTML/JS (bez przekierowań w URL)
grid_list = st.session_state.grid.tolist()

html_app = f"""
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
    }}
    .mosaic-grid {{
        display: grid;
        grid-template-columns: repeat({COLS}, 1fr);
        width: 100%;
        max-width: 360px;
        background-color: #777777;
        gap: 1px;
        border: 2px solid #333333;
    }}
    .square {{
        width: 100%;
        aspect-ratio: 1 / 1;
        box-sizing: border-box;
        cursor: pointer;
        -webkit-tap-highlight-color: transparent;
    }}
    .black {{ background-color: #000000; }}
    .white {{ background-color: #ffffff; }}
</style>
</head>
<body>

<div class="mosaic-grid" id="grid"></div>

<script>
    const gridData = {grid_list};
    const container = document.getElementById('grid');

    gridData.forEach((row, r) => {{
        row.forEach((val, c) => {{
            const sq = document.createElement('div');
            sq.className = 'square ' + (val === 1 ? 'black' : 'white');
            
            sq.addEventListener('click', () => {{
                // Natychmiastowa zmiana koloru wizualnie na ekranie
                if (sq.classList.contains('black')) {{
                    sq.className = 'square white';
                }} else {{
                    sq.className = 'square black';
                }}
                
                // Przekazanie bezpiecznej informacji do Pythona bez zmieniania URL
                window.parent.postMessage({{
                    isStreamlit: true,
                    type: "streamlit:setComponentValue",
                    value: [r, c]
                }}, "*");
            }});

            container.appendChild(sq);
        }});
    }});
</script>

</body>
</html>
"""

# Renderowanie komponentu
clicked = st.components.v1.html(html_app, height=1350)

# Jeśli kliknięto w pole, zapisujemy zmianę i przeliczamy statystyki
if clicked and isinstance(clicked, list) and len(clicked) == 2:
    st.session_state.last_toggle = clicked
    st.rerun()
