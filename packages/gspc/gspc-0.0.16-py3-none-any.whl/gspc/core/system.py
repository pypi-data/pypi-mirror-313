# external imports
import numpy as np
from tqdm import tqdm
from scipy.spatial import cKDTree
from numba import njit, prange
from numba_progress import ProgressBar  # NOTE: uncomment while debugging
import importlib
import os
import re
import inspect

# internal imports
from .cutoff import Cutoff
from ..utils.generate_color_gradient import generate_color_gradient


class System:
    r"""
    Represents a system of atoms and provides methods for analyzing and manipulating the system.

    Attributes:
    -----------
        - settings (Settings): Settings object containing the list of all the parameters.
        - atoms (list): List of all the atoms in the system.
        - box (Box): The Box object containing the lattice information at each frame.
        - frame (int): Frame of the system in the trajectory.
        - cutoffs (Cutoff): Cutoff object managing cutoff distances for pairs of elements.

    Methods:
    --------
        - __init__: Initializes a System object.
        - add_atom: Adds an Atom object to the list of atoms.
        - get_atoms: Returns the list of atoms.
        - get_positions: Returns the list of positions and elements of all Atom objects.
        - get_positions_by_element: Returns the list of positions of all Atom objects of the same element.
        - get_atoms_by_element: Returns the list of Atom objects belonging to the same species.
        - get_unique_element: Returns the unique elements present in the system along with their counts.
        - wrap_atomic_positions: Wraps atomic positions inside the simulation box using periodic boundary conditions.
        - compute_mass: Returns the mass of the system in atomic unit.
        - calculate_neighbours: Calculates the nearest neighbours of all atoms in the system.
        - calculate_structural_units: Determines the structural units and other structural properties.
    """

    def __init__(self, settings) -> None:
        r"""
        Initializes a System object.

        Parameters:
        -----------
            - settings (Settings): Settings object containing the list of all the parameters.
        """
        self.settings: object = (
            settings  # Settings object containing the list of all the parameters
        )
        self.atoms: list = []  # List of all the atoms
        self.box: object = (
            None  # The Box object containing the lattice information at each frame
        )
        self.frame: int = 0  # Frame of the system in the trajectory

        # Set the cutoffs of the system.
        self.cutoffs: object = Cutoff(
            settings.cutoffs.get_value()
        )  # Cutoffs of the system

        # Set the structural attributes
        self.structural_units: dict = {}  # Structural units of the system
        self.angles: dict = {}  # Bond angular distribution of the system
        self.distances: dict = {}  # Pair distribution function of the system
        self.mean_distances: dict = {} # Mean distances of the system
        self.mean_angles: dict = {} # Mean angles of the system
        self.msd: dict = {}  # Mean square displacement of the system

    def add_atom(self, atom) -> None:
        r"""
        Add an Atom object to the list of atoms.

        Returns:
        --------
            - None.
        """
        module = importlib.import_module(
            f"gspc.extensions.{self.settings.extension.get_value()}"
        )
        transformed_atom = module.transform_into_subclass(atom)
        self.atoms.append(transformed_atom)

    def get_atoms(self) -> list:
        f"""
        Return the list of atoms.
        
        Returns:
        --------
            - list : list of Atom objects in the system.
        """
        return self.atoms

    def get_positions(self) -> tuple:
        r"""
        Return the list of positions and elements of all Atom objects.

        Returns:
        --------
            - tuple : the filtered position in a np.array and their associated elements in a np.array.
        """
        filtered_positions = list(
            map(
                lambda atom: atom.position,
                filter(
                    lambda atom: hasattr(atom, "frame") and atom.frame == self.frame,
                    self.atoms,
                ),
            )
        )

        filtered_elements = list(
            map(
                lambda atom: atom.element,
                filter(
                    lambda atom: hasattr(atom, "frame") and atom.frame == self.frame,
                    self.atoms,
                ),
            )
        )

        return np.array(filtered_positions), np.array(filtered_elements)

    def get_positions_by_element(self, element) -> np.array:
        r"""
        Return the list of positions of all Atom objects of the same element.

        Returns:
        --------
            - np.array : Filtered positions.
        """
        filtered_positions = list(
            map(
                lambda atom: atom.position,
                filter(
                    lambda atom: hasattr(atom, "frame")
                    and atom.frame == self.frame
                    and atom.element == element,
                    self.atoms,
                ),
            )
        )

        return np.array(filtered_positions)

    def get_atoms_by_element(self, element) -> list:
        r"""
        Return the list of Atom objects belonging to the same species.

        Returns:
        --------
            - list : list of Atom objects.
        """
        filtered_atoms = list(
            filter(
                lambda atom: hasattr(atom, "frame")
                and atom.frame == self.frame
                and atom.element == element,
                self.atoms,
            )
        )

        return filtered_atoms

    def get_unique_element(self) -> np.array:
        r"""
        Return the uniques elements present in the system along with their counts.

        Returns:
        --------
            - np.array : array of the unique element in the system.
        """
        filtered_elements = np.array(
            list(
                map(
                    lambda atom: atom.element,
                    filter(
                        lambda atom: hasattr(atom, "frame")
                        and atom.frame == self.frame,
                        self.atoms,
                    ),
                )
            )
        )
        return np.unique(filtered_elements, return_counts=True)

    def wrap_atomic_positions(self) -> None:
        r"""
        Wrap atomic positions inside the simulation box using the periodic boundary conditions.

        Returns:
        --------
            - None.
        """
        if not self.settings.quiet.get_value():
            color_gradient = generate_color_gradient(len(self.atoms))
            progress_bar = tqdm(
                prange(len(self.atoms)),
                desc="Wrapping positions inside the box ...",
                colour="#0dff00",
                leave=False,
                unit="atom",
            )
        else:
            progress_bar = prange(len(self.atoms))
        color = 0
        for i in progress_bar:
            atom = self.atoms[i]
            # Updating progress bar
            if not self.settings.quiet.get_value():
                progress_bar.set_description(
                    f"Wrapping positions inside the box {atom.id} ..."
                )
                progress_bar.colour = "#%02x%02x%02x" % color_gradient[color]
                color += 1

            # Getting box dimensions at the current frame
            box_size = self.box.get_box_dimensions(self.frame)

            # Loop over the dimension of the simulation box (ie 3D)
            for i in range(len(box_size)):
                # Apply periodic boundary conditions for each dimension
                atom.position[i] = np.mod(atom.position[i] + box_size[i], box_size[i])

    def calculate_neighbours(self) -> None:
        r"""
        Calculate the nearest neighbours of all the atom in the system.
        - NOTE: this method is extension dependant.

        Returns:
        --------
            - None.
        """

        # Wrap all the positions inside the simulation box first
        self.wrap_atomic_positions()

        # Get the simulation box size
        box_size = self.box.get_box_dimensions(self.frame)

        # Get all the atomic positions
        positions, mask = self.get_positions()

        # Get the maximum value of the cutoffs of the system
        max_cutoff = self.cutoffs.get_max_cutoff()

        # Calculate the tree with the pbc applied
        tree_with_pbc = cKDTree(positions, boxsize=box_size)

        # Set the progress bar
        if not self.settings.quiet.get_value():
            color_gradient = generate_color_gradient(len(positions))
            progress_bar = tqdm(
                prange(len(positions)),
                desc="Fetching nearest neighbours ...",
                colour="#00ffff",
                leave=False,
                unit="atom",
            )
        else:
            progress_bar = prange(len(positions))

        # Loop over the atomic positions
        for i in progress_bar:
            # Update progress bar
            if not self.settings.quiet.get_value():
                progress_bar.set_description(f"Fetching nearest neighbours {i} ...")
                progress_bar.colour = "#%02x%02x%02x" % color_gradient[i]

            # Process with pbc applied
            # Query the neighbouring atoms within the cutoff distance
            index = tree_with_pbc.query_ball_point(positions[i], max_cutoff)

            # Calculate the distance with k nearest neighbours
            distances, indices = tree_with_pbc.query(positions[i], k=len(index))

            # Check if result is a list or a int
            if isinstance(indices, int):
                # indices is an int, turn indices into a list of a single int
                indices = [indices]

            # Check if results is a list of a int
            if isinstance(distances, int):
                # distances is an int, turn distances into a list of a single int
                distances = [distances]

            # Add the nearest neighbours to central atom
            for j in indices:
                self.atoms[i].add_neighbour(self.atoms[j])

            self.atoms[i].filter_neighbours(distances)
            self.atoms[i].calculate_coordination()

    # ---------------------- Structural properties calculation methods ---------------------- #

    def calculate_structural_units(self, extension) -> None:
        r"""
        Determine the structural units and other structural properties.
        - NOTE: this method is extension dependant.

        Parameters:
        -----------
            - extension (str) : name of the extension to use to calculate the structural units.

        Returns:
        --------
            - None.
        """

        module = importlib.import_module(f"gspc.extensions.{extension}")

        box = self.box.get_box_dimensions(self.frame)

        self.structural_units = module.calculate_structural_units(self.get_atoms(), box)


    # @njit(parallel=True) # TODO : implement a fork of gspc without the progress bar and prange instead
    def calculate_bond_angular_distribution(self) -> None:
        r"""
        Determine the bond angular distribution of the system.

        Returns:
        --------
            - None.
        """

        if self.settings.quiet.get_value() == False:
            progress_bar = tqdm(
                prange(len(self.atoms)),
                desc="Calculating bond angular distribution ...",
                colour="#00ffff",
                leave=False,
                unit="atom",
            )
            color_gradient = generate_color_gradient(len(self.atoms))
        else:
            progress_bar = prange(len(self.atoms))

        for i in progress_bar: # NOTE : uncomment this when done testing
        # for i in prange(len(self.atoms)):
            # Update the progress bar
            atom = self.atoms[i]
            if self.settings.quiet.get_value() == False:
                progress_bar.set_description(
                    f"Calculating bond angular distribution {atom.id} ..."
                )
                progress_bar.colour = "#%02x%02x%02x" % color_gradient[atom.id]
            dict_angles = atom.calculate_angles_with_neighbours(self.box)
            for key, value in dict_angles.items():
                if key in self.angles:
                    self.angles[key].extend(value)
                else:
                    self.angles[key] = value
                    
        # calculate the mean angles
        for key, value in self.angles.items():
            if key == "theta":
                continue
            self.mean_angles[key] = list( filter(lambda x: x <= 180, self.angles[key]))
            self.mean_angles[key] = np.mean(self.mean_angles[key])

        # Calculate the bond angular distribution
        nbins = self.settings.bad_settings.get_nbins()
        theta_max = self.settings.bad_settings.get_theta_max()
        self.angles["theta"] = None  # Initialize the theta values
        for key, value in self.angles.items():
            if key == "theta":
                continue
            self.angles[key], bins = np.histogram(
                value, bins=nbins, range=(0, theta_max)
            )
            self.angles["theta"] = bins[:-1]
            self.angles[key] = self.angles[key] / (
                np.sum(self.angles[key]) * 180 / nbins
            )

    def get_bond_angular_distribution(self) -> dict:
        r"""
        Return the bond angular distribution of the system.

        Returns:
        --------
            - dict : Bond angular distribution of the system.
        """
        return self.angles

    def calculate_long_range_neighbours(self):
        r"""
        Calculate the nearest neighbours of all the atom in the system.
        - NOTE: this method is extension dependant.

        Returns:
        --------
            - None.
        """

        # Wrap all the positions inside the simulation box first
        self.wrap_atomic_positions()

        # Get the simulation box size
        box_size = self.box.get_box_dimensions(self.frame)

        # Get all the atomic positions
        positions, mask = self.get_positions()

        # Get the maximum value of the cutoffs of the system
        max_cutoff = self.settings.pdf_settings.get_rmax()

        # Calculate the tree with the pbc applied
        tree_with_pbc = cKDTree(positions, boxsize=box_size)

        # Set the progress bar
        if self.settings.quiet.get_value() == False:
            color_gradient = generate_color_gradient(len(positions))
            progress_bar = tqdm(
                range(len(positions)),
                desc="Fetching long range neighbours ...",
                colour="#00ffff",
                leave=False,
                unit="atom",
            )
        else:
            progress_bar = range(len(positions))

        # Loop over the atomic positions
        for i in progress_bar:
            # Update progress bar
            if self.settings.quiet.get_value() == False:
                progress_bar.set_description(f"Fetching long range neighbours {i} ...")
                progress_bar.colour = "#%02x%02x%02x" % color_gradient[i]

            # Process with pbc applied
            # Query the neighbouring atoms within the cutoff distance
            index = tree_with_pbc.query_ball_point(positions[i], max_cutoff)

            # Calculate the distance with k nearest neighbours
            distances, indices = tree_with_pbc.query(positions[i], k=len(index))

            # Remove self from the list of neighbours
            distances = distances[1:]
            indices = indices[1:]

            # Check if result is a list or a int
            if isinstance(indices, int):
                # indices is an int, turn indices into a list of a single int
                indices = [indices]

            # Check if results is a list of a int
            if isinstance(distances, int):
                # distances is an int, turn distances into a list of a single int
                distances = [distances]

            # Add the nearest neighbours to central atom
            for counter, j in enumerate(indices):
                self.atoms[i].add_long_range_neighbour(self.atoms[j])
                self.atoms[i].add_long_range_distance(distances[counter])

    def calculate_pair_distribution_function(self):
        r"""
        Determine the pair distribution function of the system.

        Returns:
        --------
            - None.
        """

        self.settings.pdf_settings.check_rmax(self.box, self.frame)

        self.calculate_long_range_neighbours()

        if self.settings.quiet.get_value() == False:
            progress_bar = tqdm(
                prange(len(self.atoms)),
                desc="Calculating pair distribution function ...",
                colour="#00ffff",
                leave=False,
                unit="atom",
            )
            color_gradient = generate_color_gradient(len(self.atoms))
        else:
            progress_bar = prange(len(self.atoms))

        for i in progress_bar:
            atom = self.atoms[i]
            # Update the progress bar
            if self.settings.quiet.get_value() == False:
                progress_bar.set_description(
                    f"Calculating pair distribution function {atom.id} ..."
                )
                progress_bar.colour = "#%02x%02x%02x" % color_gradient[atom.id]

            dict_distances = atom.calculate_distances_with_neighbours()
            for key, value in dict_distances.items():
                if key in self.distances:
                    self.distances[key].extend(value)
                else:
                    self.distances[key] = value

        # Filter the distances with cutoffs for mean distances calculations and calculate the mean distances
        for key, value in self.distances.items():
            if key == "r":
                continue
            s = self.decrypt_key(key)[1]
            self.mean_distances[key] = list(
                filter(
                    lambda x: x <= self.cutoffs.get_cutoff(s[0], s[1]), self.distances[key]
                )
            )
            self.mean_distances[key] = np.mean(self.mean_distances[key])
            
        # Calculate the pair distribution function
        nbins = self.settings.pdf_settings.get_nbins()
        rmax = self.settings.pdf_settings.get_rmax()
        self.distances["r"] = None
        for key, value in self.distances.items():
            if key == "r":
                continue
            self.distances[key], bins = np.histogram(value, bins=nbins, range=(0, rmax))
            self.distances["r"] = bins[:-1]
            self.distances[key] = (
                self.distances[key] / 2
            )  # divide by 2 to avoid double counting
            same_species, species = self.decrypt_key(key)
            n_atoms_norm = 1
            for s in species:
                n_atoms_norm *= len(self.get_atoms_by_element(s))
            if same_species:
                n_atoms_norm -= 1
            normalization_factor = self.box.get_volume(self.frame) / (
                4.0 * np.pi * n_atoms_norm
            )
            for i in range(1, nbins):
                vdr = self.distances["r"][i] ** 2
                self.distances[key][i] = (
                    self.distances[key][i] * normalization_factor / vdr
                )

    def decrypt_key(self, key) -> bool:
        r"""
        Decrypt a key of a dictionary.

        Parameters:
        -----------
            - key (str) : Key to decrypt.

        Returns:
        --------
            - bool : True if the key is same species, False otherwise.
        """
        import re

        species = []

        matchs = re.findall(r"[A-Z][a-z]?", key)
        for match in matchs:
            if len(match) == 2 and match[1].isupper():
                species.extend(match)
            else:
                species.append(match)

        return species[0] == species[1], species

    def get_pair_distribution_function(self) -> dict:
        r"""
        Return the pair distribution function of the system.

        Returns:
        --------
            - dict : Pair distribution function of the system.
        """
        return self.distances

    def calculate_mass_per_species(self) -> dict:
        r"""
        Returns a dictionary containing the total mass of each species in the system.

        Returns:
        --------
            - dict : Dictionary containing the total mass of each species in the system.
        """
        mass = {}
        mass["total"] = 0
        for atom in self.atoms:
            if atom.element in mass:
                mass[atom.element] += atom.atomic_mass
                mass["total"] += atom.atomic_mass
            else:
                mass[atom.element] = atom.atomic_mass

        return mass

    def init_mean_square_displacement(self) -> None:
        r"""
        Initialize the mean square displacement of the system.

        Returns:
        --------
            - None.
        """
        # Create key for each species of the system
        species = self.get_unique_element()
        for s in species[0]:
            self.msd[s] = 0.0
        self.msd["total"] = 0.0

    def calculate_mean_square_displacement(self) -> None:
        r"""
        Calculate the mean square displacement of the system.

        Returns:
        --------
            - None.
        """
        if self.settings.quiet.get_value() == False:
            progress_bar = tqdm(
                self.atoms,
                desc="Calculating mean square displacement ...",
                colour="#00ffff",
                leave=False,
                unit="atom",
            )
            color_gradient = generate_color_gradient(len(self.atoms))
        else:
            progress_bar = self.atoms

        for atom in progress_bar:
            # Update the progress bar
            if self.settings.quiet.get_value() == False:
                progress_bar.set_description(
                    f"Calculating mean square displacement {atom.id} ..."
                )
                progress_bar.colour = "#%02x%02x%02x" % color_gradient[atom.id]

            dist = atom.calculate_mean_square_displacement()

            # Add the mean square displacement to the corresponding species
            self.msd[atom.element] += dist**2
            self.msd["total"] += dist**2

    def append_forms(self, stored_forms):
        r"""
        TODO finish documentation
        """

        module = importlib.import_module(
            f"gspc.extensions.{self.settings.extension.get_value()}"
        )

        self.forms = module.append_forms(
            self.settings.number_of_frames.get_value(),
            self.atoms,
            stored_forms,
        )

        return self.forms

    def calculate_lifetime(self):
        r"""
        TODO finish documentation
        """

        module = importlib.import_module(
            f"gspc.extensions.{self.settings.extension.get_value()}"
        )

        self.lifetime, prob = module.calculate_lifetime(self.settings, self.forms)

        return self.lifetime, prob

    def calculate_neutron_structure_factor(self, pairs) -> None:
        r"""
        Calculate the neutron structure factor of the system.

        Returns:
        --------
            - None.
        """

        # Calculate all possible pairs of the system:
        #   a-b, a-a, b-b, total
        #   a-b, a-c, b-c, a-a, b-b, c-c, total
        #   etc.

        # NOTE: not sure if three species are possible

        if self.settings.quiet.get_value() == False:
            progress_bar = tqdm(
                pairs,
                desc="Calculating neutron structure factor ...",
                colour="#00ffff",
                leave=False,
                unit="pair",
            )
            color_gradient = generate_color_gradient(len(pairs))
        else:
            progress_bar = pairs

        tpol = (2 * np.pi) / (
            self.box.get_box_dimensions(self.frame)[0]
        )  # NOTE: assuming box is cubic

        # generate the q vectors
        x_ = np.arange(tpol, 6, tpol)
        y_ = np.arange(tpol, 6, tpol)
        z_ = np.arange(tpol, 6, tpol)
        x__ = x_ * -1
        y__ = y_ * -1
        z__ = z_ * -1
        x__ = np.flip(x__)
        y__ = np.flip(y__)
        z__ = np.flip(z__)
        x__ = np.append(x__, 0)
        y__ = np.append(y__, 0)
        z__ = np.append(z__, 0)
        x_ = np.concatenate((x__, x_))
        y_ = np.concatenate((y__, y_))
        z_ = np.concatenate((z__, z_))
        qx, qy, qz = np.meshgrid(x_, y_, z_, indexing="ij")

        assert np.all(qx[:, 0, 0] == x_)
        assert np.all(qy[0, :, 0] == y_)
        assert np.all(qz[0, 0, :] == z_)

        q_norm = np.sqrt(qx**2 + qy**2 + qz**2)
        q_norm_unique = np.unique(q_norm)
        q_norm_1D = np.reshape(q_norm_unique, len(q_norm_unique))
        are_greater_than_10 = q_norm_1D > 10.0
        q_norm_1D = np.delete(q_norm_1D, np.where(are_greater_than_10)[0])

        # Calculate the neutron structure factor
        qsin = {}
        qcos = {}
        correlation_lentgh = {}

        number_of_atoms = np.sum(self.get_unique_element()[1])

        for species in self.get_unique_element()[0]:
            qsin[species] = np.zeros_like(qx)
            qcos[species] = np.zeros_like(qx)

            atoms = self.get_atoms_by_element(species)

            correlation_lentgh[species] = atoms[0].correlation_length

            positions = np.array([atom.position for atom in atoms])

            if self.settings.quiet.get_value() == False:
                with ProgressBar(
                    total=len(positions),
                    leave=False,
                    colour="#00ffff",
                    unit="atom",
                    desc=species,
                ) as progress:
                    cosd, sind = self._calculate_neutron_structure_factor(
                        qx, qy, qz, positions, progress
                    )
            else:
                cosd, sind = self._calculate_neutron_structure_factor(
                    qx, qy, qz, positions, None 
                )

            qcos[species] += cosd
            qsin[species] += sind

        structure_factor = {}
        f = {}

        structure_factor["q"] = q_norm_1D

        for i, pair in enumerate(progress_bar):
            # Update the progress bar
            if self.settings.quiet.get_value() == False:
                progress_bar.set_description(
                    f"Calculating neutron structure factor {pair} ..."
                )
                progress_bar.colour = "#%02x%02x%02x" % color_gradient[i]

            structure_factor[pair] = np.zeros_like(q_norm_1D)

            try:
                species1, species2 = pair.split("-")

                if species1 == species2:
                    f[pair] = (
                        qcos[species1] ** 2 + qsin[species1] ** 2
                    ) / number_of_atoms
                else:
                    A = (qcos[species1] + qcos[species2]) ** 2
                    B = (qsin[species1] + qsin[species2]) ** 2
                    C = qcos[species1] ** 2 + qsin[species1] ** 2
                    D = qcos[species2] ** 2 + qsin[species2] ** 2
                    f[pair] = (A + B - C - D) / (2 * number_of_atoms)

            except ValueError:
                # pair = "total"

                f[pair] = np.zeros_like(qx)

                for species in self.get_unique_element()[0]:
                    f[pair] += (
                        correlation_lentgh[species] ** 2 * f[f"{species}-{species}"]
                    )

                try:
                    f[pair] += (
                        2
                        * correlation_lentgh[self.get_unique_element()[0][0]]
                        * correlation_lentgh[self.get_unique_element()[0][1]]
                        * f[
                            f"{self.get_unique_element()[0][0]}-{self.get_unique_element()[0][1]}"
                        ]
                    )
                except:
                    f[pair] += (
                        2
                        * correlation_lentgh[self.get_unique_element()[0][0]]
                        * correlation_lentgh[self.get_unique_element()[0][1]]
                        * f[
                            f"{self.get_unique_element()[0][1]}-{self.get_unique_element()[0][0]}"
                        ]
                    )

                normalization = (
                    self.get_unique_element()[1][0]
                    * correlation_lentgh[self.get_unique_element()[0][0]] ** 2
                    + self.get_unique_element()[1][1]
                    * correlation_lentgh[self.get_unique_element()[0][1]] ** 2
                ) / number_of_atoms

                f[pair] /= normalization

        # Build the structure factor histogram
        if self.settings.quiet.get_value() == False:
            progress_bar = tqdm(
                range(len(q_norm_1D) - 1),
                desc="Building the structure factor histogram ...",
                colour="#00ffff",
                leave=False,
                unit="pair",
            )
            color_gradient = generate_color_gradient(len(q_norm_1D) - 1)
        else:
            progress_bar = range(len(q_norm_1D) - 1)
        for i in progress_bar:
            # Update progress bar
            if self.settings.quiet.get_value() == False:
                progress_bar.colour = "#%02x%02x%02x" % color_gradient[i]

            if q_norm_1D[i] == 0.0 or q_norm_1D[i] > 10.0:
                continue
            lower_bound = q_norm_1D[i]
            upper_bound = q_norm_1D[i + 1]

            q_lower = lower_bound <= q_norm
            q_upper = q_norm < upper_bound
            q = q_lower & q_upper
            elements_to_sum = np.where(q)

            for pair in structure_factor.keys():
                if pair == "q":
                    continue

                temp = f[pair][elements_to_sum]
                average = np.mean(temp)
                structure_factor[pair][i] += average

        self.q = structure_factor["q"]
        self.nsf = structure_factor

    @staticmethod
    @njit(parallel=True, nogil=True)
    def _calculate_neutron_structure_factor(qx, qy, qz, positions, progress_proxy):
        r"""
        Calculate the neutron structure factor of the atom.

        Returns:
        --------
            - nsf (float) : The neutron structure factor of the atom.
        """
        qcos, qsin = np.zeros_like(qx), np.zeros_like(qx)
        for i in prange(len(positions)):
            position = positions[i]
            dot = qx * position[0] + qy * position[1] + qz * position[2]
            sind = np.sin(dot)
            cosd = np.cos(dot)
            qcos += cosd
            qsin += sind
            if progress_proxy is not None:
                progress_proxy.update(1)

        return qcos, qsin
