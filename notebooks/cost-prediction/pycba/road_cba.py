import pandas as pd
import numpy as np
from numpy.matlib import repmat
import time
from .param_container import ParamContainer


VEHICLE_TYPES = ["car", "lgv", "hgv", "bus"]
ENVIRONMENTS = ["intravilan", "extravilan"]
DAYS_YEAR = 365.0


class RoadCBA(ParamContainer):
    def __init__(self,
                 init_year,
                 price_level,
                 country,
                 period=30,
                 fin_discount_factor=0.04,
                 eco_discount_factor=0.05,
                 currency="EUR",
                 verbose=False
                 ):
        """
        Input
        -----
        - init_year: initial year of construction and economic analysis
        - price_level: 
        - country: country code
        - period: number of years for the economic analysis
        - fin_discount_factor: discount factor for financial analysis
        - eco_discount_factor: discount factor for economic analysis

        """
        self.yr_i = init_year
        self.N_yr = period
        self.yr_f = self.yr_i + self.N_yr - 1
        self.pl = price_level
        if self.yr_i != self.pl:
            print("Warning: start year not same as price level.")
        self.N_yr_bld = None
        self.N_yr_op = None
        self.yr_op = None
        self.yrs = np.arange(self.yr_i, self.yr_i + self.N_yr)

        self.r_fin = fin_discount_factor
        self.r_eco = eco_discount_factor

        self.country = country
        self.currency = currency

        self.veh_types = VEHICLE_TYPES
        self.envs = ENVIRONMENTS

        self.verbose = verbose

        # define empty frames
        self.RP = None       # road parameters
        self.C_fin = None
        self.C_eco = None
        self.O0_fin = None
        self.O0_eco = None
        self.O1_fin = None
        self.O1_eco = None

        self.V0 = None
        self.V1 = None
        self.L = None
        self.T0 = None
        self.T1 = None
        self.I0 = None
        self.I1 = None

        self.RF = None      # ratio of fuel types
        self.QF0 = None     # quantity of fuel burnt on a section in variant 0
        self.QF1 = None     # quantity of fuel burnt on a section in variant 1

        self.UC = {}        # unit costs
        self.B0 = {}        # benefits in 0th variant
        self.B1 = {}        # benefits in 1st variant
        self.NB = {}        # net benefits
        self.NC = {}        # net costs

        super().__init__(self.country, self.pl, verbose=self.verbose)


    # =====
    # Initialisation functions
    # =====
    def load_parameters(self, source="default"):
        """Read in the CBA parameters
        Can read from a user-defined directory"""
        if source == "default":
            super().read_raw_params()
        else:
            raise NotImplementedError("To add soon.")
            

    def replace_parameter(self, param):
        """Replace a specific parameter frame"""
        raise NotImplementedError("To add soon.")


    def prepare_parameters(self):
        """Read in and manipulate all the CBA parameters"""
        super().adjust_cpi(yr_max=self.yr_f)
        super().clean_params()
        super().adjust_price_level()
        super().wrangle_params()

    
    def _assign_core_variables(self):
        """After reading project inputs define years of operation
        and various arrays of sections"""
        if self.C_fin is not None:
            self.yr_op = int(self.C_fin.columns[-1]) + 1
            self.N_yr_bld = len(self.C_fin.columns)
            self.N_yr_op = self.N_yr - self.N_yr_bld
            self.yrs_op = \
                np.arange(self.yr_i + self.N_yr_bld, self.yr_i + self.N_yr)

            self.secs = self.RP.index
            self.secs_0 = self.RP[self.RP.variant_0 == 1].index
            self.secs_1 = self.RP[self.RP.variant_1 == 1].index
            self.secs_old = \
                self.RP[(self.RP.variant_0 == 1) & (self.RP.variant_1 == 1)].index
            self.secs_repl = \
                self.RP[(self.RP.variant_0 == 1) & (self.RP.variant_1 == 0)].index
            self.secs_new = \
                self.RP[(self.RP.variant_0 == 0) & (self.RP.variant_1 == 1)].index


    def _wrangle_inputs(self):
        """Modify input matrices of intensities and velocities
        in line with the economic period and other global requirements.
        Ensure that the columns representing years are integers."""
        self.I0.columns = self.I0.columns.astype(int)
        self.I1.columns = self.I1.columns.astype(int)
        self.V0.columns = self.V0.columns.astype(int)
        self.V1.columns = self.V1.columns.astype(int)

        # remove unused rows in 0th variant
        self.I0 = self.I0.loc[self.secs_0]
        self.V0 = self.V0.loc[self.secs_0]

        if self.I0.columns[-1] < self.yr_f:
            if self.verbose:
                print("Warning: I0 not forecast until the end of period,\
                filling by zeros.")
        self.I0 = self.I0[self.yrs].fillna(0)

        if self.I1.columns[-1] < self.yr_f:
            if self.verbose:
                print("Warning: I0 not forecast until the end of period,\
                filling by zeros.")
        self.I1 = self.I1[self.yrs].fillna(0)

        if self.V0.columns[-1] < self.yr_f:
            if self.verbose:
                print("Warning: V0 not forecast until the end of period,\
                filling by zeros.")
        self.V0 = self.V0[self.yrs].fillna(0)

        if self.V1.columns[-1] < self.yr_f:
            if self.verbose:
                print("Warning: V0 not forecast until the end of period,\
                filling by zeros.")
        self.V1 = self.V1[self.yrs].fillna(0)


    def read_project_inputs(self, df_road_params, df_capex,\
        df_int_0, df_int_1, df_vel_0, df_vel_1,):
        """Read the dataframes
        * road parameters
        * capital investment (CAPEX)
        * intensities in variants 0 and 1
        * velocities in variant 0 and 1"""
        if self.verbose:
            print("Reading project inputs from df...")
        self.RP = df_road_params
        self.C_fin = df_capex
        self.I0 = df_int_0
        self.I1 = df_int_1
        self.V0 = df_vel_0
        self.V1 = df_vel_1

        # assign core variables
        self._assign_core_variables()
        self._wrangle_inputs()

    
    def read_project_inputs_xls(self, file_xls):
        assert file_xls.split(".")[-1] in ["xls", "xlsx"], \
            "Invalid file extension. Must be xls or xlsx."
        if self.verbose:
            print("Reading project inputs from xls/xlsx...")
        xls = pd.ExcelFile(file_xls)
        self.RP = xls.parse("road_params", index_col=0)
        self.C_fin = xls.parse("capex").reset_index(drop=True)
        self.C_fin.set_index(['item', 'category'], inplace=True)
        self.I0 = xls.parse("intensities_0").reset_index(drop=True)
        self.I0.set_index(["id_section", "vehicle"], inplace=True)
        self.I1 = xls.parse("intensities_1").reset_index(drop=True)
        self.I1.set_index(["id_section", "vehicle"], inplace=True)
        self.V0 = xls.parse("velocities_0").reset_index(drop=True)
        self.V0.set_index(["id_section", "vehicle"], inplace=True)
        self.V1 = xls.parse("velocities_1").reset_index(drop=True)
        self.V1.set_index(["id_section", "vehicle"], inplace=True)

        self._assign_core_variables()
        self._wrangle_inputs()


    def replace_intensities(self, df_int_0, df_int_1):
        if self.verbose:
            print("Replacing intensities...")
        self.I0 = df_int_0
        self.I1 = df_int_1


    def replace_velocities(self, df_vel_0, df_vel_1):
        if self.verbose:
            print("Replacing velocities...")
        self.V0 = df_vel_0
        self.V1 = df_vel_1


#    def read_project_inputs_csv(self,
#                                file_road_params,
#                                file_capex,
#                                file_int_0,
#                                file_int_1,
#                                verbose=False
#                                ):
#        if verbose:
#            print("Reading project inputs from csv...")
#        self.RP = pd.read_csv(file_road_params, index_col=0)
#        self.C_fin = pd.read_csv(file_capex, index_col=0)
#        self.I0 = pd.read_csv(file_int_0).reset_index()
#        self_I0.set_index(["id_section", "vehicle"], inplace=True)
#        self.I1 = pd.read_csv(file_int_1).reset_index()
#        self.I1.reset_index(inplace=True)
#        self.I1.set_index(["id_section", "vehicle"], inplace=True)
#
#        # assign core variables
#        self._assign_remaining_years()
#        self.secs_0 = self.RP[self.RP.variant_0 == 1].index
#        self.secs_1 = self.RP[self.RP.variant_1 == 1].index
#        self.secs_old = \
#            self.RP[(self.RP.variant_0 == 1) & (self.RP.variant_1 == 1)].index
#        self.secs_repl = \
#            self.RP[(self.RP.variant_0 == 1) & (self.RP.variant_1 == 0)].index
#        self.secs_new = \
#            self.RP[(self.RP.variant_0 == 0) & (self.RP.variant_1 == 1)].index


#    def read_velocities_csv(self, csv_vel_0, csv_vel_1, verbose=False):
#        """Read the dataframe of velocities ordered by project section
#        and vehicle category"""
#        if csv_vel_0[-3:] != "csv" or csv_vel_1[-3:] != "csv":
#            print("One of files does not have required extension: csv.")
#
#        if verbose:
#            print("Reading velocities from csv...")
#        self.V0 = pd.read_csv(csv_vel_0).reset_index()
#        self.V0.set_index(["id_section", "vehicle"], inplace=True)
#        self.V1 = pd.read_csv(csv_vel_1).reset_index()
#        self.V1.set_index(["id_section", "vehicle"], inplace=True)
#
#
#    def read_velocities_excel(self, xls_vel, verbose=False):
#        """Read the dataframe of velocities from one excel file."""
#        if not xls_vel.split(".")[-1] in ["xls", "xlsx"]:
#            print("File does not have the required extension: xls, xlsx.")
#
#        if verbose:
#            print("Reading velocities xls/xlsx...")
#        self.V0 = pd.read_excel(xls_vel, sheet_name="velocities_0")
#        self.V0.set_index(["id_section", "vehicle"], inplace=True)
#        self.V1 = pd.read_excel(xls_vel, sheet_name="velocities_1")
#        self.V1.set_index(["id_section", "vehicle"], inplace=True)


    def _verify_input_integrity(self):
        int_idx = ["id_section", "vehicle"]
        assert self.I0 is not None, "I0 not defined."
        assert self.I0.index.names == int_idx, "Index of I0 not correct."
        assert self.I1 is not None, "I1 not defined."
        assert self.I1.index.names == int_idx, "Index of I1 not correct."

        assert self.V0 is not None, "V0 not defined."
        assert self.V0.index.names == int_idx, "Index of V0 not correct."
        assert self.V1 is not None, "V1 not defined."
        assert self.V1.index.names == int_idx, "Index of V1 not correct."

        rp_cols = ["name", "variant_0", "variant_1", "length", \
            "length_bridges", "length_tunnels", "category", "lanes", \
            "environment", "width", "layout", "toll_sections"]
        assert self.RP is not None, "Road parameters not defined."
        assert set(self.RP.columns) == set(rp_cols), \
            "Columns of road parameters not correct."

#        capex_idx = ["land", "pavements", "bridges", "tunnels", "buildings",\
#            "slope_stabilisation", "retaining_walls", "noise_barriers",\
#            "safety_features", "supervision", "planning_design"]
#        assert self.C_fin is not None, "CAPEX not defined."
#        assert set(self.C_fin.index) == set(capex_idx), \
#            "Index of CAPEX not correct."


    def _verify_param_integrity(self):
        """Verify all the relevant parameter frames contain 
        correct columns and indices"""
        pass


    # =====
    # Computing CAPEX, OPEX and residual value
    # =====
    def _wrangle_capex(self):
        """Removing columns and squeezing investment expenses
        in years before the start into the first year
        of the economic period"""

        if "category" in self.C_fin.columns:
            self.C_fin.drop(columns="category", inplace=True)
        if "category" in self.C_fin.index.names:
            self.C_fin = self.C_fin.reset_index("category")\
                .drop(columns="category")
        if "total" in self.C_fin.columns:
            self.C_fin.drop(columns="total", inplace=True)
        self.C_fin.columns = self.C_fin.columns.astype(int)

        self.C_fin.fillna(0, inplace=True)

        # collect investment before the first year
        capex_yrs = self.C_fin.columns
        if len(capex_yrs[capex_yrs < self.yr_i]) != 0:
            if self.verbose:
                print("Squeezing CAPEX into the given economic period...")
            yrs_bef = capex_yrs[capex_yrs < self.yr_i]
            yrs_aft = capex_yrs[capex_yrs >= self.yr_i]
            self.C_fin[self.yr_i] += self.C_fin[yrs_bef].sum(1)
            self.C_fin = self.C_fin[yrs_aft]


    def compute_capex(self):
        """Apply conversion factors to compute
        CAPEX for the economic analysis."""
        if self.verbose:
            print("Computing CAPEX...")

        self._wrangle_capex()

        # reindex columns
        self.C_fin = pd.DataFrame(self.C_fin, columns=self.yrs).fillna(0)
        self.C_fin_tot = pd.DataFrame(self.C_fin.sum(1), columns=["value"])

        # apply conversion factors to get economic CAPEX
        self.cf = self.C_fin.copy()\
            .merge(self.df_clean["conv_fac"][["aggregate"]], \
            how="left", on="item")\
            .fillna(self.df_clean["conv_fac"]\
            .loc["construction", "aggregate"])["aggregate"]
        self.C_eco = self.C_fin.multiply(self.cf, axis=0)
        self.C_eco_tot = pd.DataFrame(self.C_eco.sum(1), columns=["value"])

        self.NC["capex"] = self.C_eco.sum()


    def compute_residual_value(self):
        """Create a dataframe of residual values by each element"""
        if self.verbose:
            print("Computing residual value...")

        RV = self.df_clean["res_val"].copy()
        RV.replacement_cost_ratio.fillna(1.0, inplace=True)
        RV["op_period"] = self.N_yr_op
        RV["replace"] = \
            np.where(RV.lifetime <= RV.op_period, 1, 0)
        RV["rem_ratio"] = \
            np.where(RV.lifetime <= RV.op_period,\
            (2*RV.lifetime - RV.op_period) / RV.lifetime,\
            (RV.lifetime - RV.op_period) / RV.lifetime).round(2)
        RV.rem_ratio.fillna(1.0, inplace=True) # fill land

        # financial
        self.RV_fin = RV.merge(self.C_fin_tot, how="left", on="item")\
            .fillna(0)
        self.RV_fin["res_value"] = np.where(self.RV_fin.replace == 0,\
            self.RV_fin.value * self.RV_fin.rem_ratio,\
            self.RV_fin.value * self.RV_fin.rem_ratio * \
                self.RV_fin.replacement_cost_ratio)

        # economic
        self.RV_eco = RV.merge(self.C_eco_tot, how="left", on="item")
        self.RV_eco["res_value"] = np.where(self.RV_eco.replace == 0,\
            self.RV_eco.value * self.RV_eco.rem_ratio,\
            self.RV_eco.value * self.RV_eco.rem_ratio * \
                self.RV_eco.replacement_cost_ratio)

        self.NB["res_val"] = pd.Series(\
            np.array([0] * (self.N_yr-1) + [1]) * self.RV_eco.res_value.sum(),\
            index=self.yrs)


    def compute_opex(self):
        """Create a dataframe of operation costs (OPEX)."""
        if self.verbose:
            print("Computing OPEX...")

        assert bool(self.UC) == True, "Unit costs not computed."

        UC = self.UC["c_op"].copy()
        lvl_order = ["id_section", "operation_type", "item"]

        # create area matrix
        def define_area(x):
            return x if x in ["tunnels", "bridges"] else "pavements"

        UC = UC.reset_index(["item"])
        UC["area_type"] = UC.item.map(lambda x: define_area(x))
        UC = UC.reset_index().set_index(["category", "operation_type", \
            "area_type", "item"]).sort_index()
        
        # variant 0
        RA0 = self.RP.loc[self.secs_0, ["category", "length", \
            "length_bridges", "length_tunnels", "width"]].copy()
        RA0["pavements"] = RA0.width * RA0.length * 1e3
        RA0["bridges"] = RA0.width * RA0.length_bridges * 1e3
        RA0["tunnels"] = RA0.width * RA0.length_tunnels * 1e3
        RA0 = RA0.drop(\
            columns=["length", "length_bridges", "length_tunnels", "width"])
        RA0 = RA0.reset_index().melt(id_vars=["id_section", "category"], \
            var_name="area_type", value_name="value")
        RA0 = RA0.groupby(["id_section", "category", "area_type"])\
            [["value"]].sum()
        
        # time matrix of road areas
        RA0 = pd.DataFrame(np.outer(RA0.value, np.ones_like(self.yrs)), \
            index=RA0.index, columns=self.yrs)
        
        # summary
        self.O0_fin = (RA0 * (UC * self.mask0)).dropna().droplevel(\
            ["category", "area_type"]).reorder_levels(lvl_order).sort_index()
        
        # variant 1
        O1_old = self.O0_fin.loc[self.secs_old].copy()
        O1_repl = self.O0_fin.loc[self.secs_repl].copy()
        if not O1_repl.empty:
            O1_repl[self.yrs_op] = 0.0
        
        RA1 = self.RP.loc[self.secs_new, ["category", "length",\
            "length_bridges", "length_tunnels", "width"]].copy()
        RA1["pavements"] = RA1.width * RA1.length * 1e3
        RA1["bridges"] = RA1.width * RA1.length_bridges * 1e3
        RA1["tunnels"] = RA1.width * RA1.length_tunnels * 1e3
        RA1 = RA1.drop(columns=["length", "length_bridges", \
            "length_tunnels", "width"])
        RA1 = RA1.reset_index().melt(id_vars=["id_section", "category"], \
            var_name="area_type", value_name="value")
        RA1 = RA1.groupby(["id_section", "category", "area_type"])\
            [["value"]].sum()
        
        # time matrix of road areas
        RA1 = pd.DataFrame(np.outer(RA1.value, np.ones_like(self.yrs)), \
            index=RA1.index, columns=self.yrs)
        
        # summary
        O1_new = (RA1 * (UC * self.mask1)).dropna().droplevel(\
            ["category", "area_type"]).reorder_levels(lvl_order).sort_index()
        self.O1_fin = pd.concat([O1_old, O1_repl, O1_new]).sort_index()
        
        # economic values
        c = "conv_fac"
        cf = self.df_clean[c]\
            .loc[self.df_clean[c].expense_type == "operation", "aggregate"]
        cf.index.name = "operation_type"
        cf = pd.DataFrame(np.outer(cf, np.ones_like(self.yrs)), \
            columns=self.yrs, index=cf.index)
        
        self.O0_eco = self.O0_fin * cf
        self.O1_eco = self.O1_fin * cf
        self.NC["opex"] = self.O1_eco.sum() - self.O0_eco.sum()


    def _compute_toll(self):
        raise NotImplementedError()


    # =====
    # Preparation functions
    # =====
    def _create_unit_cost_matrix(self):
        """Define the unit cost matrices for each benefit"""
        if self.verbose:
            print("Creating time matrices for benefits...")

        for b in ["c_op", "toll_op", \
            "vtts", "voc", "c_fuel", "c_acc", "c_em", "noise"]:
            if self.verbose:
                print("    Creating: %s" % b)
            self.UC[b] = \
                pd.DataFrame(columns=self.yrs, index=self.df_clean[b].index)
            self.UC[b][self.yr_i] = self.df_clean[b].value
            for yr in self.yrs[1:]:
                self.UC[b][yr] = \
                    self.UC[b][self.yr_i]# * self.cpi.loc[yr, "cpi_index"]
                if "gdp_growth_adjustment" in self.df_clean[b].columns:
                    self.UC[b][yr] = self.UC[b][yr] \
                    * (1.0 + self.gdp_growth.loc[yr].gdp_growth \
                    * self.df_clean[b].gdp_growth_adjustment)

            if b in ["noise"]:
                self.UC[b] = self.UC[b].sort_index().round(5)
            else:
                self.UC[b] = self.UC[b].sort_index().round(2)

        # greenhouse unit cost computed separately
        b = "c_ghg"
        self.UC[b] = \
            pd.DataFrame(self.df_clean[b].loc[self.yr_i:self.yr_f, "value"])
        self.UC[b].columns = ["co2eq"] 
        self.UC[b] = self.UC[b].T

    
    def _create_unit_cost_opex_mask(self):
        """Compose a time matrix of zeros and ones indicating 
        if maintanance has to be performed in a given year."""
        lvl_order = ["category", "operation_type", "item"]
        # variant 0
        mask0 = pd.DataFrame(0, \
            index=self.df_clean["c_op"].index, columns=self.yrs)

        for itm in mask0.index:
            p = self.df_clean["c_op"].loc[itm, "periodicity"].astype(int)
            if p == 1:
                mask0.loc[itm] = 1
            else:
                v = np.zeros(mask0.shape[1]).astype(int)
                for i, _ in enumerate(v):
                    if (i+1) % p == 0:
                        v[i] = 1
                mask0.loc[itm] = v
        
        self.mask0 = mask0.reorder_levels(lvl_order).sort_index()
        
        # variant 1
        mask1 = pd.DataFrame(0, \
            index=self.df_clean["c_op"].index, columns=self.yrs_op)
        
        for itm in mask1.index:
            p = self.df_clean["c_op"].loc[itm, "periodicity"].astype(int)
            if p == 1:
                mask1.loc[itm] = 1
            else:
                v = np.zeros(mask1.shape[1]).astype(int)
                for i, _ in enumerate(v):
                    if (i+1) % p == 0:
                        v[i] = 1
                mask1.loc[itm] = v
        
        mask1 = pd.DataFrame(mask1, columns=self.yrs).fillna(0).astype(int)
        self.mask1 = mask1.reorder_levels(lvl_order).sort_index()


    def _create_length_matrix(self):
        """Create the matrix of lengs with years as columns"""
        if self.verbose:
            print("Creating length matrix...")
        self.L = pd.DataFrame(\
            np.outer(self.RP.length, np.ones_like(self.yrs)), \
            columns=self.yrs, index=self.RP.index)


    def _compute_travel_time_matrix(self):
        """Compute travel time by road section and vehicle type"""
        if self.verbose:
            print("Creating matrices of travel times...")
        assert self.L is not None, "Compute length matrix first."

        self.T0 = (self.L / self.V0).replace([np.inf, -np.inf], 0.0)
        self.T1 = (self.L / self.V1).replace([np.inf, -np.inf], 0.0)


    def _create_fuel_ratio_matrix(self):
        if self.verbose:
            print("Creating matrix of fuel ratios by vehicle...")
        rfuel = self.df_clean["r_fuel"].ratio.sort_index()
        self.RF = pd.DataFrame(repmat(rfuel, self.N_yr, 1).T, \
            columns=self.yrs, index=rfuel.index)


    # =====
    # Functions to compute economic benefits
    # =====
    def economic_analysis(self):
        """Wrapping method for the overall computation
        of costs, benefits and overall indicators (ENPV, ERR, BCR)."""
        ti = time.time()
        self.prepare_parameters()
        self.compute_costs_benefits()
        self.compute_economic_indicators()
        print("Done. Time: %.2f s." % (time.time() - ti))


    def compute_costs_benefits(self):
        """Compute financial and economic costs and benefits"""
        self._verify_input_integrity()
        self._verify_param_integrity()

        # unit costs
        if self.verbose:
            print("Preparing unit values...")
        self._create_unit_cost_matrix()
        self._create_unit_cost_opex_mask()

        # costs
        if self.verbose:
            print("Computing costs...")
        self.compute_capex()
        self.compute_opex()
        self.compute_residual_value()

        # benefits
        if self.verbose:
            print("Computing benefits...")

        self._create_length_matrix()
        self._compute_travel_time_matrix()
        
        self._compute_vtts()
        self._compute_voc()
        self._compute_accidents()
        self._create_fuel_ratio_matrix()
        self._compute_fuel_consumption()
        self._compute_fuel_cost()
        self._compute_greenhouse()
        self._compute_emissions()
        self._compute_noise()


    def compute_economic_indicators(self):
        """Perform economic analysis"""
        assert self.NB is not None, "Compute economic benefits first."

        if self.verbose:
            print("\nComputing ENPV, ERR, BCR...")
        self.df_eco = pd.DataFrame(self.NB).T
        self.df_eco = pd.concat(\
            [-pd.DataFrame(self.NC).T, pd.DataFrame(self.NB).T],\
                   keys=["cost", "benefit"], names=["type", "item"])\
                   .round(2)

        self.df_enpv = pd.DataFrame(self.df_eco\
            .apply(lambda x: np.npv(self.r_eco, x), axis=1).round(2), \
            columns=["value"])

        self.ENPV = np.npv(self.r_eco, self.df_eco.sum())
        self.ERR = np.irr(self.df_eco.sum())
        self.EBCR = (self.df_enpv.loc["benefit"].sum() \
            / -self.df_enpv.loc["cost"].sum()).value

    
    def print_economic_indicators(self):
        print("ENPV: %.2f M %s" % (self.ENPV / 1e6, self.currency.upper()))
        print("ERR : %.2f %%" % (self.ERR * 100))
        print("BCR : %.2f" % self.EBCR)


    def _compute_vtts(self):
        """Mask is given by the intensities, as these are zero
        in the construction years"""
        if self.verbose:
            print("    Computing VTTS...")
        assert self.T0 is not None, "Compute travel time first."
        assert self.T1 is not None, "Compute travel time first."

        b = "vtts"
        self.B0[b] = self.UC[b] * self.T0 * self.I0 * DAYS_YEAR
        self.B1[b] = self.UC[b] * self.T1 * self.I1 * DAYS_YEAR
        self.NB[b] = self.B0[b].sum() - self.B1[b].sum()


    def _compute_voc(self):
        assert self.L is not None, "Compute length matrix first."
        if self.verbose:
            print("    Computing VOC...")
        assert self.L is not None, "Compute length matrix first."

        b = "voc"
        dum = pd.DataFrame(1, index=pd.MultiIndex.from_product(\
            [self.L.index, self.UC[b].index]), columns=self.yrs)
        dum.index.names = ["id_section", "vehicle"]
        self.B0[b] = ((self.UC[b] * dum) * self.L) * self.I0 * DAYS_YEAR
        self.B1[b] = ((self.UC[b] * dum) * self.L) * self.I1 * DAYS_YEAR
        self.NB[b] = self.B0[b].sum() - self.B1[b].sum()


    def _compute_accidents(self):
        assert self.L is not None, "Compute length matrix first."
        if self.verbose:
            print("    Computing accidents...")
        assert self.L is not None, "Compute length matrix first."

        b = "acc"
        scale = 1e-8
        LL = self.L.merge(\
            self.RP[["lanes", "environment", "category", "layout"]], \
            how="left", on="id_section").reset_index()\
            .set_index(["id_section", "lanes", "environment", "category", \
            "layout"]).reorder_levels(\
                ["id_section", "category", "lanes", "layout", "environment"])
        LL.columns = LL.columns.astype(int)

        UCA = (LL * self.UC["c_acc"] * scale)\
            .droplevel(["layout", "lanes", "category", "environment"])\
            .dropna(subset=[self.yr_i]).sort_index()

        self.B0[b] = UCA * self.I0 * DAYS_YEAR
        self.B1[b] = UCA * self.I1 * DAYS_YEAR
        self.NB[b] = self.B0[b].sum() - self.B1[b].sum()


    def _compute_fuel_consumption(self):
        """Compute the consumption by section, vehicle and fuel type"""
        if self.verbose:
            print("    Computing fuel consumption...")
        assert self.L is not None, "Compute length matrix first."

        # polynomial coefficients and consumption function
        def vel2cons(c, v):
            """Convert velocity in km/h to fuel consumption in
            kg/km via a polynomial"""
            return np.polyval(c[::-1], v)

        # length matrix with appropriate division of fuel/vehicle types
        dum = pd.DataFrame(1, index=pd.MultiIndex.from_product(\
            [self.secs, self.veh_types]), columns=self.yrs)
        dum.index.names = ["id_section", "vehicle"]
        L = self.L * dum
        
        ind = self.df_clean["r_fuel"].reset_index()[["vehicle", "fuel"]]
        L = L.reset_index().merge(ind, how="left", on="vehicle")\
            .set_index(["id_section", "vehicle", "fuel"])
        L = L.sort_index()

        # quantity of fuel, 0th variant
        self.QF0 = pd.DataFrame(columns=self.yrs, index=L.loc[self.secs_0].index)
        for ind, _ in self.QF0.iterrows():
            ids, veh, f = ind
            self.QF0.loc[(ids, veh, f)] = self.V0.loc[(ids, veh)]\
                .map(lambda v: vel2cons(\
                self.df_clean["fuel_coeffs"].loc[(veh, f)], v)) * L.loc[ind]

        # quantity of fuel in 1st variant
        self.QF1 = pd.DataFrame(columns=self.yrs, index=L.loc[self.secs_1].index)
        for ind, _ in self.QF1.iterrows():
            ids, veh, f = ind
            self.QF1.loc[(ids, veh, f)] = self.V1.loc[(ids, veh)]\
                .map(lambda v: vel2cons(\
                self.df_clean["fuel_coeffs"].loc[(veh, f)], v)) * L.loc[ind]


    def _compute_fuel_cost(self):
        if self.verbose:
            print("    Computing fuel cost...")
        assert self.RF is not None, "Compute matrix of fuel ratios (RF) first."
        assert self.QF0 is not None, "Compute matrix of fuel consumption (QF0) first."
        assert self.QF1 is not None, "Compute matrix of fuel consumption (QF1) first."

        b = "fuel"
        c = "c_fuel"
        self.B0[b] = (self.UC[c] * self.RF) * (self.QF0 * self.I0) * DAYS_YEAR
        self.B1[b] = (self.UC[c] * self.RF) * (self.QF1 * self.I1) * DAYS_YEAR
        self.NB[b] = self.B0[b].sum() - self.B1[b].sum()


    def _compute_greenhouse(self):
        if self.verbose:
            print("    Computing greenhouse gases...")
        assert self.RF is not None, "Compute matrix of fuel ratios (RF) first."
        assert self.QF0 is not None, "Compute matrix of fuel consumption (QF0) first."
        assert self.QF1 is not None, "Compute matrix of fuel consumption (QF1) first."
        b = "ghg"

        # UCG: unit cost of greenhouse gases in EUR/kg(fuel)
        UCG = pd.DataFrame(\
            np.outer(self.df_clean["r_ghg"].values, self.UC["c_ghg"].values),\
            index=self.df_clean["r_ghg"].index, columns=self.yrs)
        
        self.B0[b] = (UCG * self.RF) * (self.QF0 * self.I0) * DAYS_YEAR
        self.B1[b] = (UCG * self.RF) * (self.QF1 * self.I1) * DAYS_YEAR
        self.NB[b] = self.B0[b].sum() - self.B1[b].sum()


    def _compute_emissions(self):
        if self.verbose:
            print("    Computing emissions...")
        assert self.RF is not None, "Compute matrix of fuel ratios (RF) first."
        assert self.QF0 is not None, "Compute matrix of fuel consumption (QF0) first."
        assert self.QF1 is not None, "Compute matrix of fuel consumption (QF1) first."
        
        b = "em"
        RE = pd.DataFrame(repmat(self.df_clean["r_em"].value, self.N_yr, 1).T, 
                  columns=self.yrs, index=self.df_clean["r_em"].index)

        # UCE: unit cost of emissions in EUR/kg(fuel)
        UCE = RE * self.UC["c_em"]
        UCE = UCE.groupby(["fuel","vehicle","environment"]).sum()
        UCE = UCE.reset_index()\
            .set_index(["environment","vehicle","fuel"]).sort_index()

        # add section ID
        UCE = UCE.reset_index().merge(self.RP.environment.reset_index(), \
            how="left", on="environment").set_index(\
            ["id_section", "environment", "vehicle", "fuel"]).sort_index()
        
        lvl_order = ["id_section", "vehicle", "fuel", "environment"]
        self.B0[b] = (UCE * self.RF).reorder_levels(lvl_order).sort_index() \
            * (self.QF0 * self.I0) * DAYS_YEAR
        self.B1[b] = (UCE * self.RF).reorder_levels(lvl_order).sort_index() \
            * (self.QF1 * self.I1) * DAYS_YEAR
        self.NB[b] = self.B0[b].sum() - self.B1[b].sum()


    def _compute_noise(self):
        if self.verbose:
            print("    Computing noise...")
        assert self.L is not None, "Compute length matrix first."

        b = "noise"
        L = self.L.reset_index().merge(self.RP.environment.reset_index())
        L = L.set_index(["id_section", "environment"])
        
        # CN: cost of noise in EUR
        CN = (self.UC[b] * L).reorder_levels(\
            ["id_section", "environment", "vehicle"]).sort_index()

        self.B0[b] = CN * self.I0 * DAYS_YEAR
        self.B1[b] = CN * self.I1 * DAYS_YEAR
        self.NB[b] = self.B0[b].sum() - self.B1[b].sum()


    # =====
    # Financial analysis
    # =====
    def financial_analysis(self):
        """Perform financial analysis"""
        raise NotImplementedError()







