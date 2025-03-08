# q_learning.py
import numpy as np
from config import ALPHA, GAMMA, EPSILON, EPSILON_DECAY, MIN_EPSILON, NUM_EPISODES, MAX_STEPS, Q_INIT_MIN, Q_INIT_MAX

def initialize_q_table(env):
    """
    Initializes the Q-table
    """
    # actions = list(next(iter(env.transitions.values())).keys())
    actions = ["up", "down", "left", "right"]
    Q = {state: {action: np.random.uniform(Q_INIT_MIN, Q_INIT_MAX) for action in actions} for state in env.grid}
    return Q

def train_q_learning(env, Q):
    epsilon = EPSILON
    rewards = []

    for episode in range(NUM_EPISODES):
        state = (0, 0)
        total_reward = 0
        done = False
        steps = 0
        # print(Q)
        while not done and steps < MAX_STEPS:
            if np.random.random() < epsilon:
                action = np.random.choice(list(Q[state].keys()))
            else:
                max_value = max(Q[state].values())
                best_actions = [a for a in Q[state] if Q[state][a] == max_value]
                action = np.random.choice(best_actions)  # Break ties randomly

            transition = env.get_transition(state, action)
            next_state, reward, done = transition["next_state"], transition["reward"], transition["done"]

            # Update Q value
            next_max_q = max(Q[next_state].values()) if not done else 0
            Q[state][action] += ALPHA * (reward + GAMMA * next_max_q - Q[state][action])

            # Move to next state
            state = next_state
            total_reward += reward
            steps += 1

        rewards.append(total_reward)
        epsilon = max(MIN_EPSILON, epsilon * EPSILON_DECAY)

        if (episode + 1) % 1000 == 0:
            print(f"Episode {episode+1}: Avg Reward (last 100): {np.mean(rewards[-100:])}, Epsilon: {epsilon}")

    return Q