# https://docs.google.com/spreadsheets/d/1XN2FaVXGyQgwDPaqrOwjeOuLSnB-Bdmm3Zk81awdGII/edit?gid=0#gid=0 - Table 4


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import FuncFormatter


# Create DataFrame from provided data
data = {
    '20 Gbps': [61.745158, 61.619968, 61.597648, 61.611528, 62.588168, 62.798948,
               63.476888, 65.329818, 71.550498, 90.660988, 121.642138],
    '10 Gbps': [86.156086, 86.030896, 86.008576, 86.022456, 86.999096, 87.209876,
               87.887816, 89.740746, 95.961426, 115.071916, 146.053066],
    '1Gbps': [529.55179, 529.4266, 529.40428, 529.41816, 530.3948, 530.60558,
            531.28352, 533.13645, 539.35713, 558.46762, 589.44877],
    '500 Mbps': [1017.77035, 1017.64516, 1017.62284, 1017.63672, 1018.61336, 1018.82414,
               1019.50208, 1021.35501, 1027.57569, 1046.68618, 1077.66733]
}

x_values = [2**20, 2**21, 2**22, 2**23, 2**24, 2**25, 
           2**26, 2**27, 2**28, 2**29, 2**30]

df = pd.DataFrame(data, index=x_values)
df.index.name = 'Sender set Size (Total)'

# Create plot
plt.figure(figsize=(7, 4))

# Maintain consistent color/marker scheme
styles = {
    '20 Gbps': ('#1f77b4', '', '-'),       # Blue circle
    '10 Gbps': ('#ff7f0e', '', '--'),      # Orange triangle
    '1Gbps': ('#2ca02c', '', '-.'),        # Green square
    '500 Mbps': ('#d62728', '', ':')       # Red diamond
}

for col in df.columns:
    plt.plot(df.index, df[col], 
             color=styles[col][0],
             marker=styles[col][1],
             linestyle=styles[col][2],
             markersize=8,
             linewidth=2,
             label=col)

# Configure logarithmic scales
plt.yscale('log')
plt.xscale('log', base=2)

# Custom x-axis formatter for power-of-two labels
def format_x_ticks(x, pos):
    exponent = int(np.log2(x))
    return f'$2^{{{exponent}}}$'
plt.gca().xaxis.set_major_formatter(FuncFormatter(format_x_ticks))

# Y-axis formatting
# plt.yticks([50, 100, 200, 500, 1000, 2000, 5000], 
#          ['50', '100', '200', '500', '1K', '2K', '5K'])

# Formatting
#plt.title('Network Performance by Bandwidth and Sender Set Size', fontsize=14, pad=20)
plt.xlabel('Total Set Size Across Senders', fontsize=12)
plt.ylabel('Latency (s)', fontsize=12)
plt.grid(True, which='both', linestyle='--', alpha=0.7)
plt.legend(loc='center left', fontsize=10)

# Adjust layout
plt.tight_layout()

# Save the plot
plt.savefig("benchmark_ours_sender_set.pdf")