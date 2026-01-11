NetworkSim: 3D Epidemic Simulator

NetworkSim is a high-fidelity, interactive epidemic simulation platform. It bridges network science, stochastic SIR dynamics, and cinematic 3D rendering to visualize how contagions propagate through complex social graphs. Built with efficiency in mind, it allows for real-time interaction with large-scale population datasets directly in the browser.

Table of Contents

Core Features

System Parameters

System Architecture

Technical Highlights

Installation

Usage Guide

Project Structure

Extending the Model

Core Features

Flexible Network Topologies: Generate synthetic social structures using Erdős-Rényi, Watts-Strogatz, or Barabási-Albert models with tunable parameters (rewiring probability $p$, edges $m$, neighbors $k$).

High-Performance SIR Engine: A set-based simulation core optimized for large graphs, recording full node-state history for precise playback without recalculation.

Cinematic 3D Visualization: An immersive Three.js renderer featuring:

Instanced mesh rendering for thousands of nodes.

Dynamic neighbor highlighting (golden threads) on interaction.

Force-directed layouts (Spring) for structural clarity.

Live HUD statistics overlay.

Interactive Analytics: Integrated Plotly charts for tracking Susceptible, Infected, and Recovered (S-I-R) trajectories over time.

Time-Travel Control: Full playback control (Play, Pause, Replay, Speed Slider) to analyze specific moments of the outbreak.

System Parameters

NetworkSim is designed to explore the complex dynamics of disease spread by allowing users to tweak fundamental epidemiological and structural parameters in real-time. This variability allows for the simulation of diverse scenarios, from rapid flu-like outbreaks to slow-burning contagions.

Population Size ($N$): Scale the simulation from small communities (100 nodes) to town-sized networks (3000+ nodes) to observe how population density impacts spread.

Infection Spread Rate ($\beta$): Control the transmission probability per contact. Adjusting this parameter allows the system to model pathogens with varying levels of contagiousness (e.g., highly infectious Measles vs. less transmissible viruses).

Recovery Rate ($\gamma$): Define the probability of an infected individual recovering in a given time step. This directly influences the duration of the infectious period.

Simulation Duration (Days): Set the temporal scope of the simulation to capture short-term outbreak spikes or long-term endemic behaviors.

Initial Outbreak Size: Configure the number of "Patient Zeros" to seed the infection, allowing analysis of how outbreak origins affect containment.

System Architecture

The application follows a modular architecture separating simulation logic from the presentation layer.

1. Frontend & Orchestration (main_app.py)

Streamlit manages the application state, caches expensive topology generations, and embeds the 3D visualization via custom HTML components.

2. Simulation Core (backend/simulation/)

Generator: Creates graph topologies and assigns spatial coordinates using NetworkX.

Simulator: Manages the stochastic transition between states (S -> I -> R). It utilizes efficient set operations for $O(1)$ lookup times during infection steps.

Model: Encapsulates disease parameters (infection rate $\beta$, recovery rate $\gamma$).

3. Visualization Layer (visualization/)

Three.js Renderer: A Python wrapper that generates complex HTML/JS to render the scene using WebGL. It handles the "Cinematic Replay" by consuming the simulation history.

Analytics: Plotly integration for aggregate epidemiological curves.

Technical Highlights

Synthetic City Modeling: Nodes are assigned abstract spatial coordinates to emulate "clusters" and "communities" realistic to human contact graphs.

Instanced Rendering: Utilizes Three.js InstancedMesh to render high node counts (2000+) at 60 FPS, avoiding the performance bottlenecks of standard DOM-based visualizations.

Full-History Capture: The simulation loop records snapshots of every node's state at every timestep, enabling the frontend to "scrub" through the timeline instantly.

Reactive Data Flow: Changes in simulation parameters trigger optimized re-runs, updating both the 3D scene and the 2D charts in sync.

Installation

Clone the repository

git clone https://github.com/shaheer-shehri/Disease-Network-Simulator
cd Disease-Network-Simulator



Set up a virtual environment (Recommended)

python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate



Install dependencies

pip install -r requirements.txt



Run the application

streamlit run main_app.py



Usage Guide

Configuration (Sidebar):

Population: Set the number of nodes (agents).

Disease Model: Adjust Infection Rate ($p_{inf}$) and Recovery Rate ($p_{rec}$).

Topology: Choose the graph algorithm and tune its specific parameters (e.g., Randomness for Small-World).

Execution:

Click START to run the backend simulation.

Interaction:

3D View: Left-click nodes to highlight connections (golden threads) and view metadata. Right-click/Drag to pan and rotate.

Playback: Use the HUD controls inside the 3D view to Pause or change simulation speed.

Analysis: Observe the real-time S-I-R curves updating below the visualizer.

Project Structure

NetworkSim/
├── main_app.py                  # Entry point (Streamlit UI)
├── requirements.txt             # Project dependencies
├── backend/
│   └── simulation/
│       ├── __init__.py
│       ├── network_generator.py # Graph topology & spatial logic
│       ├── disease_model.py     # Infection probability logic
│       └── simulator.py         # Core time-step engine
└── visualization/
    ├── __init__.py
    ├── threejs_renderer.py      # WebGL generation logic
    ├── analytics_plotter.py     # Plotly charting functions
    └── color_map.py             # Visual consistency utils



Extending the Model

Disease Dynamics: Modify simulation/disease_model.py to implement SEIR (Exposed) or SIS (Re-infection) models.

Visual Channels: Update visualization/threejs_renderer.py to map node size or glow intensity to other metrics (e.g., centrality or vaccination status).

Data Export: Use pandas in main_app.py to export the sim.stats_history to CSV for offline analysis in Jupyter Notebooks.

Built with Python, Streamlit, and NetworkX.
