"""
main.py — Streamlit Workflow Demo
==================================
This file demonstrates key Streamlit concepts:
  • Page config & layout
  • Widgets (sliders, selects, checkboxes, inputs)
  • Native Streamlit charts  (line, bar, area)
  • Matplotlib figures embedded with st.pyplot()
  • Plotly interactive charts embedded with st.plotly_chart()
  • Sidebar controls
  • Columns & expanders
  • Metrics & dataframes

Run with:  streamlit run main.py
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ── Page configuration (must be first Streamlit call) ──────────────────────
st.set_page_config(
    page_title="Streamlit Charts Demo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS for a slightly polished look ─────────────────────────────────
st.markdown(
    """
    <style>
    /* Gradient header */
    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6C63FF, #48CAE4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .hero-sub {
        color: #888;
        font-size: 1rem;
        margin-top: 0.2rem;
    }
    section[data-testid="stSidebar"] {
        background: #0f0f1a;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Hero header ─────────────────────────────────────────────────────────────
st.markdown('<p class="hero-title">📊 Streamlit Charts Demo</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-sub">Explore native charts, Matplotlib figures, and interactive Plotly graphs — all in one app.</p>',
    unsafe_allow_html=True,
)
st.divider()

# ════════════════════════════════════════════════════════════════════════════
# SIDEBAR — Global controls
# ════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.title("⚙️ Controls")
    st.markdown("Adjust settings that affect every chart below.")

    n_points = st.slider("Number of data points", min_value=20, max_value=500, value=100, step=10)
    noise_level = st.slider("Noise level", min_value=0.0, max_value=5.0, value=1.0, step=0.1)
    color_theme = st.selectbox(
        "Plotly colour theme",
        ["plotly", "plotly_dark", "ggplot2", "seaborn", "simple_white"],
        index=1,
    )
    show_raw_data = st.checkbox("Show raw dataframes", value=False)
    st.divider()
    st.info("This app is a self-contained Streamlit workflow demo.")

# ════════════════════════════════════════════════════════════════════════════
# DATA GENERATION (shared across sections)
# ════════════════════════════════════════════════════════════════════════════
np.random.seed(42)
x = np.linspace(0, 4 * np.pi, n_points)
y_sin = np.sin(x) + np.random.normal(0, noise_level * 0.1, n_points)
y_cos = np.cos(x) + np.random.normal(0, noise_level * 0.1, n_points)
y_tan_clipped = np.clip(np.tan(x / 2), -3, 3) + np.random.normal(0, noise_level * 0.05, n_points)

df_waves = pd.DataFrame({"x": x, "sin": y_sin, "cos": y_cos, "tan(clipped)": y_tan_clipped})

categories = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
sales_A = np.random.randint(50, 200, size=7)
sales_B = np.random.randint(30, 180, size=7)
df_sales = pd.DataFrame({"Day": categories, "Product A": sales_A, "Product B": sales_B})

scatter_x = np.random.randn(n_points)
scatter_y = scatter_x * 1.5 + np.random.normal(0, noise_level * 0.5, n_points)
scatter_size = np.abs(scatter_y) * 10 + 5
scatter_color = scatter_x  # colour mapped to x value

# ════════════════════════════════════════════════════════════════════════════
# SECTION 1 — Native Streamlit Charts
# ════════════════════════════════════════════════════════════════════════════
st.header("1 · Native Streamlit Charts")
st.markdown(
    "Streamlit provides lightweight wrappers around Vega-Altair for quick "
    "charts that need zero configuration."
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Line Chart — Wave Functions")
    st.line_chart(df_waves.set_index("x")[["sin", "cos", "tan(clipped)"]])

with col2:
    st.subheader("📊 Bar Chart — Weekly Sales")
    st.bar_chart(df_sales.set_index("Day"))

st.subheader("🌊 Area Chart — Cumulative Random Walk")
random_walk = pd.DataFrame(
    np.cumsum(np.random.randn(n_points, 3), axis=0),
    columns=["Asset A", "Asset B", "Asset C"],
)
st.area_chart(random_walk)

if show_raw_data:
    with st.expander("📄 Raw wave data"):
        st.dataframe(df_waves.head(20), use_container_width=True)

st.divider()

# ════════════════════════════════════════════════════════════════════════════
# SECTION 2 — Matplotlib Charts
# ════════════════════════════════════════════════════════════════════════════
st.header("2 · Matplotlib Charts")
st.markdown("Embed any `matplotlib` figure with `st.pyplot(fig)`.")

col3, col4 = st.columns(2)

# 2a — Scatter plot with colour map
with col3:
    st.subheader("🎨 Scatter Plot (Matplotlib)")
    fig1, ax1 = plt.subplots(figsize=(6, 4), facecolor="#0e1117")
    ax1.set_facecolor("#0e1117")
    scatter = ax1.scatter(
        scatter_x,
        scatter_y,
        c=scatter_color,
        cmap="plasma",
        s=scatter_size,
        alpha=0.8,
        edgecolors="none",
    )
    cbar = fig1.colorbar(scatter, ax=ax1)
    cbar.ax.yaxis.label.set_color("white")
    cbar.ax.tick_params(colors="white")
    ax1.set_title("Scatter — coloured by X value", color="white", fontsize=11)
    ax1.set_xlabel("X", color="white")
    ax1.set_ylabel("Y", color="white")
    ax1.tick_params(colors="white")
    for spine in ax1.spines.values():
        spine.set_edgecolor("#444")
    st.pyplot(fig1, use_container_width=True)
    plt.close(fig1)

# 2b — Histogram
with col4:
    st.subheader("📉 Histogram (Matplotlib)")
    fig2, ax2 = plt.subplots(figsize=(6, 4), facecolor="#0e1117")
    ax2.set_facecolor("#0e1117")
    ax2.hist(scatter_y, bins=25, color="#6C63FF", edgecolor="#0e1117", alpha=0.9)
    ax2.set_title("Distribution of Y values", color="white", fontsize=11)
    ax2.set_xlabel("Y", color="white")
    ax2.set_ylabel("Count", color="white")
    ax2.tick_params(colors="white")
    for spine in ax2.spines.values():
        spine.set_edgecolor("#444")
    st.pyplot(fig2, use_container_width=True)
    plt.close(fig2)

# 2c — Subplots grid
st.subheader("🔢 Multi-panel Figure (Matplotlib subplots)")
fig3, axes = plt.subplots(1, 3, figsize=(14, 3.5), facecolor="#0e1117")
wave_data = [("sin", y_sin, "#48CAE4"), ("cos", y_cos, "#6C63FF"), ("tan(clipped)", y_tan_clipped, "#FF6B6B")]
for ax, (label, data, color) in zip(axes, wave_data):
    ax.set_facecolor("#0e1117")
    ax.plot(x, data, color=color, linewidth=1.5)
    ax.fill_between(x, data, alpha=0.15, color=color)
    ax.set_title(label, color="white", fontsize=10)
    ax.tick_params(colors="white")
    for spine in ax.spines.values():
        spine.set_edgecolor("#333")
fig3.tight_layout()
st.pyplot(fig3, use_container_width=True)
plt.close(fig3)

st.divider()

# ════════════════════════════════════════════════════════════════════════════
# SECTION 3 — Interactive Plotly Charts
# ════════════════════════════════════════════════════════════════════════════
st.header("3 · Interactive Plotly Charts")
st.markdown("Use `st.plotly_chart()` for fully interactive, zoomable, pannable figures.")

col5, col6 = st.columns(2)

# 3a — Animated scatter / bubble chart
with col5:
    st.subheader("🫧 Bubble Chart")
    fig_bubble = px.scatter(
        x=scatter_x,
        y=scatter_y,
        size=scatter_size,
        color=scatter_color,
        color_continuous_scale="Plasma",
        template=color_theme,
        labels={"x": "X", "y": "Y", "color": "X value", "size": "Size"},
        title="Bubble chart — size & colour encoded",
    )
    fig_bubble.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig_bubble, use_container_width=True)

# 3b — Grouped bar chart
with col6:
    st.subheader("📊 Grouped Bar Chart")
    fig_bar = px.bar(
        df_sales.melt(id_vars="Day", var_name="Product", value_name="Sales"),
        x="Day",
        y="Sales",
        color="Product",
        barmode="group",
        template=color_theme,
        title="Weekly Sales by Product",
        color_discrete_sequence=["#6C63FF", "#48CAE4"],
    )
    fig_bar.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig_bar, use_container_width=True)

# 3c — Heatmap (correlation matrix)
st.subheader("🌡️ Correlation Heatmap")
heatmap_data = pd.DataFrame(np.random.randn(n_points, 5), columns=["Alpha", "Beta", "Gamma", "Delta", "Epsilon"])
corr_matrix = heatmap_data.corr()
fig_heat = px.imshow(
    corr_matrix,
    text_auto=".2f",
    color_continuous_scale="RdBu_r",
    template=color_theme,
    title="Correlation Matrix (random data)",
    zmin=-1,
    zmax=1,
)
fig_heat.update_layout(margin=dict(l=20, r=20, t=50, b=20))
st.plotly_chart(fig_heat, use_container_width=True)

# 3d — 3-D surface
st.subheader("🏔️ 3-D Surface Plot")
grid_size = 40
gx = np.linspace(-3, 3, grid_size)
gy = np.linspace(-3, 3, grid_size)
GX, GY = np.meshgrid(gx, gy)
GZ = np.sin(np.sqrt(GX**2 + GY**2)) * np.exp(-0.1 * (GX**2 + GY**2))

fig_3d = go.Figure(
    data=[go.Surface(z=GZ, x=GX, y=GY, colorscale="Viridis", showscale=True)]
)
fig_3d.update_layout(
    title="sin(r) · e^(-0.1r²) — 3-D Surface",
    scene=dict(
        xaxis_title="X",
        yaxis_title="Y",
        zaxis_title="Z",
        bgcolor="rgba(0,0,0,0)",
    ),
    template=color_theme,
    margin=dict(l=0, r=0, t=50, b=0),
    height=500,
)
st.plotly_chart(fig_3d, use_container_width=True)

st.divider()

# ════════════════════════════════════════════════════════════════════════════
# SECTION 4 — Metrics & KPIs
# ════════════════════════════════════════════════════════════════════════════
st.header("4 · Metrics")
st.markdown("Use `st.metric()` to display KPI cards with optional delta indicators.")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Sales A", f"{sales_A.sum():,}", delta=int(sales_A[-1] - sales_A[-2]))
m2.metric("Total Sales B", f"{sales_B.sum():,}", delta=int(sales_B[-1] - sales_B[-2]))
m3.metric("Mean sin(x)", f"{y_sin.mean():.4f}", delta=f"{y_sin.std():.4f} σ")
m4.metric("Data Points", n_points, delta=n_points - 100)

st.divider()

# ════════════════════════════════════════════════════════════════════════════
# SECTION 5 — Streamlit Workflow Cheatsheet
# ════════════════════════════════════════════════════════════════════════════
st.header("5 · Streamlit Workflow Cheatsheet")
with st.expander("📖 Click to expand the quick reference"):
    st.markdown(
        """
| Feature | Code |
|---------|------|
| Text | `st.write()`, `st.markdown()`, `st.title()` |
| Input widgets | `st.slider()`, `st.selectbox()`, `st.text_input()` |
| Layouts | `st.columns()`, `st.tabs()`, `st.expander()` |
| Native charts | `st.line_chart()`, `st.bar_chart()`, `st.area_chart()` |
| Matplotlib | `st.pyplot(fig)` |
| Plotly | `st.plotly_chart(fig)` |
| DataFrames | `st.dataframe(df)`, `st.table(df)` |
| Metrics | `st.metric(label, value, delta)` |
| Sidebar | `with st.sidebar: ...` |
| Status | `st.spinner()`, `st.success()`, `st.error()` |
| Caching | `@st.cache_data`, `@st.cache_resource` |

> **Run the app:** `streamlit run main.py`
"""
    )

st.success("✅ All charts rendered successfully. Use the sidebar to tweak parameters!")
