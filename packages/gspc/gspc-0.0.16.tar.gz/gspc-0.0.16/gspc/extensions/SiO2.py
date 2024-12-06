"""
This file contains all the methods / functions that are specific to SiO2 oxide.
"""

# external imports
import numpy as np
from tqdm import tqdm
from numba import njit

# internal imports
from ..core.atom import Atom
from ..core.box import Box
from ..utils.generate_color_gradient import generate_color_gradient


# List of supported elements for the extension SiO2
LIST_OF_SUPPORTED_ELEMENTS = ["Si", "O"]


class Silicon(Atom):
    def __init__(self, element, id, position, frame, cutoffs, extension) -> None:
        super().__init__(element, id, position, frame, cutoffs, extension)
        self.number_of_corners: int = 0
        self.number_of_edges: int = 0
        self.number_of_faces: int = 0
        self.qi_species: int = 0
        self.form: str = ""

    def get_number_of_corners(self) -> int:
        """
        Return the number of corner sharings
        """
        return self.number_of_corners

    def get_number_of_edges(self) -> int:
        """
        Return the number of edge sharings
        """
        return self.number_of_edges

    def get_number_of_faces(self) -> int:
        """
        Return the number of face sharings
        """
        return self.number_of_faces

    def get_qi_species(self) -> int:
        """
        Return the Qi species
        """
        return self.qi_species

    def get_form(self) -> str:
        """
        Return the form of the polyhedron
        """
        return self.form

    def calculate_coordination(self) -> None:
        """
        Calculate the coordination number of the atom (ie the number of first neighbours) for the extension SiO2
        """
        self.coordination = len(
            [
                neighbour
                for neighbour in self.neighbours
                if neighbour.get_element() == "O"
            ]
        )

    def calculate_angles_with_neighbours(self, box: Box) -> dict:
        r"""
        Calculate and sort the angles between the atom and its neighbours.

        Parameters:
        ----------
            - box (Box) : Box object.

        Returns:
        --------
            - dict : List of angles between the atom and its neighbours.
        """
        angles = {}
        angles_OSiO = []
        angles_SiSiSi = []

        for neighbour_1 in self.neighbours:
            for neighbour_2 in self.neighbours:
                if neighbour_1 != neighbour_2:
                    if (
                        neighbour_1.get_element() == "O"
                        and neighbour_2.get_element() == "O"
                    ):
                        angle = self.calculate_angle(neighbour_1, neighbour_2, box)
                        angles_OSiO.append(angle)
                    if (
                        neighbour_1.get_element() == "Si"
                        and neighbour_2.get_element() == "Si"
                    ):
                        angle = self.calculate_angle(neighbour_1, neighbour_2, box)
                        angles_SiSiSi.append(angle)

        angles["OSiO"] = angles_OSiO
        angles["SiSiSi"] = angles_SiSiSi

        return angles

    def calculate_distances_with_neighbours(self) -> dict:
        r"""
        Calculate and sort the distances between the atom and its neighbours.

        Returns:
        --------
            - dict : List of distances between the atom and its neighbours.
        """
        distances = {}
        distances_SiO = []
        distances_SiSi = []

        for counter, neighbour in enumerate(self.long_range_neighbours):
            if neighbour.get_element() == "O":
                distance = self.long_range_distances[counter]
                distances_SiO.append(distance)
            if neighbour.get_element() == "Si":
                distance = self.long_range_distances[counter]
                distances_SiSi.append(distance)

        distances["SiO"] = distances_SiO
        distances["SiSi"] = distances_SiSi

        return distances


class Oxygen(Atom):
    def __init__(self, element, id, position, frame, cutoffs, extension) -> None:
        super().__init__(element, id, position, frame, cutoffs, extension)

    def calculate_coordination(self) -> None:
        """
        Calculate the coordination number of the atom (ie the number of first neighbours) for the extension SiO2
        """
        self.coordination = len(
            [
                neighbour
                for neighbour in self.neighbours
                if neighbour.get_element() == "Si"
            ]
        )

    def calculate_angles_with_neighbours(self, box: Box) -> dict:
        r"""
        Calculate the angles between the atom and its neighbours.

        Parameters:
        ----------
            - box (Box) : Box object.

        Returns:
        --------
            - dict : List of angles between the atom and its neighbours.
        """
        angles = {}
        angles_SiOSi = []
        angles_OOO = []

        for neighbour_1 in self.neighbours:
            for neighbour_2 in self.neighbours:
                if neighbour_1 != neighbour_2:
                    if (
                        neighbour_1.get_element() == "O"
                        and neighbour_2.get_element() == "O"
                    ):
                        angle = self.calculate_angle(neighbour_1, neighbour_2, box)
                        angles_OOO.append(angle)
                    if (
                        neighbour_1.get_element() == "Si"
                        and neighbour_2.get_element() == "Si"
                    ):
                        angle = self.calculate_angle(neighbour_1, neighbour_2, box)
                        angles_SiOSi.append(angle)

        angles["OOO"] = angles_OOO
        angles["SiOSi"] = angles_SiOSi

        return angles

    def calculate_distances_with_neighbours(self) -> dict:
        r"""
        Calculate and sort the distances between the atom and its neighbours.

        Returns:
        --------
            - dict : List of distances between the atom and its neighbours.
        """
        distances = {}
        # distances_OSi = [] # NOTE: not used because it's already calculate in the Silicon class: distances_SiO.
        distances_OO = []

        for counter, neighbour in enumerate(self.long_range_neighbours):
            if neighbour.get_element() == "Si":
                continue
            if neighbour.get_element() == "O":
                distance = self.long_range_distances[counter]
                distances_OO.append(distance)

        distances["OO"] = distances_OO

        return distances


def transform_into_subclass(atom: Atom) -> object:
    """
    Return a Silicon object or Oxygen object from the subclass Silicon or Oxygen whether the atom.element is 'Si' or 'O'.
    """
    if atom.get_element() == "O":
        return Oxygen(
            atom.element,
            atom.id,
            atom.position,
            atom.frame,
            atom.cutoffs,
            atom.extension,
        )
    elif atom.get_element() == "Si":
        return Silicon(
            atom.element,
            atom.id,
            atom.position,
            atom.frame,
            atom.cutoffs,
            atom.extension,
        )
    else:
        raise ValueError(
            f"\tERROR: Atom {atom.element} - {atom.id} can be transformed into Silicon or Oxygen object."
        )


def get_default_settings() -> dict:
    """
    Method that load the default parameters for extension SiO2.
    """
    # internal imports
    from ..settings.parameter import Parameter

    # Structure of the system
    list_of_elements = [{"element": "Si", "number": 0}, {"element": "O", "number": 0}]

    # Pair cutoffs for the clusters
    list_of_cutoffs = [
        {"element1": "O", "element2": "O", "value": 3.05},
        {"element1": "Si", "element2": "O", "value": 2.30},
        {"element1": "Si", "element2": "Si", "value": 3.50},
    ]

    # Settings
    dict_settings = {
        "extension": Parameter("extension", "SiO2"),
        "structure": Parameter("structure", list_of_elements),
        "cutoffs": Parameter("cutoffs", list_of_cutoffs),
    }

    return dict_settings


def return_keys(property: str) -> list:
    """
    Return the keys needed for the results dictionary.
    """
    if property == "pair_distribution_function":
        return ["SiO", "SiSi", "OO"]
    elif property == "bond_angular_distribution":
        return ["SiOSi", "SiSiSi", "OSiO", "OOO"]
    elif property == "mean_square_displacement":
        return ["Si", "O", "total"]
    elif property == "structural_units":
        return [
            {"SiOz": ["SiO4", "SiO5", "SiO6", "SiO7"]},
            {"OSiz": ["OSi1", "OSi2", "OSi3", "OSi4"]},
            {"connectivity_SiO4": ["CS_SiO4", "ES_SiO4", "FS_SiO4"]},
            {"connectivity_SiO5": ["CS_SiO5", "ES_SiO5", "FS_SiO5"]},
            {"connectivity_SiO6": ["CS_SiO6", "ES_SiO6", "FS_SiO6"]},
            {
                "connectivity": [
                    "proportion_corners",
                    "proportion_edges",
                    "proportion_faces"
                ]
            },
            {
                "polyhedricity": [
                    "tetrahedra",
                    "pentahedra",
                    "square_based_pyramid",
                    "triangular_bipyramid",
                    "octahedra"
                ]
            },
            {
                "hist_polyhedricity": [
                    "bins",
                    "hist_SiO4",
                    "hist_SiO5",
                    "hist_SiO5_allSQP",
                    "hist_SiO5_sqp",
                    "hist_SiO5_allTBP",
                    "hist_SiO5_tBP",
                    "hist_SiO6"
                ]
            },
            {
                "lifetime": [
                    "time",
                    "4_to_5p",
                    "4_to_5bp",
                    "4_to_6",
                    "5p_to_4",
                    "5p_to_6",
                    "5p_to_5bp",
                    "5bp_to_5p",
                    "5bp_to_4",
                    "5bp_to_6",
                    "6_to_4",
                    "6_to_5p",
                    "6_to_5bp",
                    "4_to_5" ,
                    "5_to_4" ,
                    "5_to_6" ,
                    "6_to_5" ,
                ]
            },
            {
                "switch_probability": [
                    "4_to_4",
                    "4_to_5p",
                    "4_to_5bp",
                    "4_to_6",
                    "4_to_5" ,
                    "5p_to_4",
                    "5p_to_6",
                    "5p_to_5bp",
                    "5bp_to_5p",
                    "5bp_to_4",
                    "5bp_to_6",
                    "5bp_to_5bp",
                    "5p_to_5p",
                    "5_to_5",
                    "5_to_4" ,
                    "5_to_6" ,
                    "6_to_5" ,
                    "6_to_4",
                    "6_to_5p",
                    "6_to_5bp",
                    "6_to_6", 
                ]
            }
        ]
    elif property == "neutron_structure_factor":
        return ["Si-Si", "Si-O", "O-O", "total"]

    # TODO: add the other properties
    else:
        return []


def calculate_structural_units(atoms, box) -> dict:
    """
    Calculate the number of SiO_z and OSi_k units for each atom in the system.
    """

    # Initialize the lists
    SiO4 = []
    SiO5 = []
    SiO6 = []
    SiO7 = []
    OSi1 = []
    OSi2 = []
    OSi3 = []
    OSi4 = []
    CS_SiO4, ES_SiO4, FS_SiO4 = [], [], []
    CS_SiO5, ES_SiO5, FS_SiO5 = [], [], []
    CS_SiO6, ES_SiO6, FS_SiO6 = [], [], []
    proportion_corners, proportion_edges, proportion_faces = [], [], []

    tetrahedricity = []
    pentahedricity = []
    octahedricity = []

    SQP_pentahedricity = []  # all SiO5 are considered as square base pyramid
    TBP_pentahedricity = []  # all SiO5 are considered as triangular bipyramid
    sqp_pentahedricity = []  # only SiO5 that are square base pyramid
    tbp_pentahedricity = []  # only SiO5 that are triangular bipyramid

    silicons = [atom for atom in atoms if atom.get_element() == "Si"]
    oxygens = [atom for atom in atoms if atom.get_element() == "O"]

    # Calculate the proportion of each SiOz units
    coordination_SiOz = []
    for atom in silicons:
        counter = len(
            [
                neighbour
                for neighbour in atom.get_neighbours()
                if neighbour.get_element() == "O"
            ]
        )
        coordination_SiOz.append(counter)
        if counter == 4:
            SiO4.append(atom)
        if counter == 5:
            SiO5.append(atom)
        if counter == 6:
            SiO6.append(atom)
        if counter == 7:
            SiO7.append(atom)

    _debug_histogram_proportion_SiOz = np.histogram(
        coordination_SiOz, bins=[4, 5, 6, 7, 8], density=True
    )

    # Calculate the proportion of each OSiz units
    coordination_OSiz = []
    for atom in oxygens:
        counter = len(
            [
                neighbour
                for neighbour in atom.get_neighbours()
                if neighbour.get_element() == "Si"
            ]
        )
        coordination_OSiz.append(counter)
        if counter == 1:
            OSi1.append(atom)
        if counter == 2:
            OSi2.append(atom)
        if counter == 3:
            OSi3.append(atom)
        if counter == 4:
            OSi4.append(atom)

    _debug_histogram_proportion_OSik = np.histogram(
        coordination_OSiz, bins=[1, 2, 3, 4, 5], density=True
    )

    # Calculate the Qi species (ie number of bridging oxygens for SiO4 units)
    for silicon in SiO4:
        bridging_oxygens = [
            neighbour
            for neighbour in silicon.get_neighbours()
            if neighbour.get_element() == "O"
        ]
        counter = 0
        for oxygen in bridging_oxygens:
            if oxygen in OSi2 or oxygen in OSi3 or oxygen in OSi4:
                counter += 1
        silicon.qi_species = counter

    # Calculate the number of edge-sharing (2 oxygens shared by 2 silicons)
    for silicon in silicons:
        unique_bond = []
        for oxygen in [
            atom for atom in silicon.get_neighbours() if atom.get_element() == "O"
        ]:
            for second_silicon in [
                atom for atom in oxygen.get_neighbours() if atom.get_element() == "Si"
            ]:
                if second_silicon.id != silicon.id:
                    unique_bond.append(second_silicon.id)
        unique_bond = np.array(unique_bond)

        uniques, counts = np.unique(unique_bond, return_counts=True)

        for connectivity in counts:
            if (
                connectivity == 1
            ):  # 1 oxygen is shared by 'silicon' and 'second_silicon'
                silicon.number_of_corners += 1
            if (
                connectivity == 2
            ):  # 2 oxygens are shared by 'silicon' and 'second_silicon'
                silicon.number_of_edges += 1
            if (
                connectivity == 3
            ):  # 3 oxygens are shared by 'silicon' and 'second_silicon'
                silicon.number_of_faces += 1

        distances = calculate_distances_between_vertices(silicon, box)

        if silicon.coordination == 4:
            CS_SiO4.append(silicon.number_of_corners)
            ES_SiO4.append(silicon.number_of_edges)
            FS_SiO4.append(silicon.number_of_faces)

            tetrahedricity.append(calculate_tetrahedricity(distances))

            silicon.form = "tetrahedron"

        if silicon.coordination == 5:
            CS_SiO5.append(silicon.number_of_corners)
            ES_SiO5.append(silicon.number_of_edges)
            FS_SiO5.append(silicon.number_of_faces)

            this_sbp_pentahedricity, this_tbp_pentahedricity = calculate_pentahedricity(
                distances
            )
            SQP_pentahedricity.append(this_sbp_pentahedricity)
            TBP_pentahedricity.append(this_tbp_pentahedricity)
            if this_sbp_pentahedricity < this_tbp_pentahedricity:
                pentahedricity.append(this_sbp_pentahedricity)
                sqp_pentahedricity.append(this_sbp_pentahedricity)
                silicon.form = "square base pyramid"
            else:
                pentahedricity.append(this_tbp_pentahedricity)
                tbp_pentahedricity.append(this_tbp_pentahedricity)
                silicon.form = "triangular bipyramid"

        if silicon.coordination == 6:
            CS_SiO6.append(silicon.number_of_corners)
            ES_SiO6.append(silicon.number_of_edges)
            FS_SiO6.append(silicon.number_of_faces)

            octahedricity.append(calculate_octahedricity(distances))
            
            silicon.form = "octahedron"

        proportion_corners.append(silicon.number_of_corners)
        proportion_edges.append(silicon.number_of_edges)
        proportion_faces.append(silicon.number_of_faces)

    # Perform the average
    proportion_corners = np.sum(proportion_corners) / len(silicons)
    proportion_edges = np.sum(proportion_edges) / len(silicons)
    proportion_faces = np.sum(proportion_faces) / len(silicons)
    nSiO4 = len(SiO4)
    nSiO5 = len(SiO5)
    nSiO6 = len(SiO6)
    nSiO7 = len(SiO7)
    if nSiO4 == 0:
        nSiO4 = 1
    if nSiO5 == 0:
        nSiO5 = 1
    if nSiO6 == 0:
        nSiO6 = 1
    if nSiO7 == 0:
        nSiO7 = 1
    SiO4 = len(SiO4) / len(silicons)
    SiO5 = len(SiO5) / len(silicons)
    SiO6 = len(SiO6) / len(silicons)
    SiO7 = len(SiO7) / len(silicons)
    OSi1 = len(OSi1) / len(oxygens)
    OSi2 = len(OSi2) / len(oxygens)
    OSi3 = len(OSi3) / len(oxygens)
    OSi4 = len(OSi4) / len(oxygens)
    CS_SiO4 = np.sum(CS_SiO4) / nSiO4
    ES_SiO4 = np.sum(ES_SiO4) / nSiO4
    FS_SiO4 = np.sum(FS_SiO4) / nSiO4
    CS_SiO5 = np.sum(CS_SiO5) / nSiO5
    ES_SiO5 = np.sum(ES_SiO5) / nSiO5
    FS_SiO5 = np.sum(FS_SiO5) / nSiO5
    CS_SiO6 = np.sum(CS_SiO6) / nSiO6
    ES_SiO6 = np.sum(ES_SiO6) / nSiO6
    FS_SiO6 = np.sum(FS_SiO6) / nSiO6

    # Build the histogram for the polyhedricity
    bins = np.linspace(0, 0.5, 1000)
    dbin = 0.0005
    hist_tetrahedricity = np.zeros(len(bins))
    hist_pentahedricity = np.zeros(len(bins))
    hist_SBP_pentahedricity = np.zeros(len(bins))
    hist_sbp_pentahedricity = np.zeros(len(bins))
    hist_TBP_pentahedricity = np.zeros(len(bins))
    hist_tbp_pentahedricity = np.zeros(len(bins))
    hist_octahedricity = np.zeros(len(bins))

    for i in range(len(tetrahedricity)):
        hist_tetrahedricity[int(tetrahedricity[i] / dbin) + 1] += 1 / len(
            tetrahedricity
        )
    for i in range(len(pentahedricity)):
        hist_pentahedricity[int(pentahedricity[i] / dbin) + 1] += 1 / len(
            pentahedricity
        )
    for i in range(len(SQP_pentahedricity)):
        hist_SBP_pentahedricity[int(SQP_pentahedricity[i] / dbin) + 1] += 1 / len(
            pentahedricity
        )
    for i in range(len(sqp_pentahedricity)):
        hist_sbp_pentahedricity[int(sqp_pentahedricity[i] / dbin) + 1] += 1 / len(
            pentahedricity
        )
    for i in range(len(TBP_pentahedricity)):
        hist_TBP_pentahedricity[int(TBP_pentahedricity[i] / dbin) + 1] += 1 / len(
            pentahedricity
        )
    for i in range(len(tbp_pentahedricity)):
        hist_tbp_pentahedricity[int(tbp_pentahedricity[i] / dbin) + 1] += 1 / len(
            pentahedricity
        )
    for i in range(len(octahedricity)):
        hist_octahedricity[int(octahedricity[i] / dbin) + 1] += 1 / len(octahedricity)

    tetrahedra = len(tetrahedricity) / len(silicons)
    pentahedra = len(pentahedricity) / len(silicons)
    square_base_pyramid = len(sqp_pentahedricity) / len(silicons)
    triangular_bipyramid = len(tbp_pentahedricity) / len(silicons)
    octahedra = len(octahedricity) / len(silicons)

    results = {
        "SiOz": [SiO4, SiO5, SiO6, SiO7],
        "OSiz": [OSi1, OSi2, OSi3, OSi4],
        "connectivity_SiO4": [CS_SiO4, ES_SiO4, FS_SiO4],
        "connectivity_SiO5": [CS_SiO5, ES_SiO5, FS_SiO5],
        "connectivity_SiO6": [CS_SiO6, ES_SiO6, FS_SiO6],
        "connectivity": [proportion_corners, proportion_edges, proportion_faces],
        "polyhedricity": [
            tetrahedra,
            pentahedra,
            square_base_pyramid,
            triangular_bipyramid,
            octahedra,
        ],
        "hist_polyhedricity": np.array(
            [
                bins,
                hist_tetrahedricity,
                hist_pentahedricity,
                hist_SBP_pentahedricity,
                hist_sbp_pentahedricity,
                hist_TBP_pentahedricity,
                hist_tbp_pentahedricity,
                hist_octahedricity,
            ]
        ),
    }

    _debug_check_SiOz = np.sum(results["SiOz"])
    _debug_check_OSiz = np.sum(results["OSiz"])

    return results


def calculate_distances_between_vertices(atom, box):  # -> np.array
    """
    Calculate the distances between the vertices of the polyhedron.
    """
    distances = []
    neighbours = [
        neighbour for neighbour in atom.neighbours if neighbour.get_element() == "O"
    ]
    for i in range(len(neighbours)):
        neighbour_1 = neighbours[i]
        for j in range(i + 1, len(neighbours)):
            neighbour_2 = neighbours[j]
            distance = neighbour_1.position - neighbour_2.position
            distance = distance - np.round(distance / box) * box
            distances.append(np.linalg.norm(distance))

    distances.sort()

    if atom.coordination == 4 and len(distances) != 6:
        print("ERROR: SiO4 unit should have 6 distances")
    if atom.coordination == 5 and len(distances) != 10:
        print("ERROR: SiO5 unit should have 10 distances")
    if atom.coordination == 6 and len(distances) != 15:
        print("ERROR: SiO6 unit should have 15 distances")

    return np.array(distances)


def calculate_tetrahedricity(distances) -> float:
    mean_distance = np.mean(distances**2)

    tetrahedricity = 0

    for i in range(len(distances)):
        for j in range(i + 1, len(distances)):
            tetrahedricity += (distances[i] - distances[j]) ** 2

    tetrahedricity /= 15 * mean_distance

    return tetrahedricity


def calculate_pentahedricity(distances) -> tuple:
    # case 1 : square base pyramid
    # copy distances to avoid modifying the original array
    sbp_distances = np.copy(distances)
    sbp_distances[-2] /= np.sqrt(2)
    sbp_distances[-1] /= np.sqrt(2)

    sbp_pentahedricity = 0

    sbp_mean_distances = np.mean(sbp_distances**2)

    for i in range(len(sbp_distances)):
        for j in range(i + 1, len(sbp_distances)):
            sbp_pentahedricity += (sbp_distances[i] - sbp_distances[j]) ** 2
    sbp_pentahedricity /= 45 * sbp_mean_distances

    # case 2 : triangular bipyramid
    tbp_distances = np.copy(distances)
    tbp_distances[-1] /= np.sqrt(8 / 3)

    tbp_pentahedricity = 0

    tbp_mean_distances = np.mean(tbp_distances**2)

    for i in range(len(tbp_distances)):
        for j in range(i + 1, len(tbp_distances)):
            tbp_pentahedricity += (tbp_distances[i] - tbp_distances[j]) ** 2
    tbp_pentahedricity /= 45 * tbp_mean_distances

    return sbp_pentahedricity, tbp_pentahedricity


def calculate_octahedricity(distances) -> float:
    distances[-3] /= np.sqrt(2)
    distances[-2] /= np.sqrt(2)
    distances[-1] /= np.sqrt(2)

    octahedricity = 0

    mean_distance = np.mean(distances**2)

    for i in range(len(distances)):
        for j in range(i + 1, len(distances)):
            octahedricity += (distances[i] - distances[j]) ** 2
    octahedricity /= 105 * mean_distance

    return octahedricity


def append_forms(number_of_frames, atoms, forms):  # -> np.array
    """
    Calculate the lifetime of each SiOz units inside the whole trajectory.
    """

    # Initialize the lists or read storage
    silicons = [atom for atom in atoms if atom.get_element() == "Si"]

    if forms is None:
        # if frame 0 is being analyzed, create variable
        forms = {}

    # Calculate the lifetime of each SiOz units
    for i, silicon in enumerate(silicons):
        if silicon.frame not in forms:
            forms[silicon.frame] = []
        forms[silicon.frame].append(silicon.get_form())

    return forms


def calculate_lifetime(settings, forms):
    """
    Calculate the lifetime of each SiOz units inside the whole trajectory.
    """

    number_of_frames = len(forms)
    number_of_atoms = len(forms[0])

    types = ["tetrahedron", "square base pyramid", "triangular bipyramid", "octahedron"]

    dt = settings.msd_settings.get_dt()
    printlevel = settings.msd_settings.get_printlevel()

    # create the histograms
    bins = np.arange(1, number_of_frames + 1, 1) * dt * printlevel  # time in ps
    hist_4_to_5p = np.zeros(number_of_frames)
    hist_4_to_5bp = np.zeros(number_of_frames)
    hist_4_to_6 = np.zeros(number_of_frames)
    hist_5p_to_4 = np.zeros(number_of_frames)
    hist_5p_to_6 = np.zeros(number_of_frames)
    hist_5p_to_5bp = np.zeros(number_of_frames)
    hist_5bp_to_5p = np.zeros(number_of_frames)
    hist_5bp_to_4 = np.zeros(number_of_frames)
    hist_5bp_to_6 = np.zeros(number_of_frames)
    hist_6_to_4 = np.zeros(number_of_frames)
    hist_6_to_5p = np.zeros(number_of_frames)
    hist_6_to_5bp = np.zeros(number_of_frames)
    hist_4_to_4 = 0
    hist_5bp_to_5bp = 0
    hist_5p_to_5p = 0
    hist_6_to_6 = 0

    counter = np.zeros(len(forms[0]), dtype=np.int32)  # counter for each atom

    if not settings.quiet.get_value():
        # create progress bar
        pbar = tqdm(range(1, len(forms)), desc="Calculating SiOz lifetime")
    else:
        pbar = range(1, len(forms))

    for f in pbar:
        # loop over frames
        previous_f = forms[f - 1]
        this_f = forms[f]
        for a in range(len(this_f)):
            # loop over atoms
            if previous_f[a] == this_f[a]:
                # if the form is the same as the previous frame, increment the counter
                counter[a] += 1
            else:
                # if the form is different, check the previous form
                # atom a has changed form
                # count the number of frames the atom has been in the previous form before changing
                # then reset the counter
                if previous_f[a] == "tetrahedron":
                    if this_f[a] == "square base pyramid":
                        hist_4_to_5p[counter[a]] += 1
                    elif this_f[a] == "triangular bipyramid":
                        hist_4_to_5bp[counter[a]] += 1
                    elif this_f[a] == "octahedron":
                        hist_4_to_6[counter[a]] += 1
                elif previous_f[a] == "square base pyramid":
                    if this_f[a] == "tetrahedron":
                        hist_5p_to_4[counter[a]] += 1
                    elif this_f[a] == "triangular bipyramid":
                        hist_5p_to_5bp[counter[a]] += 1
                    elif this_f[a] == "octahedron":
                        hist_5p_to_6[counter[a]] += 1
                elif previous_f[a] == "triangular bipyramid":
                    if this_f[a] == "tetrahedron":
                        hist_5bp_to_4[counter[a]] += 1
                    elif this_f[a] == "square base pyramid":
                        hist_5bp_to_5p[counter[a]] += 1
                    elif this_f[a] == "octahedron":
                        hist_5bp_to_6[counter[a]] += 1
                elif previous_f[a] == "octahedron":
                    if this_f[a] == "tetrahedron":
                        hist_6_to_4[counter[a]] += 1
                    elif this_f[a] == "square base pyramid":
                        hist_6_to_5p[counter[a]] += 1
                    elif this_f[a] == "triangular bipyramid":
                        hist_6_to_5bp[counter[a]] += 1
                counter[a] = 0
    
    no_changes = np.where(counter==len(forms)-1)[0]
    forms = np.array(forms[0])
    unchanged_forms = forms[no_changes]

    unchanged_forms = np.unique(unchanged_forms, return_counts=True)
    # print(unchanged_forms)
    for i in range(len(unchanged_forms[0])):
        if unchanged_forms[0][i] == 'tetrahedron':
            hist_4_to_4 = unchanged_forms[1][i]
        if unchanged_forms[0][i] == 'square base pyramid':
            hist_5p_to_5p = unchanged_forms[1][i]
        if unchanged_forms[0][i] == 'triangular bipyramid':
            hist_5bp_to_5bp = unchanged_forms[1][i]
        if unchanged_forms[0][i] == 'octahedron':
            hist_6_to_6 = unchanged_forms[1][i]

    results = {
        "time": bins,
        "4_to_5p": hist_4_to_5p,
        "4_to_5bp": hist_4_to_5bp,
        "4_to_6": hist_4_to_6,
        "5p_to_4": hist_5p_to_4,
        "5p_to_6": hist_5p_to_6,
        "5p_to_5bp": hist_5p_to_5bp,
        "5bp_to_5p": hist_5bp_to_5p,
        "5bp_to_4": hist_5bp_to_4,
        "5bp_to_6": hist_5bp_to_6,
        "6_to_4": hist_6_to_4,
        "6_to_5p": hist_6_to_5p,
        "6_to_5bp": hist_6_to_5bp,
        "4_to_5" : hist_4_to_5p + hist_4_to_5bp,
        "5_to_4" : hist_5p_to_4 + hist_5bp_to_4,
        "5_to_6" : hist_5p_to_6 + hist_5bp_to_6,
        "6_to_5" : hist_6_to_5p + hist_6_to_5bp,
    }

    counts = {
        # TODO : find a normalization factor and apply it to the following results
        "4_to_4": hist_4_to_4/number_of_atoms,
        "4_to_5p": np.sum(hist_4_to_5p, dtype=np.int32)/number_of_atoms,
        "4_to_5bp": np.sum(hist_4_to_5bp, dtype=np.int32)/number_of_atoms,
        "4_to_6": np.sum(hist_4_to_6, dtype=np.int32)/number_of_atoms,
        "4_to_5" : np.sum(hist_4_to_5p + hist_4_to_5bp, dtype=np.int32)/number_of_atoms,
        "5p_to_4": np.sum(hist_5p_to_4, dtype=np.int32)/number_of_atoms,
        "5p_to_6": np.sum(hist_5p_to_6, dtype=np.int32)/number_of_atoms,
        "5p_to_5bp": np.sum(hist_5p_to_5bp, dtype=np.int32)/number_of_atoms,
        "5bp_to_5p": np.sum(hist_5bp_to_5p, dtype=np.int32)/number_of_atoms,
        "5bp_to_4": np.sum(hist_5bp_to_4, dtype=np.int32)/number_of_atoms,
        "5bp_to_6": np.sum(hist_5bp_to_6, dtype=np.int32)/number_of_atoms,
        "5bp_to_5bp": hist_5bp_to_5bp/number_of_atoms,
        "5p_to_5p": hist_5p_to_5p/number_of_atoms,
        "5_to_5": (hist_5p_to_5p + hist_5bp_to_5bp)/number_of_atoms,
        "5_to_4" : np.sum(hist_5p_to_4 + hist_5bp_to_4, dtype=np.int32)/number_of_atoms,
        "5_to_6" : np.sum(hist_5p_to_6 + hist_5bp_to_6, dtype=np.int32)/number_of_atoms,
        "6_to_5" : np.sum(hist_6_to_5p + hist_6_to_5bp, dtype=np.int32)/number_of_atoms,
        "6_to_4": np.sum(hist_6_to_4, dtype=np.int32)/number_of_atoms,
        "6_to_5p": np.sum(hist_6_to_5p, dtype=np.int32)/number_of_atoms,
        "6_to_5bp": np.sum(hist_6_to_5bp, dtype=np.int32)/number_of_atoms,
        "6_to_6": hist_6_to_6/number_of_atoms,
    }

    return results, counts
