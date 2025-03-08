# visualize.py
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
from celluloid import Camera
import os

def visualize_gridworld(env, path, output_dir="/Videos"):
    """
    Visualize the agent's path in the GridWorld as an animation

    Args:
        env: GridWorld environment
        path: List of (x,y) coordinates showing the agent's path
        output_dir: Directory to save the video
    """
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Find the next available file number
    base_name = "Optimal_path_"
    i = 1
    while os.path.exists(os.path.join(output_dir, f"{base_name}{i}.mp4")):
        i += 1
    output_file = os.path.join(output_dir, f"{base_name}{i}.mp4")

    # Create figure and camera for animation
    fig, ax = plt.subplots(figsize=(8, 8))
    camera = Camera(fig)

    # Create grid representation
    grid_size = env.size
    grid = np.zeros((grid_size, grid_size))

    # Color mapping for different cell types
    cell_colors = {
        'normal': 0,  # White
        'goal': 1,  # Green
        'hole': 2  # Red
    }

    # Create figure and camera for animation
    fig, ax = plt.subplots(figsize=(8, 8))
    camera = Camera(fig)

    # Create grid representation
    grid_size = env.size
    grid = np.zeros((grid_size, grid_size))

    # Color mapping for different cell types
    cell_colors = {
        'normal': 0,  # White
        'goal': 1,  # Green
        'hole': 2  # Red
    }

    # Fill grid with cell types, swap i and j to treat (i, j) as (x, y)
    for pos, cell in env.grid.items():
        i, j = pos
        grid[j, i] = cell_colors[cell.cell_type]  # Swap i and j

    # Create colormap
    cmap = colors.ListedColormap(['white', 'green', 'red'])
    bounds = [-0.5, 0.5, 1.5, 2.5]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    # Animate the path
    for step in range(len(path)):
        # Plot the grid
        ax.imshow(grid, cmap=cmap, norm=norm)

        # Add grid lines
        ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=1)
        ax.set_xticks(np.arange(-0.5, grid_size, 1))
        ax.set_yticks(np.arange(-0.5, grid_size, 1))

        # Plot the path up to current step, swap x and y
        if step > 0:
            path_x = [pos[0] for pos in path[:step + 1]]  # Use pos[0] as x
            path_y = [pos[1] for pos in path[:step + 1]]  # Use pos[1] as y
            ax.plot(path_x, path_y, 'b-', linewidth=2)

        # Plot current position, swap x and y
        current_pos = path[step]
        ax.plot(current_pos[0], current_pos[1], 'bo', markersize=10)  # Swap x and y

        # Add title
        ax.set_title(f"Step {step}")

        # Remove axis labels
        ax.set_xticklabels([])
        ax.set_yticklabels([])

        # Capture the frame
        camera.snap()

    # Create animation
    animation = camera.animate(interval=500, repeat=False)

    # Save animation
    animation.save(output_file, writer='ffmpeg')
    plt.close()

    print(f"Animation saved as {output_file}")