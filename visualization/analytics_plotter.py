import pandas as pd
import plotly.express as px
from .color_map import STATE_COLORS

def plot_epidemic_curve(stats_history):
    """
    Generates an interactive Plotly line chart of the 
    Susceptible, Infected, and Recovered populations over time.

    Args:
        stats_history (list or DataFrame): The list of stat dicts 
                              from DiseaseSimulator.stats_history or a DataFrame.

    Returns:
        plotly.graph_objects.Figure: The interactive line chart.
    """
    # Handle both list and DataFrame inputs
    if isinstance(stats_history, pd.DataFrame):
        df = stats_history
    else:
        if not stats_history:
            return px.line(title="No data to display.")
        # Convert the stats history list of dicts into a DataFrame
        df = pd.DataFrame(stats_history)
    
    # Check if DataFrame is empty
    if df.empty:
        return px.line(title="No data to display.")
    
    # Melt the DataFrame to "long" format, which is what Plotly prefers
    # 'time' is the id, 'S', 'I', 'R' become 'variable' and 'value'
    df_long = df.melt(
        id_vars=['time'], 
        value_vars=['S', 'I', 'R'], 
        var_name='State', 
        value_name='Population'
    )

    # Create the line chart
    fig = px.line(
        df_long,
        x='time',
        y='Population',
        color='State',  # This automatically creates a legend
        title='Epidemic Curve (S-I-R Model)',
        color_discrete_map={
            'S': STATE_COLORS.get('S'),
            'I': STATE_COLORS.get('I'),
            'R': STATE_COLORS.get('R')
        }
    )
    
    fig.update_layout(
        xaxis_title="Time Step (Days)",
        yaxis_title="Number of People",
        uirevision='constant'  # Preserve zoom/pan across updates
    )
    
    return fig