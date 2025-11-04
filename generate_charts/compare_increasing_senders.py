#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Update global parameter
plt.rcParams.update({'font.size': 10})

# Define data
x_values = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 5000]

data = {
    'Cong et al. (plain)': [None, None, 1.021486576, 2.375245336, 5.091930354, 11.50610722, 
                    44.48220374, 100.82912, 227.2760053, 496.7981393, 1116.394706, 2502.176334, None],
    'KTSJ24 (encrypted)': [None, None, 139.10724, 141.38836 ,145.9506 ,155.07508 ,173.32404 ,209.82196 ,282.8178 ,428.80948 ,720.79284 ,1304.75956, None],
    'PEPSI (plain)': [14.30848689, 14.48615943, 14.84291329, 15.55588737, 16.9827469, 
              19.83573099, 25.54531919, 36.96230054, 59.8006808, 105.4901788, 
              196.9410136, 380.073368, 592.717116],
    'Ours (encrypted)': [70.85681036, 71.0583719, 71.3980506, 72.0971767, 73.507377, 
             76.24639, 81.409034, 91.112861, 108.518168, 146.499836, 
             220.909302, 370.282634, 535.03377]
}

# 139.10724, 141.38836 ,145.9506 ,155.07508 ,173.32404 ,209.82196 ,282.8178 ,428.80948 ,720.79284 ,1304.75956

# Create DataFrame
df = pd.DataFrame(data, index=x_values)
df.index.name = 'Number of Senders'

# Plotting
plt.figure(figsize=(6, 4))

# Plot each method's line
for method in df.columns:
    plt.plot(df.index, df[method], label=method, marker='', linestyle='-')

# Set log scale for Y-axis to highlight latency differences
plt.xscale("log", base=2)
plt.yscale("log")

# Axis labels and formatting
plt.xlabel("Number of Senders", fontsize=13)
plt.ylabel("Latency (s)", fontsize=13)
#plt.title("Latency vs Number of Senders (Log Scale)")
plt.legend()
plt.grid(True, which="both", linestyle='--', linewidth=0.5)
plt.tight_layout()

# Save the plot
plt.savefig("compare_increasing_senders.pdf")
plt.show()
