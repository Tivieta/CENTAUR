#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2018 Julius Susanto. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""
CENTAUR: Hybrid Power System Simulation

Global Objects and Variables

Author: Julius Susanto
Last edited: January 2018
"""

import numpy as np
import simplejson as json
import sys

def init():
    """Initialise project with set of default parameters"""
    
    global latitude
    global longitude
    global sys_data
    global pv_resource
    global pv_data
    global loads
    global load_sigma
    global gen_data
    global batt_data
    global batt_char
    
    latitude = -5.945556
    longitude = 105.488494
    
    sys_data = {
        'sys_config'    : 3,                  # System configuration (0=Gen, 1=PV-Gen, 2=PV-batt, 3=PV-batt-gen)
        'ctrl_mode'     : 2,                  # PV-battery-gen control mode (0,1,2,3,4)
        'proj_title'    : 'Default project',
        'proj_desc'     : 'Default project'
    }
    
    pv_resource = np.array([[0.448, 25.59],
                        [0.447, 25.65],
                        [0.471, 25.84],
                        [0.484, 26.09],
                        [0.499, 26.18],
                        [0.501, 25.99],
                        [0.501, 25.86],
                        [0.510, 26.08],
                        [0.509, 26.22],
                        [0.478, 26.15],
                        [0.453, 25.81],
                        [0.443, 25.66]])
    
    pv_data = {
        'k_e'    : 0.90,                # Environmental factor for solar module output, e.g. dirt, dust, etc
        'P_inv'  : 150000,              # PV system inverter output (Wac)
        'k_m'    : 0.95,                # Manufacturer tolerance factor
        'P_stc'  : 175000,              # PV system output at STC (Wp)
        'gamma'  : 0.0038,              # Power temperature coefficient (pu per deg C)
        'eff_pv' : 0.95,                # Efficiency of PV inverter (AC coupled) or charge controller (DC coupled) in pu
        'pv_cpl' : 'DC',                # PV coupling - AC or DC
        'tilt'   : 10.0,                # Tilt angle
        'azimuth' : 180.0,              # Azimuth angle
        'albedo' : 0.2                  # Albedo / ground reflectance
        }
    
    loads = np.array([[43.9, 43.9],   # 00:00
                    [40.8, 40.8],     # 01:00
                    [40.9, 40.9],     # 02:00
                    [40.4, 40.4],     # 03:00
                    [40.2, 40.2],     # 04:00
                    [43.9, 43.9],     # 05:00
                    [45.2, 43.2],     # 06:00
                    [35.2, 35.2],     # 07:00
                    [34.0, 34.0],     # 08:00
                    [32.1, 32.1],     # 09:00
                    [31.1, 31.1],     # 10:00
                    [31.3, 31.3],     # 11:00
                    [30.9, 30.9],     # 12:00
                    [33.1, 33.1],     # 13:00
                    [32.1, 32.1],     # 14:00
                    [32.2, 32.2],     # 15:00
                    [32.2, 32.2],     # 16:00
                    [34.5, 34.5],     # 17:00
                    [56.8, 56.8],     # 18:00
                    [58.5, 58.5],     # 19:00
                    [59.3, 59.3],     # 20:00
                    [55.8, 55.8],     # 21:00
                    [51.9, 51.9],     # 22:00
                    [48.4, 48.4]])    # 23:00
    
    load_sigma = [0.1,0.1]
    
    batt_char = np.array([[1, 600.0],
                        [3, 260.0],
                        [5, 180.0],
                        [8, 120.0],
                        [10, 100.2]])
    
    batt_data = {
        'n_batt'     : 2,                                      # Number of batteries
        'C_nom'      : 1000,                                   # Nominal capacity (Ah)
        'v_dc'       : 400,                                    # Nominal system dc voltage (V)
        'SOC_min'    : 30,                                     # Minimum state of charge (battery "empty")
        'SOC_0'      : 100,                                    # Initial state of charge
        'SOC_cyc'    : 80,                                     # State of charge setpoint for cycle charging
        'eff_conv'   : 0.94,                                   # Battery converter / inverter   efficiency
        'p_set'      : 80000,                                  # PV output setpoint for ramp control mode at AC load side (in W)
        't_set'      : [9,15]                                  # Time start/end for ramp control mode (hour of day)
    }

    gen_data = {
        'n_gen'     : 1,                   # Number of parallel generators
        'P_gen'     : 60,                  # Generator capacity (kW)
        'l_min'     : 0.4,                 # Minimum generator loading (pu)
        'e_f'       : 0.27,                # Fuel efficiency (litres/kWh)
        'chg_eff'   : 0.95,                # Generator AC/DC charger efficiency (for DC coupled only)
        'c_f'       : 0.65                 # Fuel cost (USD/kWh)   
    }
    
    global filename   
    filename = ""    
    

def write_project_to_file(fname, data = False, readable = True):
    """Write project settings and data to file.  Uses simplejson library.
    
    File is stored in human readable(ish) format.  We can make this compact by removing whitespace from
    indent and separators.  This is an option in case we start getting huge file sizes.
    
    :param fname: String of file (name and path) to write to.
    :type fname: String
    :param data: Optional argument.  Dictionary of data to write to file.  If not supplied the function will read from globals.
    :param type: Dictionary
    :param readable: Optional argument.  True if output should be formatted to be more easily readable.
    :type readable: Boolean
    :returns: True if the write was successful."""    
    global filename
        
    if not data:    
        data = dict()    
        
        data['latitude'] = latitude
        data['longitude'] = longitude
        data['sys_data'] = sys_data
        data['pv_resource'] = pv_resource
        data['pv_data'] = pv_data
        data['loads'] = loads
        data['load_sigma'] = load_sigma
        data['gen_data'] = gen_data
        data['batt_data'] = batt_data
        data['batt_char'] = batt_char
        
    try:
        fp = open(fname, mode = 'w')
        if readable:
            json.dump(data, fp, cls=NumpyJSONEncoder, indent = "  ", separators=(',', ': '), sort_keys = True)
        else:
            json.dump(data, fp, cls=NumpyJSONEncoder, indent = 2, separators=(',',':'))
        fp.close()
        filename = fname
    except:
        return False
    return True
    

def load_project_from_file(fname, populate = True):
    """Load project settings and data from file.  Uses simplejson library.
    Global variables will be populated from data in file unless otherwise directed.
    
    Checks that input data is numerical however does not ensure it is within standard boundaries.
    
    :param fname: String of file (name and path) to read from.
    :type fname: String
    :param populate: Boolean indicating if read data should be populated into global variables.
    :type populate: Boolean
    :returns: Dictionary of data if read was successful, otherwise returns False.
    """
    global latitude
    global longitude
    global sys_data
    global pv_resource
    global pv_data
    global loads
    global load_sigma
    global gen_data
    global batt_data
    global batt_char
    global filename
    
    try:
        fp = open(fname, mode = 'r')
        data = json.load(fp, object_hook = NumpyJSONDecoder)
        fp.close    
        filename = fname
        if populate:
            latitude = data['latitude']
            longitude = data['longitude']
            sys_data = data['sys_data']
            pv_resource = data['pv_resource']
            pv_data = data['pv_data']
            loads = data['loads']
            load_sigma = data['load_sigma']
            gen_data = data['gen_data']
            batt_data = data['batt_data']
            batt_char = data['batt_char']
            
    except:
        print(sys.exc_info()[0], sys.exc_info()[1])
        return False
    return data
    

class NumpyJSONEncoder(json.JSONEncoder):
    """JSON encoder to support encoding of Numpy arrays and complex numbers."""
    def default(self, obj):
        """Default is called by JSONEncoder for serialisation of data.
           Passes back to core default method if not Numpy data."""
        if isinstance(obj, np.complex):
            return dict(__npcomplex__=True, real=obj.real, imag=obj.imag)            
        if isinstance(obj, np.ndarray):
            return dict(__nparray__=True, data=obj.tolist())
        return json.JSONEncoder.default(self, obj)

def NumpyJSONDecoder(dct):
    """Decoder function to support Numpy data encoded by NumpyJSONEncoder."""
    if '__npcomplex__' in dct:
        return np.complex(dct['real'], dct['imag'])
    if '__nparray__' in dct:
        return np.array(dct['data'])
    return dct
