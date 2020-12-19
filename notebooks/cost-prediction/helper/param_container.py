import pandas as pd
from numpy import arange, ones_like, where
import os


available_countries = ["svk"]
svk_params = ["gdp_growth", "cpi", "c_op", "toll_op", "res_val", \
    "c_fuel", "conv_fac", \
    "occ_p", "occ_f", "r_tp", "vtts", "voc", "fuel_coeffs", \
    "r_acc", "c_acc", "r_ghg", "c_ghg", "r_em", "c_em", "noise"]



class ParamContainer(object):
    def __init__(self, country, price_level, verbose=False):
        """Read in all the CBA values necessary for economic analysis
        for a given country"""
        if country not in available_countries:
            raise ValueError("Data for country '%s' not available." % country)
        
        self.country = country
        self.dirn = os.path.dirname(__file__) + "/parameters/%s/" % self.country
        self.pl = price_level
        self.verbose = verbose
        
        self.df_raw = {}
        self.df_clean = {}


    def read_raw_params(self):
        """Load all parameter dataframes"""
        if self.verbose:
            print("Reading CBA parameters...")

        # macro data
        self.gdp_growth = pd.read_csv(self.dirn + "gdp_growth.csv", \
            index_col="year")
        self.cpi = pd.read_csv(self.dirn + "cpi.csv", index_col="year")

        # financial data
        self.df_raw["c_op"] = \
            pd.read_csv(self.dirn + "operation_cost.csv", index_col=0)
        self.df_raw["toll_op"] = \
            pd.read_csv(self.dirn + "toll_operation_cost.csv", index_col=0)
        self.df_raw["res_val"] = \
            pd.read_csv(self.dirn + "residual_value.csv", index_col=0)
        self.df_raw["c_fuel"] =\
            pd.read_csv(self.dirn + "fuel_cost.csv", index_col=0)

        # physical data
        self.fuel_rho = \
            pd.read_csv(self.dirn + "fuel_density.csv", index_col="fuel")

        # economic data
        self.df_raw["conv_fac"] =\
            pd.read_csv(self.dirn + "conversion_factors.csv", index_col=0)
        self.df_raw["occ_p"] =\
            pd.read_csv(self.dirn + "passenger_occupancy.csv", index_col=0)
        self.df_raw["occ_f"] =\
            pd.read_csv(self.dirn + "freight_occupancy.csv", index_col=0)
        self.df_raw["r_tp"] =\
            pd.read_csv(self.dirn + "trip_purpose.csv", index_col=0)
        self.df_raw["vtts"] =\
            pd.read_csv(self.dirn + "vtts.csv", index_col=0)
        self.df_raw["voc"] =\
            pd.read_csv(self.dirn + "voc.csv", index_col=0)
        self.df_raw["fuel_coeffs"] =\
            pd.read_csv(self.dirn + "fuel_consumption.csv", index_col=0)
        self.df_raw["r_fuel"] =\
            pd.read_csv(self.dirn + "fuel_ratio.csv", index_col=0)
        self.df_raw["r_acc"] =\
            pd.read_csv(self.dirn + "accident_rate.csv", index_col=0)
        self.df_raw["c_acc"] =\
            pd.read_csv(self.dirn + "accident_cost.csv", index_col=0)
        self.df_raw["r_ghg"] =\
            pd.read_csv(self.dirn + "greenhouse_rate.csv", index_col=0)
        self.df_raw["c_ghg"] =\
            pd.read_csv(self.dirn + "greenhouse_cost.csv", index_col=0)
        self.df_raw["r_em"] =\
            pd.read_csv(self.dirn + "emission_rate.csv", index_col=0)
        self.df_raw["c_em"] =\
            pd.read_csv(self.dirn + "emission_cost.csv", index_col=0)
        self.df_raw["noise"] =\
            pd.read_csv(self.dirn + "noise.csv", index_col=0)


    def adjust_cpi(self, infl=0.02, yr_min=2000, yr_max=2100):
        """Fill in mising values and compute cumulative inflation 
        to be able to adjust the price level"""
        if self.verbose:
            print("Adjusting CPI...")

        self.cpi = self.cpi.reindex(arange(yr_min, yr_max+1))
        self.cpi["cpi"].fillna(infl, inplace=True)

        # compute cumulative CPI
        self.cpi["cpi_index"] = ""
        self.cpi["cpi_index"] = \
            pd.to_numeric(self.cpi.cpi_index, errors="coerce")
        self.cpi.loc[self.pl, "cpi_index"] = 1.0
        ix = self.cpi.index.get_loc(self.pl)

        # backward
        for i in range(ix-1, -1, -1):
            self.cpi.iloc[i]["cpi_index"] = \
                self.cpi.iloc[i+1].cpi_index * (self.cpi.iloc[i].cpi + 1.0)
        
        # forward
        for i in range(ix+1, len(self.cpi)):
            self.cpi.iloc[i]["cpi_index"] = \
                self.cpi.iloc[i-1].cpi_index * (self.cpi.iloc[i-1].cpi + 1.0)


    def clean_params(self):
        """Incorporate scale into values.
        Remove unimportant columns. Populate the df_clean dictionary"""
        if self.verbose:
            print("Cleaning parameters...")
        for itm in self.df_raw.keys():
            if self.verbose:
                print("    Cleaning: %s" % itm)
            self.df_clean[itm] = self.df_raw[itm].copy()
            if "nb" in self.df_clean[itm].columns:
                self.df_clean[itm].drop(columns=["nb"], inplace=True)
            if "unit" in self.df_clean[itm].columns:
                self.df_clean[itm].drop(columns=["unit"], inplace=True)
        
        # adjusting scale if supplied
        for c in ["c_op", "vtts", "voc", "c_acc", "c_ghg", "c_em", "noise"]:
            if "scale" in self.df_clean[c].columns:
                if self.verbose:
                    print("Changing scale of %s" % c)
                self.df_clean[c]["value"] =\
                   self.df_clean[c].value * self.df_clean[c].scale
                self.df_clean[c].drop(columns=["scale"], inplace=True)


    def adjust_price_level(self):
        """Unify the prices for one price level"""
        if self.verbose:
            print("Adjusting price level...")
        for c in ["c_op", "toll_op", \
            "vtts", "voc", "c_fuel", "c_acc", "c_ghg", "c_em", "noise"]:
            if self.verbose:
                print("    Adjusting: %s" % c)
            self.df_clean[c]["value"] = self.df_clean[c].value \
                * self.df_clean[c].price_level\
                .map(lambda x: self.cpi.loc[x].cpi_index)
            self.df_clean[c].drop(columns=["price_level"], inplace=True)
            self.df_clean[c]["value"] = self.df_clean[c].value#.round(3)


    def wrangle_params(self):
        if self.verbose:
            print("Wrangling parameters...")
        self._wrangle_opex()
        self._wrangle_vtts()
        self._wrangle_fuel()
        self._wrangle_accidents()
        self._wrangle_greenhouse()
        self._wrangle_emissions()
        self._wrangle_noise()


    def _wrangle_opex(self):
        """Set up index"""
        c = "c_op"
        self.df_clean[c].reset_index(inplace=True)
        self.df_clean[c].set_index(\
            ["item", "operation_type", "category"], inplace=True)


    def _wrangle_vtts(self):
        """Average the value of the travel time saved"""
        if "distance" in self.df_clean["vtts"].columns:
            if self.verbose:
                print("Averaging VTTS over distance type.")
            gr = self.df_clean["vtts"]\
                .groupby(by=["vehicle", "substance", "purpose",\
                "gdp_growth_adjustment"])
            vtts = gr["value"].mean()
            vtts = vtts.reset_index()
        else:
            vtts = self.df_clean["vtts"].copy()

        # add trip purpose and merge
        r_tp = self.df_clean["r_tp"].reset_index().melt(id_vars="vehicle", \
            var_name="purpose", value_name="purpose_ratio")
        vtts = pd.merge(vtts, r_tp, how="left", on=["vehicle", "purpose"])

        # add passenger occupancy
        self.df_clean["occ_p"]["substance"] = "passengers"
        self.df_clean["occ_p"].reset_index(inplace=True)
        
        vtts = pd.merge(vtts, \
            self.df_clean["occ_p"][["vehicle", "value", "substance"]],
            how="left", on=["vehicle", "substance"], suffixes=("", "_occ"))

        # add freight occupancy
        self.df_clean["occ_f"]["substance"] = "freight"
        self.df_clean["occ_f"].reset_index(inplace=True)
        vtts = pd.merge(vtts, 
            self.df_clean["occ_f"][["vehicle", "value", "substance"]],
            how="left", on=["vehicle", "substance"], suffixes=("", "_freight"))

        vtts["value_occ"] = vtts.value_occ.fillna(vtts.value_freight)
        vtts.drop(columns=["value_freight"], inplace=True)

        vtts.rename(columns={"value": "value_subst"}, inplace=True)
        vtts["value"] = vtts.value_subst * vtts.value_occ
        vtts.drop(columns=["value_subst", "value_occ"], inplace=True)

        # contract by substance
        vtts = vtts.groupby(by=["vehicle", "purpose",\
            "gdp_growth_adjustment", "purpose_ratio"])\
            ["value"].sum().reset_index()

        # unify gdp growth adjustment by trip purpose ratio
        vtts["gdp_ga2"] = vtts.purpose_ratio * vtts.gdp_growth_adjustment
        vtts["value2"] = vtts.purpose_ratio * vtts.value

        vtts = vtts.groupby(["vehicle"])["gdp_ga2", "value2"].sum()
        vtts.columns = ["gdp_growth_adjustment", "value"]
        vtts["value"] = vtts.value.round(2)

        self.df_clean["vtts"] = vtts.copy()


    def _wrangle_fuel(self):
        """Convert units from eur/l to eur/kg"""
        # fuel ratios for vehicle types
        c = "r_fuel"
        self.df_clean[c].reset_index(inplace=True)
        self.df_clean[c].set_index(["vehicle", "fuel"], inplace=True)

        # convert to kg/km and add conversion factors
        c = "c_fuel"
        self.df_clean[c]["value"] = \
            self.df_clean[c].value / self.fuel_rho.value
        self.df_clean[c] *= self.df_clean["conv_fac"].loc["factor", "fuel"]

        c = "fuel_coeffs"
        self.df_clean[c] = pd.merge(self.df_clean[c].reset_index(), 
            self.fuel_rho.drop(columns=["unit"]), how="left", on="fuel")\
            .set_index(["vehicle","fuel"])
        
        # multiply polynomial coefficients by density
        for itm in ["a0", "a1", "a2", "a3"]:
            self.df_clean[c][itm] = \
                self.df_clean[c][itm] * self.df_clean[c].value
        self.df_clean[c].drop(columns=["value"], inplace=True)


    def _wrangle_accidents(self):
        """Unify the two datasets storing values for accidents"""
        self.df_clean["c_acc"]["value"] = self.df_clean["c_acc"].value *\
            self.df_clean["c_acc"].correct_unreported *\
            self.df_clean["c_acc"].correct_pass_per_acc
        self.df_clean["c_acc"].drop(columns=["correct_unreported",\
            "correct_pass_per_acc"], inplace=True)
        
        self.df_clean["r_acc"]["value"] = \
            self.df_clean["r_acc"]\
            [["fatal", "severe_injury", "light_injury", "damage"]]\
            .values @ self.df_clean["c_acc"].value.values

        self.df_clean["r_acc"]["gdp_growth_adjustment"] = \
            self.df_clean["c_acc"].gdp_growth_adjustment.values[0]
        
        # copy to the cost dataframe
        self.df_clean["c_acc"] = self.df_clean["r_acc"]\
            [["lanes", "layout", "environment", "value", \
                "gdp_growth_adjustment"]].copy()

        self.df_clean["c_acc"].reset_index(inplace=True)
        self.df_clean["c_acc"].set_index(\
            ["category", "lanes", "layout", "environment"], inplace=True)


    def _wrangle_greenhouse(self):
        b = "r_ghg"
        self.df_clean[b]["value"] = \
            self.df_clean[b].value * self.df_clean[b].factor

        gr = self.df_clean[b].groupby(["vehicle", "fuel"])["value"].sum()
        self.df_clean[b] = pd.DataFrame(gr).round(0)


    def _wrangle_emissions(self):
        b = "c_em"
        self.df_clean[b].reset_index(inplace=True)
        self.df_clean[b].set_index(["polluant", "environment"], \
            inplace=True)
        self.df_clean[b] = self.df_clean[b].sort_index()

        b = "r_em"
        self.df_clean[b].reset_index(inplace=True)
        self.df_clean[b].set_index(["polluant", "vehicle", "fuel"], \
            inplace=True)
        self.df_clean[b] = self.df_clean[b].sort_index()


    def _wrangle_noise(self):
        b = "noise"
        self.df_clean[b] = self.df_clean[b]\
            [self.df_clean[b].traffic_type == "thin"]
        self.df_clean[b].drop(columns=["traffic_type"], inplace=True)
        self.df_clean[b]["value2"] = self.df_clean[b].value\
            * self.df_clean[b].ratio
        gr = self.df_clean[b]\
            .groupby(["vehicle", "environment", "gdp_growth_adjustment"])

        self.df_clean[b] = gr["value2"].sum()
        self.df_clean[b] = self.df_clean[b].reset_index()
        self.df_clean[b].rename(columns={"value2": "value"}, inplace=True)
        self.df_clean[b].set_index(["vehicle", "environment"], inplace=True)




