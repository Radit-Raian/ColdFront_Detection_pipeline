import os
from glob import glob
from ciao_contrib.runtool import dmcoords
import pandas as pd
from astropy.coordinates import SkyCoord
import astropy.units as u

base_dir = "data"

for obsid in os.listdir(base_dir):

    repro_path = os.path.join(base_dir, obsid, "repro")

    if not os.path.isdir(repro_path):
        continue

    print(f"\nProcessing ObsID: {obsid}")

    reg_files = glob(os.path.join(repro_path, "*noem.reg"))
    evt_files = glob(os.path.join(repro_path, "*evt2.fits"))

    if not reg_files or not evt_files:
        print("  Required files missing — skipping.")
        continue

    region_file = reg_files[0]
    event_file = evt_files[0]

    x_coords = []
    y_coords = []

    with open(region_file) as f:
        for line in f:
            line = line.strip()
            if line.startswith("ellipse") and not line.startswith("-"):
                content = line[line.find("(")+1 : line.find(")")]
                parts = content.split(",")
                x_coords.append(float(parts[0]))
                y_coords.append(float(parts[1]))

    if len(x_coords) < 3:
        print("  Less than 3 sources found — skipping.")
        continue

    ra_list = []
    dec_list = []

    for x, y in zip(x_coords, y_coords):
        dmcoords.infile = event_file
        dmcoords.x = x
        dmcoords.y = y
        dmcoords.opt = "sky"
        dmcoords()

        c = SkyCoord(dmcoords.ra, dmcoords.dec, unit=(u.hourangle, u.deg))
        ra_list.append(c.ra.deg)
        dec_list.append(c.dec.deg)

    output_file = os.path.join(repro_path, f"{obsid}_src.csv")

    df = pd.DataFrame({"RA": ra_list, "Dec": dec_list})
    df.to_csv(output_file, index=False)

    print(f"  Saved: {output_file}")

print("\nAll ObsIDs processed.")
