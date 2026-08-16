import streamlit as st
import numpy as np
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events

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

st.title("🧩 Mozaika 10x42")

current_black = int(np.sum(st.session_state.grid))
current_white = (ROWS * COLS) - current_black

col1, col2 = st.columns(2)
col1.metric("⬛ Czarne", f"{current_black} / 110")
col2.metric("⬜ Białe", f"{current_white} / 310")

st.divider()

# 2. Przygotowanie danych do rysowania siatki
x_coords = []
y_coords = []
colors = []
row_idx = []
col_idx = []

for r in range(ROWS):
    for c in range(COLS):
        # Bokeh rysuje od dołu do góry, więc odwracamy wiersze
        x_coords.append(c + 0.5)
        y_coords.append((ROWS - 1 - r) + 0.5)
        colors.append("#000000" if st.session_state.grid[r, c] == 1 else "#ffffff")
        row_idx.append(r)
        col_idx.append(c)

source = ColumnDataSource(data=dict(
    x=x_coords,
    y=y_coords,
    color=colors,
    row=row_idx,
    col=col_idx
))

# 3. Tworzenie płótna i rysowanie dokładnie identycznego obrazka
p = figure(
    x_range=(0, COLS),
    y_range=(0, ROWS),
    tools="tap",
    toolbar_location=None,
    width=320,
    height=1300,
    match_aspect=True
)

rects = p.rect(
    x='x', y='y', width=0.98, height=0.98,
    fill_color='color', line_color='#777777', line_width=1,
    source=source
)

# Skrypt przechwytujący kliknięcie na telefonie
source.selected.js_on_change('indices', CustomJS(args=dict(source=source), code="""
    const inds = cb_obj.indices;
    if (inds.length == 0) return;
    const idx = inds[0];
    const r = source.data['row'][idx];
    const c = source.data['col'][idx];
    document.dispatchEvent(new CustomEvent("SQUARE_CLICKED", {detail: {row: r, col: c}}));
"""))

p.axis.visible = False
p.grid.grid_line_color = None

# 4. Obsługa kliknięcia w Streamlit
result = streamlit_bokeh_events(
    p,
    events="SQUARE_CLICKED",
    key="bokeh_grid",
    refresh_on_update=False
)

if result and "SQUARE_CLICKED" in result:
    data = result.get("SQUARE_CLICKED")
    r, c = data["row"], data["col"]
    st.session_state.grid[r, c] = 1 - st.session_state.grid[r, c]
    st.rerun()
