"""This files stores the get_symbols function which can input a string and return its corresponding symbol as a string"""

global symbols_dict,key_symbols_dict
symbols_dict= dict()

symbols_dict["alp_sym"]= "\u03b1"
symbols_dict["Cpc_sym"]= "Cp_c"
symbols_dict["Cpt_sym"]= "Cp_t"
symbols_dict["Cpab_sym"]= "Cp_AB"
symbols_dict["Hpr_sym"]= "hpr"
symbols_dict["AB_sym"]= "Afterburner"
symbols_dict["gam_c_sym"]= "\u03B3" + "_c"
symbols_dict["gam_t_sym"]= "\u03B3" + "_t"
symbols_dict["gam_ab_sym"]= "\u03B3" + "_AB"
symbols_dict["Rc_sym"]= "R_c"
symbols_dict["Rt_sym"]= "R_t"
symbols_dict["Rab_sym"]= "R_AB"
symbols_dict["eta_b_sym"]= "\u03B7" + "_b"
symbols_dict["eta_m_sym"]= "\u03B7" + "_m"
symbols_dict["eta_ab_sym"]= "\u03B7" + "_AB"
symbols_dict["pi_d_max_sym"]= "\u03C0" + "_d_max"
symbols_dict["pi_f_sym"]= "\u03C0" + "_f"
symbols_dict["pi_c_sym"]= "\u03C0" + "_c"
symbols_dict["pi_cL_sym"]= "\u03C0" + "_cL"
symbols_dict["pi_cH_sym"]= "\u03C0" + "_cH"
symbols_dict["pi_b_sym"]= "\u03C0" + "_b"
symbols_dict["pi_m_max_sym"]= "\u03C0" + "_m_max"
symbols_dict["pi_ab_sym"]= "\u03C0" + "_AB"
symbols_dict["pi_n_sym"]= "\u03C0" + "_n"
symbols_dict["pi_fn_sym"]= "\u03C0" + "_fn"
symbols_dict["peta_f_sym"]= "e" + "_f"
symbols_dict["peta_c_sym"]= "e" + "_c"
symbols_dict["peta_t_sym"]= "e" + "_t"
symbols_dict["P0_P9_sym"]= "P0" + "/" + "P9"
symbols_dict["P0_P19_sym"]= "P0" + "/" + "P19"

symbols_dict["a0_sym"]= "a0"
symbols_dict["f_sym"]= "\u1E41" + "_\u0066" + "/" + "\u1E41" + "\u2080"
symbols_dict["f_CC_sym"]= "\u0192" + "_CC"
symbols_dict["f_AB_sym"]= "\u0192" + "_AB"
symbols_dict["M9_sym"]= "M9"
symbols_dict["pi_d_sym"]= "\u03C0" + "_d"
symbols_dict["tau_r_sym"]= "\u03C4" + "_r"
symbols_dict["pi_r_sym"]= "\u03C0" + "_r"
symbols_dict["tau_L_CC_sym"]= "_\u039B"+"_CC"
symbols_dict["tau_L_AB_sym"]= "_\u039B"+"_AB"
symbols_dict["tau_L_sym"]= "\u03C4" + "_L"
symbols_dict["tau_f_sym"]= "\u03C4" + "_f"
symbols_dict["tau_cL_sym"]= "\u03C4" + "_cL"
symbols_dict["tau_cH_sym"]= "\u03C4" + "_cH"
symbols_dict["tau_c_sym"]= "\u03C4" + "_c"
symbols_dict["tau_tL_sym"]= "\u03C4" + "_tL"
symbols_dict["tau_tH_sym"]= "\u03C4" + "_tH"
symbols_dict["tau_t_sym"]= "\u03C4" + "_t"
symbols_dict["pi_tL_sym"]= "\u03C0" + "_tL"
symbols_dict["pi_tH_sym"]= "\u03C0" + "_tH"
symbols_dict["pi_t_sym"]= "\u03C0" + "_t"
symbols_dict["eta_t_sym"]= "\u03B7" + "_t"
symbols_dict["eta_p_sym"]= "\u03B7" + "_p"
symbols_dict["eta_o_sym"]= "\u03B7" + "_o"
symbols_dict["v9_sym"]= "V9"
symbols_dict["v0_sym"]= "V0"
symbols_dict["v9_v0_sym"]= "V9" + "/" + "V0"

keys_symbols_dict= symbols_dict.keys()
def get_symbol(word):
    if word+"_sym" not in keys_symbols_dict:
        return word
    symbol= symbols_dict[word+"_sym"]
    return symbol




global fullform_dict,keys_fullform_dict
#To be used for x and y axis labelling in plotting
fullform_dict= dict()
fullform_dict["f_fullform"]= "Fuel air ratio"
fullform_dict["ST_fullform"]= "Specific Thrust (N-s/kg)"
fullform_dict["TSFC_fullform"]= "Thrust Specific Fuel Consumption (kg/N-s) *1e+6"
fullform_dict["pi_c_fullform"]= "Compressor pressure ratio"
fullform_dict["Tt4_fullform"]= "Turbine Inlet Temperature (K)"
fullform_dict["alt_fullform"]= "Altitude (m)"
fullform_dict["M0_fullform"]= "Mach number"
fullform_dict["alp_fullform"]= "Bypass ratio"

keys_fullform_dict= fullform_dict.keys()
def get_fullform(word):
    if word+"_fullform" not in keys_fullform_dict:
        return word
    fullform= fullform_dict[word+"_fullform"]
    return fullform