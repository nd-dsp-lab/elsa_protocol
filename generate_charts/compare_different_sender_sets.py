# https://docs.google.com/spreadsheets/d/1XN2FaVXGyQgwDPaqrOwjeOuLSnB-Bdmm3Zk81awdGII/edit?gid=0#gid=0 - Table 2

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import FuncFormatter


# Create DataFrame from provided data
data = {
    'Cong et al. (plain)': [463.7926728, 462.4469218, 461.5702318, 463.5747888, 462.3424308,
            464.3361928, 460.7276098, 471.7820378, 469.5985768, 480.7324195, 502.5504168],
    'KTSJ24 (encrypted)': [260.895, np.nan, np.nan, 260.895, np.nan, 260.895, 260.895,
              360.08548, 372.06348, 384.54148, 396.00948],
    'PEPSI (plain)': [120.3621168, 120.3000288, 120.2247818, 120.2388928, 120.1617238,
             120.9321628, 121.3963188, 121.4407638, 121.9461888, 125.0465298, 133.1039028],
    'Ours (encrypted)': [86.156086, 86.030896, 86.008576, 86.022456, 86.999096, 87.209876,
            87.887816, 89.740746, 95.961426, 115.071916, 146.053066]
}

x_values = [2**20, 2**21, 2**22, 2**23, 2**24, 2**25,
           2**26, 2**27, 2**28, 2**29, 2**30]

df = pd.DataFrame(data, index=x_values)
df.index.name = 'Sender Set Size'

# Create plot
plt.figure(figsize=(6, 4))

# Define consistent color scheme based on previous encoding
styles = {
    'Cong et al. (plain)': ('#1f77b4', '', '-'),     # Blue circle
    'KTSJ24 (encrypted)': ('#ff7f0e', '', '-'),  # Orange triangle
    'PEPSI (plain)': ('#2ca02c', '', '-'),   # Green square
    'Ours (encrypted)': ('#d62728', '', '-')      # Red diamond
}

# Plot each series with individual handling
for col in df.columns:
    # Plot non-null values with markers
    non_null = df[col].notna()
    plt.plot(df.index[non_null], df[col][non_null],
             color=styles[col][0],
             marker=styles[col][1],
             linestyle=styles[col][2],
             markersize=8,
             linewidth=2,
             label=col)
    
    # Plot dashed line for missing values if needed
    if df[col].isna().any():
        null_segments = df[col].isna().cumsum()
        for _, group in null_segments.groupby(null_segments):
            if group.iloc[0] == 1:
                start = group.index[0] - 1
                end = group.index[-1] + 1
                plt.plot(df.index[start:end], df[col][start:end],
                        color=styles[col][0],
                        linestyle=styles[col][2],
                        linewidth=2,
                        alpha=0.3)

# Configure logarithmic scales
plt.yscale('log')
plt.xscale('log', base=2)

# Custom x-axis formatter
def format_x_ticks(x, pos):
    exponent = int(np.log2(x))
    return f'$2^{{{exponent}}}$'
plt.gca().xaxis.set_major_formatter(FuncFormatter(format_x_ticks))

# Y-axis formatting
#plt.yticks([50, 100, 200, 500, 1000, 2000, 5000, 10000, 50000], 
 #         ['50', '100', '200', '500', '1K', '2K', '5K', '10K', '50K'])

# Formatting
#plt.title('Performance Comparison Across Methods', fontsize=14, pad=20)
plt.xlabel('Total Set Size Across Senders', fontsize=13)
plt.ylabel('Latency (s)', fontsize=13)
plt.grid(True, which='both', linestyle='--', alpha=0.7)
plt.legend(loc='center right', fontsize=10)

# Set axis limits
#plt.ylim(50, 100000)
plt.xlim(2**20*0.9, 2**30*1.1)

plt.tight_layout()


# Save the plot
plt.savefig("compare_different_sender_sets.pdf")
