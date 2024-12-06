# external imports
import warnings


class Parameter:
    """
    The Parameter class represents a parameter with a name and a value.

    Attributes:
    -----------
        - name (str) : Name of the parameter.
        - value () : Value associated with the parameter.

    Methods:
    --------
        - __init__(self, name, value) : Initializes a Parameter object with a name and value.
        - get_name(self) : Returns the name of the parameter.
        - get_value(self) : Returns the value associated with the parameter.
        - set_value(self, new_value) : Sets a new value for the parameter.
    """

    def __init__(self, name, value) -> None:
        """
        Initializes a Parameter object with a name and value.

        Parameters:
        -----------
            - name (str) : Name of the parameter.
            - value () : Value associated with the parameter.
        """
        self.name: str = name
        self.value = value
        self.disable_warnings = False

        @property
        def name(self):
            return self.__name

        name.setter

        def name(self, value):
            if not isinstance(value, str):
                raise ValueError(f"Invalid value for 'name': {value}")
            self.__name = value

        @property
        def value(self):
            return self.__value

        value.setter

        def value(self, value):
            self.__value = value

    def get_name(self) -> str:
        """
        Returns the name of the parameter.

        Returns:
        --------
            - str : Name of the parameter.
        """
        return self.name

    def get_value(self):
        """
        Returns the value associated with the parameter.

        Returns:
        --------
            - value () : Value associated with the Parameter.
        """
        return self.value

    def set_value(self, new_value) -> None:
        """
        Sets a new value for the parameter.

        Parameters:
        -----------
            - new_value (bool or any): The new value to be set for the parameter.
        """
        self.value = new_value


class PDFParameter:
    r"""
    The PDFParameter class represents the parameters for the Pair Distribution Functions.

    Attributes:
    -----------
        - nbins (int) : Number of bins in the histograms.
        - rmax (float) : Maximum distance of the distribution.
        - disable_warnings (bool) : Disable the warnings.


    """

    def __init__(self, nbins: int, rmax: float) -> None:
        self.nbins: int = nbins
        self.rmax: float = rmax
        self.disable_warnings: bool = False

    def get_nbins(self) -> int:
        """
        Return the number of bins in the histograms.

        Returns:
        --------
            - int : Number of bins in the histograms.
        """
        return self.nbins

    def get_rmax(self) -> float:
        """
        Return the maximum distance of the distribution.

        Returns:
        --------
            - float : Maximum distance of the distribution.
        """
        return self.rmax

    def set_nbins(self, new_nbins: int) -> None:
        """
        Set a new value for the number of bins in the histograms.
        """
        if new_nbins < 1:
            raise ValueError(f"Invalid value for 'nbins': {new_nbins}")
        else:
            self.nbins = new_nbins

    def set_rmax(self, new_rmax: float) -> None:
        """
        Set a new value for the maximum distance of the distribution.

        Parameters:
        -----------
            - new_rmax (float) : New value for the maximum distance of the distribution.
        """
        if new_rmax < 0:
            raise ValueError(f"Invalid value for 'rmax': {new_rmax}")
        else:
            self.rmax = new_rmax

    def check_rmax(self, box, configuration) -> None:
        """
        Set the maximum distance of the distribution to half the box size if the distance is superior to this value.
        """
        lbox = box.get_box_dimensions(configuration)[
            0
        ]  # NOTE: We assume that the box is cubic.
        if self.rmax > lbox / 2:
            if not self.disable_warnings:
                warnings.warn(
                    f"rmax is superior to half the box size. rmax is set to {lbox / 2}.",
                    UserWarning,
                )
            self.rmax = lbox / 2


class BADParameter:
    r"""
    The BADParameter class represents the parameters for the Bond Angular Distribution.

    Attributes:
    -----------
        - nbins (int) : Number of bins in the histograms.
        - theta_max (float) : Maximum angle of the distribution.
        - disable_warnings (bool) : Disable the warnings.
    """

    def __init__(self, nbins: int, theta_max: float) -> None:
        self.nbins: int = nbins
        self.theta_max: float = theta_max
        self.disable_warnings: bool = False

    def get_nbins(self) -> int:
        """
        Return the number of bins in the histograms.
        """
        return self.nbins

    def get_theta_max(self) -> float:
        """
        Return the maximum angle of the distribution.
        """
        return self.theta_max

    def set_nbins(self, new_nbins: int) -> None:
        """
        Set a new value for the number of bins in the histograms.
        """
        if new_nbins < 1:
            raise ValueError(f"Invalid value for 'nbins': {new_nbins}")
        else:
            self.nbins = new_nbins

    def set_theta_max(self, new_theta_max: float) -> None:
        """
        Set a new value for the maximum angle of the distribution.
        """
        if new_theta_max < 0:
            raise ValueError(f"Invalid value for 'theta_max': {new_theta_max}")
        elif new_theta_max > 180:
            raise ValueError(f"Invalid value for 'theta_max': {new_theta_max}")
        else:
            self.theta_max = new_theta_max


class MSDParameter:
    r"""
    The MSDParameter class represents the parameters for the Mean Square Displacement.

    Attributes:
    -----------
        - dt (float) : Time step.
        - printlevel (int) : Print level.
    """

    def __init__(self, dt: float, printlevel: int) -> None:
        self.dt: float = dt
        self.printlevel: int = printlevel

    def get_dt(self) -> float:
        """
        Return the time step.
        """
        return self.dt

    def get_printlevel(self) -> int:
        """
        Return the print level.
        """
        return self.printlevel

    def set_dt(self, new_dt: float) -> None:
        """
        Set a new value for the time step.
        """
        if new_dt < 0:
            raise ValueError(f"Invalid value for 'dt': {new_dt}")
        else:
            self.dt = new_dt

    def set_printlevel(self, new_printlevel: int) -> None:
        """
        Set a new value for the print level.
        """
        if new_printlevel <= 0:
            raise ValueError(f"Invalid value for 'printlevel': {new_printlevel}")
        else:
            self.printlevel = new_printlevel

    def return_duration(self, number_of_frames) -> float:
        """
        Return the duration of the simulation.
        """
        return number_of_frames * self.dt * self.printlevel

