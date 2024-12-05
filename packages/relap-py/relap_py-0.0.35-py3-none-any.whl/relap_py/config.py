"""
Title: Configuration options
Date: 30/10/2024 
Created by: Jordi Freixa
Description: 
"""
import os


def_path_to_exe = os.getenv('RELAP_EXE_PATH')
if def_path_to_exe is None:
    raise ValueError("Path to the RELAP executable is not set. Set the environment variable RELAP_EXE_PATH.")

def_relapwin_loc = os.path.dirname(def_path_to_exe)

def path_to_exe():
    return def_path_to_exe
def relapwin_loc():
    return def_relapwin_loc

def set_path_to_exe(new: str):
    global def_path_to_exe
    def_path_to_exe = new
def set_relapwin_loc(new: str):
    global def_relapwin_loc
    def_relapwin_loc = new

"""
Defaults
    :figures_type: (otional) figures format: pdf or png
    :figures_loc: (optional) location where the figures will be saved
    :show_plot: (optional) show interactive python plot window?
    :exp_file_bool: (optional) is there a experimental file?
    :unc_bands: (optional) is there a uncertainty file?
"""
def_figures_type = 'png'
def_figures_loc = './'
def_show_plot = False
def_unc_bands = False
def_relap_scdap = False
"""
Getter and setter functions so the user can change the defaults on the go

Getter
"""

def figures_type():
    return def_figures_type
def figures_loc():
    return def_figures_loc
def show_plot():
    return def_show_plot
def unc_bands():
    return def_unc_bands
def relap_scdap():
    return def_relap_scdap

"""
Setter
"""
def set_figures_type(new: str):
    global def_figures_type
    def_figures_type = new
def set_figures_loc(new: str):
    global def_figures_loc
    def_figures_loc = new
    try :
        os.mkdir(new)
    except OSError :
        print(30*'-'+'WARNING'+30*'-')
        print('          directory ' + new + ' already present')
        print(67*'-')
def set_show_plot(new: bool):
    global def_show_plot
    def_show_plot = new
def set_unc_bands(new: str):
    global def_unc_bands
    def_unc_bands = new
def set_relap_scdap(new: str):
    global def_relap_scdap
    def_relap_scdap = new


