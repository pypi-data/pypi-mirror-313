# internal imports
from .parameter import Parameter, PDFParameter, BADParameter, MSDParameter

# external imports
import importlib


class Settings:
    """
    Represents the settings for a project.

    Attributes:
    -----------

    Methods:
    --------


    """

    def __init__(self, extension) -> None:
        """
        Initializes a Settings object with default settings.

        Parameters:
        -----------
            - extension (str): The extension of the project.
        """
        self.load_default_settings(extension)

    def load_default_settings(self, extension) -> None:
        """
        Loads default settings based on the extension.

        Parameters:
        -----------
            - extension (str): The extension of the project.
        """
        self.project_name: Parameter = Parameter("project_name", "default")
        self.export_directory: Parameter = Parameter("export_directory", "export")
        self._output_directory: str = ""
        self.build_fancy_recaps: Parameter = Parameter("build_fancy_recaps", False)
        self.build_fancy_plots: Parameter = Parameter("build_fancy_plots", False)
        self.path_to_xyz_file: Parameter = Parameter("path_to_xyz_file", "default.xyz")
        self.number_of_atoms: Parameter = Parameter("number_of_atoms", 0)
        self.number_of_frames: Parameter = Parameter("number_of_frames", 0)
        self.header: Parameter = Parameter("header", 0)
        self.range_of_frames: Parameter = Parameter("range_of_frames", None)
        self.frames_to_analyse: Parameter = Parameter("frames_to_analyse", 0)
        self.timestep: Parameter = Parameter("timestep", 0.0016)
        self.lbox: Parameter = Parameter("lbox", 0)
        self.temperature: Parameter = Parameter("temperature", 300)
        self.pressure: Parameter = Parameter("pressure", 0)
        self.version: Parameter = Parameter("version", "0.0.16")
        self.quiet: Parameter = Parameter("quiet", False)
        self.overwrite_results: Parameter = Parameter("overwrite_results", False)
        self.logging: Parameter = Parameter("logging", False)

        self.supported_extensions: Parameter = Parameter(
            "extensions", ["SiO2", "NSx"]
        )  # Update the list of supported extensions when adding a new one

        if extension in self.supported_extensions.get_value():
            module = importlib.import_module(f"gspc.extensions.{extension}")
            default_settings = module.get_default_settings()
            self.extension: Parameter = default_settings["extension"]
            self.structure: Parameter = default_settings["structure"]
            self.cutoffs: Parameter = default_settings["cutoffs"]
        else:
            raise ValueError(
                f"Unsupported extension: {extension}. Please choose one of the following: {self.supported_extensions.get_value()}."
            )

        list_properties = [
            "mean_square_displacement",
            "pair_distribution_function",
            "bond_angular_distribution",
            "structural_units",
            "neutron_structure_factor",
        ]

        self.properties: Parameter = Parameter("properties", list_properties)

        self.pdf_settings: PDFParameter = PDFParameter(nbins=600, rmax=10.0)
        self.bad_settings: BADParameter = BADParameter(nbins=600, theta_max=180.0)
        self.msd_settings: MSDParameter = MSDParameter(dt=0.0016, printlevel=1)

    def print_settings(self) -> None:
        """
        Prints the current settings.
        """
        max_attr_length = max(len(attr) for attr in self.__dict__)
        separator = "\t\t________________________________________________"
        settings_output = f"\tSETTINGS:\n{separator}\n"
        max_attr_length = max(len("Path to input file"), len("Number of frames"))
        settings_output += f"\t\t{'Path to input file'.ljust(max_attr_length)} \u279c\t {self.path_to_xyz_file.get_value()}\n"
        settings_output += f"\t\t{'Number of frames'.ljust(max_attr_length)} \u279c\t {self.number_of_frames.get_value()}\n"
        if self.range_of_frames.get_value() is not None:
            settings_output += (
                f"\t\tRange of frames    \u279c\t {self.range_of_frames.get_value()}\n"
            )
        settings_output += f"{separator}\n"
        settings_output += f"\t\tStructure:\n"
        max_attr_length = max(len("Number of atoms"), len("Species"))
        settings_output += f"\t\t  {'Number of atoms'.ljust(int(max_attr_length/2))} \u279c\t {self.number_of_atoms.get_value()}\n"
        for atom in self.structure.get_value():
            settings_output += f"\t\t  {'Species'.ljust(max_attr_length)} \u279c\t {atom['element']:2}\t|\tNumber of atoms \u279c\t {atom['number']}\n"
        settings_output += f"{separator}\n"
        settings_output += (
            f"\t\tExport directory   \u279c\t {self.export_directory.get_value()}/{self.project_name.get_value()}\n"
        )
        settings_output += f"{separator}\n"
        settings_output += f"\t\tStructural properties:\n"
        max_attr_length = max(len(prop) for prop in self.properties.get_value())
        for prop in self.properties.get_value():
            settings_output += f"\t\t\t\u279c {prop}\n"
            # TODO : add the detail of the properties like :
            #        -> mean_square_displacement : dt, printlevel

        settings_output += "\n"
        if self.quiet.get_value() == False:
            print("\r" + settings_output, end="")
            self.settings_to_print = settings_output
        else:
            self.settings_to_print = settings_output

    def print_all_settings(self) -> None:
        """
        Prints all settings, including those not recommended for printing.
        """
        max_attr_length = max(len(attr) for attr in self.__dict__)
        separator = "\t\t________________________________________________"
        print(f"\tSETTINGS:")
        print(separator)
        for p, v in self.__dict__.items():
            print(f"\t\t{v.get_name().ljust(max_attr_length)} ➜ {v.get_value()}")

    def write_readme_file(self) -> None:
        """
        Writes the settings to a README file.
        """
        from datetime import datetime

        with open(f"{self._output_directory}/README.md", "w") as f:
            f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Version: {self.version.get_value()}\n")
            f.write(f"# {self.project_name.get_value()}\n")
            f.write("## Settings\n")
            f.write(f"### Input file\n")
            f.write(f"- Path to input file: {self.path_to_xyz_file.get_value()}\n")
            f.write(f"- Number of frames: {self.number_of_frames.get_value()}\n")
            if self.range_of_frames.get_value() is not None:
                f.write(f"- Range of frames: {self.range_of_frames.get_value()}\n")
            f.write(f"### Structure\n")
            f.write(f"- Number of atoms: {self.number_of_atoms.get_value()}\n")
            for atom in self.structure.get_value():
                f.write(
                    f"- Species: {atom['element']} | Number of atoms: {atom['number']}\n"
                )
            f.write(f"### Export\n")
            f.write(f"- Export directory: {self.export_directory.get_value()}/{self.project_name.get_value()}\n")
            f.write(f"### Structural properties\n")
            for prop in self.properties.get_value():
                f.write(f"- {prop}\n")

            f.write("## Informations\n")
            f.write(f"Pressure (GPa) : {self.pressure.get_value()}\n")
            f.write(f"Temperature (K) : {self.temperature.get_value()}\n")
            f.write(f"Timestep (ps) : {self.timestep.get_value()}\n")
            f.write(
                f"Time of simulation (ps) : {self.msd_settings.return_duration(self.number_of_frames.get_value())}\n"
            )
