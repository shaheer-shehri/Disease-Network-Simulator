import random

class DiseaseSimulator:
    """
    running disease simulations.
    """
    
    def __init__(self, graph, disease_model):
        self.graph = graph
        self.model = disease_model
        self.time = 0
        
        # State Sets for O(1) ops
        self.susceptible_set = set()
        self.infected_set = set()
        self.recovered_set = set()

        # Stats for the Graph (Counts) - Used for Charts
        self.stats_history = []
        
        #  - Used for 3D Replay
        # Stores a list of dictionaries: [{node_id: 'S', ...}, {node_id: 'I', ...}]
        self.node_history = []
        
        self._initialize_node_states()

    def _initialize_node_states(self):
        for node, data in self.graph.nodes(data=True):
            if data.get("state", "S") == "S":
                self.susceptible_set.add(node)
            # Add other states if necessary
        
        self._record_stats()

    def infect_initial(self, count=5):
        if count > len(self.susceptible_set):
            count = len(self.susceptible_set)
            
        patient_zero_nodes = random.sample(list(self.susceptible_set), count)

        for node in patient_zero_nodes:
            self._set_node_state(node, "I")

    def _set_node_state(self, node, new_state):
        self.susceptible_set.discard(node)
        self.infected_set.discard(node)
        self.recovered_set.discard(node)

        if new_state == "S":
            self.susceptible_set.add(node)
        elif new_state == "I":
            self.infected_set.add(node)
        elif new_state == "R":
            self.recovered_set.add(node)
        
        self.graph.nodes[node]["state"] = new_state

    def step(self):
        newly_infected = set()
        newly_recovered = set()

        # Infection Logic (Optimized)
        for node in self.infected_set:
            for neighbor in self.graph.neighbors(node):
                if neighbor in self.susceptible_set:
                    if self.model.should_infect():
                        newly_infected.add(neighbor)
            
            if self.model.should_recover():
                newly_recovered.add(node)

        # Apply Changes
        for node in newly_infected:
            self._set_node_state(node, "I")
            
        for node in newly_recovered:
            self._set_node_state(node, "R")

        self.time += 1
        self._record_stats()

    def _record_stats(self):
        # 1. Record aggregate counts (for Charts)
        stats = {
            "time": self.time,
            "S": len(self.susceptible_set),
            "I": len(self.infected_set),
            "R": len(self.recovered_set)
        }
        self.stats_history.append(stats)
        
        # 2. Record node states (for 3D Replay)
        # We save the state of EVERY node at this specific time step.
        # This allows the JavaScript frontend to "replay" the infection like a movie.
        snapshot = {n: self.graph.nodes[n]["state"] for n in self.graph.nodes()}
        self.node_history.append(snapshot)

    def run(self, max_steps=100):
        """
        Runs the full simulation loop at once.
        """
        while self.time < max_steps:
            if not self.infected_set:
                break
            self.step()