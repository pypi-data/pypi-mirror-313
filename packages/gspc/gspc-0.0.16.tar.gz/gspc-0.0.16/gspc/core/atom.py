# internal imports
from ..data import chemical_symbols, atomic_masses, correlation_lengths
from .cutoff import Cutoff
from .box import Box

# external imports
import numpy as np
import sys
from dataclasses import dataclass
from numba import njit


@dataclass
class ReferencePosition:
    r"""
    Represents a reference position of an atom in the system at the first frame.

    Attributes:
    -----------
        - position (np.array): Position of the atom.
        - element (str): Element of the atom.
        - id (int): Id of the atom.
    """

    def __init__(self, position, element, id) -> None:
        r"""
        Initializes a ReferencePosition object.

        Parameters:
        -----------
            - position (np.array): Position of the atom.
            - element (str): Element of the atom.
            - id (int): Id of the atom.
        """
        self.position: np.array = position
        self.element: str = element
        self.id: int = id

    def get_position(self) -> np.array:
        r"""
        Return the position of the atom.

        Returns:
        --------
            - np.array: Position of the atom.
        """
        return self.position

    def get_element(self) -> str:
        r"""
        Return the element of the atom.

        Returns:
        --------
            - str: Element of the atom.
        """
        return self.element

    def get_id(self) -> int:
        r"""
        Return the id of the atom.

        Returns:
        --------
            - int: Id of the atom.
        """
        return self.id


@dataclass
class CurrentPosition:
    r"""
    Represents the non-wrapped current position of an atom in the system at a given frame.

    Attributes:
    -----------
        - position (np.array): Position of the atom.
        - element (str): Element of the atom.
        - id (int): Id of the atom.
        - frame (int): Frame number.
    """

    def __init__(self, position, element, id, frame) -> None:
        r"""
        Initializes a CurrentPosition object.

        Parameters:
        -----------
            - position (np.array): Position of the atom.
            - element (str): Element of the atom.
            - id (int): Id of the atom.
            - frame (int): Frame number.
        """
        self.position: np.array = position
        self.element: str = element
        self.id: int = id
        self.frame: int = frame

    def get_position(self) -> np.array:
        r"""
        Return the position of the atom.

        Returns:
        --------
            - np.array: Position of the atom.
        """
        return self.position

    def get_element(self) -> str:
        r"""
        Return the element of the atom.

        Returns:
        --------
            - str: Element of the atom.
        """
        return self.element

    def get_id(self) -> int:
        r"""
        Return the id of the atom.

        Returns:
        --------
            - int: Id of the atom.
        """
        return self.id

    def get_frame(self) -> int:
        r"""
        Return the frame number.

        Returns:
        --------
            - int: Frame number.
        """
        return self.frame


class Atom:
    r"""
    Represents an atom within a system.

    Attributes:
    -----------
        - element (str) : Atomic element.
        - id (int) : Identifier of the atom in the system.
        - position (np.array) : XYZ coordinates.
        - frame (int) : Frame index in the trajectory.
        - cutoffs (dict) : Cutoff distances dictionary (Cutoff object).
        - extension (str) : Extension used for method determination.
        - atomic_mass (float) : Atomic mass of the atom.
        - neighbours (list) : List of first neighbours (PBC applied).
        - coordination (int) : Number of neighbours around the atom (PBC applied).

    Methods:
    --------
        - __init__ : Initializes an Atom object.
        - get_element : Returns the element of the Atom.
        - get_id : Returns the unique identifier of the Atom.
        - get_position : Returns the spatial coordinates of the Atom.
        - get_frame : Returns the frame index associated with the Atom.
        - get_neighbours : Returns the list of neighbours of the Atom.
        - get_atomic_mass : Returns the atomic mass of the Atom.
        - get_coordination : Returns the coordination number of the Atom.
        - add_neighbour : Adds a neighbour to the list of neighbours of the Atom.
        - add_direct_neighbour : Adds a neighbour to the list of direct neighbours of the Atom.
        - filter_neighbours : Removes neighbours not within cutoff distances (depending on pair of atoms).
    """

    def __init__(self, element, id, position, frame, cutoffs, extension="SiOz") -> None:
        r"""
        Initializes an Atom object with the provided information.

        Parameters:
        -----------
            - element (str): Atomic element.
            - id (int): Identifier of the atom in the system.
            - position (np.array): XYZ coordinates.
            - frame (int): Frame index in the trajectory.
            - cutoffs (dict): Cutoff distances dictionary (Cutoff object).
            - extension (str): Extension used for method determination.
        """
        # Initialize an Atom object with the provided information
        self.element: str = element  # atomic element
        self.id: int = id  # id of the atom in the system
        self.position: np.array = np.array(position)  # xyz coordinates
        self.frame: int = frame  # frame that this atom belong to in the trajectory
        self.cutoffs: Cutoff = cutoffs  # cutoffs dictionary (Cutoff object)

        # Initialize the extension so that correct methods are used.
        self.extension: str = extension

        # Initialize atomic data from the periodic table and other informations
        if self.element in chemical_symbols:
            index = np.where(self.element == chemical_symbols)[0].astype(int)
            self.atomic_mass: float = atomic_masses[index][0]
            self.correlation_length: float = correlation_lengths[index][0]
        else:
            print(f"\tERROR: Element {self.element} not found in the periodic table.")
            print(
                "\tFailed to initialize the Atom object {self.id} in the frame {self.frame}."
            )
            print("Exiting.")
            sys.exit(1)

        # Initialize neighbours attributes
        self.neighbours: list = []  # first neighbours (pbc applied)
        self.coordination: int = 0  # number of neighbours around the atom (pbc applied)
        self.long_range_neighbours: list = []  # long range neighbours (pbc applied)
        self.long_range_distances: list = []  # long range distances with long range neighbours (pbc applied)

        # Initialize the mean square displacement attributes
        self.reference_position = None  # ReferencePosition object
        self.current_position = None  # CurrentPosition object

    # ____________GETTER METHODS____________

    def get_element(self) -> str:
        r"""
        Return the element of the Atom.

        Returns:
        --------
            - str : Name of the element of the Atom.
        """
        return self.element

    def get_id(self) -> int:
        r"""
        Return the unique identifier of the Atom.

        Returns:
        --------
            - int : Index of the Atom in the frame.
        """
        return self.id

    def get_position(self) -> np.array:
        r"""
        Return the spatial coordinates of the Atom.

        Returns:
        --------
            - np.array : Cartesian coordinates of the Atom.
        """
        return self.position

    def get_frame(self) -> int:
        r"""
        Return the frame index associated with the Atom.

        Returns:
        --------
            - int : Frame index of the trajectory.
        """
        return self.frame

    def get_neighbours(self) -> list:
        r"""
        Return the list of neighbours of the Atom.

        Returns:
        --------
            - list : List of the nearest neighbours of the Atom.
        """
        return self.neighbours

    def get_atomic_mass(self) -> float:
        r"""
        Return the atomic mass of the Atom.

        Returns:
        --------
            - float : Atomic mass of the Atom.
        """
        return self.atomic_mass

    def get_coordination(self) -> int:
        r"""
        Return the coordination number of the Atom. (ie the number of first neighbours)

        Returns:
        --------
            - int : Coordination number of the Atom.
        """
        return self.coordination

    def get_long_range_neighbours(self) -> list:
        r"""
        Return the list of long range neighbours of the Atom.

        Returns:
        --------
            - list : List of the long range neighbours of the Atom.
        """
        return self.long_range_neighbours

    def get_long_range_distances(self) -> list:
        r"""
        Return the list of distances to the long range neighbours of the Atom.

        Returns:
        --------
            - list : List of the distances to the long range neighbours of the Atom.
        """
        return self.long_range_distances

    # ____________NEIGHBOURS METHODS____________

    def add_neighbour(self, neighbour) -> None:
        r"""
        Add a neighbour to the list of neighbours of the Atom.

        Parameters:
        -----------
            - neighbour (Atom) : Atom object to append to the list of neighbours.

        Returns:
        --------
            - None.
        """
        self.neighbours.append(neighbour)

    def add_long_range_neighbour(self, neighbour) -> None:
        r"""
        Add a long range neighbour to the list of neighbours of the Atom.

        Parameters:
        -----------
            - neighbour (Atom) : Atom object to append to the list of long range neighbours.

        Returns:
        --------
            - None.
        """
        self.long_range_neighbours.append(neighbour)

    def add_long_range_distance(self, distance) -> None:
        r"""
        Add the distance to a long range neighbour to the list of distances.

        Parameters:
        -----------
            - distance (float) : Distance to append to the list of distances.

        Returns:
        --------
            - None.
        """
        self.long_range_distances.append(distance)

    def filter_neighbours(self, distances) -> None:
        r"""
        Removes the neighbours that are not within the cutoff distances (depending of pair of atoms).

        Parameters:
        -----------
            - distances (list): List of distances to the neighbours.

        Returns:
        --------
            - None.
        """
        new_list_neighbours = []
        new_list_distances = []

        for k, neighbour in enumerate(self.neighbours):
            rcut = self.cutoffs.get_cutoff(self.element, neighbour.get_element())

            if isinstance(distances, float):
                # if 'distances' is a float, it means that the neighbour of this atom is itself.
                current_distance = distances
            else:
                current_distance = distances[k]

            if current_distance > rcut:  # neighbour is too far
                continue  # go next neighbour
            elif current_distance == 0:  # neighbour is this atom.
                continue  # go next neighbour
            else:
                new_list_neighbours.append(neighbour)  # keep the neighbour
                new_list_distances.append(current_distance)

        self.neighbours = new_list_neighbours

    # ------------------ Structural properties ------------------

    def calculate_angle(self, neighbour_1, neighbour_2, box: Box) -> float:
        r"""
        Calculate the angle between the atom and two neighbours.

        Parameters:
        -----------
            - neighbour_1 (Atom) : First neighbour.
            - neighbour_2 (Atom) : Second neighbour.
            - box (Box) : The simulation box.

        Returns:
        --------
            - float : Angle between the atom and the two neighbours.
        """
        box_dimensions = box.get_box_dimensions(self.frame)
        vector_1 = box.minimum_image_distance(
            box_dimensions, self.position, neighbour_1.get_position()
        )
        vector_2 = box.minimum_image_distance(
            box_dimensions, self.position, neighbour_2.get_position()
        )

        angle = np.arccos(
            np.dot(vector_1, vector_2)
            / (np.linalg.norm(vector_1) * np.linalg.norm(vector_2))
        )

        return np.degrees(angle)

    def set_reference_position(self, reference_position: ReferencePosition) -> None:
        r"""
        Set the reference position of the atom.

        Parameters:
        -----------
            - reference_position (ReferencePosition) : Reference position of the atom.

        Returns:
        --------
            - None.
        """
        self.reference_position = reference_position

    def set_current_position(self, current_position: CurrentPosition) -> None:
        r"""
        Set the current position of the atom.

        Parameters:
        -----------
            - current_position (CurrentPosition) : Current position of the atom.

        Returns:
        --------
            - None.
        """
        self.current_position = current_position

    def calculate_mean_square_displacement(self):
        r"""
        Calculate the mean squared displacement of the atom.

        Returns:
        --------
            - msd (float) : The mean squared displacement of the atom.
        """

        # get the calculate the distance between the reference position and the current position
        # without considering the pbc
        rp = self.reference_position
        cp = self.current_position

        dist = np.linalg.norm(cp.position - rp.position)

        return dist
