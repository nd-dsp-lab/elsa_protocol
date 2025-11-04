# https://docs.google.com/spreadsheets/d/1XN2FaVXGyQgwDPaqrOwjeOuLSnB-Bdmm3Zk81awdGII/edit?gid=0#gid=0 - Table 3


import matplotlib.pyplot as plt
import pandas as pd


# Create DataFrame from provided data
data = {
    '20 Gbps': [70.80940636, 70.9632839, 71.2075946, 71.7159847, 72.744713, 74.720782,
               78.357538, 85.009589, 96.311344, 122.085908, 172.081166, 272.626082],
    '10 Gbps': [70.85381036, 71.0553719, 71.3950506, 72.0941767, 73.504377, 76.24339,
               81.406034, 91.109861, 108.515168, 146.496836, 220.906302, 370.279634],
    '1Gbps': [75.65208236, 76.7119559, 78.7682586, 82.9006327, 91.177329, 107.649334,
            140.277962, 204.913757, 332.183, 589.89254, 1103.75775, 2132.04257],
    '500 Mbps': [76.54016236, 78.5537159, 82.5173786, 90.4644727, 106.370609, 138.101494,
               201.247882, 326.919197, 576.25948, 1078.1111, 2080.26047, 4085.11361]
}

x_values = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]

df = pd.DataFrame(data, index=x_values)
df.index.name = '# of senders'

# Create plot
plt.figure(figsize=(6, 4))

# Plot each series with different styles
styles = {
    '20 Gbps': ('#1f77b4', '', '-'),       # Blue
    '10 Gbps': ('#ff7f0e', '', '--'),      # Orange
    '1Gbps': ('#2ca02c', '', '-.'),        # Green
    '500 Mbps': ('#d62728', '', ':')       # Red
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

# Formatting
#plt.title('Network Performance by Bandwidth (Logarithmic Scale)', fontsize=14, pad=20)
plt.xlabel('Number of Senders', fontsize=13)
plt.ylabel('Latency (s)', fontsize=13)
plt.grid(True, which='both', linestyle='--', alpha=0.7)
plt.legend(loc='upper left', fontsize=12)

# Customize tick labels
#plt.xticks(x_values, [str(x) for x in x_values], rotation=45)
#plt.yticks([70, 100, 200, 500, 1000, 2000, 5000], 
#          ['70', '100', '200', '500', '1000', '2000', '5000'])

#plt.gca().get_xaxis().set_major_formatter(plt.ScalarFormatter())
#plt.tight_layout()
# Save the plot

plt.savefig("benchmark_ours.pdf")