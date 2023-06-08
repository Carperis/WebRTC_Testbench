import matplotlib.pyplot as plt
import numpy as np

def plot_time_sequence(nodes, arrows):
    fig, ax = plt.subplots()

    # Set up x-axis for nodes
    ax.xaxis.tick_top()
    ax.xaxis.set_ticks_position('none')
    ax.set_xticks(np.arange(0, len(nodes), 1))
    ax.set_xticklabels(nodes)
    
    # Set up y-axis for time
    ax.yaxis.set_ticks_position('none')
    ax.set_yticks(np.arange(0, 10, 1))
    ax.invert_yaxis()

    # Plot vertical time lines
    for node in range(len(nodes)):
        ax.axvline(node, color='gray', linestyle='--')

    # Plot arrows
    for arrow in arrows:
        source = arrow['source']
        target = arrow['target']
        time = arrow['time']
        description = arrow['description']
        
        start_x = source
        start_y = time
        end_x = target
        end_y = time

        dx = end_x - start_x
        dy = end_y - start_y
        
        if (dx < 0):
            dx += 0.05
            text_pos = target + 0.1
        else:    
            dx -= 0.05
            text_pos = source + 0.1
        ax.arrow(start_x, start_y, dx, dy, head_width=0.2, head_length=0.05, fc='black', ec='black')
        ax.text(text_pos, time - 0.1, description)

    plt.ylabel('Time')
    plt.title('Time Sequence Diagram')
    plt.show()

# Example nodes
nodes = ['Private Address', 'Translated Address', 'Public Address', 'one more']

# Example arrows
arrows = [
    {'source': 0, 'target': 1, 'time': 1, 'description': 'Packet 1'},
    {'source': 1, 'target': 2, 'time': 3, 'description': 'Packet 2'},
    {'source': 2, 'target': 0, 'time': 5, 'description': 'Packet 3'}
]

plot_time_sequence(nodes, arrows)
