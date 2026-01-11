import random

class DiseaseModel:
    """
    Encapsulates the epidemiological parameters and rules for a disease.
    """
    
    def __init__(self, infection_prob=0.03, recovery_prob=0.01):
        """
        Initializes the disease model.

        Args:
            infection_prob (float): Probability (0-1) of transmission
                                    on contact between I and S.
            recovery_prob (float): Probability (0-1) of an I node
                                   moving to R in a time step.
        """
        self.infection_prob = infection_prob
        self.recovery_prob = recovery_prob

    def should_infect(self):
        """Returns True if an infection event should occur."""
        return random.random() < self.infection_prob

    def should_recover(self):
        """Returns True if a recovery event should occur."""
        return random.random() < self.recovery_prob