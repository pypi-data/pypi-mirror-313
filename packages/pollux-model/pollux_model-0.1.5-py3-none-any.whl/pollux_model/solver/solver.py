import numpy as np


class Solver:
    def __init__(self, time_vector, components, components_with_control):
        self.connections = []
        self.time_vector = time_vector
        self.components = components  # dict with key component name and value component object
        self.components_with_control = components_with_control  # list of components with control
        self.inputs = {}  # dict to store inputs of each component over time
        self.outputs = {}  # dict to store outputs of each component over time

    def connect(self, predecessor,  successor, predecessor_output, successor_input):
        # Connect the output of the predecessor component to one of the successor's input.
        self.connections.append((predecessor,  successor, predecessor_output, successor_input))

    def run(self, control):
        # Control is unscaled
        # Clean outputs/inputs which is needed when run is called multiple times
        control = np.array(control)
        for component_name in self.components:
            component = self.components[component_name]
            if hasattr(component, 'set_time'):
                component.set_time(0)  # reset time, this should become simulation start time
            if hasattr(component, 'set_initial_state'):
                component.set_initial_state()  # reset initial storage H2 mass for the tank model

        # Update the components with the control profiles
        number_of_components_with_control = len(self.components_with_control)
        control_reshaped = control.reshape(number_of_components_with_control, -1)
        for ii in range(number_of_components_with_control):
            self.components[self.components_with_control[ii]]. \
                update_time_function(control_reshaped[ii])

        time_index = -1
        for t in self.time_vector:
            time_index = time_index + 1
            # Process each connection in the system.
            for predecessor, successor, predecessor_output, successor_input in self.connections:
                for component in [predecessor, successor]:
                    if hasattr(component, 'set_time'):
                        component.set_time(t)  # reset time, should become simulation start time

                # First, calculate the predecessor to get its output
                predecessor.calculate_output()
                # Pass the output to the successor's input
                successor.input[successor_input] = predecessor.output[predecessor_output]
                # Calculate the successor component
                successor.calculate_output()

                # Store outputs for each component at each time step
                for component in [predecessor, successor]:
                    if component not in self.outputs:
                        self.outputs[component] = np.zeros((len(self.time_vector),
                                                            len(component.output.values())))
                    self.outputs[component][time_index] = list(component.output.values())

                    if component not in self.inputs:
                        self.inputs[component] = np.zeros((len(self.time_vector),
                                                           len(component.input.values())))
                    self.inputs[component][time_index] = list(component.input.values())
