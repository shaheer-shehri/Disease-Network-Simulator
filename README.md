# Disease Network Simulator

Disease Network Simulator is a high-fidelity, interactive epidemic simulation platform that integrates **network science**, **stochastic SIR dynamics**, and **real-time 3D visualization**.  
It enables users to explore how infectious diseases propagate through complex social networks using an efficient, browser-based simulation pipeline.

The platform is designed for scalability, analytical clarity, and reproducibility, supporting large populations, multiple network topologies, and synchronized visual and statistical analysis.

---

## Table of Contents

- [Core Features](#core-features)
- [System Variability and Parameters](#system-variability-and-parameters)
- [System Architecture](#system-architecture)
- [Technical Highlights](#technical-highlights)
- [Installation and Setup](#installation-and-setup)
- [Running the Application](#running-the-application)
- [Usage Guide](#usage-guide)
- [Project Structure](#project-structure)
- [Extending the Model](#extending-the-model)
- [Potential Improvements](#potential-improvements)
- [Technology Stack](#technology-stack)

---

## Core Features

### Flexible Network Topologies
NetworkSim supports the generation of synthetic social networks using widely studied graph models:

- **Erdos–Rényi Random Graphs**
- **Watts–Strogatz Small-World Networks**
- **Barabási–Albert Scale-Free Networks**

Each topology exposes tunable parameters such as rewiring probability, node degree, and edge attachment rate.

---

### High-Performance SIR Simulation Engine
- Discrete-time stochastic SIR model
- Set-based state tracking for constant-time lookups
- Full per-node state history recorded at every timestep
- Deterministic playback without recomputation

---

### Real-Time 3D Visualization
A WebGL-based renderer built on **Three.js**, featuring:

- Instanced mesh rendering for thousands of agents
- Force-directed (spring) layouts for structural clarity
- Interactive node inspection and neighbor highlighting
- Heads-up display for live statistics and playback controls

---

### Interactive Analytics
- Real-time **Susceptible–Infected–Recovered (SIR)** curves
- Plotly-based dynamic charts
- Full synchronization with simulation timeline

---

### Temporal Playback and Analysis
- Play, pause, replay, and speed control
- Timeline scrubbing through recorded simulation history
- Enables post-hoc analysis of outbreak phases

---

## System Variability and Parameters

NetworkSim allows real-time exploration of epidemiological and structural parameters.

### Population Size (N)
Scales from small communities (≈100 agents) to large networks (3000+ agents), enabling density and scale analysis.

### Infection Rate (β)
Controls the probability of transmission per contact, allowing modeling of pathogens with varying contagiousness.

### Recovery Rate (γ)
Defines the probability of recovery per timestep, directly influencing infectious period duration.

### Simulation Duration
Configurable number of simulated days to observe short-term outbreaks or long-term endemic behavior.

### Initial Outbreak Size
Controls the number of initially infected individuals (patient zero seeding).

---

## System Architecture

The application follows a modular architecture separating simulation logic, visualization, and orchestration.

### 1. Frontend and Orchestration
**`main_app.py`**
- Streamlit-based user interface
- Application state management
- Caching of expensive graph generation
- Embedding of WebGL visualization via custom HTML components

---

### 2. Simulation Core (`backend/simulation/`)
- **network_generator.py**  
  Generates graph topologies and assigns spatial coordinates using NetworkX.

- **disease_model.py**  
  Encapsulates epidemiological parameters (β, γ).

- **simulator.py**  
  Executes stochastic S → I → R transitions using efficient set operations.

---

### 3. Visualization Layer (`visualization/`)
- **threejs_renderer.py**  
  Generates Three.js scenes and handles cinematic replay.

- **analytics_plotter.py**  
  Produces real-time SIR plots using Plotly.

- **color_map.py**  
  Centralized visual state consistency utilities.

---

## Technical Highlights

- **Synthetic City Modeling**  
  Abstract spatial clustering emulates realistic social communities.

- **Instanced Rendering**  
  Efficient GPU-based rendering enables smooth interaction at high node counts.

- **Full-History Capture**  
  Enables instant timeline scrubbing without re-running simulations.

- **Reactive Data Flow**  
  Parameter changes trigger optimized re-simulation with synchronized visual and analytical updates.

---

## Installation and Setup

### Prerequisites
- Python **3.9 or higher**
- pip package manager
- A modern web browser with WebGL support

---

### Clone the Repository
```bash
git clone[ https://github.com/yourusername/networksim.git](https://github.com/shaheer-shehri/Disease-Network-Simulator)
cd networksim
```
. Create a Virtual Environment (Recommended)
python -m venv venv


Activate:

Windows:

    venv\Scripts\activate

macOS / Linux:

    source venv/bin/activate

Install Dependencies
    pip install -r requirements.txt

Run the Application
    streamlit run main_app.py

###Usage Guide
 Configuration (Sidebar)

Population Size

Infection Rate (β)

Recovery Rate (γ)

Network Topology & Parameters

###Execution

Click START to run the simulation backend.

###Interaction

Left-click nodes to highlight neighbors

Right-click / Drag to rotate and pan

HUD Controls for playback & speed

###Analysis

Monitor live S-I-R curves updating in real time beneath the 3D visualizer.

---

##Project Structure
NetworkSim/
├── main_app.py
├── requirements.txt
├── backend/
│   └── simulation/
│       ├── network_generator.py
│       ├── disease_model.py
│       └── simulator.py
└── visualization/
    ├── threejs_renderer.py
    ├── analytics_plotter.py
    └── color_map.py

##Extending the Model

Disease Dynamics
Implement SEIR, SIS, or custom compartment models.

Visual Channels
Map node size, glow, or color to centrality or vaccination status.

Data Export
Export simulation history to CSV for offline analysis in Jupyter.

##Technology Stack

Python

Streamlit

NetworkX

Three.js

Plotly

WebGL
