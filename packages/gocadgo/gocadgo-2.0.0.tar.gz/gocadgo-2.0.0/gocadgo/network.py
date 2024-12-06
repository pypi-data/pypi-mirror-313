import numpy as np
import json
from helper import set_boundary, set_initial, validate_config
import cantera as ct

class Network:
    def __init__(self, path_to_config = 'config.json', k:dict = None):
        """
        Create a network object representing a heat exchanger.
        Parameters
        ----------
        dims: list of [width, height, length] dimensions (by an integer number of elements)
        boundary : starting conditions, set by the set_boundary function
        """
        self.config = self.load_config(path_to_config)

        try:
            validate_config(self.config)
        except ValueError as e:
            print(f"Validation error: {e}")

        self.hnet, self.cnet = self.create_network()

        if k == None:
            self.k = {}
            self._get_k_t()
            self._get_k_p()
        else:
            self.k = k

        self.run_network()

    def load_config(self, path_to_config):
        with open(path_to_config, 'r') as file:
            config_data = json.load(file)
            print(config_data)
        return config_data

    def create_network(self):
        """
        Instantiate a network with the correct initial conditions
        Returns
        -------

        """
        def create_single_network(name):
            ix_s = 0
            if name == "hot":
                ix_s == 1
            elif name == "cold":
                ix_s == -2
            else:
                raise TypeError("Network name in json not recognised!")
            #Populate entire fields with initial conditions:
            # Initialize the network dictionary row by row
            network = {}

            # Initialize each key in `key_list` with values from `self.config`
            network["T"] = np.full(self.config["sim"]["dimensions"], self.config[name]["i"][0])  # Temperature
            network["P"] = np.full(self.config["sim"]["dimensions"], self.config[name]["i"][1])  # Pressure
            network["m"] = np.full(self.config["sim"]["dimensions"], self.config[name]["i"][2])  # Mass flow rate

            # Set second-row conditions (temperature and pressure)
            network["T"][:, :, ix_s] = self.config[name]["s"][0]  # Second row temperature
            network["P"][:, :, ix_s] = self.config[name]["s"][1]  # Second row pressure

            # Normalise the initial mass flow rate across all cells:
            network["m"] /= (self.config["sim"]["dimensions"][0] * self.config["sim"]["dimensions"][1])

            # Determine the gas type:
            if self.config[name]["gas_type"] in ["N2", "nitrogen", "Nitrogen"]:
                gas = ct.Nitrogen()
                print(f"{gas} - N2 network creating!")
            elif self.config[name]["gas_type"] in ["air", "Air"]:
                gas = ct.Solution('air.yaml')
                print(f"{gas} - Air network creating!")
            else:
                raise ValueError(f"Unknown gas type: {self.config[name]['gas_type']}")
            # Set initial gas state using initial T and P
            network["gas"] =  np.full(self.config["sim"]["dimensions"], gas)
            gas.TP = self.config[name]["i"][0], self.config[name]["i"][1]

            # Initialize `c_p` and `rho` arrays with the initial values
            initial_cp = gas.cp_mass / 1000  # Convert J/kg·K to kJ/kg·K if needed
            initial_rho = gas.density

            network["c_p"] = np.full(self.config["sim"]["dimensions"], initial_cp)  # Specific heat capacity
            network["rho"] = np.full(self.config["sim"]["dimensions"], initial_rho)  # Density
            # Compute `c_p` and `rho` for the second row only ([:, :, 1])
            for x in range(self.config["sim"]["dimensions"][0]):  # Iterate through x-dimension
                for y in range(self.config["sim"]["dimensions"][1]):  # Iterate through y-dimension
                    # Set gas state based on T and P in the second row
                    gas.TP = network["T"][x, y, ix_s], network["P"][x, y, ix_s]
                    # Compute and store c_p and rho for the second row
                    network["c_p"][x, y, ix_s] = gas.cp_mass / 1000  # Convert J/kg·K to kJ/kg·K
                    network["rho"][x, y, ix_s] = gas.density
            gas()
            return network

        # Create the hot and cold networks
        hnet = create_single_network("hot")
        cnet = create_single_network("cold")

        return hnet, cnet

    def _get_k_t(self):
        """
        Temperature constant for the system is as follows:
        k_t = (T_1(H) - T_0(H)) * m_dot(H) * c_p(H) /((T_0(H) - T_0(C))
        k_t = (T_1(C) - T_0(C)) * m_dot(C) * c_p(C) /((T_0(H) - T_0(C))

        Order of indexing in config sheets must match to "key_list": ["T", "P", "m"]
        Returns
        -------
        """
        self.k["k_t_c"] = (self.config["cold"]["s"][0] - self.config["cold"]["i"][0]) * self.config["cold"]["i"][2] * \
                          self.cnet["c_p"][0,0, 0] / (self.config["hot"]["i"][0] - self.config["cold"]["i"][0])
        self.k["k_t_h"] = (self.config["hot"]["s"][0] - self.config["hot"]["i"][0]) * self.config["hot"]["i"][2] * \
                          self.cnet["c_p"][0, 0, 0] / (self.config["hot"]["i"][0] - self.config["cold"]["i"][0])

    def _get_k_p(self):
        """

        Pressure constant for the system is as follows:
        k_p = (P_1(C) - P_0(C)) / rho_1(C) * m_dot(C)
        k_p = (P_1(H) - P_0(H)) / rho_1(H) * m_dot(H)

        Order of indexing in config sheets must match to "key_list": ["T", "P", "m"]
        Returns
        -------
        """
        self.k["k_p_c"] = (self.config["cold"]["s"][1] - self.config["cold"]["i"][1]) / (
                    self.cnet["rho"][0,0, 0] * self.config["cold"]["i"][2])
        self.k["k_p_h"] = (self.config["hot"]["s"][1] - self.config["hot"]["i"][1]) / (
                self.hnet["rho"][0, 0, 0] * self.config["hot"]["i"][2])


    def _inc_T(self, h_i, c_i):
        """
        Forward iteration on a slice of network for T

        Parameters
        ----------
        z: int
            The current z-plane index for the iteration.

        Returns
        -------
        2D array of temperature values for the next z-plane in both h and c networks.
        """
        # Calculate the temperature increment for both h and c networks
        T_increment_h = self.k["k_t_h"] * (self.hnet["T"][:, :, h_i - 1] - self.cnet["T"][:, :, h_i - 1]) / (self.hnet["m"][:, :, h_i - 1] - self.hnet["c_p"][:, :, h_i - 1])
        T_increment_c = self.k["k_t_c"] * (self.hnet["T"][:, :, c_i + 1] - self.cnet["T"][:, :, c_i + 1]) / (self.cnet["m"][:, :, c_i + 1] - self.cnet["c_p"][:, :, c_i + 1])
        return T_increment_h, T_increment_c

    def _inc_P(self, h_i, c_i):
        """
        Forward iteration on a slice of network for P
        Parameters
        ----------
        h_i
        c_i

        Returns
        -------

        """

        P_increment_h = self.k["k_p_h"] * (self.hnet["m"][:, :, h_i - 1] - self.hnet["rho"][:, :, h_i - 1])
        P_increment_c = self.k["k_p_c"] * self.cnet["m"][:, :, c_i + 1] - self.cnet["rho"][:, :, c_i + 1]
        return P_increment_h, P_increment_c

    def update_prop(self, network):
        """
        Updating cp and rho for all cells
        Returns
        -------
        """
        for x in range(self.config["sim"]["dimensions"][0]):  # Iterate through x-dimension
            for y in range(self.config["sim"]["dimensions"][1]):  # Iterate through y-dimension
                for z in range(self.config["sim"]["dimensions"][2]):  # Iterate through z-dimension (if 3D)

                    # Get the gas object for the current cell
                    gas_cell = network["gas"][x, y, z]  # Access the ct.Solution object for this cell

                    # Set the gas state (temperature and pressure) for the current cell
                    gas_cell.TP = network["T"][x, y, z], network["P"][x, y, z]

                    # Compute the specific heat capacity (c_p) and density (rho) for the current cell
                    network["c_p"][x, y, z] = gas_cell.cp_mass / 1000  # Convert J/kg·K to kJ/kg·K if needed
                    network["rho"][x, y, z] = gas_cell.density
    def run_network(self):
        for h_i, c_i in zip(list(range(2, 20)), list(range(18, -1, -1))):
            print(f"incrementing temperature for row {h_i}")
            increment_T_h, increment_T_c = self._inc_T(h_i, c_i)
            increment_P_h, increment_P_c = self._inc_P(h_i, c_i)

            # Update the temperature values for hnet and cnet
            self.hnet["T"][:, :, h_i] = self.hnet["T"][:, :, h_i - 1] + increment_T_h  # Add increment to previous value
            self.cnet["T"][:, :, c_i] = self.cnet["T"][:, :, c_i - 1] + increment_T_c  # Add increment to previous value

            # Update the pressure values for hnet and cnet
            print(f"incrementing pressure for row {h_i}")
            self.hnet["P"][:, :, h_i] = self.hnet["P"][:, :, h_i - 1] - increment_P_h  # Add increment to previous value
            self.cnet["P"][:, :, c_i] = self.cnet["P"][:, :, c_i - 1] - increment_P_c  # Add increment to previous value

            # Update other properties
            print(f"update other properties for row {h_i}")
            self.update_prop(self.hnet)
            self.update_prop(self.cnet)

