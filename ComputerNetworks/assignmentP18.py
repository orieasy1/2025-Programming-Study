import numpy as np

rtt_values = [209, 3, 1, 6, 2, 1, 5, 3, 6, 3, 3, 8, 2, 2, 3, 33, 11, 13, 7, 4, 5, 38, 39, 38, 60, 60, 81, 40, 44, 79, 40, 43, 41, 40, 40, 40]

average_rtt = np.mean(rtt_values)
std_dev_rtt = np.std(rtt_values)

print(f"Mean RTT: {average_rtt} ms")
print(f"Standard Deviation: {std_dev_rtt} ms")
