from pollux_model.model_abstract import Model


class Splitter(Model):
    def __init__(self):
        super().__init__()

    def initialize_state(self, x):
        """ generate an initial state based on user parameters """

    pass

    def calculate_output(self):
        if len(self.input) == 1:
            self.output['output_0'] = self.input['input'] * \
                self.time_function.evaluate(self.current_time)
            self.output['output_1'] = self.input['input'] * \
                (1 - self.time_function.evaluate(self.current_time))
        else:
            raise ValueError("splitter requires exactly 1 input.")
