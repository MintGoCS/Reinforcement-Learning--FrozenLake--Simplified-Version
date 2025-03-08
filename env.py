# env.py
import numpy as np

class GridCell:
    def __init__(self, cell_type='normal', reward=0.0, is_terminal=False):
        self.cell_type = cell_type
        self.reward = reward
        self.is_terminal = is_terminal

    def __str__(self):
        return f"GridCell(type={self.cell_type}, reward={self.reward}, is_terminal={self.is_terminal})"

class GridWorld:
    def __init__(self, size=5):
        self.size = size
        self.grid = self.__create_grid()
        self.transitions = self._create_transitions()

    def __create_grid(self):
        """
        Create a grid of size self.size multiply self.size
        {
            (0, 0): GridCell(),
            (0, 1): GridCell(),
        }
        :return: Grid
        """
        grid = {}
        for i in range(self.size):
            for j in range(self.size):
                grid[(i, j)] = GridCell()
        return grid

    def _create_transitions(self):
        """
        Initialize the transition Table
        """
        transitions = {}
        for state in self.grid:
            transitions[state] = {}
            for action in ["up", "down", "left", "right"]:
                next_state = self._get_next_state(state, action)  # Return the new coordinates

                # Compute rewards
                base_reward = self.grid[next_state].reward
                penalty = -5 if next_state == state else 0  # If agent move outside the boundary

                transitions[state][action] = {
                    "next_state": next_state,  # Coordinates of next cell(x + dx, y + dy)
                    "reward": base_reward + penalty,
                    "done": self.grid[next_state].is_terminal,
                    "prob": 1.0
                }
        return transitions

    def _get_next_state(self, state, action):
        """
        Get the coordinates of the next state
        :param state: Current state
        :param action: What kind of action to take
        :return: New coordinates of the next state
        """
        i, j = state
        action_effects = {
            "up": (-1, 0),
            "down": (1, 0),
            "left": (0, -1),
            "right": (0, 1),
        }
        di, dj = action_effects[action]
        next_i = max(0, min(self.size - 1, i + di))
        next_j = max(0, min(self.size - 1, j + dj))
        return (next_i, next_j)

    def get_transition(self, state, action):
        next_state = self._get_next_state(state, action)
        cell = self.grid[next_state]
        return {
            "next_state": next_state,
            "reward": cell.reward,  # 直接从 grid 中获取最新值
            "done": cell.is_terminal,  # 直接从 grid 中获取最新值
            "prob": 1.0
        }

    def set_cell(self, position, cell_type, reward, is_terminal):
        """
        Set cell type and reward and is_terminal
        :param position: (x, y)
        :param cell_type: Type of cell
        :param reward: Feedback entering the cell
        :param is_terminal: Whether the cell is terminal or not
        """
        if position in self.grid:
            self.grid[position].cell_type = cell_type
            self.grid[position].reward = reward
            self.grid[position].is_terminal = is_terminal
        else:
            raise ValueError(f"Position {position} not in grid")

    def get_cell(self, position):
        """
        Get specific property of the cell
        """
        return self.grid.get(position, None)

    def __str__(self):
        grid_str = ""
        for i in range(self.size):
            row = [str(self.grid[(i,j)]) for j in range(self.size)]
            grid_str += "\n".join(row) + "\n"
        return grid_str