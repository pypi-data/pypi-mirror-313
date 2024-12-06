from pollux_model.model_abstract import Model


class Model1(Model):
    def __init__(self):
        super().__init__()

    def initialize_state(self, x):
        """ generate an initial state based on user parameters """
        pass

    def calculate_output(self):
        """calculate output based on input u"""

        input_model = self.input['input_key_1']

        # OUTPUT calculations
        output_model = self._internal_function(input_model)

        # Assign output to self
        self.output['output_key_1'] = output_model

    def _internal_function(self, input_function):
        """model function defined internally"""
        output_function = input_function
        return output_function
