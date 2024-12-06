from pollux_model.model_abstract import Model


class Compressor(Model):
    def __init__(self):
        super().__init__()

        # specific_heat_ratio (Cp/Cv) also called gas isentropic coefficient
        self.parameters['specific_heat_ratio'] = 1.41  # = 1.41 for hydrogen
        self.parameters['inlet_temperature'] = 298  # K
        self.parameters['inlet_pressure'] = 1E5  # Pa
        self.parameters['outlet_pressure'] = 20E6  # Pa
        self.parameters['R'] = 4124.2  # J/(kg K), gas constant = 4124 for hydrogen
        self.parameters['Z'] = 1  # Z = 1 assuming ideal gas
        self.parameters['mechanical_efficiency'] = 0.97
        self.parameters['compressor_efficiency'] = 0.88
        self.parameters['number_of_stages'] = 2

    def initialize_state(self, x):
        """ generate an initial state based on user parameters """
        pass

    def calculate_output(self):
        """calculate output based on input"""

        mass_flow = self.input['mass_flow']  # kg/s

        compressor_power = self._power_calculation(mass_flow)

        self.output['compressor_power'] = compressor_power

    def _power_calculation(self, mass_flow):
        """See https://myengineeringtools.com/Compressors/Tools_Compressor_Power.html"""

        # Assumptions:
        # ideal intercooling: after each stage, the hydrogen is cooled back to inlet temperature T1
        # equal pressure ratio: each stage compresses the hydrogen with same pressure ratio

        e_m = self.parameters['mechanical_efficiency']
        e_c = self.parameters['compressor_efficiency']
        k = self.parameters['specific_heat_ratio']
        R = self.parameters['R']
        T1 = self.parameters['inlet_temperature']
        P1 = self.parameters['inlet_pressure']
        P2 = self.parameters['outlet_pressure']
        n = self.parameters['number_of_stages']
        r_stage = (P2 / P1) ** (1 / n)  # pressure ratio per stage

        compressor_power = (n * mass_flow * R * T1 / (k - 1)) * ((r_stage) ** ((k - 1) / k) - 1)

        # correcting for efficiency factors
        compressor_power = compressor_power / (e_m * e_c)

        return compressor_power
