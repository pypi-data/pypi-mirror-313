#!/usr/bin/env python3
"""List failing cores from JSon files."""
import sys
import argparse
from pathlib import Path
import json



def main(options):
    """main entry."""
    petal_cores = {}
    for fnam in options.files:
        ifile = Path(fnam).expanduser().resolve()
        with open(ifile, "r", encoding="utf-8") as fin:
            data = json.load(fin)

        if not data["passed"]:
            petalId = data["component"]
            if petalId not in petal_cores:
                petal_cores[petalId] = {"FRONT": [], "BACK": []}

            side = "FRONT" if "FRONT" in data["testType"] else "BACK"
            for D in data["defects"]:
                petal_cores[petalId][side].append("{}: {}".format(D["name"], D["description"]))


    keys = sorted(petal_cores.keys())
    for petalId in keys:
        print(petalId)
        for side in ["FRONT","BACK"]:
            if len(petal_cores[petalId][side])>0:
                print("+-", side)
            for D in petal_cores[petalId][side]:
                print("  ", D)

        print("\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*', help="Input files")
    opts = parser.parse_args()
    
    from petal_qc.utils.all_files import all_files
    
    opts.files = []
    for fnam in all_files(Path("~/tmp/petal-metrology/Production/Results").expanduser(), "*.json"):
        opts.files.append(fnam)
    
    main(opts)