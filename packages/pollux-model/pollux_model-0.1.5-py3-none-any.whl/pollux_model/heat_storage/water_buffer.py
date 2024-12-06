from pollux_model.model_abstract import Model


class WaterBufferTankModel(Model):
    """Ideal water buffer tank model for heat. Currently modelled as ideal buffer."""

    def __init__(self):
        super().__init__()

        self.parameters['timestep'] = 1  # seconds
        self.parameters['maximum_volume'] = 1  # maximum volume [m3]
        self.parameters['temperature_top_layer'] = 80  # top side temperature [C]
        self.parameters['temperature_bottom_layer'] = 30  # bottom side temperature [C]

        x = dict()
        x['current_volume'] = 0
        self.initialize_state(x)

    def initialize_state(self, x):
        """ generate an initial state based on user parameters """

        self.state['current_volume'] = x['current_volume']
        self._calculate_fill_level()

    def calculate_output(self):
        """calculate output based on input"""

        volume_flow = self.input['volume_flow']
        timestep = self.parameters['timestep']

        delta_volume = volume_flow * timestep
        self.state['current_volume'] = self.state['current_volume'] + delta_volume

        self._calculate_fill_level()

        # Assign output to state
        self.output = self.state

    def _calculate_fill_level(self):
        """function to calculate fill level"""
        self.state['fill_level'] = self.state['current_volume'] / self.parameters['maximum_volume']
