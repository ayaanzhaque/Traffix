# Section types: road, bridge, tunnel
# Section categories: motorway (D/R), standard (I/II/UUU)
import numpy as np
import pandas as pd
import os


def load_sample_bypass():
    """Load a sample bypass from prepared csv's"""
    dirn = os.path.dirname(__file__) + "/examples/"
    
    d = {}
    d["RP"] = pd.read_csv(dirn + "bypass_road_params.csv", index_col=0)
    d["C_fin"] = pd.read_csv(dirn + "bypass_capex.csv", index_col=[0, 1])
    d["C_fin"].columns = d["C_fin"].columns.astype(int)

    d["I0"] = pd.read_csv(dirn + "bypass_intensities_0.csv")
    d["I1"] = pd.read_csv(dirn + "bypass_intensities_1.csv")
    d["I0"].set_index(["id_section", "vehicle"], inplace=True)
    d["I1"].set_index(["id_section", "vehicle"], inplace=True)
    d["I0"].columns = d["I0"].columns.astype(int)
    d["I1"].columns = d["I1"].columns.astype(int)
    d["I0"] = d["I0"].sort_index()
    d["I1"] = d["I1"].sort_index()

    d["V0"] = pd.read_csv(dirn + "bypass_velocities_0.csv")
    d["V1"] = pd.read_csv(dirn + "bypass_velocities_1.csv")
    d["V0"].set_index(["id_section", "vehicle"], inplace=True)
    d["V1"].set_index(["id_section", "vehicle"], inplace=True)
    d["V0"].columns = d["V0"].columns.astype(int)
    d["V1"].columns = d["V1"].columns.astype(int)
    d["V0"] = d["V0"].sort_index()
    d["V1"] = d["V1"].sort_index()
    
    return d


def create_sample_bypass(yr, N_yr_bld=3, L_in=4.0, L_byp=6.0):
    """
    Generate a road through a city with a bypass.
    Label is for accident categories.

    Output
    ------
    * road sections
    * CAPEX
    """
    road_itms = ["length","name","type","lanes","label","width"]
    capex_itms = ["land","pavements","bridges","tunnels","buildings",\
                  "slope_stabilisation","retaining_walls","noise_barriers",\
                  "safety_features"]

    # investment costs
    yrs = np.arange(yr, yr + N_yr_bld)
    C_fin = pd.DataFrame(index=capex_itms, columns=["total"] + list(yrs))
    C_fin["total"] = [0.9, 42, 4.5, 0, 0, 0, 0, 0.9, 0]
    C_fin["total"] = C_fin.total * 1e6
    for yr in yrs:
        C_fin[yr] = C_fin.total / N_yr_bld

    # road parameters
    N_sec = 4
    R = pd.DataFrame(
        {"variant": [0, 0, 0, 1],
         "name": ["entrance", "city", "exit", "bypass"],
         "length": [0.5, L_in, 0.5, L_byp],
         "type": ["road", "road", "road", "road"],
         "lanes": [2, 2, 2, 2],
         "label": [np.nan] * 4,
         "width": [9.5, 9.5, 9.5, 11.5]
         },
         index=np.arange(N_sec))
    R.index.name = "id_section"

    return R, C_fin


def load_sample_mountain_pass():
    pass


def load_visnove():
    """Load inputs for the major motorway project 
    D1 Hricovske Podhradie - Lietavska Lucka - Dubna Skala as an Excel file.
    Contains the following sheets:
    * Road parameters for the relevant road sections in the region
    * CAPEX for three sections:
     - Hricovske Podhradie - Lietavska Lucka
     - Lietavska Lucka - Dubna Skala
     - Feeder Lietavska Lucka
    * Intensities in variants 0 and 1
    * Velocities in variants 0 and 1
    """
    dirn = os.path.dirname(__file__) + "/examples/"
    return pd.ExcelFile(dirn + "cba_inputs_d1_hp_ll_ds.xlsx")


def load_soroska():
    pass


def load_kezmarok():
    pass


def load_hyperloop():
    """Inspiration:
    https://www.facebook.com/konstantin.cikovsky/posts/10221316645854995
    """
    pass



