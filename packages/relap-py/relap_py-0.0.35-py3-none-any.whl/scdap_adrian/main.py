"""
Title: RELAP utilities
created: May 2020
last modified: 02/11/2020 20:52:47 
Version: 3.1
Created by: Jordi Freixa
Description: This Module provides function tools for postprocessing RELAP data

INSTALLATION:
    - put the file in the site-package folder
          mine is in ~/Anaconda3/Lib/side-packages/
    - modify the relapwin_loc and relap_exe variables to your environment


TODO:
    - adapt to TRACE plotting (basically reading data from csv files)
    - Make steady state table
    - read and plot uncertainty bands
    - just perform data extraction and write to file
"""
from .config import (
        path_to_exe,
        set_path_to_exe,
        relapwin_loc,
        set_relapwin_loc,
        set_figures_type,
        figures_type,
        set_figures_loc,
        figures_loc,
        set_show_plot,
        show_plot,
        set_relap_scdap,
        relap_scdap,
        set_unc_bands,
        unc_bands
        )
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from subprocess import Popen, PIPE
from numpy.lib.recfunctions import append_fields



#▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
relap_labels = {
    "count": "Current attempted advancement count number",
    "cputime": "CPU time(s)",
    "dt": "Current time step (s)",
    "dtcrnt": "Current Courant time step (s)",
    "emass": "Estimate of mass error in all the systems (kg)",
    "errmax": "Current estimate of the truncation mass error fraction",
    "extsnn": "Extra system variables where NN goes from 01 to 20",
    "maxvme": "Maximum value of all the individual volume mass errors (kg)",
    "null": "Specifies null field",
    "rktpow3d": "Total reactor power for the RELAP5/PARCS 3-D kinetics coupled code (W)",
    "stdtrn": "Steady-state/transient flag",
    "sysmer": "Estimate of mass error in system N (kg)",
    "sysmerb": "Estimate of boron mass error in system N (kg)",
    "sysmerf": "Estimate of liquid mass error in system N (kg)",
    "sysmerg": "Estimate of vapor mass error in system N (kg)",
    "sysmern": "Estimate of noncondensable mass error in system N (kg)",
    "systmb": "Total mass of boron in system N (kg) from state equation",
    "systmc": "Total mass of steam, water, and noncondensable in system N (kg) from continuity equation",
    "systmf": "Total mass of liquid in system N (kg) from state equation",
    "systmfc": "Total mass of liquid in system N (kg) from continuity equation",
    "systmg": "Total mass of vapor (steam plus noncondensable) in system N (kg) from state equation",
    "systmgc": "Total mass of vapor (steam plus noncondensable) in system N (kg) from continuity equation",
    "systmn": "Total mass of noncondensables in system N (kg) from state equation",
    "systmnc": "Total mass of noncondensables in system N (kg) from continuity equation",
    "systms": "Total mass of steam, water, and noncondensable in system N (kg) from state equation",
    "testda": "An array, testda, of one hundred quantities",
    "time": "Time (s)",
    "timeof": "Time of trip occurring (s)",
    "tmass": "Total mass of water, steam, and noncondensables in all the systems (kg)",
    "tothgen": "Total hydrogen generation from metal-water reactions in all the systems (kg)",
    "vnmaxvme": "Volume number of the volume having the maximum volume mass error (see MAXVME)",
    "acpgtg": "Accumulator vapor specific heat, Cp, at vapor temperature (J/kg•K)",
    "acpnit": "Accumulator noncondensable specific heat, Cp, at vapor temperature (J/kg•K)",
    "acqtank": "Total energy transport to the gas by heat and mass transfer in the accumulator (W)",
    "acrhon": "Accumulator noncondensable density (kg/m3)",
    "acttank": "Mean accumulator tank wall metal temperature (K)",
    "acvdm": "Gas volume in the accumulator tank, standpipe, and surge line (m3)",
    "acvgtg": "Accumulator vapor specific heat, Cv, at vapor temperature (J/kg•K)",
    "acvliq": "Liquid volume in the accumulator tank, standipipe, and surge line (m3)",
    "ahfgtf": "Accumulator heat of vaporization at liquid temperature (J/kg)",
    "ahfgtg": "Accumulator heat of vaporization at vapor temperature (J/kg)",
    "ahftg": "Accumulator liquid enthalpy at vapor temperature (J/kg)",
    "ahgtf": "Accumulator vapor enthalpy at liquid temperature (J/kg)",
    "avgtg": "Accumulator specific volume at vapor temperature (m3/kg)",
    "aviscn": "Accumulator noncondensable viscosity (kg/m•s)",
    "betav": "Accumulator steam saturation coefficient of expansion (K-1)",
    "cdim": "GE mechanistic dryer critical inlet moisture quality",
    "dim": "GE mechanistic dryer inlet moisture quality",
    "dmgdt": "Accumulator/time rate of change in dome vapor mass (kg/s)",
    "gdry": "GE mechanistic separator capacity factor",
    "omega": "Inertial valve disk angular velocity (rad/s)",
    "pmphead": "Pump head in the pump component (Pa)",
    "pmpmt": "Pump motor torque (N•m)",
    "pmpnrt": "Calculated pump inertia (kg•m 2)",
    "pmptrq": "Pump torque in the pump component (N•m)",
    "pmpvel": "Pump rotational velocity in the pump component (rad/s)",
    "przlvl": "Pressurizer level in the PRIZER component (m)",
    "theta": "Inertial valve disk angular position (deg)",
    "tureff": "Efficiency of the turbine component",
    "turpow": "Power developed in the turbine component (W)",
    "turtrq": "Torque developed in the turbine component (N•m)",
    "turvel": "Rotational velocity of the turbine component (rad/s)",
    "vlvarea": "Ratio of the current valve physical area to the junction area",
    "vlvstem": "Ratio of the current valve stem position to the fully open valve stem position for the motor and servo valves when the normalized stem position option is used",
    "xco": "GE mechanistic separator liquid carryover quality",
    "xcu": "GE mechanistic separator vapor carryunder quality",
    "xi": "GE mechanistic separator inlet quality",
    "avol": "Area of the volume (m2); the parameter is the volume number plus F",
    "betaff": "Liquid isobaric coefficient of the thermal expansion, βf, bulk conditions (K-1, oF-1)",
    "betagg": "Vapor isobaric coefficient of the thermal expansion, βg, bulk conditions (K-1, oF-1)",
    "boron": "Spatial boron density, ρb (kg/m3)",
    "csubpf": "Liquid specific heat, Cpf, bulk conditions (J/kg•K)",
    "csubpg": "Vapor specific heat, Cpg, bulk conditions (J/kg•K)",
    "drfdp": "Partial derivative of ρf with respect to P (s2/m2)",
    "drfduf": "Partial derivative of ρf with respect to Uf (kg•s2/m5)",
    "drgdp": "Partial derivative of ρg with respect to P (s2/m2)",
    "drgdug": "Partial derivative of ρg with respect to Ug (kg•s 2/m5)",
    "drgdxa": "Partial derivative of ρg with respect to Xn (kg/m3)",
    "dtdp": "Partial derivative of Ts with respect to P (K/Pa)",
    "dtdug": "Partial derivative of Ts with respect to Ug (s2•K/m2)",
    "dtdxa": "Partial derivative of Ts with respect to Xn (K)",
    "dtfdp": "Partial derivative of Tf with respect to pressure (K/Pa)",
    "dtfduf": "Partial derivative of Tf with respect to Uf (s2•K/m2)",
    "dtgdp": "Partial derivative of Tg with respect to P (K/Pa)",
    "dtgdug": "Partial derivative of Tg with respect to Ug (s2•K/m2)",
    "dtgdxa": "Partial derivative of Tg with respect to Xn (K)",
    "entropyf": "Liquid specific entropy, sf, at bulk conditions (J/kg•K)",
    "entropyg": "Vapor specific entropy, sg, at bulk conditions (J/kg•K)",
    "extvnn": "Extra volume variables where NN goes from 01 to 20",
    "floreg": "Flow regime number",
    "fwalf": "Liquid wall frictional drag coefficient (kg/m3•s)",
    "fwalg": "Vapor wall frictional drag coefficient (kg/m3•s)",
    "gammac": "For explicit coupling of heat conduction/transfer and hydrodynamics, this is 0",
    "gammai": "Mass transfer rate per unit volume at the vapor/liquid interface in the bulk fluid for vapor generation/condensation (kg/m3•s)",
    "gammaw": "For explicit coupling of heat conduction/transfer and hydrodynamics, this is the mass transfer rate per unit volume at the vapor/liquid interface in the boundary layer near the wall for vapor generation/condensation (kg/m3•s)",
    "hgf": "Direct heating heat transfer coefficient per unit volume (W/m3•K)",
    "hif": "Liquid side interfacial heat transfer coefficient per unit volume (W/m3•K)",
    "hig": "Vapor side interfacial heat transfer coefficient per unit volume (W/m3•K)",
    "hsteam": "Steam specific enthalpy at bulk conditions using partial pressure of steam (J/kg)",
    "hvmix": "Enthalpy of the liquid and vapor (J/kg)",
    "kappaf": "Liquid isothermal compressibility, κf , at bulk conditions (Pa-1)",
    "kappag": "Vapor isothermal compressibility, , at bulk conditions (Pa-1)",
    "p": "Volume pressure (Pa)",
    "pecltv": "Peclet number",
    "pps": "Steam partial pressure (Pa)",
    "q": "Total volume heat source from the wall and direct moderator heating to liquid and vapor (W)",
    "quala": "Volume noncondensable mass fraction",
    "qualair": "Volume noncondensable mass fraction for AIR",
    "qualar": "Volume noncondensable mass fraction for ARGON",
    "argon": "to the total mass of the noncondensable gas",
    "argon": "is specified on the 110 card",
    "quale": "Volume equilibrium quality",
    "qualhe": "Volume noncondensable mass fraction for HELIUM",
    "helium": "to the total mass of the noncondensable gas",
    "helium": "is specified on the 110 card",
    "qualhy": "Volume noncondensable mass fraction for HYDROGEN",
    "hydrogen": "to the total mass of the noncondensable gas",
    "qualkr": "Volume noncondensable mass fraction for KRYPTON",
    "krypton": "to the total mass of the noncondensable gas",
    "krypton": "is specified on the 110 card",
    "qualni": "Volume noncondensable mass fraction for NITROGEN",
    "nitrogen": "to the total mass of the noncondensable gas",
    "nitrogen": "is specified on the 110 card",
    "quals": "Volume static quality",
    "qualxe": "Volume noncondensable mass fraction for XENON",
    "xenon": "to the total mass of the noncondensable gas",
    "xenon": "is specified on the 110 card",
    "qwg": "Volume heat source from the wall and direct moderator heating to vapor (W)",
    "rho": "Total density (kg/m3)",
    "rhof": "Liquid density ρf (kg/m3)",
    "rhog": "Vapor density ρg (kg/m3)",
    "rhom": "Total density for the mass error check (kg/m3)",
    "sathf": "Liquid specific enthalpy at saturation conditions using partial pressure of steam (J/kg)",
    "sathg": "Steam specific enthalpy at saturation conditions using partial pressure of steam (J/kg)",
    "sattemp": "Volume saturation temperature based on the partial pressure of steam (K)",
    "sigma": "Surface tension (N/m)",
    "sounde": "Volume sonic velocity (m/s)",
    "tempf": "Volume liquid temperature Tf (K)",
    "tempg": "Volume vapor temperature Tg (K)",
    "thconf": "Liquid thermal conductivity (W/m•K)",
    "thcong": "Vapor thermal conductivity (W/m•K)",
    "tiengv": "Total internal energy (of both phases and noncondensables) in volume (J)",
    "tmassbv": "Boron mass in volume from state equation (kg)",
    "tmassfv": "Liquid mass in volume from state equation (kg)",
    "tmassgv": "Vapor mass (includes noncondensables) in volume from state equation (kg)",
    "tmassnv": "Noncondensable mass in volume from state equation (kg)",
    "tmassv": "Total fluid mass (includes both phases) in volume from state equation (kg)",
    "tsatt": "Saturation temperature corresponding to total pressure (K)",
    "tspinf": "Liquid spinodal temperature (K)",
    "tsping": "Vapor spinodal temperature (K)",
    "uf": "Liquid specific internal energy (J/kg)",
    "ug": "Vapor specific internal energy (J/kg)",
    "usatf": "Liquid specific internal energy at saturation (J/kg)",
    "usatg": "Vapor specific internal energy at saturation (J/kg)",
    "vapgen": "Total mass transfer rate per unit volume at the vapor/liquid interface in the bulk fluid for vapor generation/condensation and in the boundary layer near the wall for vapor generation/condensation (kg/m3•s)",
    "velf": "Volume oriented liquid velocity (m/s)",
    "velg": "Volume oriented vapor velocity (m/s)",
    "vlev": "Velocity of level in volume (m/s)",
    "viscf": "Liquid viscosity (kg/m•s)",
    "viscg": "Vapor viscosity (kg/m•s)",
    "voidf": "Volume liquid fraction",
    "voidg": "Volume vapor fraction",
    "voidla": "Volume vapor fraction above the level",
    "voidlb": "Volume vapor fraction below the level",
    "vollev": "Elevation of the level in the volume (m)",
    "volmas": "Volume mass in volume from continuity equation (kg)",
    "volmasb": "Volume boron mass from continuity equation (kg)",
    "volmasf": "Volume liquid mass from continuity equation (kg)",
    "volmasg": "Volume vapor mass from continuity equation (kg)",
    "volmasn": "Volume noncondensable mass from continuity equation (kg)",
    "volmer": "Volume mass error (kg)",
    "volmerb": "Volume boron mass error (kg)",
    "volmerf": "Volume liquid mass error (kg)",
    "volmerg": "Volume vapor mass error (kg)",
    "volmern": "Volume noncondensable mass error (kg)",
    "boronj": "Junction boron density (kg/m3)",
    "c0j": "Junction distribution coefficient",
    "chokef": "Junction choking flag",
    "extjnn": "Extra junction variables where NN goes from 01 to 20",
    "fij": "Interphase frictionΣ coefficient (N•s 2/m5)",
    "fjunft": "Total forward user input form loss coefficient for irreversible losses)",
    "fjunrt": "Total reverse user input form loss coefficient for irreversible losses)",
    "flenth": "Total enthalpy flow in junction (includes both phases and noncondensables) (J/s)",
    "flenthf": "Liquid enthalpy flow in junction (J/s)",
    "flenthg": "Vapor enthalpy flow in junction (J/s)",
    "florgj": "Junction flow regime number",
    "formfj": "Liquid abrupt area change model form loss factor (dimensionless)",
    "formgj": "Vapor abrupt area change model form loss factor (dimensionless)",
    "fwalfj": "Non-dimensional liquid wall friction coefficient (dimensionless)",
    "fwalgj": "Non-dimensional vapor wall friction coefficient (dimensionless)",
    "iregj": "Vertical bubbly/slug flow junction flow regime number",
    "mflowbj": "Boron flow rate (kg/s)",
    "mflowfj": "Liquid flow rate (kg/s)",
    "mflowgj": "Vapor flow rate (kg/s)",
    "mflowj": "Mass flow rate (kg/s)",
    "mflownj": "Noncondensable flow rate (kg/s)",
    "qualaj": "Junction noncondensable mass fraction",
    "qualjair": "Junction noncondensable mass fraction for AIR",
    "qualjar": "Junction noncondensable mass fraction for ARGON",
    "argon": "to the total mass of the noncondensable gas",
    "argon": "is specified on the 110 card",
    "qualjhe": "Junction noncondensable mass fraction for HELIUM",
    "helium": "to the total mass of the noncondensable gas",
    "helium": "is specified on the 110 card",
    "qualjhy": "Junction noncondensable mass fraction for HYDROGEN",
    "hydrogen": "to the total mass of the noncondensable gas",
    "qualjkr": "Junction noncondensable mass fraction for KRYPTON",
    "krypton": "to the total mass of the noncondensable gas",
    "krypton": "is specified on the 110 card",
    "qualjni": "Junction noncondensable mass fraction for NITROGEN",
    "nitrogen": "to the total mass of the noncondensable gas",
    "nitrogen": "is specified on the 110 card",
    "qualjxe": "Junction noncondensable mass fraction for XENON",
    "xenon": "to the total mass of the noncondensable gas",
    "xenon": "is specified on the 110 card",
    "rhofj": "Junction liquid density (kg/m3)",
    "rhogj": "Junction vapor density (kg/m3)",
    "sonicj": "Junction sound speed (m/s)",
    "ufj": "Junction liquid specific internal energy (J/kg)",
    "ugj": "Junction vapor specific internal energy (J/kg)",
    "velfj": "Junction liquid velocity (m/s)",
    "velgj": "Junction vapor velocity (m/s)",
    "vgjj": "Vapor drift velocity (m/s)",
    "voidfj": "Junction liquid fraction",
    "voidgj": "Junction vapor fraction (void fraction)",
    "voidj": "Junction vapor fraction (void fraction) used in the interphase friction",
    "xej": "Junction equilibrium quality",
    "hfrad": "Radiation heat flux (W/m2)",
    "hftot": "Total heat flux, i",
    "htchf": "Critical (maximum) heat flux (W/m2)",
    "htchfr": "Critical hat flux ratio",
    "htgamw": "Wall vapor generation rate per unit volume (kg/m3•s)",
    "hthgen": "Total hydrogen generation at this heat structure (kg)",
    "htmode": "Boundary heat transfer mode number",
    "htoxi": "Inside oxide layer thickness (m)",
    "htoxo": "Outside oxide layer thickness (m)",
    "htrg": "Heat flux to vapor phase (W/m2)",
    "htrnr": "Convective heat flux (W/m2)",
    "httemp": "Mesh point temperature (K)",
    "cccg0nn": "with a two-digit number appended (mesh point number)",
    "htvat": "Volume averaged temperature in the heat structure (K)",
    "pecl": "Liquid Peclet number for the heat structures",
    "stant": "Stanton number",
    "kgap": "Effective gap thermal conductivity (W/m•K)",
    "pgap": "Pressure of the gas gap (Pa)",
    "tgap": "Temperature of the gas gap (K)",
    "gapwd": "Width of the gas gap (m)",
    "clstrn": "Total cladding strain",
    "clhoop": "Cladding hoop stress (Pa)",
    "fines": "Current number of axial nodes on a reflood structure",
    "tchfqf": "Temperature at the critical (maximum) heat flux (K)",
    "trewet": "Rewet, quench, Leidenfrost, or minimum film boiling temperature (K)",
    "zqbot": "Elevation of bottom quench front (m)",
    "zqtop": "Elevation of top quench front (m)",
    "reac": "Reactivity feedback total (dollars)",
    "reactf.": "(Only available when the SEPARABL option is used on the 30000000 card)",
    "reacm": "Reactivity feedback total from moderator density changes (dollars)",
    "reacrb": "Reactivity feedback from boron density changes (dollars)",
    "separabl": "option is used on the 30000000 card)",
    "reacrm": "Reactivity feedback from moderator density changes (dollars)",
    "separabl": "option is used on the 30000000 card)",
    "reacs": "Reactivity feedback from scram curve (dollars)",
    "reactf": "Reactivity feedback from fuel temperature changes (dollars)",
    "separabl": "option is used on the 30000000 card)",
    "reactm": "Reactivity feedback from moderator temperature (spectral) changes (dollars)",
    "rkfipow": "Reactor power from fission (W)",
    "rkgapow": "Reactor power from decay of fission products and actinides (W)",
    "rkpowa": "Reactor power from decay of actinides (W)",
    "rkpowk": "Reactor power from decay of fission products (W)",
    "rkreac": "Reactivity (dollars)",
    "rkrecper": "Reciprocal period (s-1)",
    "rktpow": "Total reactor power, i",
    "cntrlvar": "Control component",
    "shaft": "component",
    "trip": "Trip number",
    "bgnhg": "Core nuclear heat generation (W)",
    "bgmct": "Core maximum surface temperature (K)",
    "bgtfprn": "Core cumulative noncondensable fission product release (kg)",
    "bgtfprs": "Core cumulative soluble fission product release (kg)",
    "bgth": "Core total hydrogen generation rate (kg/s)",
    "bgthq": "Core total oxidation heat generation (W)",
    "bgthqu": "Core oxidation heat generation due to uranium oxidation (W)",
    "bgthu": "Core hydrogen generation rate due to uranium oxidation",
    "crucb": "Failure of crust supporting molten pool indicator",
    "repool": "Equivalent radius of the molten pool of core material (m)",
    "shqin": "Total heat flowing through the inside surface of the flow shroud (W)",
    "shqout": "Total heat flowing through the outside surface of the flow shroud (W)",
    "achdpn": "Temperature of the bottom surface of the cohesive debris layer for component jj (K)",
    "pgas": "Gas pressure inside component jj (MPa)",
    "wdtqlp": "Thermal energy in the material from component jj that slumped below the bottom of component jj (J)",
    "zbtcoh": "Elevation of the bottom surface of the cohesive debris bed (m)",
    "zbtrub": "Elevation of the bottom of the rubble debris bed (m)",
    "ztpcoh": "Elevation of the top surface of the cohesive debris bed (m)",
    "ztprub": "Elevation of the top of the rubble debris bed (m)",
    "brchv": "Double-sided oxidation indicator",
    "damlev": "Damage state (unitless)",
    "dzfrcq": "Height of cohesive debris (m)",
    "effoxd": "Effective oxide thickness ",
    "h2oxd2": "Hydrogen production rate (kg/s)",
    "hoop": "Cladding hoop strain",
    "oxdeo": "Oxide thickness of the cladding (m)",
    "rci": "Inside radius of the cladding (m)",
    "rco": "Outside radius of the cladding (not including the crust of solidified material) (m)",
    "rnalf": "Inner radius of the alpha oxide layer (m)",
    "rnoxd": "Inner radius of the oxide layer (m)",
    "rocrst": "Outside radius of cladding (including the crust of the solidified material) (m)",
    "rpel": "Radius of fuel pellet (m)",
    "ruliq": "Outside radius of the solid part of the fuel pellet (m)",
    "wfrosr": "Mass of stainless steel resolidified (kg)",
    "wfrouo": "Mass of UO2 resolidified (kg)",
    "wfrozr": "Mass of zircaloy resolidified (kg)",
    "wremsr": "Mass of stainless steel remaining (kg)",
    "wremuo": "Mass of removed fuel (kg)",
    "wremzr": "Mass of removed cladding (kg)",
    "cadct": "Temperature of radial node ii, axial node kk, and component jj (K)",
    "cggivy": "Inventory of fission product kk released into the fuel/clad gap of component jj",
    "dcrepc": "Fraction of life expended for ii-th COUPLE heat structure identified for creep rupture calculation",
    "dcreph": "Fraction of life expended for ii-th RELAP5 heat structure identified for creep rupture calculation",
}
#▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
def read_variables(input_variables_file):

    """read_variables: just reads a file that lists all variables

    :USAGE: your_name = read_variables(input_variables)

    :input_variables_file: [str] the file that lists all the variables
                                 to be stripped
                           [DataFrame] name of the variable that stores the list of
                                 variables
    :returns: the information in 'input_variables' stored in 'your_name' variable
    """
    if type(input_variables_file) == str:
       variables = pd.read_csv(input_variables_file, delim_whitespace=True, comment='%')
    else :
        variables = input_variables_file
    return variables
#▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
def make_strip(input_variables_file, strip_filename: str, form="fmtout"):

    """make_strip: creates a strip file

    :USAGE: your_name = make_strip(input_variables, strip_filename)

    :input_variables_file: [str] file that lists all the variables to be stripped.
                                 The file name should include the extension, and be
                                 located in the running folder
                           [DataFrame] name of the variable that stores the list of
                                 variables to be stripped.
    :strip_filename: [str] the desired file name of the strip to be created. The
                           file name should include the extension, and be located
                           in the running folder
    :form: [str] (optional) field 'csv' or 'fmtout'. If using SCDAP, set it to 'csv'

    :returns: the information in 'input_variables' stored in 'your_name' variable
        - in addition, it creates a strip file in the folder
    """
    if form != 'csv' and form != 'fmtout' :
        print('WARNING: argument 1 should be either csv or fmtout')
        if relap_scdap():
            form = 'csv'
            print('Argument 1 is set to csv')
        else:
            form = 'fmtout'
            print('Argument 1 is set to fmtout')
    variables = read_variables(input_variables_file)
    # if type(input_variables_file) == str:
       # variables = pd.read_csv(input_variables_file, delim_whitespace=True, comment='%')
    # else :
        # variables = input_variables_file
    with open(strip_filename, 'w+') as st:
        st.truncate(0)
        st.write('= stripf \n')
        st.write('0000100 strip ' + form + '\n')
        st.write('101  run \n')
        st.write('103  0 \n')
        st.write('*--------------------------------------------------------------------- \n')
        for index, plot in variables.iterrows():
            st.write(str(1001 + index) + ' ')
            for word in plot:
                st.write(str(word) + ' ')
            st.write('\n')
        st.write('. \n')
        st.close()
        print('Your strip file ' + strip_filename + ' has been created')
    return variables
#▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
def remove_blanks(string):
    """remove_blanks: auxiliary function that removes all blanks except one from a header 
                    string in a stripf file

    :USAGE: remove_blanks(string)
    """
    count_ns = 0
    ns=""
    for i in string:
        if(not i.isspace()):
            ns+=i
        else:
            #Just keep the first blank space for clearer labelling
            #For correct labelling, it is assumed that no leading blanks existed anymore
            if count_ns == 0:
                ns+=i
                count_ns+=1
            else:
                count_ns+=1
    return ns
#▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
def correct_labels(case_folder=''):
    """correct_labels performs the following consecutive actions:
            1.- reads the strip file called 'stripf' as extracted from scdap
            2.- corrects the stripf format to be more readable
            3.- stores the corrected data in a pandas.DataFrame

    :case_folder: [str] (optional) folder location of the stripf file

    :returns:
        - a [DataFrame] with the data with name 'case_folder'
    """
    if case_folder != '':
       case_folder = './' + case_folder + '/'

    # It adds one empty column at the end
    bad_labels = pd.read_csv(case_folder + 'stripf', delimiter=',', skipinitialspace=True, header=3)

    # Remove the last empty column, and the first one (with key 'plotalf')
    bad_labels = bad_labels.iloc[:, 1:-1]
    #print(bad_labels.keys())
    #print(bad_labels)
    
    # CORRECT LABELS
    # Remove all blank spaces except for one
    new_labels = []
    for lab in bad_labels.columns:
        new_labels.append(remove_blanks(lab))
    #print(labels)

    #Replace the remaining blank by - to avoid mixing variable names with identifiers
    new_labels = [new_labels[i].replace(" ", "-") for i in range(len(new_labels))]
    #print(labels)
    
    # LOAD DATA WITH CORRECTED LABELS 
    corr_data = pd.read_csv(case_folder + 'stripf', delimiter=',', skipinitialspace=True, header=3)
    #corr_data = pd.read_csv('stripf', delimiter=',', skipinitialspace=True, header=3)
    corr_data = corr_data.iloc[:, 1:-1]
    corr_data.columns = new_labels
    #print(corr_data)
    
    return corr_data
#▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
def read_stripf_df(case_folder='', names=''):

    """read_stripf_df performs the following consecutive actions:
            1.- reads the stripf file. Note that a maximum number of 
                99 strip variable requests can be set
            2.- creates a csv file in 'case_folder' with the data
            3.- stores the data in a DataFrame to be used in python

    :case_folder: [str] (optional) folder location of the stripf file
    :names: list (optional) names to be added to the DataFrame. If you have
            the variables file, you can specify the names column here

    :returns:
        - a [DataFrame] with the data in 'case_folder'
    """
    if case_folder != '':
       case_folder = './' + case_folder + '/'

    if relap_scdap():
        # LOAD DATA OF THE CASE WITH CORRECTED LABELS IN PANDAS
        case = correct_labels(case_folder)
        if names != '':
            case.columns = names
        case.to_csv(case_folder + 'stripf.csv', mode='w', index=False, header=True)
        return case
    else:
        with open(case_folder + 'stripf', 'r+') as st:
             val = [[]]
             lin, lini = 0, 0
             for l in st:
                 if not l == '\n':
                    line = l.split()
                    if (line[0] == 'plotrec' or line[0] == 'plotalf'
                                             or line[0] == 'plotnum'):
                       val.append(line[1:])
                       lini = 1
                       lin = lin + 1
                    else :
                        if lini == 1:
                           for ii in range(len(line)):
                               val[lin].append(line[ii])
             val.pop(0)
        st.close()
        tras = [*zip(*val)]
        try:
            os.remove(case_folder + 'stripf.dat')
        except OSError:
            pass
        with open(case_folder + 'stripf.dat', 'w+') as auxi:
            for i2 in range(len(tras[0])):
                for i1 in range(len(tras)):
                    if i1 < len(tras) - 1:
                        if i2 == 0:
                           auxi.write(str(tras[i1][i2]) + '-' + str(tras[i1][i2+1]) + ',')
                        if i2 > 1:
                           auxi.write(str(tras[i1][i2]) + ',')
                    else :
                        if i2 == 0:
                           auxi.write(str(tras[i1][i2]) + '-' + str(tras[i1][i2+1]))
                        if i2 > 1:
                           auxi.write(str(tras[i1][i2]))
                if i2 != 1:
                    auxi.write('\n')
        auxi.close()
        if names == '':
           case = pd.read_csv(case_folder + 'stripf.dat', sep=',', header=0,
                  usecols=np.arange(0, len(tras)))
        else :
           case = pd.read_csv(case_folder + 'stripf.dat', sep=',',
                   skiprows=1, header=None, index_col=0)
           case.columns = names[1:]
        return case
#▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
def read_stripf(case_folder='', names=''):

    """read_stripf performs the following consecutive actions:
            1.- reads the stripf file. Note that a maximum number of 
                99 strip variable requests can be set
            2.- creates a csv file in 'case_folder' with the data
            3.- stores the data in a narray to be used in python

    :case_folder: [str] (optional) folder location of the stripf file
    :names: list (optional) names to be added to the DataFrame. If you have
            the variables file, you can specify the names column here

    :returns:
        - a [ndarray] containing the data of 'case_folder'
    """
    if case_folder != '':
        case_folder = './' + case_folder + '/'

    if relap_scdap():
        # LOAD DATA OF THE CASE WITH CORRECTED LABELS IN PANDAS
        case = correct_labels(case_folder)
        ##if names != '':
          ##  case.columns = names
        
        # ADAPT DATA OF THE CASE FROM PANDAS TO NUMPY
        case.to_csv(case_folder + 'stripf.csv', mode='w', index=False, header=True)
        ##case = np.genfromtxt(case_folder + 'stripf.csv', delimiter=",", skip_header=0, names=True)
        if names == '':
            case = np.genfromtxt(case_folder + 'stripf.csv', delimiter=",", skip_header=0, names=True)
        else:
            case = np.genfromtxt(case_folder + 'stripf.csv', delimiter=",", skip_header=1, names=names)
        return case
    else:
        with open(case_folder + 'stripf', 'r+') as st:
             val = [[]]
             lin, lini = 0, 0
             for l in st:
                 if not l == '\n':
                    line = l.split()
                    if (line[0] == 'plotrec' or line[0] == 'plotalf'
                        or line[0]=='plotnum'):
                       val.append(line[1:])
                       lini = 1
                       lin = lin + 1
                    else:
                        if lini == 1:
                           for ii in range(len(line)):
                               val[lin].append(line[ii])
             val.pop(0)
        st.close()
        tras = [*zip(*val)]
        try:
            os.remove(case_folder + 'stripf.dat')
        except OSError:
            pass
        with open(case_folder + 'stripf.dat', 'w+') as auxi:
            for i2 in range(len(tras[0])):
                for i1 in range(len(tras)):
                    if i1 < len(tras) - 1:
                        if i2 == 0:
                           auxi.write(str(tras[i1][i2]) + '-' + str(tras[i1][i2+1]) + ',')
                        if i2>1:
                           auxi.write(str(tras[i1][i2]) + ',')
                    else :
                        if i2 == 0:
                           auxi.write(str(tras[i1][i2]) + '-' + str(tras[i1][i2+1]))
                        if i2 > 1:
                           auxi.write(str(tras[i1][i2]))
                if i2 != 1:
                    auxi.write('\n')
        auxi.close()
        if names == '':
           case = np.genfromtxt(case_folder + 'stripf.dat', delimiter=",",
                   usecols=np.arange(0, len(tras)), names=True)
        else :
           case = np.genfromtxt(case_folder + 'stripf.dat', delimiter=",",
                   usecols=np.arange(0, len(tras)), skip_header=1, names=names)
        return case
#▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
def run_strip(strip_file: str, restart: str, case_folder=''):

    """ run_strip performs a strip with the defined strip_file
    if relap/scdap is used, remember to declare rp.set_relap_scdap(True)
    and to copy the scdap license file (e.g. anh0.lic) to the current
    working directory

    :strip_file: [str] strip file
    :restart: [str] case name without extension
    :case_folder: [str] (optional) folder of the case
    :returns: nothing
        - a file stripf is created in the specified case_folder

    """
    if case_folder != '':
       case_folder = './' + case_folder + '/'
    # exe = relapwin_loc + '/' + relap_exe
    exe = path_to_exe()
    if relap_scdap() :
        arg1 = ' -i ' + case_folder + strip_file
        arg2 = ' -o ' + case_folder + 'stripout' + '.o'
        arg3 = ' -r ' + case_folder + restart + '.r'
        arg4 = ''
        print("relap_scdap() is used")
    else:
        arg1 = ' -i ' + strip_file
        arg2 = ' -O ' + case_folder + 'stripout'
        arg3 = ' -r ' + case_folder + restart + '.r'
        arg4 = ' -Z ' + relapwin_loc() + '/tpfh2onew'
    cmd = exe + arg1 + arg2 + arg3 + arg4
    print(cmd)
    try :
        os.remove('stripf')
    except OSError :
        pass
    try :
        os.remove(case_folder + 'stripf')
    except OSError :
        pass
    try :
        os.remove('stripout' + '.o')
    except OSError :
        pass
    try :
        os.remove(case_folder + 'stripout' + '.o')
    except OSError :
        pass
    try :
        os.remove('screen')
    except OSError :
        pass
    with Popen(cmd, stdout=PIPE, shell=True, bufsize=1, universal_newlines=True) as p:
        for line in p.stdout:
            print(line, end='')
    try :
        os.rename('stripf', case_folder + 'stripf')
    except OSError :
        pass
    try :
        os.remove(case_folder + 'stripout')
    except OSError :
        pass
    try :
        os.remove('screen')
    except OSError :
        pass
    # pd.read_csv('fjdklf', f)
    # try :
        # os.remove('stripf')
    # except OSError :
        # pass
#▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
def extract_data(input_variables_file, restart: str, case_folder=''):

    """extract_data performs the following consecutive actions:
            1.- creates a strip file from the input_variables and the paths
                to each case_folder
            2.- runs the strip to load the data for each case

    USAGE:
    cases, variables = extract_data(input_variables_file: str, restart: str,
                                    case_folder = '')

    :input_variables_file: [str] file that lists all the variables to be stripped.
                                 The file name should include the extension
                           [DataFrame] name of the variable that stores the list of
                                 variables to be stripped.
    :restart: [str] the case name without extension
    :case_folder: (optional) [str] name of the case folder or a [list] with cases

    :returns:
        - a [DataFrame] with the read variables
        - an [Ndarray] of Ndarrays for each case
    :files:
        - a file containing the extracted data in the calculation folder: 'stripf'
        - a strip file with the requested filename in the running folder
    """
    """
    1.- creates a strip file from the input_variables and the paths to each
        case_folder
    """
    if relap_scdap():

        case_paths = []
        if type(case_folder) == str:
            case_paths = [case_folder]
        else :
            for i in range(0, len(case_folder)):
                case_paths.append(case_folder[i])

        #variables = make_strip(input_variables_file, 'strip_' + restart + '.i', 'csv')
        variables = []
        for i in range(len(case_paths)):
            variables.append(make_strip(input_variables_file, 
                                        './'+case_paths[i]+'/' + 'strip_' + restart + '.i', 
                                        'csv'))

        #Assuming 'input_variables_file' is the same for all 'case_folder':
        noms_codi = ['time']
        noms_codi.extend(variables[0].loc[:, 'experiment_tag'])
        noms_descrip = ['Time']
        noms_descrip.extend(variables[0].loc[:, 'figure_tag'])
        for i in range(len(noms_descrip)):
            noms_descrip[i] = str(noms_descrip[i]).replace('_', ' ')
        noms_units = ['(s)']
        for index, line in variables[0].iterrows():
            noms_units.append('('+line['unit']+')')

    else:
        variables = make_strip(input_variables_file, 'strip_' + restart + '.i')
        noms_codi = ['time']
        noms_codi.extend(variables.loc[:, 'experiment_tag'])    
        noms_descrip = ['Time']
        noms_descrip.extend(variables.loc[:, 'figure_tag'])
        for i in range(len(noms_descrip)):
            noms_descrip[i] = str(noms_descrip[i]).replace('_', ' ')
        noms_units = ['(s)']
        for index, line in variables.iterrows():
            noms_units.append('('+line['unit']+')')

        case_paths = []
        if type(case_folder) == str:
            case_paths = [case_folder]
        else :
            for i in range(0, len(case_folder)):
                case_paths.append(case_folder[i])
            # if case_paths[i] != '':
                # case_paths[i] = './' + case_folder[i] + '/'
    """
    2.- runs the strip to load the data for each case
    """
    print(case_paths)
    cases = {}
    for item in case_paths:
        run_strip('strip_' + restart + '.i', restart=restart, case_folder=item)
        case = read_stripf(item, noms_codi)
        cases[item] = case
        case_df = pd.DataFrame(case)
        case_df.to_csv('./'+item+'/' + restart + '.dat', float_format='%1.4e',
                       index=False)
        #try:
        #    os.remove('./' + item + '/' + 'stripf.dat')
        #except:
        #    pass
        #try:
        #    os.remove('./' + item + '/' + restart + '.dat')
        #except:
        #    pass
        #os.remove('./' + item + '/' + 'stripf')

    if relap_scdap():
        #The list is converted to pd.DataFrame to ease the use of other functions
        variables = pd.concat(variables, ignore_index=True)
        #print("variables final:\n", variables)
        #print("type(variables):\n", type(variables))
    return cases, variables
#▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
def extract_df(input_variables_file: str, restart: str, case_folder=''):

    """extract_data performs the following consecutive actions:
            1.- creates a strip file from the input_variables and the paths
                to each case_folder
            2.- runs the strip to load the data for each case

    USAGE:
    cases, variables = extract_data(input_variables_file: str, restart: str,
                                    case_folder = '')

    :input_variables_file: [str] the file that lists all the variables
                                 to be stripped
                           [DataFrame] name of the variable that stores the list of
                                 variables
    :restart: [str] the case name without extension
    :case_folder: name of the case folder or a [list] with cases

    :returns:
        - a [DataFrame] with the read variables
        - an [Ndarray] of Ndarrays for each case
    :files:
        - a file containing the extracted data in the calculation folder: 'stripf'
        - a strip file with the requested filename in the running folder
    """
    """
    1.- creates a strip file from the input_variables and the paths to each
        case_folder
    """
    if relap_scdap():
        case_paths = []
        if type(case_folder) == str:
            case_paths = [case_folder]
        else :
            for i in range(0, len(case_folder)):
                case_paths.append(case_folder[i])

        variables = []
        for i in range(len(case_paths)):
            variables.append(make_strip(input_variables_file, 
                                        './'+case_paths[i]+'/' + 'strip_' + restart + '.i', 
                                        'csv'))

        #Assuming 'input_variables_file' is the same for all 'case_folder':
        noms_codi = ['time']
        noms_codi.extend(variables[0].loc[:, 'experiment_tag'])
        noms_descrip = ['Time']
        noms_descrip.extend(variables[0].loc[:, 'figure_tag'])
        for i in range(len(noms_descrip)):
            noms_descrip[i] = str(noms_descrip[i]).replace('_', ' ')
        noms_units = ['(s)']
        for index, line in variables[0].iterrows():
            noms_units.append('('+line['unit']+')')

    else:
        variables = make_strip(input_variables_file,'strip_'+restart+'.i')
        noms_codi = ['time']
        noms_codi.extend(variables.loc[:,'experiment_tag'])
        noms_descrip = ['Time']
        noms_descrip.extend(variables.loc[:,'figure_tag'])
        for i in range(len(noms_descrip)):
            noms_descrip[i] = str(noms_descrip[i]).replace('_',' ')
        noms_units = ['(s)']
        for index, line in variables.iterrows():
            noms_units.append('('+line['unit']+')')
    
        case_paths = []
        if type(case_folder) == str:
            case_paths = [case_folder]
        else :
            for i in range(0,len(case_folder)):
                case_paths.append(case_folder[i])
                # if case_paths[i] != '':
                    # case_paths[i] = './' + case_folder[i] + '/'
    """
    2.- runs the strip to load the data for each case
    """
    print(noms_codi)
    # cases = {}
    cases = []
    for item in case_paths:
        run_strip('strip_' + restart + '.i', restart, item)
        case = read_stripf_df(item, noms_codi)
        # cases[item] = case
        cases.append(case)
    result = pd.concat(cases, keys=case_paths)

    if relap_scdap():
        #variables = pd.concat(variables, ignore_index=True)
        variables = pd.concat(variables, keys=case_paths)

    return result, variables
#▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
def plot_var(variable: str, variables_df, cases_df, case_folder = '',
        dataExp = '', label = ''):

    """ plots one of the variables extracted. It may plot for each of the cases
        specified in case_folder

    :variable: str name of the variable to be plotted
    :variables_df: Dataframe containing the variables and properties
                         of each variable
    :cases_df: Ndarray containing the data cases
    :case_folder: (optional) name of the case folder or a [list] with cases
    :dataExp: (optional) name of the Ndarray containing the experimental data
    :label: str (optional) Label of the y axis

    :returns: if used as
        figure, axes = rp.plot_var(...)
        a figure and axes objects are returned
    :output: TODO

    """
    global exp_file_bool 
    exp_file_bool = False
    if type(dataExp) != str : exp_file_bool = True
    if type(case_folder) == str : case_folder = [case_folder]
    print('making plot for', variable)
    # plt.figure(variable)
    fig, ax = plt.subplots()
    i = variables_df[variables_df['figure_tag'] == variable].index.values[0]
    tag = variables_df['experiment_tag'][i] 
    if exp_file_bool :
        if tag in dataExp.dtype.names :
            ax.plot(dataExp['time'], dataExp[tag],
                     linewidth=0.75,color='k',label='Experimental')
    for j in case_folder :
        ax.plot(cases_df[j]['time'], cases_df[j][tag], linewidth=0.75, label=j)
    # plt.ylabel(variable.replace('_',' ') + ' (' + variables_df['unit'][i] + ')')
    if label == '' : label = relap_labels.get(variables_df['alphanum'][i])
    ax.set(ylabel =label, xlabel ='Time (s)',
        xlim =(float(variables_df['timei'][i]), float(variables_df['timee'][i])),
        title = variable.replace('_',' '))
    if float(variables_df['ymin'][i]) != 0 or float(variables_df['ymax'][i]) != 0:
      ax.set_ylim(variables_df['ymin'][i], variables_df['ymax'][i])
    ax.grid(which='major', linestyle=':', linewidth=1.0,
             alpha=0.8, color='grey')
    ax.legend()
    fig.tight_layout()
    fig.savefig(figures_loc() + variable + '.' + figures_type(),
                format= figures_type(), dpi=300,bbox_inches='tight')
    print("plot has been saved as:", figures_loc() + variable + '.' + figures_type())
    if show_plot() : fig.show()
    return fig, ax 
#▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
def plot_all(variables_df, cases_df, case_folder='', dataExp=''):

    """TODO: Docstring for plot_all.

    :variables_df: dataframe containing the requested variables
    :cases_df: numpy array containing all results
    :case_folder: name of the case folder or a [list] with cases
    :dataExp: (optional) name of the Ndarray containing the experimental data

    :returns: TODO
    :output: TODO

    """
    for item in variables_df['figure_tag'] :
        plot_var(item, variables_df, cases_df, case_folder, dataExp)
#▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
def plot(alpha: str, numeric: str, restart: str, case_folder='', save_fig=''):

    """ plot is used to plot a single relap variable. It can be done for
        one single case or for a list of cases

    :alpha: [str] type of variable to be plotted
    :numeric: [str] numeric part of the variable
    :restart: [str] the restart code name
    :case_folder: [str or list] (optional) case or cases to be plotted
    :save_fig: [str] (optional) write 'pdf' or 'png' if you want to save a fig
    :returns: [ndarray] with the data extracted
        - it plots the specified variable for all specified cases
        - you may save the figure

    NOTE: When using RELAP/SCDAP, if case_folder!='', the restart file must be 
          in the immediate daughter directory
    """
    with open('dummy_strip.i', 'w+') as st:
        st.truncate(0)
        st.write('= stripf \n')
        if relap_scdap():
            st.write('0000100 strip csv \n')
        else:
            st.write('0000100 strip fmtout \n')
        st.write('101  run \n')
        st.write('103  0 \n')
        st.write('*--------------------------------------------------------------------- \n')
        st.write('1001 ' + alpha + ' ' + numeric + '\n')
        st.write('. \n')
    if type(case_folder) == str:
        case_folder = [case_folder]
    # cases = []
    print("case_folder:", case_folder)
    for i in range(0, len(case_folder)):
        print("now plotting for case:", case_folder[i])
        try :
            os.remove('./' + case_folder[i] + '/' + 'stripf')
        except OSError :
            pass
        if relap_scdap():
            if case_folder[i] != '':
                run_strip('../' + 'dummy_strip.i', restart, case_folder[i])
            else:
                run_strip('dummy_strip.i', restart, case_folder[i])
        else:
            run_strip('dummy_strip.i', restart, case_folder[i])
        cas = read_stripf(case_folder[i])
        # cases.append(cas)
        what = alpha + numeric
        plt.plot(cas['time0'],cas[what],linewidth=0.75,label=case_folder[i])
        if alpha in relap_labels:
           plt.ylabel(relap_labels.get(alpha))
        else :
           plt.ylabel('-')
        plt.xlabel('Time (s)')
    plt.legend()
    plt.title(alpha + '-' + numeric)
    plt.tight_layout()
    if save_fig == 'pdf' or save_fig == 'png':
        plt.savefig(figures_loc() + what + '.' + save_fig, format=save_fig,
                    dpi=300,bbox_inches='tight')
        print("plot has been saved as:", figures_loc() + what + '.' + save_fig)
    if show_plot() : plt.show()
    return cas
#▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
def general_fig(variables, dataCalc0, dataExp='' , annotations=[], labels=[]):
    """

    :variables: Dataframe containing all the requested variables and properties
    :dataCalc0: Numpy array containing all results: cases_df['base']
    :annotations: (optional) location of the tags for each line
    :labels: (optional) list of labels for each y_axes

    :USAGE:
           rp.general_fig(variables, cases_df_sbloca['base'])
           your_name, your_axes = rp.general_fig(variables, cases_df_sbloca['base'])
        :with annotations:

           rp.general_fig(variables, cases_df[item], data_test62,
                         [[300., 15030000.0],
                         [7500.0, 8000000.0],
                         [100.0,5500000.0],
                         [23930.06, 1445.9],
                         [18930.06, 6191.244],
                         [920.04699999999, 44.045],
                         [920.04699999999, 38.1251],
                         [1500, 4.045],
                         [1500, 1.9],
                         [300, 8.59974]])
            
            You add a list of pairs of data for each plot. The pairs of values
            are the time and y coordinate (same as the data)

            You can first run the case without the annotations and the default
            values appear on screen, you can use them later to edit

    :returns: A figure with the general evolution of the transient
             - a figure object and axes named 'your_name' and 'your_axes'

    """
    global exp_file_bool 
    initial_time = variables.loc[1,'timei']
    final_time   = variables.loc[1,'timee']
    ticks        = variables.loc[1,'timee']/10
    initial_index = np.where(dataCalc0['time'] >= initial_time)[0][0]
    try : final_index = np.where(dataCalc0['time'] >= final_time)[0][0]
    except : final_index = -1
    exp_file_bool = False
    if type(dataExp) != str : exp_file_bool = True

    f, axes = plt.subplots(3, sharex=True, sharey=False)
    colors = ['k','mediumblue','red','green','tab:orange','tab:purple',
            'tab:brown','tab:pink','tab:olive','tab:cyan', 'tab:grey']
    label = 'UPC'
    label_exp = 'Experimental'
    l_style = '-'
    tags = ['top_left', 'mid_left', 'bottom_left']
    tags_right = ['top_right', 'mid_right', 'bottom_right']
    ll = 0
    prop_box = dict(boxstyle="round", color = 'w', alpha=0.5)

    print('annotation location coordinates are the following')
    for i in range(0,3):
        l = 0
        axes[i].grid( linestyle = '-', linewidth = 0.5)
        plotted = variables[variables['general'] == tags[i]].reset_index()
        try :
            axes[i].set_ylabel(labels[i])
        except :
            axes[i].set_ylabel(relap_labels.get(plotted['alphanum'][0]))
        for k, plot in plotted.iterrows():
            align = 'left'
            time_coord = (dataCalc0['time'][initial_index
                    + np.argmax(dataCalc0[plot[4]][initial_index:final_index])])
            time_var = max(dataCalc0[plot[4]][initial_index:final_index])
            if time_coord <= initial_time or time_coord >= final_time :
                time_coord = 0.0
                time_var = dataCalc0[plot[4]][initial_index]
            if time_coord > (final_time - initial_time) / 2 : align = 'right'
            if not annotations:
                anot = [time_coord, time_var]
            else :
                anot = annotations[ll]
            print(anot)
            if exp_file_bool :
               l_style = ':'
               if plot[4] in dataExp.dtype.names :
                  axes[i].plot(dataExp['time'],dataExp[plot[4]], linewidth=1,
                          color=colors[l], alpha=1.0, linestyle='-',
                          label=label_exp)
                  label_exp = '_nolegend_'
            axes[i].plot(dataCalc0['time'],dataCalc0[plot[4]], linewidth=1,
                    color=colors[l], alpha=1.0, linestyle= l_style,label=label)
            axes[i].annotate(plot[5].replace('_',' '), xy = anot,
                    xycoords='data', color=colors[l],horizontalalignment=align,
                    bbox= prop_box, verticalalignment='bottom' )
            label = '_nolegend_'
            ll += 1
            l += 1
        plotted = variables[variables['general'] == tags_right[i]].reset_index()
        for k, plot in plotted.iterrows():
            align = 'left'
            time_coord = (dataCalc0['time'][initial_index +
                      np.argmax(dataCalc0[plot[4]][initial_index:final_index])])
            time_var = max(dataCalc0[plot[4]][initial_index:final_index])
            if time_coord > (final_time - initial_time) / 2 : align = 'right'
            if not annotations:
                anot = [time_coord, time_var]
            else :
                anot = annotations[ll]
            print(anot)
            if k == 0 : ax2=axes[i].twinx()
            if exp_file_bool :
               l_style = ':'
               if plot[4] in dataExp.dtype.names :
                  ax2.plot(dataExp['time'], dataExp[plot[4]], linewidth=1,
                          color=colors[l], alpha=1.0, linestyle='-',
                          label=label_exp)
                  label_exp = '_nolegend_'
            ax2.plot(dataCalc0['time'], dataCalc0[plot[4]], linewidth=1,
                    color=colors[l], alpha=1.0, linestyle= l_style,label=label)
            ax2.annotate(plot[5].replace('_', ' '), xy=anot, xycoords='data',
                    color=colors[l], horizontalalignment=align, bbox=prop_box,
                    verticalalignment='bottom' )
            l += 1
            ll += 1
            try :
                ax2.set_ylabel(labels[i+3])
            except :
                ax2.set_ylabel(relap_labels.get(plotted['alphanum'][0]))
    axes[0].legend(bbox_to_anchor=(0.6, 1.0, 0.4, 0.1), loc='lower left',
            frameon=False, ncol=2, mode="expand")
    axes[2].set_xlabel('Time(s)')
    axes[0].tick_params(axis="x", direction="in")
    axes[1].tick_params(axis="x", direction="in")
    axes[2].tick_params(axis="x", direction="inout")
    axes[2].set_xlim(initial_time,final_time)
    axes[2].set_xticks(np.arange(0, final_time + ticks / 2, ticks))
    f.subplots_adjust(hspace=0)
    f.set_size_inches(10, 12)
    f.savefig(figures_loc() + 'general.' + figures_type(), format=figures_type(), dpi=300)
    print("plot has been saved as:", figures_loc() + 'general.' + figures_type())
    if show_plot() : plt.show()
    return f, axes


def plot_variables(variable: list, variables_df, cases_df):

    """ plots various variables in the same plot. Only one Yaxes so must have
        the same units.

    :variable: list containing the variables to be plotted
    :variables_df: Dataframe containing the variables and properties
                         of each variable
    :cases_df: Ndarray containing the data for the particular case:
               cases_df['base']

    :USAGE:
    rp.plot_variables(['SGTR_MF', 'REL_VLV_MF'], variables, cases_df['base'])

    :returns: TODO
    :output: a plot with the two variables listed

    """
    print('making plot for', variable[0] + '_' + variable[-1])
    plt.figure(variable[0] + '_' + variable[-1])
    for var in variable :
        i = variables_df[variables_df['experiment_tag'] == var].index.values[0]
        plt.plot(cases_df['time'], cases_df[variables_df['experiment_tag'][i]],
                 linewidth=0.75, label=var)
    plt.ylabel(relap_labels.get(variables_df['alphanum'][i]))
    plt.xlabel('Time (s)')
    plt.xlim(float(variables_df['timei'][i]), float(variables_df['timee'][i]))
    if float(variables_df['ymin'][i]) !=0 or float(variables_df['ymax'][i]) !=0:
       plt.ylim(variables_df['ymin'][i], variables_df['ymax'][i])
    plt.grid(visible=True, which='major', linestyle=':', linewidth=1.0, alpha=0.8,
             color='grey')
    plt.legend()
    plt.tight_layout()
    plt.savefig(figures_loc() + variable[0] +'_'+ variable[-1] +'.'+ figures_type(),
            format= figures_type(), dpi=300, bbox_inches='tight')
    print("plot has been saved as:", 
        figures_loc() + variable[0] +'_'+ variable[-1] +'.'+ figures_type())
    if show_plot() : plt.show()


def append_variable(dataframe, experiment_tag: str, unit: str,
                    general='no', figure_tag=''):
    """ Append a variable to the variables dataframe.

    :dataframe: dataframe where to add the line
    :experiment_tag:
    :unit:
    :general: (optional) change column 'general' if you wish
    :figure_tag: (optional) same as experiment_tag if not entered
    :returns: the dataframe with the added row

    :USAGE:
    variables = append_variable(variables, 'Maximum_PCT', 'K', 'top_right')
    """
    if figure_tag == '' : figure_tag = experiment_tag
    new_line = dataframe.loc[[0]]
    new_line.loc[0, 'experiment_tag'] = experiment_tag
    new_line.loc[0, 'figure_tag'] = figure_tag
    new_line.loc[0, 'unit'] = unit
    new_line.loc[0, 'general'] = general
    dataframe = pd.concat([dataframe, new_line], ignore_index=True)
    return dataframe

def read_exp(expdata_loc: str):
    """TODO: Docstring for read_exp.

    :expdata_loc: the file path to the experimental data
    :returns: Ndarray with the experimental data
    :USAGE:
        your_exp_data = read_exp('your_path.txt')

    """
    global exp_file_bool 
    try : 
        dataExp=np.genfromtxt(expdata_loc, dtype=float, delimiter='\t',
                names=True)
        exp_file_bool = True
    except :
        print('WARNING! Experimental data not used')
        dataExp = np.zeros(shape=(10, 10))
        exp_file_bool = False
    return dataExp
def print_ss(case, exp='', llista= False, end_ss = 0, length = 60):
    """ Prints a table for steady state values
    TODO: 
    - Print the result in a text file

    :case: [ndarray] or [DataFrame] specific case for which you want to make the table
    :exp: (optional) If '', no experimental data is to be printed
          otherwise, provide the name of the variable containing the experimental data
          
    :llista: (optional) list of variables to add to the table. Default is False and 
             all variables are shown
    :end_ss: (optional) end time of the steady state
    :length: Number of time steps to be averaged as steady state value
    :returns: prints on screen the table of steady state

    """
    if not llista:
        try:
            llista = case.dtype.names
            pd_df = False
        except AttributeError:
            llista = case.columns
            pd_df = True
    def avg_ss(cas, var):
        """ Makes the average of the variable for the specified length
        :var: name of the variable 
        """
        if relap_scdap():
            i = 0
            if pd_df:
                while cas['time-0'][i] < (end_ss - length):
                     index_start = i
                     i += 1
                while cas['time-0'][i] < end_ss:
                    index_end = i
                    i += 1
                return sum(cas[var][index_start:index_end]) / (index_end - index_start)
            else:
                while cas['time0'][i] < (end_ss - length):
                     index_start = i
                     i += 1
                while cas['time0'][i] < end_ss:
                    index_end = i
                    i += 1
                return sum(cas[var][index_start:index_end]) / (index_end - index_start)   
        else:
            i = 0
            while cas['time'][i] < (end_ss - length):
                 index_start = i
                 i += 1
            while cas['time'][i] < end_ss:
                index_end = i
                i += 1
            return sum(cas[var][index_start:index_end]) / (index_end - index_start)
    dash = '-' * 50
    print(dash)
    if exp != '':
       print('{:<20s}{:>8s}{:>18s}'.format('variable', 'calc', 'experiment'))
    else :
       print('{:<20s}{:>8s}'.format('variable', 'calc'))
    print(dash)
    if exp != '':
        for var in llista: 
            if var in exp.dtype.names :
               print('{:<20s}{:>8E}{:>18E}'.format(var, avg_ss(case, var), avg_ss(exp, var)))
            else :
               print('{:<20s}{:>8E}{:>18s}'.format(var, avg_ss(case, var), '-'))
    else :
        for var in llista: 
            print('{:<20s}{:>8E}'.format(var, avg_ss(case, var)))
    print(dash)


def mypie(data: list, labels: list, title='',unit: str='%'):
    """TODO: Docstring for mypie.
    :data: a list or array with the data to plot
    :labels: a list or array with the labels
    :title: title of the pie
    :unit: the unit of the variables
    :returns: a pie plot
    """
    # colors = ['#E6E6FA', '#D8BFD8', '#DDA0DD', '#EE82EE', '#DA70D6', '#FF00FF',
        # '#FF00FF', '#BA55D3', '#9370DB', '#8A2BE2', '#9400D3', '#9932CC',
        # '#8B008B', '#800080', '#4B0082']
    colors = ['#FCD8F9', '#F8B1F1', '#F273E7', '#EE44DE', '#EB25D8', '#DA14C7',
         '#A40F96', '#7C0C72']
    
    fig, ax = plt.subplots(figsize=(10, 5), subplot_kw=dict(aspect="equal"))
    perc = [str(round(e / s * 100., 1)) + '%' for s in (sum(data),) for e in data]
    wedges, texts = ax.pie(data, colors=colors, wedgeprops=dict(width=0.5), startangle=-40)
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(arrowprops=dict(arrowstyle="-"),
              #bbox=bbox_props,
              zorder=0, va="center")
    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format(ang)
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax.annotate(labels[i] + ' ' + perc[i], xy=(x, y), xytext=(1.2*np.sign(x), 1.2*y),
                horizontalalignment=horizontalalignment, fontsize=12, **kw)
    centre_circle = plt.Circle((0,0),0.40,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    total = sum(data)
    ax.annotate('Total\n{t:.0f}\n{u}'.format(t=total, u=unit), [0,0],
            xycoords='data', va='center', ha='center', fontsize=16)
    plt.title(title, fontsize=16)
    plt.tight_layout() 
    plt.savefig(figures_loc() + title.replace(' ','_')+'.'+figures_type(),
            format=figures_type(), dpi=300, bbox_inches='tight')
    plt.close('all')
    return fig, ax


