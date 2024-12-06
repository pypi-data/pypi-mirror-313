# external imports
import numpy as np
import os

# internal imports
from .make_lines_unique import make_lines_unique


class Result:
    """
    Represents a generic results.

    Attributes
    ----------
        - property (str) : The structural property name.
        - info (str) : Additional informations about the property.
        - init_frame (int) : The initial frame number.
        - timeline (dict) : The timeline of the property.
        - result (float) : The final result averaged over the number of frames.
        - error (float) : The error of the final result.
    """

    def __init__(self, property: str, info: str, init_frame: int) -> None:
        """
        Initialize the Result object.

        Parameters
        ----------
            - property (str) : The structural property name.
            - info (str) : Additional informations about the property.
            - init_frame (int) : The initial frame number.
        """
        self.property: str = property
        self.info: str = info
        self.init_frame: int = init_frame
        self.timeline: dict = {}  # keys are the frame number and values are the property value
        self.result: float = 0.0
        self.error: float = 0.0


class DistResult(Result):
    """
    Represents a Distribution result.

    Attributes
    ----------
        - property (str) : The structural property name.
        - info (str) : Additional informations about the property.
        - init_frame (int) : The initial frame number.
        - timeline (dict) : The timeline of the property.
        - result (float) : The final result averaged over the number of frames.
        - error (float) : The error of the final result.
        - bins (np.ndarray) : The bins of the histogram.
        - histogram (np.ndarray) : The histogram of the property.
        - filepath (str) : the path to the output file.
    """

    def __init__(self, name: str, info: str, init_frame: int) -> None:
        """
        Initialize the DistResult object.

        Parameters
        ----------
            - name (str) : The structural property name.
            - info (str) : Additional informations about the property.
            - init_frame (int) : The initial frame number.
        """
        super().__init__(name, info, init_frame)
        self.bins: np.ndarray = np.array([])
        self.histogram: np.ndarray = np.array([])
        self.error: np.ndarray = np.array([])
        self.result: np.ndarray = np.array([])
        self.filepath: str = ""

    def add_to_timeline(self, frame: int, bins: np.array, hist: np.array) -> None:
        """
        Appends a data point to the timeline.
        """
        self.bins = bins
        self.timeline[frame] = hist

    def calculate_average_distribution(self) -> None:
        """
        Calculates the average distribution based on the timeline data.
        """
        for frame, array in self.timeline.items():
            self.error = np.zeros((len(self.timeline), len(array)))
            break

        for frame, array in self.timeline.items():
            if len(self.timeline) > 1:
                i = frame - self.init_frame
                self.error[i] = array
            if len(self.histogram) == 0:
                # Initialize histogram ndarray
                self.histogram = array
            else:
                self.histogram += array

        if len(self.timeline) > 1:
            self.error = np.std(self.error, axis=0) / np.sqrt(len(self.timeline))
        else:
            self.error = np.zeros_like(self.histogram)

        self.result = self.histogram / len(self.timeline)

    def write_file_header(self, path_to_directory: str, number_of_frames: int) -> None:
        """
        Initializes the output file with a header.

        Parameters:
        -----------
            - path_to_directory (str) : The path to the output directory.
            - number_of_frames (int) : The number of frames in the trajectory used in the averaging.
        """
        filename = f"{self.property}-{self.info}.dat"
        if not os.path.exists(path_to_directory):
            os.makedirs(path_to_directory)

        self.filepath = os.path.join(path_to_directory, filename)

        with open(self.filepath, "w") as output:
            output.write(
                f"# {self.property} {self.info} \u279c {number_of_frames} frames averaged.\n"
            )
            # TODO add more information to the header such as the cutoff values, etc. #PRIO2
        output.close()

    def append_results_to_file(self) -> None:
        """
        Appends the results to the output file.
        """
        with open(self.filepath, "a") as output:
            for i in range(len(self.bins)):
                output.write(f"{self.bins[i]:10.6f} {self.result[i]:10.6f} +/- {self.error[i]:<10.5f}\n")
        output.close()


class PropResult(Result):
    """
    Represents a Proportion result.

    Attributes
    ----------
        - property (str) : The structural property name.
        - info (str) : Additional informations about the property.
        - init_frame (int) : The initial frame number.
        - timeline (dict) : The timeline of the property.
        - result (float) : The final result averaged over the number of frames.
        - error (float) : The error of the final result.
        - filepath (str) : the path to the output file.
    """

    def __init__(self, property: str, info: str, init_frame: int) -> None:
        super().__init__(property, info, init_frame)
        self.filepath: str = ""
        self.result: dict = {}
        self.error: dict = {}

    def add_to_timeline(self, frame: int, keys: list, values: list) -> None:
        """
        Appends a data point to the timeline.
        """
        for key, val in zip(keys, values):
            if key not in self.timeline:
                self.timeline[key] = []
            self.timeline[key].append(val)

    def calculate_average_proportion(self) -> None:
        """
        Calculates the average proportion based on the timeline data.
        """
        for key, list_value in self.timeline.items():
            self.result[key] = sum(list_value)
            self.error[key] = np.std(list_value)

        for key in self.result.keys():
            self.result[key] /= len(self.timeline[key])
            self.error[key] /= np.sqrt(len(self.timeline[key]))

    def write_file_header(self, path_to_directory: str, number_of_frames: int) -> None:
        """
        Initializes the output file with a header.

        Parameters:
        -----------
            - path_to_directory (str) : The path to the output directory.
            - number_of_frames (int) : The number of frames in the trajectory used in the averaging.
        """
        filename = f"{self.property}.dat"
        if not os.path.exists(path_to_directory):
            os.makedirs(path_to_directory)

        self.filepath = os.path.join(path_to_directory, filename)

        with open(self.filepath, "w") as output:
            output.write(
                f"# {self.property} \u279c {number_of_frames} frames averaged.\n"
            )
            # TODO add more information to the header such as the cutoff values, etc. #PRIO2
        output.close()

    def append_results_to_file(self) -> None:
        """
        Appends the results to the output file.
        """
        with open(self.filepath, 'a', encoding='utf-8') as output:
            for key in self.result.keys():
                output.write(f"{self.result[key]:10.6f} +/- {self.error[key]:<10.5f} # {key}\n")
        output.close()

        make_lines_unique(self.filepath)

class MSDResult(Result):
    r"""
    Represents a MSD Result.

    Attributes
    ----------
        - property (str) : The structural property name.
        - info (str) : Additional informations about the property.
        - init_frame (int) : The initial frame number.
        - timeline (dict) : The timeline of the property.
        - result (float) : The final result averaged over the number of frames.
        - error (float) : The error of the final result.
        - filepath (str) : the path to the output file.
    """

    def __init__(self, property: str, info: str, init_frame: int) -> None:
        super().__init__(property, info, init_frame)
        self.filepath: str = ""
        self.result: dict = {}

    def add_to_timeline(self, frame: int, values: dict):
        """
        Appends a data point to the timeline.
        """
        values_copy = values.copy() # make a copy of the values to avoid modifying the original dict
        self.timeline[frame] = values_copy
        DEBUG = False

    def calculate_average_msd(self, mass) -> None:
        r"""
        Normalizes the MSD values by their mass
        """
        for f in self.timeline.keys():
            for key, value in self.timeline[f].items():
                if f not in self.result:
                    self.result[f] = {}
                if key not in self.result[f]:
                    self.result[f][key] = 0.0
                self.result[f][key] += value / mass[key]

    def write_file_header(self, path_to_directory: str, number_of_frames: int) -> None:
        """
        Initializes the output file with a header.

        Parameters:
        -----------
            - path_to_directory (str) : The path to the output directory.
            - number_of_frames (int) : The number of frames in the trajectory used in the averaging.
        """
        filename = f"{self.property}.dat"
        if not os.path.exists(path_to_directory):
            os.makedirs(path_to_directory)

        self.filepath = os.path.join(path_to_directory, filename)

        with open(self.filepath, "w") as output:
            output.write(
                f"# {self.property} {self.info} \u279c {number_of_frames} frames averaged.\n"
            )
            # TODO add more information to the header such as the cutoff values, etc. #PRIO2
        output.close()

    def append_results_to_file(self, dt, printlevel) -> None:
        """
        Appends the results to the output file.

        Parameters:
        -----------
            - path_to_directory (str) : The path to the output directory.
        """

        with open(self.filepath, "a") as output:
            if len(self.result) > 1:
                keys = self.result[1].keys()

                output.write("#\tframe\ttime\t")
                for key in keys:
                    output.write(f"{key:^8}")
                output.write("\n")

                for f in self.result.keys():
                    output.write(f"{f:^4}\t{f*(dt/printlevel):^3.5e}\t")
                    for key, value in self.result[f].items():
                        output.write(f"{value:^3.5f} ")
                    output.write("\n")
            else:
                output.write("# trajectory too short to calculate MSD\n")

        output.close()

        DEBUG = False
