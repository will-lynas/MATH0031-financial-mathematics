import marimo

__generated_with = "0.13.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import altair as alt
    return alt, mo, np


@app.cell
def _(mo):
    slider = mo.ui.slider(10, 1000, step=5, value=50, label="n")
    slider
    return (slider,)


@app.cell
def _(np, slider):
    def generate_walks(n_walks=1000):
        n = slider.value
        step_size = 1/np.sqrt(n)
        steps = np.random.choice([-step_size, step_size], size=(n_walks, n))
        walks = np.cumsum(steps, axis=1)
        return walks
    
    walks = generate_walks()
    final_positions = walks[:, -1]
    return walks, final_positions


@app.cell
def _(alt, np, walks):
    def plot_walks(num_walks_to_show=5):
        n_steps = walks.shape[1]
        x_values = np.arange(n_steps)
        plot_data = []
        
        for i in range(num_walks_to_show):
            plot_data.extend([
                {"step": float(x), "position": float(y), "walk": f"Walk {i+1}"}
                for x, y in zip(x_values, walks[i])
            ])
        
        chart = alt.Chart(alt.Data(values=plot_data)).mark_line().encode(
            x=alt.X('step:Q', title='Step'),
            y=alt.Y('position:Q', title='Position'),
            color=alt.Color('walk:N', title='Random Walk')
        ).properties(
            width=600,
            height=400,
            title='Sample Random Walks'
        )
        return chart
    
    walks_plot = plot_walks()
    walks_plot
    return (walks_plot,)


@app.cell
def _(alt, np, final_positions, slider):
    def create_distribution_plot():
        # Calculate histogram data
        hist, bin_edges = np.histogram(final_positions, bins='auto', density=True)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        
        # Calculate theoretical normal distribution
        mu = 0  # theoretical mean
        sigma = 1  # theoretical standard deviation
        x = np.linspace(min(final_positions), max(final_positions), 100)
        normal_pdf = 1/(sigma * np.sqrt(2*np.pi)) * np.exp(-(x-mu)**2/(2*sigma**2))
        
        # Create data dictionaries for both plots
        hist_data = [
            {"x": float(x), "density": float(y)} 
            for x, y in zip(bin_centers, hist)
        ]
        
        normal_data = [
            {"x": float(x), "density": float(y)} 
            for x, y in zip(x, normal_pdf)
        ]
        
        # Create histogram
        bars = alt.Chart(alt.Data(values=hist_data)).mark_bar(opacity=0.5).encode(
            x=alt.X('x:Q', title='Final Position'),
            y=alt.Y('density:Q', title='Density')
        )
        
        # Create normal distribution line
        line = alt.Chart(alt.Data(values=normal_data)).mark_line(color='red').encode(
            x='x:Q',
            y='density:Q'
        )
        
        # Combine the plots
        combined_plot = (bars + line).properties(
            width=600,
            height=400,
            title=f'Distribution of Final Positions (n={slider.value})'
        )
        
        return combined_plot
    
    distribution_plot = create_distribution_plot()
    distribution_plot
    return (distribution_plot,)

if __name__ == "__main__":
    app.run()
