import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
# pio.renderers.default = 'browser'

class IntensityAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.mapped_data = None
        self.threshold = None
        self.skip_intervals = []

    def read_data(self):
        # Read data from the file
        self.df = pd.read_csv(self.file_path, delimiter='\t', comment='#', skip_blank_lines=False)
        # Clean column names
        self.df.columns = self.df.columns.str.replace(r'\s|\(|\)|\-|\_+', '_', regex=True)

    def filter_data(self):
        # Filter data with sputter time <=f['Sputter_Time__s_'] <= 399] 399s
        self.df = self.df[self.df['Sputter_Time__s_'] <= 399]

    def detect_spikes(self):
        # Detect spikes in data
        intensity = self.df['Intensity'].values
        diff_intensity = np.diff(intensity)
        self.threshold = np.percentile(np.abs(diff_intensity), 99)

        spike_indices = np.where(np.abs(diff_intensity) > self.threshold)[0]
        for idx in spike_indices:
            start_idx = max(0, idx - 1)
            end_idx = min(len(intensity) - 1, idx + 5)
            if self.skip_intervals and self.skip_intervals[-1][1] >= start_idx:
                self.skip_intervals[-1] = (self.skip_intervals[-1][0], end_idx)
            else:
                self.skip_intervals.append((start_idx, end_idx))

    def map_data(self):
        # Map data excluding spikes
        skip_indices = [i for interval in self.skip_intervals for i in range(interval[0], interval[1])]

        slices = []
        last_index = 0

        for start, end in self.skip_intervals:
            slices.append(self.df.iloc[last_index:start])
            last_index = end

        slices.append(self.df.iloc[last_index:])
        self.mapped_data = slices[0]

        for i in range(1, len(slices)):
            last = self.mapped_data.iloc[-1]
            current = slices[i].iloc[0]

            diff_rate = last['Intensity'] - current['Intensity']
            diff_rate = diff_rate - (self.threshold * 0.3 * diff_rate / abs(diff_rate))

            mapped = slices[i] + diff_rate
            mapped['Sputter_Time__s_'] = slices[i]['Sputter_Time__s_']

            self.mapped_data = pd.concat([self.mapped_data, mapped])

    def plot_results(self):
        # Create a plot with Plotly
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=self.mapped_data['Sputter_Time__s_'],
                                 y=self.mapped_data['Intensity'],
                                 mode='lines+markers', name='Intensity mapped',
                                 line=dict(color='blue'), marker=dict(size=0.5)))

        fig.add_trace(go.Scatter(x=self.df['Sputter_Time__s_'],
                                 y=self.df['Intensity'],
                                 mode='lines+markers', name='Intensity',
                                 line=dict(color='green'), marker=dict(size=0.5)))

        for (start, end) in self.skip_intervals:
            fig.add_vrect(x0=start, x1=end, fillcolor='red', opacity=0.3, line_width=0)

        fig.update_layout(
            title='Intensity with Detected Spikes',
            xaxis_title='Sputter Time (s)',
            yaxis_title='Intensity',
            showlegend=True
        )

        fig.show()

    def print_spike_intervals(self):
        print("Detected spike intervals:")
        for (start, end) in self.skip_intervals:
            print(f"Start: {self.df['Sputter_Time__s_'].values[start]}, End: {self.df['Sputter_Time__s_'].values[end]}")

# Example usage
analyzer = IntensityAnalyzer('ED-C-01-depth.TXT')
analyzer.read_data()
analyzer.filter_data()
analyzer.detect_spikes() 
analyzer.map_data()
analyzer.plot_results()
analyzer.print_spike_intervals()
