import numpy as np


class StepFunction:
    def __init__(self, values, step_size):
        self.values = values  # Step values (list or array)
        self.step_size = step_size  # Fixed step size

    def get_step_size(self):
        # Return the constant step size
        return self.step_size

    def evaluate(self, t):
        t = np.array(t)
        # Evaluate the step function at a point x based on the step size
        step_indices = np.floor(t / self.step_size).astype(int)

        # Clip the step indices to the range of the constants list
        step_indices = np.clip(step_indices, 0, len(self.values) - 1)

        return np.array(self.values)[step_indices]
