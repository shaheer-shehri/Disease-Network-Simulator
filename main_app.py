import streamlit as st
import streamlit.components.v1 as components 
import networkx as nx
import pandas as pd

# Import modules
from simulation.network_generator import generate_network
from simulation.disease_model import DiseaseModel
from simulation.simulator import DiseaseSimulator
from visualization.analytics_plotter import plot_epidemic_curve
from visualization.threejs_renderer import generate_threejs_html

st.set_page_config(
    page_title="NetworkSim: 3D",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CACHING & SETUP ---
def _select_layout(G, model_type, k_val, p_val):
    """Pick a layout with distinct geometry per model for visual contrast."""
    if model_type == "watts_strogatz":
        # Lattice-like with a modest spring settle; lighter than before
        return nx.spring_layout(G, dim=3, seed=42, iterations=60)
    if model_type == "barabasi_albert":
        # Hub-heavy but faster: spring starting from a random base
        base = nx.random_layout(G, dim=3, seed=7)
        return nx.spring_layout(G, dim=3, seed=7, pos=base, iterations=35)
    # erdos_renyi or fallback: airy random base, brief spring jiggle for depth
    base = nx.random_layout(G, dim=3, seed=13)
    return nx.spring_layout(G, dim=3, seed=13, pos=base, iterations=25)

@st.cache_data
def setup_network(n_pop, model_type, k_val, p_val):
    G = generate_network(n=n_pop, model=model_type, k=k_val, p=p_val, m=5)
    pos = _select_layout(G, model_type, k_val, p_val)
    return G, pos

# --- SESSION STATE MANAGEMENT ---
if 'sim_data' not in st.session_state:
    st.session_state.sim_data = None

# --- SIDEBAR CONTROLS ---
st.sidebar.title("🧬 Control Panel")

# 1. Top Control Buttons (Fixed Position)
st.sidebar.markdown("### ⏯️ Simulation Controls")
col_ctrl1, col_ctrl2 = st.sidebar.columns(2)

# Start/Run Button
start_pressed = col_ctrl1.button("START", type="primary", use_container_width=True)

# Reset Button
reset_pressed = col_ctrl2.button("RESET", use_container_width=True)

# Pause Toggle (Maintains state across reruns)
is_paused = st.sidebar.toggle("⏸ Pause Animation", value=False)

if reset_pressed:
    st.session_state.sim_data = None
    st.rerun()

# 2. Settings Inputs
with st.sidebar.form("sim_config"):
    st.header("Settings")
    n_pop = st.number_input("Population", 50, 3000, 600, 50)
    steps = st.number_input("Duration (Days)", 20, 365, 100)
    
    st.subheader("Disease Model")
    inf_prob = st.slider("Infection Rate", 0.0, 1.0, 0.05)
    rec_prob = st.slider("Recovery Rate", 0.0, 1.0, 0.02)
    initial_infected = st.slider("Initial Cases", 1, 50, 5)

    with st.expander("Network Topology"):
        model_type = st.selectbox("Model", ["watts_strogatz", "barabasi_albert", "erdos_renyi"])
        k_val = st.slider("Neighbors (k)", 2, 20, 6)
        p_val = st.slider("Randomness (p)", 0.0, 1.0, 0.05)

    # We use this button just to apply settings changes, not strictly to run
    apply_settings = st.form_submit_button("Apply Settings")

# --- MAIN LOGIC ---
st.title("Disease Simulation Model")

# Pre-load network structure (Cached)
with st.spinner("Generating Network Topology..."):
    G_preview, pos_preview = setup_network(n_pop, model_type, k_val, p_val)

# Handle Simulation Run
if start_pressed or (apply_settings and st.session_state.sim_data is None):
    with st.spinner("Running Simulation..."):
        # 1. Backend Simulation
        G_run = G_preview.copy()
        sim = DiseaseSimulator(G_run, DiseaseModel(inf_prob, rec_prob))
        sim.infect_initial(initial_infected)
        sim.run(max_steps=steps)
        
        # 2. Store in Session State
        st.session_state.sim_data = {
            "G": G_run,
            "history": sim.node_history,
            "stats": sim.stats_history,
            "pos": pos_preview
        }

# --- RENDERING ---
if st.session_state.sim_data:
    data = st.session_state.sim_data
    
    # Render 3D View
    # We pass the 'is_paused' state directly to the renderer
    html_code = generate_threejs_html(
        data["G"], 
        data["history"], 
        data["pos"], 
        stats_history=data["stats"], 
        is_paused=is_paused,
        height=700
    )
    
    components.html(html_code, height=700)
    
    # Analysis Section
    st.subheader("Post-Simulation Analysis")
    col1, col2 = st.columns([1, 3])
    
    final = data["stats"][-1]
    with col1:
        st.info(f"Final Day: {final['time']}")
        st.markdown(f"""
        <div style="padding:10px; background:#262730; border-radius:5px;">
            <b style="color:#1f77b4">Susceptible:</b> {final['S']}<br>
            <b style="color:#d62728">Infected:</b> {final['I']}<br>
            <b style="color:#2ca02c">Recovered:</b> {final['R']}
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.plotly_chart(plot_epidemic_curve(data["stats"]), use_container_width=True)

else:
    # Placeholder State
    st.info("Click **START** in the sidebar to run the simulation.")
    st.markdown("""
    <div style="height:600px; background:#050505; border-radius:12px; border:1px dashed #333; display:flex; align-items:center; justify-content:center; color:#555;">
        <span>Waiting for Simulation...</span>
    </div>
    """, unsafe_allow_html=True)