from pollux_model.model_abstract import Model
import numpy as np
from thermo.chemical import Chemical
from scipy.optimize import root_scalar


# import math


class ElectrolyserDeGroot(Model):
    """ Abstract base class for simulation models

        Model classes implement a discrete state space model
        The state of the model is maintained outside the model object
    """

    def __init__(self):
        """ Model initialization
        """
        super().__init__()
        # PVT properties of H2, O2 and water at current pressure and temperature.
        self.parameters['T_cell'] = 273.15 + 40  # cell temperature in K
        self.parameters['p_cathode'] = 10e5  # cathode pressure in Pa
        self.parameters['p_anode'] = 10e5  # anode pressure in Pa
        self.parameters['p_0_H2O'] = 10e5  # Pa

    def update_parameters(self, parameters):
        """ To update model parameters

        Parameters
        ----------
        parameters : dict
            parameters dict as defined by the model
        """
        for key, value in parameters.items():
            self.parameters[key] = value

        if self.parameters['cell_type'] == 'alk_ref_cell':
            self.parameters['power_single_cell'] = 6222
        elif self.parameters['cell_type'] == 'low_power_cell':
            self.parameters['power_single_cell'] = 4000
        elif self.parameters['cell_type'] == 'medium_power_cell':
            self.parameters['power_single_cell'] = 10000
        elif self.parameters['cell_type'] == 'high_power_cell':
            self.parameters['power_single_cell'] = 16000

        self.parameters['N_cells'] = np.ceil(self.parameters['capacity']
                                             / self.parameters['power_single_cell'])

        # PVT properties of H2, O2 and water at current pressure and temperature.
        self.PVT_H2 = Chemical('hydrogen')
        self.PVT_O2 = Chemical('oxygen')
        self.PVT_H2O = Chemical('water')

        self.PVT_H2.calculate(T=self.parameters['T_cell'], P=self.parameters['p_cathode'])
        self.PVT_O2.calculate(T=self.parameters['T_cell'], P=self.parameters['p_anode'])
        self.PVT_H2O.calculate(T=self.parameters['T_cell'], P=self.parameters['p_0_H2O'])

    def initialize_state(self, x):
        """ generate an initial state based on user parameters """
        pass

    def calculate_output(self):
        """calculate output based on input"""

        self._calc_prod_rates()

    def _calc_prod_rates(self):
        power_input = self.input['power_input']
        self.parameters['power_cell_real'] = power_input / self.parameters[
            'N_cells']  # * self.power_multiplier
        # todo: the power multiplier
        # can be extended to include active and non active stacks,
        # for now just give the independent stacks

        # self._calc_i_cell() PJPE: check
        # wteta faraday assume to be constant
        # Production rates [mol/s]

        I_cell_array = self._calc_i_cell()

        # This could be faster and more robust
        # A_cell = self.parameters['A_cell']
        # power_cell_real = self.parameters['power_cell_real']
        # I_cell_array = self._calc_i_cell_optimized(A_cell, power_cell_real)

        self.output['prod_rate_H2'] = (self.parameters['N_cells']) * I_cell_array / (
                2 * self.parameters['Faraday_const']) * self.parameters['eta_Faraday_array']
        self.output['prod_rate_O2'] = (self.parameters['N_cells']) * I_cell_array / (
                4 * self.parameters['Faraday_const']) * self.parameters['eta_Faraday_array']
        self.output['prod_rate_H2O'] = (self.parameters['N_cells']) * I_cell_array / (
                2 * self.parameters['Faraday_const'])

        # Massflows [kg/s].
        self.output['massflow_H2'] = self.output['prod_rate_H2'] * self.PVT_H2.MW * 1e-3
        self.output['massflow_O2'] = self.output['prod_rate_O2'] * self.PVT_O2.MW * 1e-3
        self.output['massflow_H2O'] = self.output['prod_rate_H2O'] * self.PVT_H2O.MW * 1e-3

        # Densities [kg/m^3].
        self.output['rho_H2'] = self.PVT_H2.rho
        self.output['rho_O2'] = self.PVT_O2.rho
        self.output['rho_H2O'] = self.PVT_H2O.rho

        # Flowrates [m^3/s].
        self.output['flowrate_H2'] = self.output['massflow_H2'] / self.output['rho_H2']
        self.output['flowrate_O2'] = self.output['massflow_O2'] / self.output['rho_O2']
        self.output['flowrate_H2O'] = (self.output['massflow_H2O'] /
                                       self.output['rho_H2O'])

        # Integrate massflows to obtain masses of H2, O2 and H20 in this period [kg].
        # Note: it assumes constant operating conditions in the time-step
        self.output['mass_H2'] = self.output['massflow_H2'] * self.parameters['delta_t']
        self.output['mass_O2'] = self.output['massflow_O2'] * self.parameters['delta_t']
        self.output['mass_H2O'] = self.output['massflow_H2O'] * self.parameters['delta_t']

    def _calc_i_cell(self):
        I_current_sol = root_scalar(
            self._root_I_cell, bracket=[1.0, 30000],
            method='brentq',
            args=(
                self.parameters['power_cell_real'],
            )
        )
        return I_current_sol.root

    # simpler (and more robust) approximation
    # def _calc_i_cell_optimized(self, A_cell, power_cell_real):
    #     # Constants
    #     a0 = 1.58119313
    #     a1 = 0.33090383

    #     # Calculations
    #     a = -a1 / (1e4 * A_cell)
    #     b = -a0
    #     c = power_cell_real

    #     # Discriminant
    #     D = b ** 2 - 4 * a * c

    #     # Check for non-negative discriminant
    #     if D >= 0:
    #         return (-b - math.sqrt(D)) / (2 * a)  # Smallest root
    #     else:
    #         raise ValueError(f"discriminant is negative ({D})")

    def _root_I_cell(self, I_cell, power_cell):
        self.state['E_total_cell'] = \
            self._compute_potentials(
                I_cell, self.parameters['A_cell'])
        root_expr = power_cell / (self.state['E_total_cell']) - I_cell
        return root_expr

    def _compute_potentials(self, I_cell, A_cell):
        # A_cell = 0.436
        I_cell_in = I_cell / 1e4 / A_cell
        # Voltage efficiency WITH COEFFICIENTS
        E_total_cel = (-0.160249069 * I_cell_in ** 4 + 0.734073995 * I_cell_in ** 3 -
                       1.168543948 * I_cell_in ** 2 + 1.048496283 * I_cell_in + 1.46667069)
        return E_total_cel
