import networkx as nx
import random
import math

def generate_network(n=2000, model="watts", **kwargs):
    """
    Generates the social graph structure.
    """
    if model == "erdos_renyi":
        p = kwargs.get("p", 0.01)
        G = nx.erdos_renyi_graph(n, p)
    elif model == "watts_strogatz":
        k = kwargs.get("k", 10)
        p = kwargs.get("p", 0.05)
        G = nx.watts_strogatz_graph(n, k, p)
    else:  # barabasi_albert
        m = kwargs.get("m", 5)
        G = nx.barabasi_albert_graph(n, m)
    
    # Initialize state
    for node in G.nodes():
        G.nodes[node]["state"] = "S"
        
    return G

def assign_city_locations(G):
    """
    Assigns spatial 'Home' and 'Work' coordinates to every node 
    to simulate a city environment.
    
    Returns:
        home_coords (dict): {node_id: [x, y, 0]}
        work_coords (dict): {node_id: [x, y, 0]}
    """
    home_coords = {}
    work_coords = {}
    
    # Define City Districts (X range, Y range)
    # 1. Suburbs (Residential) - Spread out
    suburb_bounds = (0, 40, 0, 100) 
    # 2. Downtown (Commercial) - Dense center
    downtown_bounds = (45, 65, 45, 65)
    # 3. Industrial Zone - Bottom Right
    industrial_bounds = (70, 90, 10, 30)
    # 4. University/Tech Park - Top Right
    uni_bounds = (70, 90, 70, 90)

    for node in G.nodes():
        # --- ASSIGN HOME (mostly Suburbs) ---
        # 80% live in suburbs, 20% in city apartments
        if random.random() < 0.8:
            hx = random.uniform(suburb_bounds[0], suburb_bounds[1])
            hy = random.uniform(suburb_bounds[2], suburb_bounds[3])
        else:
            hx = random.uniform(downtown_bounds[0], downtown_bounds[1])
            hy = random.uniform(downtown_bounds[2], downtown_bounds[3])
            
        # Z is 0 (Ground level)
        home_coords[node] = [hx, hy, 0] 
        
        # --- ASSIGN WORK (Commute) ---
        # People commute to Downtown, Industrial, or Uni
        dest = random.choices(['downtown', 'industrial', 'uni', 'home'], 
                              weights=[0.4, 0.25, 0.15, 0.2])[0]
        
        if dest == 'downtown':
            wx = random.uniform(downtown_bounds[0], downtown_bounds[1])
            wy = random.uniform(downtown_bounds[2], downtown_bounds[3])
        elif dest == 'industrial':
            wx = random.uniform(industrial_bounds[0], industrial_bounds[1])
            wy = random.uniform(industrial_bounds[2], industrial_bounds[3])
        elif dest == 'uni':
            wx = random.uniform(uni_bounds[0], uni_bounds[1])
            wy = random.uniform(uni_bounds[2], uni_bounds[3])
        else: # Work from home / Unemployed
            wx, wy = hx, hy

        # Add small noise to work pos so they don't stack perfectly
        wx += random.uniform(-1, 1)
        wy += random.uniform(-1, 1)
        
        work_coords[node] = [wx, wy, 0]

    return home_coords, work_coords