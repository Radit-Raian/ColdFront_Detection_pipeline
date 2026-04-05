import subprocess
import json
import os

CONFIG_FILE = "config.txt"

def open_editor(file_path):
    subprocess.run(["nano", file_path])

def load_config(file_path):
    config = {}

    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()

            if not line or "=" not in line:
                continue

            key, value = line.split("=", 1)
            config[key.strip()] = value.strip()

    return config

def list_obsids(obsids_str):
    return [obs.strip() for obs in obsids_str.split(",")]

def save_config_json(config, output_file="config.json"):
    with open(output_file, "w") as f:
        json.dump(config, f, indent=4)

if __name__ == "__main__":
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            f.write("cluster_name = \n")
            f.write("obsIDs = \n")

    print("[INFO] Opening config file in nano...")
    open_editor(CONFIG_FILE)

    config_raw = load_config(CONFIG_FILE)

    cluster_name = config_raw.get("cluster_name")
    obsids = list_obsids(config_raw.get("obsIDs", ""))

    if not cluster_name or not obsids:
        raise ValueError("cluster_name or obsIDs missing in config.txt")

    final_config = {
        "cluster_name": cluster_name,
        "obsids": obsids
    }

    save_config_json(final_config)

    print("[INFO] Config saved successfully.")
