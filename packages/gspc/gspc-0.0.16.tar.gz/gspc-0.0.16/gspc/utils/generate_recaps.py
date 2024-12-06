import numpy as np
import os
from natsort import natsorted


def make(export_directory):
    r"""
    This function is expected to be called in the export directory
    """

    # fetch directories
    dirs = natsorted(
        [
            d
            for d in os.listdir(export_directory)
            if os.path.isdir(os.path.join(export_directory, d))
        ]
    )

    # Fetch pression or temperature
    pressures = []
    temperatures = []

    # List of files that are distributions or histograms
    files_to_avoid = [
        "bond_angular_distribution",
        "pair_distribution_function",
        "neutron_structure_factor",
        "hist_polyhedricity.dat",
        "README.md",
    ]

    output = {}
    output["Pressure"] = []
    output["Temperature"] = []

    for dir in dirs:
        if dir == "recap.dat":
            continue
        files = os.listdir(os.path.join(export_directory, dir))
        for file in files:
            # Fetch thermodynamic informations.
            if file == "README.md":
                with open(os.path.join(export_directory, dir, file), "r") as f:
                    for li, line in enumerate(f):
                        try:
                            parts = line.split()
                            if parts[0] == "Pressure":
                                output["Pressure"].append(float(parts[-1]))
                            elif parts[0] == "Temperature":
                                output["Temperature"].append(float(parts[-1]))
                        except:
                            # line is empty, go next
                            continue

            # Fetch results but avoid distributions or histograms
            if file not in files_to_avoid:
                try:
                    parts = file.split("-")
                    if parts[0] not in files_to_avoid:
                        with open(os.path.join(export_directory, dir, file), "r") as f:
                            for li, line in enumerate(f):
                                if li == 0:
                                    # skip first line
                                    continue
                                if li == 1:
                                    # line 1 shall contains the keys
                                    keys = line.split()[1:]
                                    for key in keys:
                                        if key not in output:
                                            # create an entry in output the first time
                                            output[key] = []
                                if li == 2:
                                    # line 2 shall contains the results
                                    results = line.split()
                                    for i, key in enumerate(keys):
                                        output[key].append(float(results[i]))
                except:
                    continue

    with open(os.path.join(export_directory, "recap.dat"), "w") as f:
        nlines = len(output["Pressure"])
        # write header of the recap file
        f.write("# ")
        for k in output.keys():
            f.write(f"{k}\t")
        f.write("\n")

        # write the results
        for n in range(nlines):
            for k in output.keys():
                f.write(f"{output[k][n]}\t")
            f.write("\n")
