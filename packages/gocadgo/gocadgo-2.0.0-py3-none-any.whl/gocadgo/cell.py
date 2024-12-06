import cantera as ct
class Cell:
    def __init__(self, gas_type:str, T_in:float, P_in:float, m_in:float):
        """
        Class repressenting a cell in a heat exchanger.
        Parameters
        ----------
        T_in is cell inlet temperature to cell in Kelvin
        P_in is cell inlet pressure in Pa
        m_in is cell inlet mass flow rate in kg/s
        """
        if gas_type == 'N2' or 'nitrogen':
            self.gas = ct.Nitrogen()
        if gas_type == 'Air' or 'air':
            self.gas = ct.Solution('air.yaml')
        else:
            raise ValueError(f'gas type {gas_type} not supported')

        self.T_in = T_in
        self.P_in = P_in
        self.m_in = m_in

        self.gas.TP = T_in, P_in
        self._cp = self.gas.cp_mass

    # def __repr__(self):
    #     """
    #     String representation of the cell.
    #     Returns
    #     -------
    #
    #     """
    #     return f"Cell(Cp = {self._cp}, Heat Loss ={self.calc_cell_p}, Pressure Loss={self.calc_cell_q})"


    @property
    def P_out(self, P_prev):
        """
        Heat loss is defined as Q = m * Cp * delta T.
        Parameters
        ----------
        T_in
        T_out

        Returns
        -------
        """
        self.P_out = self.cp * P_prev * self.T_in

    @property
    def T_out(self, Q_prev):
        """
        Heat loss is defined as Q = m * Cp * delta T.
        Parameters
        ----------
        T_in
        T_out

        Returns
        -------
        """
        self.T_out = self.cp * Q_prev * self.T_in

    def calc_cell_q(self):
        """
        Heat loss is defined as Q = m * Cp * delta T.
        Parameters
        ----------
        T_in
        T_out

        Returns Q_prev
        -------
        """
        return self.m_in * self.cp * (self.T_in - self.T_out)

    def calc_cell_p(self):
        """
        Pressure loss can be calculated by Darcy-Weisbach, actually removing the effect of turbulence, friction etc we assume density proportionality
        Parameters
        ----------
        Returns P_prev
        -------
        """
        return self.p_factor * self.gas.density_mass

    @property
    def p_factor(self):
        """

        Returns
        -------

        """
        self.p_factor = (self.P_out - self.P_in) / self.gas.density_mass


class StartCell(Cell):
    """
    Class representing the starting cell in a heat exchanger where outlet properties are known.
    """
    def __init__(self, gas_type:str, T_in:float, P_in:float, m_in:float, T_out:float, P_out:float):
        super().__init__(gas_type, T_in, P_in, m_in)

    @property
    def P_out(self, P_out):
        """
        Override P_out setter from Cell class.
        Parameters
        ----------
        P_out

        Returns
        -------

        """
        self.P_out = P_out
    @property
    def T_out(self, T_out):
        """
        Override T_out setter from Cell class.
        Parameters
        ----------
        T_in
        T_out

        Returns
        -------
        """
        self.T_out = T_out

