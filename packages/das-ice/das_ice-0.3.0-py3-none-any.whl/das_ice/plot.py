import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly


def all_trace(da):
    '''
    Plot all the trace using plotly. The number of trace should not be to high.
    '''
    # Determine the number of rows (channels) in da
    num_rows = da.shape[1]

    # Create a subplot with shared x-axes and `num_rows` subplots
    fig = make_subplots(rows=num_rows, cols=1, shared_xaxes=True, subplot_titles=[f'Distance {da.distance[i].values} m' for i in range(num_rows)])

    # Loop through each row to create a plot
    for i in range(num_rows):
        fig.add_trace(go.Scatter(
            x=da['time'].values,
            y=da[:, i].values,
            mode='lines',
            name=f'Distance {i} m'
        ), row=i + 1, col=1)

        # Hide the x-axis label except for the last plot
        if i < num_rows - 1:
            fig.update_xaxes(showticklabels=False, row=i + 1, col=1)

    # Update layout with a tight layout and margin adjustments
    fig.update_layout(
        title='Synchronized Strain Rate Plots',
        xaxis_title='Time',
        yaxis_title='Strain Rate',
        height=300 * num_rows,  # Adjust height dynamically based on the number of plots
        margin=dict(l=50, r=50, t=50, b=50)  # Adjust margins for a tighter layout
    )

    return fig