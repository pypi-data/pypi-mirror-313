from ase.optimize import LBFGS, BFGS, GPMin, FIRE, MDMin, BFGSLineSearch
import os
import pickle
import json
import time
from copy import deepcopy
from ase.constraints import FixAtoms
import numpy as np
from ase.io import read, write
import requests
import io
import copy
from ase.io import read
import matplotlib.pyplot as plt
import pandas as pd
import xlsxwriter
import traceback

GRAPHQL = "http://api.catalysis-hub.org/graphql"


def convert_trajectory(filename):
    images = read(filename, index=":")
    os.remove(filename)
    write(filename, images, format="extxyz")


def energy_cal_gas(
    calculator,
    atoms_origin,
    F_CRIT_RELAX,
    save_path,
    gas_distance,
    optimizer,
    log_path="no",
    filename="",
):
    optimizer_classes = {
        "LBFGS": LBFGS,
        "BFGS": BFGS,
        "GPMin": GPMin,
        "FIRE": FIRE,
        "MDMin": MDMin,
        "BFGSLineSearch": BFGSLineSearch,
    }

    if optimizer in optimizer_classes:
        # 선택한 optimizer 클래스 가져오기
        OptClass = optimizer_classes[optimizer]
        atoms = deepcopy(atoms_origin)
        atoms.calc = calculator
        atomic_numbers = atoms.get_atomic_numbers()
        max_atomic_number = np.max(atomic_numbers)
        max_atomic_number_indices = [
            i for i, num in enumerate(atomic_numbers) if num == max_atomic_number
        ]
        fixed_atom_index = np.random.choice(max_atomic_number_indices)
        c = FixAtoms(indices=[fixed_atom_index])
        atoms.set_constraint(c)
        tags = np.ones(len(atoms))
        atoms.set_tags(tags)
        while True:
            try:
                cell_size = [gas_distance, gas_distance, gas_distance]
                atoms.set_cell(cell_size)
                atoms.center()

                write(save_path, atoms)

                time_init = time.time()
                logfile = open(log_path, "w", buffering=1)
                logfile.write("######################\n")
                logfile.write("##  GNN relax starts  ##\n")
                logfile.write("######################\n")
                logfile.write("\nStep 1. Relaxing\n")

                opt = OptClass(atoms, logfile=logfile, trajectory=filename)
                opt.run(fmax=F_CRIT_RELAX, steps=500)

                convert_trajectory(filename)
                logfile.write("Done!\n")
                elapsed_time = time.time() - time_init
                logfile.write(f"\nElapsed time: {elapsed_time} s\n\n")
                logfile.write("###############################\n")
                logfile.write("##  Relax terminated normally  ##\n")
                logfile.write("###############################\n")
                logfile.close()

                return atoms, atoms.get_potential_energy()

            except Exception as e:
                # If an error occurs, reduce gas_distance by 0.5 and try again
                print(
                    f"Error occurred: {e}. Reducing gas_distance by 0.5 and retrying..."
                )
                gas_distance -= 0.5
                print(f"Gas_cell_size : {gas_distance}")

                # Ensure that gas_distance does not go below a reasonable limit
                if gas_distance <= 0:
                    raise ValueError("gas_distance has become too small to proceed.")


def energy_cal_single(calculator, atoms_origin):
    atoms = deepcopy(atoms_origin)
    atoms.calc = calculator
    tags = np.ones(len(atoms))
    atoms.set_tags(tags)

    return atoms.get_potential_energy()


def energy_cal(
    calculator,
    atoms_origin,
    F_CRIT_RELAX,
    N_CRIT_RELAX,
    damping,
    z_target,
    optimizer,
    logfile="",
    filename="",
):
    atoms = deepcopy(atoms_origin)
    atoms.calc = calculator
    tags = np.ones(len(atoms))
    atoms.set_tags(tags)
    if z_target != 0:
        atoms.set_constraint(fixatom(atoms, z_target))

    optimizer_classes = {
        "LBFGS": LBFGS,
        "BFGS": BFGS,
        "GPMin": GPMin,
        "FIRE": FIRE,
        "MDMin": MDMin,
        "BFGSLineSearch": BFGSLineSearch,
    }

    if optimizer in optimizer_classes:
        # 선택한 optimizer 클래스 가져오기
        OptClass = optimizer_classes[optimizer]

        if logfile == "no":
            # opt = OptClass(atoms, logfile=None, damping=damping)
            opt = OptClass(atoms, logfile=None)
            opt.run(fmax=F_CRIT_RELAX, steps=N_CRIT_RELAX)
            elapsed_time = 0
        else:
            time_init = time.time()
            logfile = open(logfile, "w", buffering=1)
            logfile.write("######################\n")
            logfile.write("##  GNN relax starts  ##\n")
            logfile.write("######################\n")
            logfile.write("\nStep 1. Relaxing\n")
            # opt = OptClass(atoms, logfile=logfile, trajectory=filename, damping=damping)
            opt = OptClass(atoms, logfile=logfile, trajectory=filename)
            opt.run(fmax=F_CRIT_RELAX, steps=N_CRIT_RELAX)
            convert_trajectory(filename)
            logfile.write("Done!\n")
            elapsed_time = time.time() - time_init
            logfile.write(f"\nElapsed time: {elapsed_time} s\n\n")
            logfile.write("###############################\n")
            logfile.write("##  Relax terminated normally  ##\n")
            logfile.write("###############################\n")
            logfile.close()

    return atoms.get_potential_energy(), opt.nsteps, atoms, elapsed_time


def fixatom(atoms, z_target):
    indices_to_fix = [atom.index for atom in atoms if atom.position[2] < z_target]
    const = FixAtoms(indices=indices_to_fix)
    return const


def calc_displacement(atoms1, atoms2):
    positions1 = atoms1.get_positions()
    positions2 = atoms2.get_positions()
    displacements = positions2 - positions1
    displacement_magnitudes = np.linalg.norm(displacements, axis=1)
    max_displacement = np.max(displacement_magnitudes)
    return max_displacement


def find_median_index(arr):
    orig_arr = deepcopy(arr)
    sorted_arr = sorted(arr)
    length = len(sorted_arr)
    median_index = (length - 1) // 2
    median_value = sorted_arr[median_index]
    for i, num in enumerate(orig_arr):
        if num == median_value:
            return i, median_value


def fix_z(atoms, rate_fix):
    if rate_fix:
        z_max = max(atoms.positions[:, 2])
        z_min = min(atoms.positions[:, 2])
        z_target = z_min + rate_fix * (z_max - z_min)

        return z_target

    else:
        return 0


def process_output(dataset_name, coeff_setting):
    for dirpath, dirnames, filenames in os.walk(dataset_name):
        # OSZICAR와 CONTCAR 파일이 모두 있는지 확인합니다.
        if "OSZICAR" in filenames and "CONTCAR" in filenames:
            # 해당 폴더 내의 모든 파일을 순회합니다.
            for file in filenames:
                # 파일 이름이 OSZICAR 또는 CONTCAR가 아니라면 삭제합니다.
                if file not in ["OSZICAR", "CONTCAR"]:  # , "coeff.json"]:
                    file_path = os.path.join(dirpath, file)
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")

            rxn_name = dirpath.split("/")[2]

            not_calc_dirs = [
                name
                for name in os.listdir(f"{dataset_name}/gas")
                if os.path.isdir(os.path.join(f"{dataset_name}/gas", name))
            ] + ["slab"]

            if rxn_name not in not_calc_dirs:
                coeff = coeff_setting[rxn_name]
            else:
                coeff = {}

            coeff_path = os.path.join(dirpath, "coeff.json")
            if not os.path.exists(coeff_path) and coeff != {}:
                with open(coeff_path, "w") as json_file:
                    json.dump(coeff, json_file, indent=4)

    for dir_name in os.listdir(dataset_name):
        dir_path = os.path.join(dataset_name, dir_name)
        if os.path.isdir(dir_path) and dir_name != "gas":
            slab_folder_path = os.path.join(dir_path, "slab")
            os.makedirs(slab_folder_path, exist_ok=True)


def userdata_preprocess(dataset_name):
    save_directory = os.path.join(os.getcwd(), "raw_data")
    os.makedirs(save_directory, exist_ok=True)
    path_output = os.path.join(os.getcwd(), f"raw_data/{dataset_name}.pkl")
    data_total = {}
    tags = []
    not_calc_dirs = [
        name
        for name in os.listdir(f"{dataset_name}/gas")
        if os.path.isdir(os.path.join(f"{dataset_name}/gas", name))
    ] + ["slab"]

    for dirpath, dirnames, filenames in os.walk(dataset_name):
        if "OSZICAR" in filenames and "CONTCAR" in filenames:
            rxn_name = dirpath.split("/")[2]
            if rxn_name not in not_calc_dirs:
                input = {}
                slab_name = dirpath.split("/")[1]
                slab_path = dirpath[: dirpath.find("/", dirpath.find("/") + 1)]

                coeff_path = os.path.join(dirpath, "coeff.json")
                with open(coeff_path, "r") as file:
                    coeff = json.load(file)

                tag = slab_name + "_" + rxn_name

                if tag in tags:
                    count = tags.count(tag)
                    tags.append(tag)
                    tag = f"{tag}_{count}"
                else:
                    tags.append(tag)

                input["star"] = {
                    "stoi": coeff["slab"],
                    "atoms": read(f"{slab_path}/slab/CONTCAR"),
                    "energy_cathub": read_E0_from_OSZICAR(f"{slab_path}/slab/OSZICAR"),
                }

                input[f"{rxn_name}star"] = {
                    "stoi": coeff["adslab"],
                    "atoms": read(f"{dirpath}/CONTCAR"),
                    "energy_cathub": read_E0_from_OSZICAR(f"{dirpath}/OSZICAR"),
                }

                for key in coeff:
                    if key not in ["slab", "adslab"]:
                        input[key] = {
                            "stoi": coeff[key],
                            "atoms": read(f"{dataset_name}/gas/{key}/CONTCAR"),
                            "energy_cathub": read_E0_from_OSZICAR(
                                f"{dataset_name}/gas/{key}/OSZICAR"
                            ),
                        }

                energy_check = 0
                for structure in input:
                    energy_check += (
                        input[structure]["energy_cathub"] * input[structure]["stoi"]
                    )

                data_total[tag] = {}

                data_total[tag]["raw"] = input
                data_total[tag]["cathub_energy"] = energy_check

    print(f"# of reactions : {len(data_total)}")

    with open(path_output, "wb") as file:
        pickle.dump(data_total, file)


def read_E0_from_OSZICAR(file_path):
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            last_line = lines[-1]

        # 'E0=' 다음의 값을 추출
        energy = None
        for word in last_line.split():
            if word == "E0=":
                energy_index = last_line.split().index(word) + 1
                energy = last_line.split()[energy_index]
                energy = float(energy)
                break

        if energy is None:
            raise ValueError(f"Energy value not found in file: {file_path}")

        return energy

    except Exception as e:
        raise RuntimeError(
            f"An error occurred while reading the file '{file_path}': {str(e)}"
        )


def execute_benchmark(calculators, **kwargs):
    required_keys = ["GNN_name", "benchmark"]

    if not isinstance(calculators, list) or len(calculators) == 0:
        raise ValueError("Calculators must be a non-empty list.")

    for key in required_keys:
        if key not in kwargs:
            raise ValueError(f"Missing required keyword argument: {key}")

    GNN_name = kwargs["GNN_name"]
    benchmark = kwargs["benchmark"]
    F_CRIT_RELAX = kwargs.get("F_CRIT_RELAX", 0.05)
    N_CRIT_RELAX = kwargs.get("N_CRIT_RELAX", 999)
    rate = kwargs.get("rate", 0.5)
    disp_thrs_slab = kwargs.get("disp_thrs_slab", 1.0)
    disp_thrs_ads = kwargs.get("disp_thrs_ads", 1.5)
    again_seed = kwargs.get("again_seed", 0.2)
    damping = kwargs.get("damping", 1.0)
    gas_distance = kwargs.get("gas_distance", 10)
    optimizer = kwargs.get("optimizer", "LBFGS")

    path_pkl = os.path.join(os.getcwd(), f"raw_data/{benchmark}.pkl")

    with open(path_pkl, "rb") as file:
        cathub_data = pickle.load(file)

    save_directory = os.path.join(os.getcwd(), "result", GNN_name)
    print(f"Starting {GNN_name} Benchmarking")
    # Basic Settings==============================================================================
    os.makedirs(f"{save_directory}/traj", exist_ok=True)
    os.makedirs(f"{save_directory}/log", exist_ok=True)
    os.makedirs(f"{save_directory}/gases", exist_ok=True)
    os.makedirs(f"{save_directory}/gases/POSCARs", exist_ok=True)
    os.makedirs(f"{save_directory}/gases/CONTCARs", exist_ok=True)
    os.makedirs(f"{save_directory}/gases/traj", exist_ok=True)
    os.makedirs(f"{save_directory}/gases/log", exist_ok=True)

    final_result = {}

    final_outlier = {}
    final_outlier["Time"] = []
    final_outlier["normal"] = []
    final_outlier["outlier"] = []

    # Calculation Part==============================================================================

    accum_time = 0
    gas_energies = {}

    print("Starting calculations...")
    for index, key in enumerate(cathub_data):
        print(f"[{index+1}/{len(cathub_data)}] {key}")
        final_result[key] = {}
        final_result[key]["cathub"] = {}
        final_result[key]["cathub"]["ads_eng"] = cathub_data[key]["cathub_energy"]
        for structure in cathub_data[key]["raw"]:
            if "gas" not in str(structure):
                final_result[key]["cathub"][f"{structure}_abs"] = cathub_data[key][
                    "raw"
                ][structure]["energy_cathub"]
        final_result[key]["outliers"] = {
            "slab_conv": 0,
            "ads_conv": 0,
            "slab_move": 0,
            "ads_move": 0,
            "slab_seed": 0,
            "ads_seed": 0,
            "ads_eng_seed": 0,
        }

        trag_path = f"{save_directory}/traj/{key}"
        log_path = f"{save_directory}/log/{key}"

        os.makedirs(trag_path, exist_ok=True)
        os.makedirs(log_path, exist_ok=True)

        POSCAR_star = cathub_data[key]["raw"]["star"]["atoms"]
        z_target = fix_z(POSCAR_star, rate)

        informs = {}
        informs["ads_eng"] = []
        informs["slab_disp"] = []
        informs["ads_disp"] = []
        informs["slab_seed"] = []
        informs["ads_seed"] = []

        time_total_slab = 0
        time_total_ads = 0

        for i in range(len(calculators)):
            ads_energy_calc = 0
            for structure in cathub_data[key]["raw"]:
                if "gas" not in str(structure):
                    POSCAR_str = cathub_data[key]["raw"][structure]["atoms"]
                    (
                        energy_calculated,
                        steps_calculated,
                        CONTCAR_calculated,
                        time_calculated,
                    ) = energy_cal(
                        calculators[i],
                        POSCAR_str,
                        F_CRIT_RELAX,
                        N_CRIT_RELAX,
                        damping,
                        z_target,
                        optimizer,
                        f"{log_path}/{structure}_{i}.txt",
                        f"{trag_path}/{structure}_{i}",
                    )
                    ads_energy_calc += (
                        energy_calculated * cathub_data[key]["raw"][structure]["stoi"]
                    )
                    accum_time += time_calculated
                    if structure == "star":
                        slab_steps = steps_calculated
                        slab_displacement = calc_displacement(
                            POSCAR_str, CONTCAR_calculated
                        )
                        slab_energy = energy_calculated
                        slab_time = time_calculated
                        time_total_slab += time_calculated
                    else:
                        ads_step = steps_calculated
                        ads_displacement = calc_displacement(
                            POSCAR_str, CONTCAR_calculated
                        )
                        ads_energy = energy_calculated
                        ads_time = time_calculated
                        time_total_ads += time_calculated
                else:
                    gas_tag = f"{structure}_{i}th"
                    if gas_tag in gas_energies:
                        ads_energy_calc += (
                            gas_energies[gas_tag]
                            * cathub_data[key]["raw"][structure]["stoi"]
                        )
                    else:
                        print(f"{gas_tag} calculating")
                        gas_CONTCAR, gas_energy = energy_cal_gas(
                            calculators[i],
                            cathub_data[key]["raw"][structure]["atoms"],
                            F_CRIT_RELAX,
                            f"{save_directory}/gases/POSCARs/POSCAR_{gas_tag}",
                            gas_distance,
                            optimizer,
                            f"{save_directory}/gases/log/{gas_tag}.txt",
                            f"{save_directory}/gases/traj/{gas_tag}",
                        )
                        gas_energies[gas_tag] = gas_energy
                        ads_energy_calc += (
                            gas_energy * cathub_data[key]["raw"][structure]["stoi"]
                        )
                        write(
                            f"{save_directory}/gases/CONTCARs/CONTCAR_{gas_tag}",
                            gas_CONTCAR,
                        )

            if slab_steps == N_CRIT_RELAX:
                final_result[key]["outliers"]["slab_conv"] += 1

            if ads_step == N_CRIT_RELAX:
                final_result[key]["outliers"]["ads_conv"] += 1

            if slab_displacement > disp_thrs_slab:
                final_result[key]["outliers"]["slab_move"] += 1

            if ads_displacement > disp_thrs_ads:
                final_result[key]["outliers"]["ads_move"] += 1

            final_result[key][f"{i}"] = {
                "ads_eng": ads_energy_calc,
                "slab_abs": slab_energy,
                "ads_abs": ads_energy,
                "slab_disp": slab_displacement,
                "ads_disp": ads_displacement,
                "time_slab": slab_time,
                "time_ads": ads_time,
            }

            informs["ads_eng"].append(ads_energy_calc)
            informs["slab_disp"].append(slab_displacement)
            informs["ads_disp"].append(ads_displacement)
            informs["slab_seed"].append(slab_energy)
            informs["ads_seed"].append(ads_energy)

        ads_med_index, ads_med_eng = find_median_index(informs["ads_eng"])
        slab_seed_range = np.max(np.array(informs["slab_seed"])) - np.min(
            np.array(informs["slab_seed"])
        )
        ads_seed_range = np.max(np.array(informs["ads_seed"])) - np.min(
            np.array(informs["ads_seed"])
        )
        ads_eng_seed_range = np.max(np.array(informs["ads_eng"])) - np.min(
            np.array(informs["ads_eng"])
        )
        if slab_seed_range > again_seed:
            final_result[key]["outliers"]["slab_seed"] = 1
        if ads_seed_range > again_seed:
            final_result[key]["outliers"]["ads_seed"] = 1
        if ads_eng_seed_range > again_seed:
            final_result[key]["outliers"]["ads_eng_seed"] = 1

        final_result[key]["final"] = {
            "ads_eng_median": ads_med_eng,
            "median_num": ads_med_index,
            "slab_max_disp": np.max(np.array(informs["slab_disp"])),
            "ads_max_disp": np.max(np.array(informs["ads_disp"])),
            "slab_seed_range": slab_seed_range,
            "ads_seed_range": ads_seed_range,
            "ads_eng_seed_range": ads_eng_seed_range,
            "time_total_slab": time_total_slab,
            "time_total_ads": time_total_ads,
        }

        outlier_sum = sum(final_result[key]["outliers"].values())
        final_outlier["Time"] = accum_time

        if outlier_sum == 0:
            final_outlier["normal"].append(key)
        else:
            final_outlier["outlier"].append(key)

        with open(f"{save_directory}/{GNN_name}_result.json", "w") as file:
            json.dump(final_result, file, indent=4)

        with open(f"{save_directory}/{GNN_name}_outlier.json", "w") as file:
            json.dump(final_outlier, file, indent=4)

        with open(f"{save_directory}/{GNN_name}_gases.json", "w") as file:
            json.dump(gas_energies, file, indent=4)

    print(f"{GNN_name} Benchmarking Finish")


def fetch(query):
    return requests.get(GRAPHQL, {"query": query}).json()["data"]


def reactions_from_dataset(pub_id, page_size=40):
    reactions = []
    has_next_page = True
    start_cursor = ""
    page = 0
    while has_next_page:
        data = fetch(
            """{{
      reactions(pubId: "{pub_id}", first: {page_size}, after: "{start_cursor}") {{
        totalCount
        pageInfo {{
          hasNextPage
          hasPreviousPage
          startCursor
          endCursor
        }}
        edges {{
          node {{
            Equation
            reactants
            products
            reactionEnergy
            reactionSystems {{
              name
              systems {{
                energy
                InputFile(format: "json")
              }}
            }}
          }}
        }}
      }}
    }}""".format(
                start_cursor=start_cursor,
                page_size=page_size,
                pub_id=pub_id,
            )
        )
        has_next_page = data["reactions"]["pageInfo"]["hasNextPage"]
        start_cursor = data["reactions"]["pageInfo"]["endCursor"]
        page += 1
        print(
            has_next_page,
            start_cursor,
            page_size * page,
            data["reactions"]["totalCount"],
        )
        reactions.extend(map(lambda x: x["node"], data["reactions"]["edges"]))

    return reactions


def aseify_reactions(reactions):
    for i, reaction in enumerate(reactions):
        for j, _ in enumerate(reactions[i]["reactionSystems"]):
            system_info = reactions[i]["reactionSystems"][j].pop("systems")

            with io.StringIO() as tmp_file:
                tmp_file.write(system_info.pop("InputFile"))
                tmp_file.seek(0)
                atoms = read(tmp_file, format="json")
                atoms.pbc = True
                reactions[i]["reactionSystems"][j]["atoms"] = atoms

            reactions[i]["reactionSystems"][j]["energy"] = system_info["energy"]

        reactions[i]["reactionSystems"] = {
            x["name"]: {"atoms": x["atoms"], "energy": x["energy"]}
            for x in reactions[i]["reactionSystems"]
        }


def cathub_preprocess(benchmark):
    save_directory = os.path.join(os.getcwd(), "raw_data")
    os.makedirs(save_directory, exist_ok=True)
    path_json = os.path.join(save_directory, f"{benchmark}.json")
    path_output = os.path.join(os.getcwd(), f"raw_data/{benchmark}.pkl")
    if not os.path.exists(path_output):
        if not os.path.exists(path_json):
            raw_reactions = reactions_from_dataset(benchmark)
            raw_reactions_json = {"raw_reactions": raw_reactions}
            with open(path_json, "w") as file:
                json.dump(raw_reactions_json, file, indent=4)

        with open(path_json, "r") as f:
            data = json.load(f)
        loaded_data = data["raw_reactions"]
        dat = copy.deepcopy(loaded_data)
        aseify_reactions(dat)

        data_total = {}
        tags = []

        for i, _ in enumerate(dat):
            try:
                input = {}
                input_slab_1_check = {}
                reactants_json = dat[i]["reactants"]
                reactants_dict = json.loads(reactants_json)

                products_json = dat[i]["products"]
                products_dict = json.loads(products_json)

                if "star" not in dat[i]["reactionSystems"]:
                    print(f"Error at {dat[i]}: star not exist in reaction")
                    continue

                sym = dat[i]["reactionSystems"]["star"]["atoms"].get_chemical_formula()
                reaction_name = dat[i]["Equation"]

                tag = sym + "_" + reaction_name
                if tag in tags:
                    count = tags.count(tag)
                    tags.append(tag)
                    tag = f"{tag}_{count}"
                else:
                    tags.append(tag)

                if "star" not in reactants_dict:
                    print(f"Error at {tag}: star not exist in reactants")
                    if tag in data_total:
                        del data_total[tag]
                    if tag in tags:
                        tags.remove(tag)
                    continue

                for key in dat[i]["reactionSystems"]:
                    if key in reactants_dict:
                        input[key] = {
                            "stoi": -reactants_dict[key],
                            "atoms": dat[i]["reactionSystems"][key]["atoms"],
                            "energy_cathub": dat[i]["reactionSystems"][key]["energy"],
                        }
                        input_slab_1_check[key] = {
                            "stoi": -reactants_dict[key],
                            "atoms": dat[i]["reactionSystems"][key]["atoms"],
                            "energy_cathub": dat[i]["reactionSystems"][key]["energy"],
                        }
                    elif key in products_dict:
                        input[key] = {
                            "stoi": products_dict[key],
                            "atoms": dat[i]["reactionSystems"][key]["atoms"],
                            "energy_cathub": dat[i]["reactionSystems"][key]["energy"],
                        }
                        input_slab_1_check[key] = {
                            "stoi": 1,
                            "atoms": dat[i]["reactionSystems"][key]["atoms"],
                            "energy_cathub": dat[i]["reactionSystems"][key]["energy"],
                        }

                data_total[tag] = {}
                data_total[tag]["raw"] = input
                data_total[tag]["cathub_energy"] = dat[i]["reactionEnergy"]
                energy_check = 0
                energy_check_slab_1 = 0
                star_num = 0
                for structure in input:
                    if "star" in str(structure):
                        star_num += 1
                    energy_check += (
                        input[structure]["energy_cathub"] * input[structure]["stoi"]
                    )
                    energy_check_slab_1 += (
                        input_slab_1_check[structure]["energy_cathub"]
                        * input_slab_1_check[structure]["stoi"]
                    )

                if star_num != 2:
                    print(f"Error at {tag}: Stars are not 2")
                    if tag in data_total:
                        del data_total[tag]
                    if tag in tags:
                        tags.remove(tag)
                    continue

                if dat[i]["reactionEnergy"] - energy_check > 0.001:
                    if dat[i]["reactionEnergy"] - energy_check_slab_1 < 0.001:
                        data_total[tag]["raw"] = input_slab_1_check
                        data_total[tag]["cathub_energy"] = dat[i]["reactionEnergy"]
                    else:
                        print(f"Error at {tag}: Reaction energy check failed")
                        if tag in data_total:
                            del data_total[tag]
                        if tag in tags:
                            tags.remove(tag)
                        continue

            except Exception as e:
                traceback.print_exc()
                print(f"Unexpected error {tag}: {e}")

        print(f"{len(data_total)}/{len(dat)} data construction complete!")
        with open(path_output, "wb") as file:
            pickle.dump(data_total, file)


def find_adsorbate(data):
    for key in data:
        if key.endswith("star_abs") and key != "star_abs":
            return key[: -len("star_abs")]


def min_max(DFT_values):
    min_value = float(np.min(DFT_values))
    max_value = float(np.max(DFT_values))

    range_value = max_value - min_value

    min = min_value - 0.1 * range_value
    max = max_value + 0.1 * range_value

    return min, max


def plotter_mono(ads_data, GNN_name, tag, min_value, max_value, **kwargs):
    plot_save_path = os.path.join(os.getcwd(), "plot", GNN_name)
    os.makedirs(plot_save_path, exist_ok=True)
    figsize = kwargs.get("figsize", (9, 8))
    mark_size = kwargs.get("mark_size", 100)
    linewidths = kwargs.get("linewidths", 1.5)
    specific_color = kwargs.get("specific_color", "black")
    dpi = kwargs.get("dpi", 300)
    error_bar_display = kwargs.get("error_bar_display", False)

    fig, ax = plt.subplots(figsize=figsize)
    
    # single calculation vs normal calculation 구분
    if "normal" in ads_data["all"]:
        if tag == "all":
            plot_types = ["normal", "outlier"]
        elif tag == "normal":
            plot_types = ["normal"]
        else:  # tag == "outlier"
            plot_types = ["outlier"]
            
        DFT_values = np.concatenate([ads_data["all"][type]["DFT"] for type in plot_types])
        GNN_values = np.concatenate([ads_data["all"][type]["GNN"] for type in plot_types])
        
        scatter = ax.scatter(
            DFT_values,
            GNN_values,
            color=specific_color,
            marker="o",
            s=mark_size,
            edgecolors="black",
            linewidths=linewidths,
        )
        
        if error_bar_display:
            GNN_mins = np.concatenate([ads_data["all"][type]["GNN_min"] for type in plot_types])
            GNN_maxs = np.concatenate([ads_data["all"][type]["GNN_max"] for type in plot_types])
            yerr_minus = GNN_values - GNN_mins
            yerr_plus = GNN_maxs - GNN_values
            ax.errorbar(
                DFT_values,
                GNN_values,
                yerr=[yerr_minus, yerr_plus],
                fmt='none',
                ecolor="black",
                capsize=3,
                capthick=1,
                elinewidth=1,
            )
    else:
        # Single calculation 데이터 플롯
        DFT_values = ads_data["all"]["all"]["DFT"]
        GNN_values = ads_data["all"]["all"]["GNN"]
        scatter = ax.scatter(
            DFT_values,
            GNN_values,
            color=specific_color,
            marker="o",
            s=mark_size,
            edgecolors="black",
            linewidths=linewidths,
        )

    ax.set_xlim(min_value, max_value)
    ax.set_ylim(min_value, max_value)
    ax.plot([min_value, max_value], [min_value, max_value], "r-")

    MAE = np.sum(np.abs(DFT_values - GNN_values)) / len(DFT_values) if len(DFT_values) != 0 else 0

    ax.text(
        x=0.05,
        y=0.95,
        s=f"MAE-{GNN_name}: {MAE:.2f}",
        transform=plt.gca().transAxes,
        fontsize=30,
        verticalalignment="top",
        bbox=dict(
            boxstyle="round", alpha=0.5, facecolor="white", edgecolor="black", pad=0.5
        ),
    )

    ax.set_xlabel("DFT (eV)", fontsize=40)
    ax.set_ylabel(f"{GNN_name} (eV)", fontsize=40)
    ax.tick_params(axis="both", which="major", labelsize=20)
    ax.grid(True)

    for spine in ax.spines.values():
        spine.set_linewidth(3)

    plt.tight_layout()
    plt.savefig(f"{plot_save_path}/{tag}_mono.png", dpi=dpi)
    plt.close()

    return MAE


def plotter_multi(ads_data, GNN_name, types, tag, min_value, max_value, **kwargs):
    colors = [
        "blue",
        "red",
        "green",
        "purple",
        "orange",
        "brown",
        "pink",
        "gray",
        "olive",
        "cyan",
        "magenta",
        "lime",
        "indigo",
        "gold",
        "darkred",
        "teal",
        "coral",
        "turquoise",
        "salmon",
        "navy",
        "maroon",
        "forestgreen",
        "darkorange",
        "aqua",
        "lavender",
        "khaki",
        "crimson",
        "chocolate",
        "sienna",
        "cornflowerblue",
        "lightgreen",
        "plum",
        "lightgoldenrodyellow",
        "peachpuff",
        "ivory",
        "chartreuse",
        "slategray",
        "firebrick",
        "wheat",
        "dodgerblue",
        "orchid",
        "steelblue",
    ]
    markers = [
        "o",
        "^",
        "s",
        "p",
        "*",
        "h",
        "D",
        "H",
        "d",
        "<",
        ">",
        "v",
        "8",
        "P",
        "X",
        "o",
        "^",
        "s",
        "p",
        "*",
        "h",
        "D",
        "H",
        "d",
        "<",
        ">",
        "v",
        "8",
        "P",
        "X",
        "o",
        "^",
        "s",
        "p",
        "*",
        "h",
        "D",
        "H",
        "d",
        "<",
        ">",
        "v",
        "8",
    ]
    plot_save_path = os.path.join(os.getcwd(), "plot", GNN_name)
    os.makedirs(plot_save_path, exist_ok=True)
    figsize = kwargs.get("figsize", (9, 8))
    mark_size = kwargs.get("mark_size", 100)
    linewidths = kwargs.get("linewidths", 1.5)
    dpi = kwargs.get("dpi", 300)
    legend_off = kwargs.get("legend_off", False)
    error_bar_display = kwargs.get("error_bar_display", False)

    analysis_adsorbates = [
        adsorbate for adsorbate in ads_data.keys() if adsorbate != "all"
    ]

    len_adsorbates = len(analysis_adsorbates)
    legend_width = len(max(analysis_adsorbates, key=len))

    fig, ax = plt.subplots(figsize=figsize)
    error_sum = 0
    len_total = 0
    MAEs = {}

    scatter_handles = []

    # Check if this is a single calculation by looking at data structure
    is_single_calc = "GNN_min" not in ads_data["all"].get(types[0], {})

    for i, adsorbate in enumerate(analysis_adsorbates):
        if "normal" in ads_data["all"]:
            DFT_values = []
            GNN_values = []
            for type in types:
                DFT_values.append(ads_data[adsorbate][type]["DFT"])
                GNN_values.append(ads_data[adsorbate][type]["GNN"])
        else:
            DFT_values = [ads_data[adsorbate]["all"]["DFT"]]
            GNN_values = [ads_data[adsorbate]["all"]["GNN"]]
                
        DFT_values = np.concatenate(DFT_values)
        GNN_values = np.concatenate(GNN_values)

        scatter = ax.scatter(
            DFT_values,
            GNN_values,
            color=colors[i],
            label=f"* {adsorbate}",
            marker=markers[i],
            s=mark_size,
            edgecolors="black",
            linewidths=linewidths,
        )
        
        if error_bar_display and not is_single_calc:
            GNN_mins = []
            GNN_maxs = []
            
            for type in types:
                GNN_mins.append(ads_data[adsorbate][type]["GNN_min"])
                GNN_maxs.append(ads_data[adsorbate][type]["GNN_max"])
                
            GNN_mins = np.concatenate(GNN_mins)
            GNN_maxs = np.concatenate(GNN_maxs)
            
            yerr_minus = GNN_values - GNN_mins
            yerr_plus = GNN_maxs - GNN_values
            ax.errorbar(
                DFT_values,
                GNN_values,
                yerr=[yerr_minus, yerr_plus],
                fmt='none',
                ecolor="black",
                capsize=3,
                capthick=1,
                elinewidth=1,
            )
        
        scatter_handles.append(scatter)

        MAEs[adsorbate] = (
            np.sum(np.abs(DFT_values - GNN_values)) / len(DFT_values)
            if len(DFT_values) != 0
            else 0
        )
        error_sum += np.sum(np.abs(DFT_values - GNN_values))
        len_total += len(DFT_values)

        MAEs[f"len_{adsorbate}"] = len(DFT_values)

    ax.set_xlim(min_value, max_value)
    ax.set_ylim(min_value, max_value)
    ax.plot([min_value, max_value], [min_value, max_value], "r-")

    MAE_total = error_sum / len_total if len_total != 0 else 0
    MAEs["total"] = MAE_total

    ax.text(
        x=0.05,
        y=0.95,
        s=f"MAE-{GNN_name}: {MAE_total:.2f}",
        transform=plt.gca().transAxes,
        fontsize=30,
        verticalalignment="top",
        bbox=dict(
            boxstyle="round", alpha=0.5, facecolor="white", edgecolor="black", pad=0.5
        ),
    )

    ax.set_xlabel("DFT (eV)", fontsize=40)
    ax.set_ylabel(f"{GNN_name} (eV)", fontsize=40)
    ax.tick_params(axis="both", which="major", labelsize=20)

    if (
        legend_width < 8
        and len_adsorbates < 6
        or legend_width < 5
        and len_adsorbates < 8
    ) and not legend_off:
        ax.legend(loc="lower right", fontsize=20, ncol=(len_adsorbates // 7) + 1)
    else:
        fig_legend = plt.figure()
        fig_legend.legend(
            handles=scatter_handles,
            loc="center",
            frameon=False,
            ncol=(len_adsorbates // 7) + 1,
        )
        fig_legend.savefig(f"{plot_save_path}/legend.png", dpi=dpi, bbox_inches="tight")
        plt.close(fig_legend)

    ax.grid(True)

    for spine in ax.spines.values():
        spine.set_linewidth(3)

    plt.tight_layout()
    plt.savefig(f"{plot_save_path}/{tag}_multi.png", dpi=dpi)
    plt.close()

    return MAEs


def data_to_excel(main_data, outlier_data, GNNs_data, analysis_adsorbates, **kwargs):
    benchmarking_name = kwargs.get("Benchmarking_name", os.path.basename(os.getcwd()))

    df_main = pd.DataFrame(main_data)

    output_file = f"{benchmarking_name}_Benchmarking_Analysis.xlsx"

    with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
        df_main.to_excel(writer, sheet_name="GNN_Data", index=False)

        df_outlier = pd.DataFrame(outlier_data)
        df_outlier.to_excel(writer, sheet_name="outlier", index=False)

        for GNN_name, data_dict in GNNs_data.items():
            data_tmp = []
            for adsorbate in analysis_adsorbates:
                if f"len_{adsorbate}" in data_dict["normal"]:
                    normal_rate = (
                        data_dict["normal"][f"len_{adsorbate}"]
                        / data_dict["all"][f"len_{adsorbate}"]
                        * 100
                    )
                    data_tmp.append(
                        {
                            "Adsorbate_name": adsorbate,
                            "Normal rate (%)": normal_rate,
                            "MAE_total (eV)": data_dict["all"][adsorbate],
                            "MAE_normal (eV)": data_dict["normal"][adsorbate],
                            "MAE_outlier (eV)": data_dict["outlier"][adsorbate],
                            "Num_total": data_dict["all"][f"len_{adsorbate}"],
                            "Num_normal": data_dict["normal"][f"len_{adsorbate}"],
                            "Num_outlier": data_dict["outlier"][f"len_{adsorbate}"],
                        }
                    )

            data_df = pd.DataFrame(data_tmp)
            data_df.to_excel(writer, sheet_name=GNN_name, index=False)

        # 워크북 및 포맷 정의
        workbook = writer.book
        header_format = workbook.add_format({
            "align": "center", 
            "valign": "vcenter",
            "bold": True
        })
        center_align = workbook.add_format({"align": "center", "valign": "vcenter"})
        number_format_0f = workbook.add_format(
            {"num_format": "#,##0", "align": "center", "valign": "vcenter"}
        )
        number_format_1f = workbook.add_format(
            {"num_format": "0.0", "align": "center", "valign": "vcenter"}
        )
        number_format_2f = workbook.add_format(
            {"num_format": "0.00", "align": "center", "valign": "vcenter"}
        )
        number_format_3f = workbook.add_format(
            {"num_format": "0.000", "align": "center", "valign": "vcenter"}
        )

        # 열 별 형식 및 너비 지정
        column_formats = {
            "Normal rate (%)": (
                15,
                workbook.add_format(
                    {
                        "num_format": "0.00",
                        "align": "center",
                        "bold": True,
                        "valign": "vcenter",
                    }
                ),
            ),
            "MAE_total (eV)": (15, number_format_3f),
            "MAE_normal (eV)": (
                15,
                workbook.add_format(
                    {
                        "num_format": "0.000",
                        "align": "center",
                        "bold": True,
                        "valign": "vcenter",
                    }
                ),
            ),
            "MAE_outlier (eV)": (15, number_format_3f),
            "Num_total": (12, number_format_0f),
            "Num_normal": (12, number_format_0f),
            "Num_outlier": (12, number_format_0f),
            "slab_conv": (12, number_format_0f),
            "ads_conv": (12, number_format_0f),
            "slab_move": (12, number_format_0f),
            "ads_move": (12, number_format_0f),
            "slab_seed": (12, number_format_0f),
            "ads_seed": (12, number_format_0f),
            "ads_eng_seed": (12, number_format_0f),
            "Time_total (s)": (15, number_format_0f),
            "Time_per_step (s)": (17, number_format_3f),
        }

        # 모든 시트에 대해 포맷 적용
        for sheet_name in writer.sheets:
            worksheet = writer.sheets[sheet_name]
            df = (
                df_main
                if sheet_name == "GNN_Data"
                else (
                    df_outlier
                    if sheet_name == "outlier"
                    else pd.DataFrame(
                        [dict(zip(data_tmp[0].keys(), range(len(data_tmp[0]))))]
                    )
                )
            )

            # 헤더 포맷 적용
            for col_num, col_name in enumerate(df.columns):
                worksheet.write(0, col_num, col_name, header_format)

            for col_num, col_name in enumerate(df.columns):
                if col_name in column_formats:
                    width, fmt = column_formats[col_name]
                else:
                    width = (
                        max(df[col_name].astype(str).map(len).max(), len(col_name)) + 10
                    )
                    fmt = center_align

                worksheet.set_column(col_num, col_num, width, fmt)

                # 문자열 열인 경우
                if df[col_name].dtype == "object":
                    worksheet.set_column(col_num, col_num, width, center_align)
                else:
                    worksheet.set_column(col_num, col_num, width, fmt)

            row_height = 20
            for row in range(len(df) + 1):
                worksheet.set_row(row, row_height)

    print(f"Excel file '{output_file}' created successfully.")


def count_lbfgs_steps(log_path):
    with open(log_path, "r") as file:
        lines = file.readlines()

    # Iterate through the lines in reverse to find the last "Done!" instance
    for i, line in enumerate(reversed(lines)):
        if "Done!" in line:
            # Get the line right above "Done!"
            previous_line = lines[
                -(i + 2)
            ]  # i+2 because i starts at 0 and we're looking for the line above
            if len(previous_line.split()) == 5:
                # Extract the step number from the LBFGS line and add 1
                step_number = int(previous_line.split()[1])
                return step_number + 1
            else:
                print("calculation fail")

    # Return 0 if "Done!" or "LBFGS:" is not found
    print("notfound")
    return 0


def get_txt_files_in_directory(directory_path):
    txt_files = []

    # Walk through the directory
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".txt"):
                # Get full path of the txt file
                full_path = os.path.join(root, file)
                txt_files.append(full_path)

    return txt_files

def get_ads_eng_range(data_dict):
    ads_eng_values = []
    for key in data_dict:
        if isinstance(key, (int, str)) and key.isdigit():
            ads_eng_values.append(data_dict[key]["ads_eng"])
            
    return min(ads_eng_values), max(ads_eng_values)

def analysis_GNNs(**kwargs):
    main_data = []
    outlier_data = []
    GNN_datas = {}
    adsorbates = set()
    calculating_path = kwargs.get(
        "calculating_path", os.path.join(os.getcwd(), "result")
    )

    GNN_list = kwargs.get(
        "GNN_list",
        sorted(
            [
                name
                for name in os.listdir(calculating_path)
                if os.path.isdir(os.path.join(calculating_path, name))
            ],
            key=str.lower,
        ),
    )
    for GNN_name in GNN_list:
        print(GNN_name)
        with open(f"{calculating_path}/{GNN_name}/{GNN_name}_result.json", "r") as f:
            GNN_result = json.load(f)

        with open(f"{calculating_path}/{GNN_name}/{GNN_name}_outlier.json", "r") as f:
            GNN_outlier = json.load(f)

        ads_data = {
            "all": {
                "normal": {"DFT": np.array([]), "GNN": np.array([]), "GNN_min": np.array([]), "GNN_max": np.array([])},
                "outlier": {"DFT": np.array([]), "GNN": np.array([]), "GNN_min": np.array([]), "GNN_max": np.array([])},
            }
        }

        for reaction in GNN_result:
            adsorbate = find_adsorbate(GNN_result[reaction]["cathub"])
            adsorbates.add(adsorbate)

        time_accum = 0
        step_accum = 0

        slab_conv = 0
        ads_conv = 0
        slab_move = 0
        ads_move = 0
        slab_seed = 0
        ads_seed = 0
        ads_eng_seed = 0

        analysis_adsorbates = kwargs.get("target_adsorbates", adsorbates)

        for reaction in GNN_result:
            adsorbate = find_adsorbate(GNN_result[reaction]["cathub"])
            if adsorbate in analysis_adsorbates:
                if adsorbate not in ads_data:
                    ads_data[adsorbate] = {
                        "normal": {"DFT": np.array([]), "GNN": np.array([]), "GNN_min": np.array([]), "GNN_max": np.array([])},
                        "outlier": {"DFT": np.array([]), "GNN": np.array([]), "GNN_min": np.array([]), "GNN_max": np.array([])},
                    }

                num_outliers = sum(GNN_result[reaction]["outliers"].values())
                
                GNN_min, GNN_max = get_ads_eng_range(GNN_result[reaction])

                if num_outliers == 0:
                    ads_data[adsorbate]["normal"]["DFT"] = np.append(
                        ads_data[adsorbate]["normal"]["DFT"],
                        GNN_result[reaction]["cathub"]["ads_eng"],
                    )
                    ads_data[adsorbate]["normal"]["GNN"] = np.append(
                        ads_data[adsorbate]["normal"]["GNN"],
                        GNN_result[reaction]["final"]["ads_eng_median"],
                    )
                    ads_data[adsorbate]["normal"]["GNN_min"] = np.append(
                        ads_data[adsorbate]["normal"]["GNN_min"],
                        GNN_min,
                    )
                    ads_data[adsorbate]["normal"]["GNN_max"] = np.append(
                        ads_data[adsorbate]["normal"]["GNN_max"],
                        GNN_max,
                    )
                    ads_data["all"]["normal"]["DFT"] = np.append(
                        ads_data["all"]["normal"]["DFT"],
                        GNN_result[reaction]["cathub"]["ads_eng"],
                    )
                    ads_data["all"]["normal"]["GNN"] = np.append(
                        ads_data["all"]["normal"]["GNN"],
                        GNN_result[reaction]["final"]["ads_eng_median"],
                    )
                    ads_data["all"]["normal"]["GNN_min"] = np.append(
                        ads_data["all"]["normal"]["GNN_min"],
                        GNN_min,
                    )
                    ads_data["all"]["normal"]["GNN_max"] = np.append(
                        ads_data["all"]["normal"]["GNN_max"],
                        GNN_max,
                    )
                else:
                    ads_data[adsorbate]["outlier"]["DFT"] = np.append(
                        ads_data[adsorbate]["outlier"]["DFT"],
                        GNN_result[reaction]["cathub"]["ads_eng"],
                    )
                    ads_data[adsorbate]["outlier"]["GNN"] = np.append(
                        ads_data[adsorbate]["outlier"]["GNN"],
                        GNN_result[reaction]["final"]["ads_eng_median"],
                    )
                    ads_data[adsorbate]["outlier"]["GNN_min"] = np.append(
                        ads_data[adsorbate]["outlier"]["GNN_min"],
                        GNN_min,
                    )
                    ads_data[adsorbate]["outlier"]["GNN_max"] = np.append(
                        ads_data[adsorbate]["outlier"]["GNN_max"],
                        GNN_max,
                    )
                    ads_data["all"]["outlier"]["DFT"] = np.append(
                        ads_data["all"]["outlier"]["DFT"],
                        GNN_result[reaction]["cathub"]["ads_eng"],
                    )
                    ads_data["all"]["outlier"]["GNN"] = np.append(
                        ads_data["all"]["outlier"]["GNN"],
                        GNN_result[reaction]["final"]["ads_eng_median"],
                    )
                    ads_data["all"]["outlier"]["GNN_min"] = np.append(
                        ads_data["all"]["outlier"]["GNN_min"],
                        GNN_min,
                    )
                    ads_data["all"]["outlier"]["GNN_max"] = np.append(
                        ads_data["all"]["outlier"]["GNN_max"],
                        GNN_max,
                    )

                time_accum += sum(
                    value
                    for key, value in GNN_result[reaction]["final"].items()
                    if "time_total" in key
                )

                log_dir_path = f"{calculating_path}/{GNN_name}/log/{reaction}"
                txt_files = get_txt_files_in_directory(log_dir_path)

                for txt_file in txt_files:
                    step_tmp = count_lbfgs_steps(txt_file)
                    step_accum += step_tmp

                if GNN_result[reaction]["outliers"]["slab_conv"]:
                    slab_conv += 1

                if GNN_result[reaction]["outliers"]["ads_conv"]:
                    ads_conv += 1

                if GNN_result[reaction]["outliers"]["slab_move"]:
                    slab_move += 1

                if GNN_result[reaction]["outliers"]["ads_move"]:
                    ads_move += 1

                if GNN_result[reaction]["outliers"]["slab_seed"]:
                    slab_seed += 1

                if GNN_result[reaction]["outliers"]["ads_seed"]:
                    ads_seed += 1

                if GNN_result[reaction]["outliers"]["ads_eng_seed"]:
                    ads_eng_seed += 1

        DFT_data = np.concatenate(
            (ads_data["all"]["normal"]["DFT"], ads_data["all"]["outlier"]["DFT"])
        )
        min_value_DFT, max_value_DFT = min_max(DFT_data)

        min_value = kwargs.get("min", min_value_DFT)
        max_value = kwargs.get("max", max_value_DFT)

        MAE_all = plotter_mono(
            ads_data,
            GNN_name,
            "all",
            min_value,
            max_value,
            **kwargs,
        )
        MAE_normal = plotter_mono(
            ads_data,
            GNN_name,
            "normal",
            min_value,
            max_value,
            **kwargs,
        )
        MAE_outlier = plotter_mono(
            ads_data,
            GNN_name,
            "outlier",
            min_value,
            max_value,
            **kwargs,
        )

        MAEs_all_multi = plotter_multi(
            ads_data,
            GNN_name,
            ["normal", "outlier"],
            "all",
            min_value,
            max_value,
            **kwargs,
        )
        MAEs_normal_multi = plotter_multi(
            ads_data, GNN_name, ["normal"], "normal", min_value, max_value, **kwargs
        )
        MAEs_outlier_multi = plotter_multi(
            ads_data, GNN_name, ["outlier"], "outlier", min_value, max_value, **kwargs
        )

        GNN_datas[GNN_name] = {
            "all": MAEs_all_multi,
            "normal": MAEs_normal_multi,
            "outlier": MAEs_outlier_multi,
        }

        total_num = len(ads_data["all"]["normal"]["DFT"]) + len(
            ads_data["all"]["outlier"]["DFT"]
        )
        normal_rate = len(ads_data["all"]["normal"]["DFT"]) / total_num * 100

        main_data.append(
            {
                "GNN_name": GNN_name,
                "Normal rate (%)": normal_rate,
                "MAE_total (eV)": MAE_all,
                "MAE_normal (eV)": MAE_normal,
                "MAE_outlier (eV)": MAE_outlier,
                "Num_total": total_num,
                "Num_normal": len(ads_data["all"]["normal"]["DFT"]),
                "Num_outlier": len(ads_data["all"]["outlier"]["DFT"]),
                "Time_total (s)": GNN_outlier["Time"],
                "Time_per_step (s)": time_accum / step_accum,
            }
        )

        outlier_data.append(
            {
                "GNN_name": GNN_name,
                "Num_outlier": len(ads_data["all"]["outlier"]["DFT"]),
                "slab_conv": slab_conv,
                "ads_conv": ads_conv,
                "slab_move": slab_move,
                "ads_move": ads_move,
                "slab_seed": slab_seed,
                "ads_seed": ads_seed,
                "ads_eng_seed": ads_eng_seed,
            }
        )

    data_to_excel(
        main_data, outlier_data, GNN_datas, list(analysis_adsorbates), **kwargs
    )


def analysis_GNNs_single(**kwargs):
    main_data = []
    GNN_datas = {}
    adsorbates = set()
    single_path = kwargs.get("single_path", os.path.join(os.getcwd(), "result_single"))
    if os.path.exists(single_path):
        GNN_single_list = kwargs.get(
            "GNN_list",
            sorted(
                [
                    name
                    for name in os.listdir(single_path)
                    if os.path.isdir(os.path.join(single_path, name))
                ],
                key=str.lower,
            ),
        )

        for GNN_name in GNN_single_list:
            print(GNN_name)
            with open(f"{single_path}/{GNN_name}/{GNN_name}_result.json", "r") as f:
                GNN_result = json.load(f)

            # 데이터 구조 수정
            ads_data = {
                "all": {
                    "all": {"DFT": np.array([]), "GNN": np.array([])}  # 'all' 키를 한 단계 더 추가
                }
            }

            for reaction in GNN_result:
                adsorbate = find_adsorbate(GNN_result[reaction]["cathub"])
                adsorbates.add(adsorbate)

            analysis_adsorbates = kwargs.get("target_adsorbates", adsorbates)

            for reaction in GNN_result:
                adsorbate = find_adsorbate(GNN_result[reaction]["cathub"])
                if adsorbate in analysis_adsorbates:
                    if adsorbate not in ads_data:
                        ads_data[adsorbate] = {
                            "all": {"DFT": np.array([]), "GNN": np.array([])}
                        }

                    ads_data[adsorbate]["all"]["DFT"] = np.append(
                        ads_data[adsorbate]["all"]["DFT"],
                        GNN_result[reaction]["cathub"]["ads_eng"],
                    )
                    ads_data[adsorbate]["all"]["GNN"] = np.append(
                        ads_data[adsorbate]["all"]["GNN"],
                        GNN_result[reaction]["SC_calc"]["ads_eng"],
                    )
                    ads_data["all"]["all"]["DFT"] = np.append(
                        ads_data["all"]["all"]["DFT"],
                        GNN_result[reaction]["cathub"]["ads_eng"],
                    )
                    ads_data["all"]["all"]["GNN"] = np.append(
                        ads_data["all"]["all"]["GNN"],
                        GNN_result[reaction]["SC_calc"]["ads_eng"],
                    )

            DFT_data = ads_data["all"]["all"]["DFT"]
            GNN_data = ads_data["all"]["all"]["GNN"]

            min_value_DFT, max_value_DFT = min_max(DFT_data)

            min_value = kwargs.get("min", min_value_DFT)
            max_value = kwargs.get("max", max_value_DFT)

            MAE_all = plotter_mono(
                ads_data, GNN_name, "single", min_value, max_value, **kwargs
            )

            MAEs_all_multi = plotter_multi(
                ads_data,
                GNN_name,
                ["all"],  # 여기서 'all'을 리스트로 전달
                "single",
                min_value,
                max_value,
                **kwargs,
            )

            GNN_datas[GNN_name] = MAEs_all_multi
            total_num = len(DFT_data)

            main_data.append(
                {"GNN_name": GNN_name, "MAE (eV)": MAE_all, "Num_total": total_num}
            )

        data_to_excel_single(main_data, GNN_datas, list(analysis_adsorbates), **kwargs)


def execute_benchmark_single(calculator, **kwargs):
    required_keys = ["GNN_name", "benchmark"]

    for key in required_keys:
        if key not in kwargs:
            raise ValueError(f"Missing required keyword argument: {key}")

    GNN_name = kwargs["GNN_name"]
    benchmark = kwargs["benchmark"]
    gas_distance = kwargs.get("gas_distance", 10)

    path_pkl = os.path.join(os.getcwd(), f"raw_data/{benchmark}.pkl")

    with open(path_pkl, "rb") as file:
        cathub_data = pickle.load(file)

    save_directory = os.path.join(os.getcwd(), "result_single", GNN_name)
    print(f"Starting {GNN_name} Benchmarking")
    # Basic Settings==============================================================================
    os.makedirs(f"{save_directory}/structures", exist_ok=True)
    os.makedirs(f"{save_directory}/gases", exist_ok=True)

    final_result = {}

    # Calculation Part==============================================================================

    gas_energies = {}

    print("Starting calculations...")
    for index, key in enumerate(cathub_data):
        print(f"[{index+1}/{len(cathub_data)}] {key}")
        final_result[key] = {}
        final_result[key]["cathub"] = {}
        final_result[key]["cathub"]["ads_eng"] = cathub_data[key]["cathub_energy"]
        for structure in cathub_data[key]["raw"]:
            if "gas" not in str(structure):
                final_result[key]["cathub"][f"{structure}_abs"] = cathub_data[key][
                    "raw"
                ][structure]["energy_cathub"]

        structure_path = f"{save_directory}/structures/{key}"

        os.makedirs(structure_path, exist_ok=True)

        informs = {}
        informs["ads_eng"] = []

        ads_energy_calc = 0
        for structure in cathub_data[key]["raw"]:
            if "gas" not in str(structure):
                POSCAR_str = cathub_data[key]["raw"][structure]["atoms"]
                write(f"{structure_path}/CONTCAR_{structure}", POSCAR_str)
                energy_calculated = energy_cal_single(calculator, POSCAR_str)
                ads_energy_calc += (
                    energy_calculated * cathub_data[key]["raw"][structure]["stoi"]
                )
                if structure == "star":
                    slab_energy = energy_calculated
                else:
                    ads_energy = energy_calculated

            else:
                if structure in gas_energies:
                    ads_energy_calc += (
                        gas_energies[structure]
                        * cathub_data[key]["raw"][structure]["stoi"]
                    )
                else:
                    print(f"{structure} calculating")
                    gas_CONTCAR, gas_energy = energy_cal_gas(
                        calculator,
                        cathub_data[key]["raw"][structure]["atoms"],
                        0.05,
                        f"{save_directory}/gases/POSCAR_{structure}",
                        gas_distance,
                        f"{save_directory}/gases/{structure}.txt",
                        f"{save_directory}/gases/{structure}",
                    )
                    gas_energies[structure] = gas_energy
                    ads_energy_calc += (
                        gas_energy * cathub_data[key]["raw"][structure]["stoi"]
                    )
                    write(f"{save_directory}/gases/CONTCAR_{structure}", gas_CONTCAR)

        final_result[key]["SC_calc"] = {
            "ads_eng": ads_energy_calc,
            "slab_abs": slab_energy,
            "ads_abs": ads_energy,
        }

        with open(f"{save_directory}/{GNN_name}_result.json", "w") as file:
            json.dump(final_result, file, indent=4)

        with open(f"{save_directory}/{GNN_name}_gases.json", "w") as file:
            json.dump(gas_energies, file, indent=4)

    print(f"{GNN_name} Benchmarking Finish")


def data_to_excel_single(main_data, GNNs_data, analysis_adsorbates, **kwargs):
    benchmarking_name = kwargs.get("Benchmarking_name", os.path.basename(os.getcwd()))

    df_main = pd.DataFrame(main_data)

    output_file = f"{benchmarking_name}_Single_Benchmarking_Analysis.xlsx"

    with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
        df_main.to_excel(writer, sheet_name="GNN_Data", index=False)

        for GNN_name, data_dict in GNNs_data.items():
            data_tmp = []
            for adsorbate in analysis_adsorbates:
                if f"len_{adsorbate}" in data_dict:
                    data_tmp.append(
                        {
                            "Adsorbate_name": adsorbate,
                            "MAE_total (eV)": data_dict[adsorbate],
                            "Num_total": data_dict[f"len_{adsorbate}"],
                        }
                    )

            data_df = pd.DataFrame(data_tmp)
            data_df.to_excel(writer, sheet_name=GNN_name, index=False)

        # 워크북 및 포맷 정의
        workbook = writer.book
        header_format = workbook.add_format({
            "align": "center", 
            "valign": "vcenter",
            "bold": True
        })
        center_align = workbook.add_format({"align": "center", "valign": "vcenter"})
        number_format_0f = workbook.add_format(
            {"num_format": "#,##0", "align": "center", "valign": "vcenter"}
        )
        number_format_1f = workbook.add_format(
            {"num_format": "0.0", "align": "center", "valign": "vcenter"}
        )
        number_format_2f = workbook.add_format(
            {"num_format": "0.00", "align": "center", "valign": "vcenter"}
        )
        number_format_3f = workbook.add_format(
            {"num_format": "0.000", "align": "center", "valign": "vcenter"}
        )

        # 열 별 형식 및 너비 지정
        column_formats = {
            "MAE (eV)": (
                15,
                workbook.add_format(
                    {
                        "num_format": "0.000",
                        "align": "center",
                        "bold": True,
                        "valign": "vcenter",
                    }
                ),
            ),
            "MAE_total (eV)": (15, number_format_3f),
            "Num_total": (12, number_format_0f),
        }

        # 모든 시트에 대해 포맷 적용
        for sheet_name in writer.sheets:
            worksheet = writer.sheets[sheet_name]
            df = (
                df_main if sheet_name == "GNN_Data" 
                else pd.DataFrame(data_tmp)
            )

            # 헤더 포맷 적용
            for col_num, col_name in enumerate(df.columns):
                worksheet.write(0, col_num, col_name, header_format)

            for col_num, col_name in enumerate(df.columns):
                if col_name in column_formats:
                    width, fmt = column_formats[col_name]
                else:
                    width = (
                        max(df[col_name].astype(str).map(len).max(), len(col_name)) + 10
                    )
                    fmt = center_align

                worksheet.set_column(col_num, col_num, width, fmt)

                # 문자열 열인 경우
                if df[col_name].dtype == "object":
                    worksheet.set_column(col_num, col_num, width, center_align)
                else:
                    worksheet.set_column(col_num, col_num, width, fmt)

            # 행 높이 설정
            row_height = 20
            for row in range(len(df) + 1):
                worksheet.set_row(row, row_height)

    print(f"Excel file '{output_file}' created successfully.")
