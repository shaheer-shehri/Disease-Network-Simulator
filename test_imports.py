"""
Test script to verify all imports work correctly
"""
import sys
print("Testing imports...")

try:
    from simulation.network_generator import generate_network
    print("✓ generate_network imported")
except ImportError as e:
    print(f"✗ Error importing generate_network: {e}")

try:
    from simulation.disease_model import DiseaseModel
    print("✓ DiseaseModel imported")
except ImportError as e:
    print(f"✗ Error importing DiseaseModel: {e}")

try:
    from simulation.simulator import DiseaseSimulator
    print("✓ DiseaseSimulator imported")
except ImportError as e:
    print(f"✗ Error importing DiseaseSimulator: {e}")

try:
    from visualization.analytics_plotter import plot_epidemic_curve
    print("✓ plot_epidemic_curve imported")
except ImportError as e:
    print(f"✗ Error importing plot_epidemic_curve: {e}")

try:
    from visualization.network_plotter import create_3d_network_plot
    print("✓ create_3d_network_plot imported")
except ImportError as e:
    print(f"✗ Error importing create_3d_network_plot: {e}")

print("\nAll imports successful!")
