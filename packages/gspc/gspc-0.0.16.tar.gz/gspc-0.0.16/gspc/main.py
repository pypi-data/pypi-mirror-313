# internal imports
from . import io
from . import core
from .utils.generate_color_gradient import generate_color_gradient as gcg

# external imports
import numpy as np
from tqdm import tqdm
import os
import importlib
from datetime import datetime
import logging

def main(settings):
    if settings.logging.get_value():
        # Configure the logger
        os.makedirs("gspc_logs", exist_ok=True)
        log_filename = f"gspc_logs/gspc-{os.path.basename(settings.path_to_xyz_file.get_value())}-{datetime.now().strftime('%Y%m%d-%Hh%M')}.log"
        logging.basicConfig(
            filename=log_filename,
            filemode='a',
            format='%(asctime)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )
        logging.info("Starting main function")

    # Build the output directory
    new_directory = os.path.join(
        settings.export_directory.get_value(), settings.project_name.get_value()
    )
    settings._output_directory = new_directory

    # Create the output directory if it does not exist
    if not os.path.exists(settings._output_directory):
        os.makedirs(settings._output_directory)
        if settings.logging.get_value():
            logging.info(f"Created output directory: {settings._output_directory}")

    input_file = settings.path_to_xyz_file.get_value()

    # Count the number of configurations in the trajectory
    n_config = io.count_configurations(input_file)
    n_atoms = settings.number_of_atoms.get_value()
    n_header = settings.header.get_value()
    settings.number_of_frames.set_value(n_config)

    settings.print_settings()
    if settings.logging.get_value():
        logging.info("Settings printed")

    # Import the extension
    module = importlib.import_module(
        f"gspc.extensions.{settings.extension.get_value()}"
    )
    if settings.logging.get_value():
        logging.info(f"Imported extension module: {settings.extension.get_value()}")

    # Create the box object and append lattice for each frame
    box = core.Box()
    io.read_lattice_properties(box, input_file)
    if settings.logging.get_value():
        logging.info("Lattice properties read")

    # Create the Cutoff object
    cutoffs = core.Cutoff(settings.cutoffs.get_value())
    if settings.logging.get_value():
        logging.info("Cutoff object created")

    # Settings the for loop with user settings
    if settings.range_of_frames.get_value() is not None:
        start = settings.range_of_frames.get_value()[0]
        end = settings.range_of_frames.get_value()[1]
    else:
        start = 0
        end = n_config

    if end - start == 0:
        if settings.logging.get_value():
            logging.error("Range of frames selected is invalid")
        raise ValueError(
            f"\tERROR: Range of frames selected is invalid \u279c {settings.range_of_frames.get_value()}."
        )
    else:
        settings.frames_to_analyse.set_value(end - start)
        if settings.logging.get_value():
            logging.info(f"Frames to analyse: {end - start}")

    if not settings.quiet.get_value():
        color_gradient = gcg(end - start)
        progress_bar = tqdm(
            range(start, end),
            desc="Analysing trajectory ... ",
            unit="frame",
            leave=False,
            colour="YELLOW",
        )
    else:
        progress_bar = range(start, end)

    # Create the results objects
    # TODO complete the list of results objects # PRIO1
    if "pair_distribution_function" in settings.properties.get_value():
        results_pdf = {}
        keys_pdf = module.return_keys("pair_distribution_function")
        for key in keys_pdf:
            results_pdf[key] = io.DistResult("pair_distribution_function", key, start)
            results_pdf[key].write_file_header(settings._output_directory, end - start)
        results_md = io.PropResult("mean_distances", "mean_distances", start)
        results_md.write_file_header(settings._output_directory, end - start)
        if settings.logging.get_value():
            logging.info("Pair distribution function results objects created")

    if "bond_angular_distribution" in settings.properties.get_value():
        results_bad = {}
        keys_bad = module.return_keys("bond_angular_distribution")
        for key in keys_bad:
            results_bad[key] = io.DistResult("bond_angular_distribution", key, start)
            results_bad[key].write_file_header(settings._output_directory, end - start)
        results_ma = io.PropResult("mean_angles", "mean_angles", start)
        results_ma.write_file_header(settings._output_directory, end - start)
        if settings.logging.get_value():
            logging.info("Bond angular distribution results objects created")

    if "structural_units" in settings.properties.get_value():
        results_sru = {}
        keys_sru = module.return_keys("structural_units")
        for dict_key in keys_sru:
            for key in dict_key:
                if key == 'lifetime' or key == 'hist_polyhedricity':
                    for sub_key in dict_key[key]:
                        if sub_key == 'bins' or sub_key == 'time':
                            continue
                        results_sru[sub_key] = io.DistResult(key, sub_key, start)
                        results_sru[sub_key].write_file_header(settings._output_directory, end-start)
                else:
                    results_sru[key] = io.PropResult(key, dict_key[key], start)
                    results_sru[key].write_file_header(
                        settings._output_directory, end - start
                )
        if settings.logging.get_value():
            logging.info("Structural units results objects created")

    if "mean_square_displacement" in settings.properties.get_value():
        key = module.return_keys('mean_square_displacement')
        results_msd = io.MSDResult("mean_square_displacement", key, start)
        results_msd.write_file_header(settings._output_directory, end - start)
        if settings.logging.get_value():
            logging.info("Mean square displacement results object created")

    if "neutron_structure_factor" in settings.properties.get_value():
        results_nsf = {}
        keys_nsf = module.return_keys("neutron_structure_factor")
        for key in keys_nsf:
            results_nsf[key] = io.DistResult("neutron_structure_factor", key, start)
            results_nsf[key].write_file_header(settings._output_directory, end - start)
        if settings.logging.get_value():
            logging.info("Neutron structure factor results objects created")

    # Loop over the frames in the trajectory
    for i in progress_bar:
        if settings.logging.get_value():
            logging.info(f"Processing frame {i}")
        
        # Update the progress bar
        if not settings.quiet.get_value():
            progress_bar.set_description(f"Analysing trajectory n°{i} ... ")
            progress_bar.colour = "#%02x%02x%02x" % color_gradient[i - start]

        # Create the System object at the current frame
        if i == start:
            system, reference_positions = io.read_and_create_system(
                input_file, i, n_atoms + n_header, settings, cutoffs, start, end
            )
            for atom in system.atoms:
                for ref in reference_positions:
                    if atom.id == ref.id:
                        atom.set_reference_position(ref)
                        atom.set_current_position(ref)
                        # next atom
                        break

            system.init_mean_square_displacement()

            if "structural_units" in settings.properties.get_value():
                stored_forms = None

        else:
            if 'structural_units' in settings.properties.get_value():
                stored_forms = system.forms
            if 'mean_square_displacement' in settings.properties.get_value():
               store_msd = system.msd
            system, current_positions = io.read_and_create_system(
                input_file, i, n_atoms + n_header, settings, cutoffs, start, end
            )
            if 'mean_square_displacement' in settings.properties.get_value():
                system.msd = store_msd
                for atom in system.atoms:
                    for cur in current_positions:
                        if atom.id == cur.id:
                            atom.set_current_position(cur)
                            # next atom
                            break
                for atom in system.atoms:
                    for ref in reference_positions:
                        if atom.id == ref.id:
                            atom.set_reference_position(ref)
                            # next atom
                            break
        system.frame = i

        # Set the Box object to the System object
        system.box = box
        settings.lbox.set_value(system.box.get_box_dimensions(i))

        # Calculate the nearest neighbours of all atoms in the system
        system.calculate_neighbours()
        if settings.logging.get_value():
            logging.info(f"Calculated neighbours for frame {i}")

        # Calculate the mean square displacement
        if "mean_square_displacement" in settings.properties.get_value():
            if i != start:
                system.calculate_mean_square_displacement()
                results_msd.add_to_timeline(i, system.msd)
                if settings.logging.get_value():
                    logging.info(f"Calculated mean square displacement for frame {i}")

        # Calculate the structural units of the system
        if "structural_units" in settings.properties.get_value():
            system.calculate_structural_units(settings.extension.get_value())
            # Add the results to the timeline
            for d in keys_sru:
                key = list(d.keys())[0]
                sub_keys = d[key]
                if key == "lifetime" or key == "switch_probability":
                    continue
                elif key == 'hist_polyhedricity':
                    for k, sub_key in enumerate(sub_keys):
                        if sub_key == 'bins':
                            continue
                        results_sru[sub_key].add_to_timeline(
                            frame=i,
                            bins=system.structural_units[key][0],
                            hist=system.structural_units[key][k]
                        )
                else:
                    results_sru[key].add_to_timeline(
                        i, sub_keys, system.structural_units[key]
                    )

            stored_forms = system.append_forms(stored_forms)
            if settings.logging.get_value():
                logging.info(f"Calculated structural units for frame {i}")

        # Calculate the bond angular distribution
        if "bond_angular_distribution" in settings.properties.get_value():
            system.calculate_bond_angular_distribution()
            # Add the results to the timeline
            for key in keys_bad:
                results_bad[key].add_to_timeline(
                    i, system.angles["theta"], system.angles[key]
                )
            results_ma.add_to_timeline(i, system.mean_angles.keys(), system.mean_angles.values())
            if settings.logging.get_value():
                logging.info(f"Calculated bond angular distribution for frame {i}")

        # Calculate the pair distribution function
        if "pair_distribution_function" in settings.properties.get_value():
            system.calculate_pair_distribution_function()
            # Add the results to the timeline
            for key in keys_pdf:
                results_pdf[key].add_to_timeline(
                    i, system.distances["r"], system.distances[key]
                )
            results_md.add_to_timeline(i, system.mean_distances.keys(), system.mean_distances.values())
            if settings.logging.get_value():
                logging.info(f"Calculated pair distribution function for frame {i}")

        if "neutron_structure_factor" in settings.properties.get_value():
            system.calculate_neutron_structure_factor(keys_nsf)
            # Add the results to the timeline
            for key in keys_nsf:
                results_nsf[key].add_to_timeline(i, system.q, system.nsf[key])
            if settings.logging.get_value():
                logging.info(f"Calculated neutron structure factor for frame {i}")

    if "pair_distribution_function" in settings.properties.get_value():
        for key in keys_pdf:
            results_pdf[key].calculate_average_distribution()
            results_pdf[key].append_results_to_file()
        results_md.calculate_average_proportion()
        results_md.append_results_to_file()
        if settings.logging.get_value():
            logging.info("Pair distribution function results appended to file")

    if "bond_angular_distribution" in settings.properties.get_value():
        for key in keys_bad:
            results_bad[key].calculate_average_distribution()
            results_bad[key].append_results_to_file()
        results_ma.calculate_average_proportion()
        results_ma.append_results_to_file()
        if settings.logging.get_value():
            logging.info("Bond angular distribution results appended to file")
        
    if "mean_square_displacement" in settings.properties.get_value():
        results_msd.calculate_average_msd(system.calculate_mass_per_species())
        results_msd.append_results_to_file(
            settings.msd_settings.get_dt(), settings.msd_settings.get_printlevel()
        )
        if settings.logging.get_value():
            logging.info("Mean square displacement results appended to file")
        
    if "structural_units" in settings.properties.get_value():
        lifetime, switch_probability = system.calculate_lifetime()
        for d in keys_sru:
            key = list(d.keys())[0]
            if key == "hist_polyhedricity":
                sub_keys = d[key]
                for k, sub_key in enumerate(sub_keys):
                    if sub_key == 'bins':
                        continue
                    results_sru[sub_key].calculate_average_distribution()
                    results_sru[sub_key].append_results_to_file()
            elif key == "switch_probability" or key == "lifetime":
                lifetime, switch_probability = system.calculate_lifetime()
                if key == "lifetime":
                    sub_key = d[key]
                    for k, sub_key in enumerate(sub_key):
                        if sub_key == 'time':
                            continue
                        results_sru[sub_key].add_to_timeline(
                            frame=i,
                            bins=lifetime['time'],
                            hist=lifetime[sub_key]
                        )
                        results_sru[sub_key].calculate_average_distribution()
                        results_sru[sub_key].append_results_to_file()
                else:
                    results_sru[key].add_to_timeline(
                        frame=i,
                        keys=switch_probability.keys(),
                        values=switch_probability.values()
                    )
                    results_sru[key].calculate_average_proportion()
                    results_sru[key].append_results_to_file()
            else:
                results_sru[key].calculate_average_proportion()
                results_sru[key].append_results_to_file()
        if settings.logging.get_value():
            logging.info("Structural units results appended to file")

    if "neutron_structure_factor" in settings.properties.get_value():
        for key in keys_nsf:
            results_nsf[key].calculate_average_distribution()
            results_nsf[key].append_results_to_file()
        if settings.logging.get_value():
            logging.info("Neutron structure factor results appended to file")

    settings.write_readme_file()
    if settings.logging.get_value():
        logging.info("Readme file written")
        logging.info("Main function completed")
    # END OF MAIN FUNCTION
