# config.py

# Training Hyperparameter
ALPHA = 0.3  # Learning rate
GAMMA = 0.9  # Discounting factor
EPSILON = 1  # Initial epsilon(exploration rate)
EPSILON_DECAY = 0.9995
MIN_EPSILON = 0.1  # Minimum epsilon(exploration rate)
NUM_EPISODES = 10000
MAX_STEPS = 300

# Initialize Q-table
Q_INIT_MIN = -0.1
Q_INIT_MAX = 0.1
