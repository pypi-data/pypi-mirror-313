def set_initial(T=300, P=101325, m=0.1, gas_type="N2"):
    """
    A function to set the inputs for the boundary conditions (or at least the default)
    Can take custom values for T_in, P_in, etc.
    Parameters
    ----------
    T_in: initial field and inlet temperature in Kelvin
    P_in: initial field and inlet pressure in Pa
    m_in: mass flow rate for initial field and inlet kg/s
    gas_type: "N2" or "Air"
    Returns
    -------
    """
    return {
        'T': T,
        'P': P,
        'm': m,
        'gas_type': gas_type
    }

def set_boundary(P_out, T_out):
    """
    Set the values across a cell at the inlet boundary.
    Parameters
    ----------
    P_out: previous cell's values of Pa
    T_out: previous cell's values of T

    Returns
    -------

    """
    return {
        'P_out': P_out,
        'T_out': T_out,
    }

def validate_config(config):
    def validate_config(config):
        """
        Validate that the config data is valid.

        Parameters
        ----------
        config : dict
            Configuration dictionary to validate.

        Raises
        ------
        ValueError
            If the configuration is invalid.
        """
        # Validate `sim` key and `dimensions`
        if "sim" not in config or "dimensions" not in config["sim"]:
            raise ValueError("Missing 'sim' or 'dimensions' in configuration.")

        dimensions = config["sim"]["dimensions"]
        if not (isinstance(dimensions, list) and len(dimensions) == 3 and
                all(isinstance(dim, (int, float)) and dim > 0 for dim in dimensions)):
            raise ValueError("'dimensions' in 'sim' must be a list of 3 positive numbers.")

        # Validate `hot` and `cold` sections
        for section in ["cold", "hot"]:
            if section not in config:
                raise ValueError(f"Missing '{section}' section in configuration.")

            data = config[section]

            # Validate `initial_value`
            if "initial_value" not in data or not (
                    isinstance(data["i"], list) and len(data["i"]) == 3 and
                    all(isinstance(val, (int, float)) for val in data["i"])
            ):
                raise ValueError(f"'i' in section '{section}' must be a list of 3 numbers.")

            # Validate `gas_type`
            if "gas_type" not in data:
                raise ValueError(f"Missing 'gas_type' in section '{section}'.")

            gas_type = data["gas_type"]
            if not isinstance(gas_type, str):
                raise ValueError(f"'gas_type' in section '{section}' must be a string.")
            if gas_type not in ["air", "N2"]:
                raise ValueError(f"'gas_type' in section '{section}' must be 'air' or 'N2'.")

        print("Configuration is valid.")
