import os
import yaml
from pollux_model.heat_pump.NREL_components.heat_pump_model import HeatPumpModel
from pollux_model.heat_pump.NREL_components.utilities.unit_defs import Q_

from pollux_model.model_abstract import Model
import numpy as np


class HeatpumpNREL(Model):
    """"
    This is the class with the specific format that we want and is a replicate of the
    NREL Heat pump model
    """

    def __init__(self):
        super().__init__()

        self.parameters['script_dir'] = os.path.dirname(__file__)
        self.parameters['yaml_file_path'] = os.path.join(self.parameters['script_dir'],
                                                         'NREL_components',
                                                         'heat_pump_model_inputs.yml')
        self._load_yaml_parameters(
            self.parameters['yaml_file_path'])  # load yaml content into a dict

        self.model = HeatPumpModel()  # instantiate the heat pump from NREL
        self.model.construct_yaml_input_quantities(self.parameters['yaml_file_path'])
        self.model.carnot_efficiency_factor = Q_('0.55')
        self.model.carnot_efficiency_factor_flag = False

    def update_parameters(self, parameters):
        """ To update model parameters

        Parameters
        ----------
        parameters: dict
            parameters dict as defined by the model
        """
        for key, value in parameters.items():
            self.parameters[key] = value

        self.model.refrigerant = self.parameters['refrigerant']

    def initialize_state(self, x):
        """ generate an initial state based on user parameters
         """
        pass

    def calculate_output(self):
        self.model.hot_temperature_desired = Q_(
            np.array([self.input['hot_temperature_desired']]), 'degC')
        self.model.hot_temperature_minimum = Q_(
            np.array([self.input['hot_temperature_return']]), 'degC')
        self.model.cold_temperature_available = Q_(
            np.array([self.input['cold_temperature_available']]), 'degC')
        self.model.cold_deltaT = Q_(
            np.array([self.input['cold_deltaT']]), 'delta_degC')
        self.model.process_heat_requirement = Q_(
            np.array([self.input['process_heat_requirement']]), 'W')
        self.model.hot_mass_flowrate = Q_(
            np.array([self.input['hot_mass_flowrate']]), 'kg/s')

        self.model.run_simulation()

        self.output['electricity_power_in'] = self.model.power_in.m
        self.output['hot_mass_flow_rate'] = self.model.hot_mass_flowrate.m
        self.output['cold_mass_flow_rate'] = self.model.cold_mass_flowrate.m
        self.output['actual_COP'] = self.model.actual_COP.m
        self.output['cold_temperature_return'] = self.model.cold_final_temperature.m

    def _load_yaml_parameters(self, yaml_file_path):
        """"
        Load a yaml file into a self.parameters dictionary

        """
        with open(yaml_file_path, 'r') as file:
            yaml_parameters = yaml.safe_load(file)

        for key in yaml_parameters.keys():
            self.parameters[key] = yaml_parameters[key]
