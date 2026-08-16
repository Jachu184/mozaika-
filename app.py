import streamlit as st
import numpy as np

st.set_page_config(page_title="Mozaika 10x42", layout="centered")

ROWS, COLS = 42, 10
TOTAL_BLACK = 110

# 1. Tworzenie stałej siatki początkowej
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

st.title("🧩 Mozaika 10x42")

# 2. Wygenerowanie interaktywnego komponentu z automatycznym dopasowaniem wysokości
grid_list = st.session_state.grid.tolist()

html_app = f"""
<!DOCTYPE html>
<html>
<head>
<style>
    html, body {{
        margin: 0;
        padding: 0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        color: white;
        background-color: transparent;
        overflow: hidden;
    }}
    .stats-container {{
        display: flex;
        justify-content: space-around;
        background-color: #1e1e1e;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 15px;
        border: 1px solid #333;
    }}
    .stat-box {{
        text-align: center;
    }}
    .stat-title {{
        font-size: 14px;
        color: #aaa;
        margin-bottom: 4px;
    }}
    .stat-value {{
        font-size: 20px;
        font-weight: bold;
    }}
    .mosaic-grid {{
        display: grid;
        grid-template-columns: repeat({COLS}, 1fr);
        width: 100%;
        max-width: 360px;
        margin: 0 auto 20px auto;
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

<div id="wrapper">
    <div class="stats-container">
        <div class="stat-box">
            <div class="stat-title">⬛ Czarne kwadraty</div>
            <div class="stat-value" id="black-count">110 / 110</div>
        </div>
        <div class="stat-box">
            <div class="stat-title">⬜ Białe kwadraty</div>
            <div class="stat-value" id="white-count">310 / 310</div>
        </div>
    </div>

    <div class="mosaic-grid" id="grid"></div>
</div>

<script>
    const gridData = {grid_list};
    const container = document.getElementById('grid');
    const blackCountEl = document.getElementById('black-count');
    const whiteCountEl = document.getElementById('white-count');

    let currentBlack = 0;
    const totalSquares = {ROWS * COLS};

    gridData.forEach(row => {{
        row.forEach(val => {{
            if (val === 1) currentBlack++;
        }});
    }});

    function updateStats() {{
        blackCountEl.innerText = currentBlack + ' / 110';
        whiteCountEl.innerText = (totalSquares - currentBlack) + ' / 310';
    }}

    updateStats();

    gridData.forEach((row, r) => {{
        row.forEach((val, c) => {{
            const sq = document.createElement('div');
            sq.className = 'square ' + (val === 1 ? 'black' : 'white');
            
            sq.addEventListener('click', () => {{
                if (sq.classList.contains('black')) {{
                    sq.className = 'square white';
                    currentBlack--;
                }} else {{
                    sq.className = 'square black';
                    currentBlack++;
                }}
                updateStats();
            }});

            container.appendChild(sq);
        }});
    }});

    // Automatyczne przekazanie wysokości ramki do Streamlit
    function sendHeight() {{
        const height = document.getElementById('wrapper').scrollHeight + 30;
        window.parent.postMessage({{
            isStreamlit: true,
            type: "streamlit:setFrameHeight",
            height: height
        }}, "*");
    }}

    window.addEventListener('load', sendHeight);
    window.addEventListener('resize', sendHeight);
    setTimeout(sendHeight, 500);
</script>

</body>
</html>
"""

# Zwiększony sztywny bufor wysokości dla urządzeń mobilnych
st.components.v1.html(html_app, height=1800, scrolling=False)
