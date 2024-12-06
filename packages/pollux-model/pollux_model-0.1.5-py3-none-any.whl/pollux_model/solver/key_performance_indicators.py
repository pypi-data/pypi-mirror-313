import numpy as np


class Objective:
    def __init__(self, solver, scaling_factor):
        self.inputs = {}  # dictionary to store inputs of each component over time
        self.solver = solver
        self.scaling_factor = scaling_factor

        return

    def kpi_rmse_power_demand(self, control_scaled):
        control = [(control_scaled[ii] * self.scaling_factor[ii])
                   for ii in range(len(control_scaled))]
        self.solver.run(control)
        power_demand_outputs = self.solver.outputs[self.solver.components["power_demand"]]
        power_demand = [row[0] for row in power_demand_outputs]
        splitter1_outputs = self.solver.outputs[self.solver.components["splitter1"]]
        power_delivered = [row[0] for row in splitter1_outputs]
        kpi_rmse_power_demand = rmse(power_demand, power_delivered) / 1E6  # MW

        print(kpi_rmse_power_demand)

        return kpi_rmse_power_demand

    def kpi_rmse_hydrogen_demand(self, control_scaled):
        control = [(control_scaled[ii] * self.scaling_factor[ii])
                   for ii in range(len(control_scaled))]
        self.solver.run(control)
        hydrogen_demand_outputs = self.solver.outputs[self.solver.components["hydrogen_demand"]]
        hydrogen_demand = [row[0] * 3600 for row in hydrogen_demand_outputs]
        adder_outputs = self.solver.outputs[self.solver.components["adder"]]
        hydrogen_delivered = [row[0] * 3600 for row in adder_outputs]
        kpi_rmse_hydrogen_demand = rmse(hydrogen_demand, hydrogen_delivered)  # kg/hr
        kpi_rmse_hydrogen_demand = 0.03333 * kpi_rmse_hydrogen_demand  # MW
        print(kpi_rmse_hydrogen_demand)

        return kpi_rmse_hydrogen_demand

    def kpi_rmse_demand(self, control_scaled):
        control = [(control_scaled[ii] * self.scaling_factor[ii])
                   for ii in range(len(control_scaled))]

        self.solver.run(control)
        power_demand_outputs = self.solver.outputs[self.solver.components["power_demand"]]
        power_demand = [row[0] * 1E-6 for row in power_demand_outputs]
        splitter1_outputs = self.solver.outputs[self.solver.components["splitter1"]]
        power_delivered = [row[0] * 1E-6 for row in splitter1_outputs]
        kpi_rmse_power_demand = rmse(power_demand, power_delivered)  # MW

        hydrogen_demand_outputs = self.solver.outputs[self.solver.components["hydrogen_demand"]]
        hydrogen_demand = [row[0] * 3600 for row in hydrogen_demand_outputs]
        adder_outputs = self.solver.outputs[self.solver.components["adder"]]
        hydrogen_delivered = [row[0] * 3600 for row in adder_outputs]
        kpi_rmse_hydrogen_demand = rmse(hydrogen_demand, hydrogen_delivered)  # kg/hr

        # Convert kpi_rmse_hydrogen_demand from kg/hr to MW=MJ/s
        # Power (MW)=0.03333×hydrogen consumption rate (kg/hr)
        kpi_rmse_hydrogen_demand = 0.03333 * kpi_rmse_hydrogen_demand  # MW
        # kpi_rmse_hydrogen_demand = 1.0*kpi_rmse_hydrogen_demand  # MW

        kpi_rmse_demand = kpi_rmse_power_demand + kpi_rmse_hydrogen_demand

        print(kpi_rmse_demand, kpi_rmse_power_demand, kpi_rmse_hydrogen_demand)

        return kpi_rmse_demand

    def kpi_rmse_demand_storage_penalty(self, control_scaled):
        control = [(control_scaled[ii] * self.scaling_factor[ii])
                   for ii in range(len(control_scaled))]

        self.solver.run(control)
        power_demand_outputs = self.solver.outputs[self.solver.components["power_demand"]]
        power_demand = [row[0] * 1E-6 for row in power_demand_outputs]
        splitter1_outputs = self.solver.outputs[self.solver.components["splitter1"]]
        power_delivered = [row[0] * 1E-6 for row in splitter1_outputs]
        kpi_rmse_power_demand = rmse(power_demand, power_delivered)  # MW

        hydrogen_demand_outputs = self.solver.outputs[self.solver.components["hydrogen_demand"]]
        hydrogen_demand = [row[0] * 3600 for row in hydrogen_demand_outputs]
        adder_outputs = self.solver.outputs[self.solver.components["adder"]]
        hydrogen_delivered = [row[0] * 3600 for row in adder_outputs]
        kpi_rmse_hydrogen_demand = rmse(hydrogen_demand, hydrogen_delivered)  # kg/hr

        hydrogen_storage_outputs = self.solver.outputs[self.solver.components["hydrogen_storage"]]
        # hydrogen_storage_mass_flow_out = [row[2]*3600 for row in hydrogen_storage_outputs]
        # hydrogen_storage_mass_flow_out_max = 0.01 *\
        # np.max(np.array(hydrogen_storage_mass_flow_out))

        fill_level = [row[1] * 100 for row in hydrogen_storage_outputs]
        fill_level_max = 0.1 * np.max(np.array(fill_level))

        # Convert kpi_rmse_hydrogen_demand from kg/hr to MW=MJ/s
        # Power (MW)=0.03333×hydrogen consumption rate (kg/hr)
        kpi_rmse_hydrogen_demand = 0.03333 * kpi_rmse_hydrogen_demand  # MW

        # kpi_rmse_demand = kpi_rmse_power_demand + kpi_rmse_hydrogen_demand +\
        # hydrogen_storage_mass_flow_out_max
        # print( kpi_rmse_demand, kpi_rmse_power_demand, kpi_rmse_hydrogen_demand,\
        # hydrogen_storage_mass_flow_out_max)

        kpi_rmse_demand = kpi_rmse_power_demand + kpi_rmse_hydrogen_demand + fill_level_max
        print(kpi_rmse_demand, kpi_rmse_power_demand, kpi_rmse_hydrogen_demand, fill_level_max)

        return kpi_rmse_demand


"""     # COP: coefficient of performance
    def kpi_COP(self, control_scaled):
        control = [(control_scaled[ii] * self.scaling_factor[ii])
            for ii in range(len(control_scaled))]

        self.solver.run(control)
        power_supply_outputs = self.solver.outputs[self.solver.components["power_supply"]]
        power_supply = [row[0] * 1E-6 for row in power_supply_outputs]
        power_demand_outputs = self.solver.outputs[self.solver.components["power_demand"]]
        power_demand = [row[0] * 1E-6 for row in power_demand_outputs]  # MW
        splitter1_outputs = self.solver.outputs[self.solver.components["splitter1"]]
        power_delivered = [row[0] * 1E-6 for row in splitter1_outputs]
        electrolyser_power_input = [row[1] * 1E-6 for row in splitter1_outputs]  # output_1, MW

        electrolyser_outputs = self.solver.outputs[self.solver.components["electrolyser"]]
        hydrogen_electrolyser_mass_flow_out= [row[3]*3600 for row in electrolyser_outputs]

        hydrogen_demand_outputs = self.solver.outputs[self.solver.components["hydrogen_demand"]]
        hydrogen_demand = [row[0]*3600 for row in hydrogen_demand_outputs]  # kg/hr
        adder_outputs = self.solver.outputs[self.solver.components["adder"]]
        hydrogen_delivered = [row[0]*3600 for row in adder_outputs] #kg/hr

        # Convert kpi_rmse_hydrogen_demand from kg/hr to MW=MJ/s
        # Power (MW)=0.03333 x hydrogen consumption rate [kg/hr]

        # power_supply_sum = sum(power_supply)
        # delivered_sum = sum(power_delivered) + 0.03333*sum(hydrogen_delivered)
        # COP = delivered_sum/power_supply_sum

        electrolyser_power_input_sum = sum(electrolyser_power_input)
        hydrogen_electrolyser_mass_flow_out_sum = 0.03333 * sum(hydrogen_electrolyser_mass_flow_out)
        COP = hydrogen_electrolyser_mass_flow_out_sum/electrolyser_power_input_sum
        print(-COP)

        return -COP """


# root mean square error
def rmse(profile1, profile2):
    profile1 = np.array(profile1)
    profile2 = np.array(profile2)
    rmse = np.sqrt(np.mean((profile1 - profile2) ** 2))

    return rmse
