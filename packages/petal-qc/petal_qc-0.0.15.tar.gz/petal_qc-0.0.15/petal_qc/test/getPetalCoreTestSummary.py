#!/usr/bin/env python3
"""Get a summery of Petal core TEsts."""
import json
try:
    import itkdb_gtk
    
except ImportError:
    import sys
    from pathlib import Path
    cwd = Path(__file__).parent.parent
    sys.path.append(cwd.as_posix())

from itkdb_gtk import ITkDBlogin, ITkDButils
from itkdb_gtk.dbGtkUtils import replace_in_container, DictDialog, ask_for_confirmation


def main(session, options):
    """Main entry point."""

    # find all cores
    # Now all the objects
    payload = {
        "filterMap": {
            #"componentType": ["BT"],
            "componentType": ["CORE_PETAL"],
            "type": ["CORE_AVS"],
            # "currentLocation": ["IFIC"],
        },
        "sorterList": [
            {"key": "alternativeIdentifier", "descending": False }
        ],
    }
    suff = "ALL"
    if options.institute:
        payload["filterMap"]["currentLocation"] = options.institute
        suff = options.institute
        
    core_list = session.get("listComponents", json=payload)
    core_tests = ["PETAL_METROLOGY_FRONT", "PETAL_METROLOGY_BACK", "XRAYIMAGING", "THERMAL_EVALUATION", "BTTESTING"]
    
    do_check_stage = "AT_QC_SITE"
    #do_check_stage = None
    petal_id_db = {}
    
    for core in core_list:
        SN = core["serialNumber"]
        altid = core['alternativeIdentifier']
        if "PPC" not in altid:
            continue
        
        petal_id_db[altid] = SN
        location = core["currentLocation"]['code']
        coreStage = core["currentStage"]['code']
        if do_check_stage:
            if coreStage != do_check_stage:
                rc = ITkDButils.set_object_stage(session, SN, do_check_stage)
                if rc is None:
                    print("Could not change stage")
                    return False

        print("\n\nPetal {} [{}] - {}. {}".format(SN, altid, coreStage, location))

        test_list = session.get("listTestRunsByComponent", json={"filterMap":{"serialNumber": SN, "state": "ready", "testType":core_tests}})

        for tst in test_list:
            ttype = tst["testType"]["code"]
            if ttype not in core_tests:
                print(ttype)
                continue

            T = session.get("getTestRun", json={"testRun": tst["id"]})
            if T["state"] != "ready":
                print(T)
            
            print("-- {} [{}]".format(T["testType"]["name"], T["runNumber"]))
            if not T["passed"]:
                print("\t## test FAILED")
                
            for D in T["defects"]:
                print("\t{} - {}".format(D["name"], D["description"]))

    with open("petal_ID_db_{}.json".format(suff), "w", encoding="utf-8") as fOut:
        json.dump(petal_id_db, fOut, indent=3)

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--institute", default=None, help="The petal current location")
    options = parser.parse_args()
    
    # ITk_PB authentication
    dlg = ITkDBlogin.ITkDBlogin()
    session = dlg.get_client()

    try:
        main(session, options)

    except Exception as E:
        print(E)

    dlg.die()

