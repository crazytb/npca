import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from random_access.random_access import randomaccess

if __name__ == "__main__":
    dflog = randomaccess(numnodes:=10, beaconinterval:=100000*100, frametxslot:=300, per:=0)
    # Parameters
    slot_time = 9            # microseconds per slot

    # Calculate frame duration in microseconds
    frame_duration = frametxslot * slot_time  # microseconds

    # Filter successful transmissions only
    successful_tx = dflog[dflog['result'] == 'succ']

    # Calculate throughput for each node
    throughput_data = []
    for node in range(1, numnodes + 1):
        node_tx = successful_tx[successful_tx['node'] == node]
        num_successful_tx = len(node_tx)
        
        # Throughput = (Number of successful transmissions * Frame duration) / Total simulation time
        throughput = (num_successful_tx * frame_duration) / beaconinterval
        
        throughput_data.append({
            'node': node,
            'successful_tx': num_successful_tx,
            'throughput': throughput,
            'throughput_percentage': throughput * 100
        })

    # Create DataFrame for throughput results
    throughput_df = pd.DataFrame(throughput_data)

    # Display results
    print("Throughput Analysis for Each Station:")
    print("=" * 50)
    print(throughput_df.to_string(index=False))
    print("\n" + "=" * 50)

    # Calculate total system throughput
    total_throughput = throughput_df['throughput'].sum()
    total_successful_tx = throughput_df['successful_tx'].sum()

    print(f"Total System Throughput: {total_throughput:.4f} ({total_throughput*100:.2f}%)")
    print(f"Total Successful Transmissions: {total_successful_tx}")
    print(f"Average Throughput per Node: {total_throughput/numnodes:.4f} ({total_throughput*100/numnodes:.2f}%)")

    # Additional analysis: Show distribution of results
    print("\nTransmission Result Distribution:")
    result_counts = dflog['result'].value_counts()
    print(result_counts)

    # Calculate fairness index (Jain's fairness index)
    throughputs = throughput_df['throughput'].to_numpy()
    fairness_index = (np.sum(throughputs) ** 2) / (len(throughputs) * np.sum(throughputs ** 2))
    print(f"\nFairness Index (Jain's): {fairness_index:.4f}")
    print("Note: 1.0 = perfectly fair, lower values indicate unfairness")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Bar plot of throughput per node
    ax1.bar(throughput_df['node'], throughput_df['throughput_percentage'], 
            color='skyblue', edgecolor='navy', alpha=0.7)
    ax1.set_xlabel('Node ID')
    ax1.set_ylabel('Throughput (%)')
    ax1.set_title('Throughput per Station')
    ax1.grid(True, alpha=0.3)
    ax1.set_xticks(range(1, numnodes + 1))

    # Bar plot of successful transmissions per node
    ax2.bar(throughput_df['node'], throughput_df['successful_tx'], 
            color='lightgreen', edgecolor='darkgreen', alpha=0.7)
    ax2.set_xlabel('Node ID')
    ax2.set_ylabel('Number of Successful Transmissions')
    ax2.set_title('Successful Transmissions per Station')
    ax2.grid(True, alpha=0.3)
    ax2.set_xticks(range(1, numnodes + 1))

    plt.tight_layout()
    plt.show()