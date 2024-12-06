from abc import ABC, abstractmethod
from pollux_model.solver.step_function import StepFunction
import numpy as np


class Model(ABC):
    """ Abstract base class for simulation models

        Model classes implement a discrete state space model
        The state of the model is maintained outside the model object
    """

    @abstractmethod
    def __init__(self):
        """ Model initialization
        """
        self.parameters = {}
        self.state = {}
        self.output = {}
        self.input = {}

        self.current_time = 0

        self.time_function = StepFunction(np.zeros(1), 1)

    def update_parameters(self, parameters):
        """ To update model parameters

        Parameters
        ----------
        parameters : dict
            parameters dict as defined by the model
        """
        for key, value in parameters.items():
            self.parameters[key] = value

    def update_time(self, time_step):
        self.current_time += time_step

    def set_time(self, time):
        self.current_time = time

    def set_time_function(self, time_function):
        self.time_function = time_function

    def update_time_function(self, control):
        step_size = self.time_function.get_step_size()
        step_function = StepFunction(control, step_size)
        self.time_function = step_function

    @abstractmethod
    def initialize_state(self, x):
        """ generate an initial state based on user parameters """
        pass

    @abstractmethod
    def calculate_output(self):
        """calculate output based on input u"""
        pass

    def get_output(self):
        """get output of the model"""
        return self.output
