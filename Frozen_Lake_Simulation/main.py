# main.py
from env import GridWorld
from q_learning import initialize_q_table, train_q_learning
from visualize import visualize_gridworld  # Make sure this import works
import os


env = GridWorld(size=5)
env.set_cell((4, 4), "goal", 10.0, True)
env.set_cell((2, 3), "hole", -5.0, True)
env.set_cell((1, 0), "hole", -5.0, True)
env.set_cell((0, 2), "hole", -5.0, True)
env.set_cell((3, 1), "hole", -5.0, True)
env.set_cell((3, 2), "hole", -5.0, True)

Q = initialize_q_table(env)
Q = train_q_learning(env, Q)

print(Q)

def run_policy(env, Q, max_steps=200):
    state = (0, 0)
    path = [state]
    steps = 0
    while not env.get_cell(state).is_terminal and steps < max_steps:
        action = max(Q[state], key=Q[state].get)
        state = env.get_transition(state, action)["next_state"]
        path.append(state)
        steps += 1
    return path


optimal_path = run_policy(env, Q)
print(optimal_path)

# Visualize, save to ~/Videos with incremental names
visualize_gridworld(env, optimal_path, output_dir="Videos")