#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2018 Julius Susanto. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""
Chronological Simulation Engine for Hybrid Power Systems

Author: Julius Susanto
Last edited: January 2018
"""

import numpy as np
import matplotlib.pyplot as plt

import engine.kinetic_battery as kb
import engine.synth_solar as synth_solar
import engine.load_model as load_model

def run_sim(sys_dict, pv_dict, batt_dict, gen_dict, load_dict):
    """
    Runs a chronological hybrid power system simulation 
    
    Inputs: 
        sys_dict    Dictionary of system design parameters
        pv_dict     Dictionary of solar PV input parameters
        batt_dict   Dictionary of battery input parameters
        gen_dict    Dictionary of generator input parameters
        load_dict   Dictionary of load input parameters
    
    Outputs:
        sim_out     Dictionary of simulation result outputs
    """
    
    # Initialise simulation output dictionary
    sim_out = {
        'topo'          : '',           # Hybrid system topology
        'P_ld'          : [],           # Load demand (hourly in W)
        'G0'            : [],           # GHI (hourly in kWh/m2)
        'P_pv'          : [],           # PV array output (hourly in W)
        'q'             : [],           # Battery SoC (hourly in %)
        'P_gen'         : [],           # Generator output (hourly in W)
        'P_gen_exc'     : [],           # Excess generator output (hourly in W)
        'P_uns'         : [],           # Power unsupplied / outage (hourly in W)
        'P_pv_exc'      : []            # Excess solar energy (hourly in W)
    }
    
    ########################################
    # Input parameters and data generation #
    ########################################
    
    # Unpack system design data dictionary
    is_pv = sys_dict['is_pv']
    is_batt = sys_dict['is_batt']
    is_gen = sys_dict['is_gen']
    ctrl_mode = sys_dict['ctrl_mode'] + 1
    lat = sys_dict['lat']
    
    # Unpack load data dictionary
    l_sum = load_dict['l_sum']
    l_win = load_dict['l_win']
    sigma_s = load_dict['sigma_s']
    sigma_w = load_dict['sigma_w']
    
    # Generate hourly load data (in W) for one year
    if lat < 0:
        hemi = 'South'
    else:
        hemi = 'North'
    P_ld = load_model.create_loads(l_sum, l_win, sigma_s, sigma_w, hemi) * 1000
    sim_out['P_ld'] = P_ld
    
    if is_pv:
        # Unpack PV system data dictionary
        Ktm = pv_dict['Ktm']
        T_amb = pv_dict['T_amb']
        k_e = pv_dict['k_e']
        k_m = pv_dict['k_m']
        P_stc = pv_dict['P_stc']
        P_inv = pv_dict['P_inv']
        gamma = pv_dict['gamma']
        eff_pv = pv_dict['eff_pv']
        pv_cpl = pv_dict['pv_cpl']
        tilt = pv_dict['tilt']
        azimuth = pv_dict['azimuth']
        albedo = pv_dict['albedo']
        
        # Generate hourly data for solar radiation and clearness indices for one year
        G0, Kt = synth_solar.Aguiar_hourly_G0(Ktm, lat)
        GT = synth_solar.incident_HDKR(G0, Kt, lat, tilt, azimuth, albedo)
        
        # PV module temperature derating for whole year
        # Effective cell temperature: temp_eff = temp_ambient + temp_STC (25 deg)
        # Temperature derating = 1 - gamma * (temp_eff - temp_STC) = 1 - gamma * temp_ambient
        k_t = []
        days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        for i in range(12):
            k_ti = np.ones(days[i] * 24) - np.multiply(np.ones(days[i] * 24), gamma * T_amb[i])
            k_t.extend(k_ti)

        # PV array output for every hour of the year
        P_d = np.multiply(np.array(k_t), P_stc * k_e * k_m / 1000)
        P_pv = np.multiply(np.array(GT), P_d) * eff_pv          # PV output (including inverter/SCC efficiency)
        # Limit PV output to inverter rating for AC coupled systems
        if pv_cpl == 'AC':
            P_pv = np.clip(P_pv, None, P_inv)
        
        sim_out['G0'] = G0
        sim_out['GT'] = GT
        sim_out['P_pv'] = P_pv
        
    if is_gen:
        # Unpack generator data dictionary
        n_gen = gen_dict['n_gen']
        P_gen_rtd = gen_dict['P_gen']
        l_min = gen_dict['l_min']
        e_f = gen_dict['e_f']
        chg_eff = gen_dict['chg_eff']
        c_f = gen_dict['c_f']
        Pg_tot = n_gen * P_gen_rtd * 1000           # Maximum generator capacity (in W)
        Pg_min = n_gen * l_min * P_gen_rtd * 1000   # Minimum generator loading (in W)
    
    if is_batt:
        # Unpack battery system data dictionary
        n_batt = batt_dict['n_batt']
        v_n = batt_dict['v_dc']
        I = batt_dict['I']
        T = batt_dict['T']
        SOC_min = batt_dict['SOC_min']
        SOC_cyc = batt_dict['SOC_cyc']
        SOC_0 = batt_dict['SOC_0']
        eff_conv = batt_dict['eff_conv']
        p_set = batt_dict['p_set']
        t_set = batt_dict['t_set']

        # Estimate battery constants
        x0 = [0.6, 0.4, 650]        
        [x, conv, batt_iter, err] = kb.estimate_constants(x0, np.array(I)*n_batt, T, 1, 20)
        if err < 999:
            k = x[0]        # Rate constant 
            c = x[1]        # Capacity ratio 
            qmax = x[2]     # Maximimum Ah capacity
        else:
            raise SystemExit  
        
        # Set battery initial conditions
        q0 = qmax               # Total initial charge (assumed to be qmax)
        q1_0 = qmax * c         # Available initial charge
        q2_0 = qmax * (1-c)     # Bound initial charge
        sim_out['q'] = [SOC_0]  # Initial state of charge (%)
        
    ################################
    # Run chronological simulation #
    ################################
    
    ###########################
    # Generator only topology #
    ###########################
    if is_gen and not is_pv and not is_batt:    
        sim_out['topo'] = (0, 'Generator only')
        sim_out['P_gen'] = np.clip(P_ld, None, Pg_tot)
        sim_out['P_uns'] = np.clip(np.array(P_ld) - Pg_tot * np.ones(8760), 0, None)
        sim_out['P_gen_exc'] = np.clip(Pg_min * np.ones(8760) - np.array(P_ld), 0, None)
    
    #########################
    # PV-Generator topology #
    #########################
    elif is_gen and is_pv and not is_batt:
        sim_out['topo'] = (1, 'Solar PV-Generator')
        
        # Loop through each hour of the year
        for i in range(8760):
            # PV output power taking into account PV inverter efficiency
            P_pv_out = P_pv[i]
            
            # Check if generator operates above minimum load
            if (P_pv_out + Pg_min) > P_ld[i]:
                # Low load conditions
                sim_out['P_uns'].append(0)
                
                if P_pv_out > 0 and Pg_min < P_ld[i]:
                    # Partial PV output curtailed / dumped
                    sim_out['P_pv_exc'].append(P_pv_out + Pg_min - P_ld[i])
                    sim_out['P_gen_exc'].append(0)
                    sim_out['P_gen'].append(Pg_min)
                else:
                    sim_out['P_gen_exc'].append(Pg_min - P_ld[i])
                    sim_out['P_gen'].append(P_ld[i])
                    
                    if P_pv_out > 0 and Pg_min > P_ld[i]:
                        # All PV output curtailed / dumped
                        sim_out['P_pv_exc'].append(P_pv_out)
                    else:
                        # No PV production
                        sim_out['P_pv_exc'].append(0)
            else:
                # Load is above minimum generator loading
                sim_out['P_pv_exc'].append(0)
                sim_out['P_gen_exc'].append(0)
                if (Pg_tot + P_pv_out) < P_ld[i]:
                    # Generator under-capacity / overloaded
                    sim_out['P_gen'].append(Pg_tot)
                    sim_out['P_uns'].append(P_ld[i] - Pg_tot - P_pv_out)
                else:
                    # Normal operation
                    sim_out['P_gen'].append(P_ld[i] - P_pv_out)
                    sim_out['P_uns'].append(0)
        
    #######################
    # PV-Battery topology #
    #######################
    elif not is_gen and is_pv and is_batt:
        sim_out['topo'] = (2, 'Solar PV-Battery')

        # Calculate net battery current for each hour of the year (i_b)
        # Positive current denotes battery discharge
        if pv_cpl == 'DC':
            # DC coupled PV
            i_l = np.divide(P_ld, (v_n * eff_conv))     # Load current at DC side taking into account converter efficiency
            i_s = np.divide(P_pv, v_n)                  # Solar PV output current at output of charge controller
            i_b = np.array(i_l - i_s)                   # Net battery current
        else:
            # AC coupled PV
            i_b = np.divide(P_ld - P_pv, v_n)           # Load current less solar PV output (taking into account PV inverter efficiency)
        
        # Loop through each hour of the year
        for i in i_b:
            # Adjust battery current for AC coupled PV depending on direction of current through battery converter (efficiency losses)
            if pv_cpl == 'AC' and i < 0:
                # Battery charging
                i = i * eff_conv
            else:
                # Battery discharging
                i = i / eff_conv
            
            # Check if battery is under minimum SOC and net battery current > 0 (i.e. discharging)
            if (SOC_0 < SOC_min) and (i > 0):
                # Calculate energy unsupplied
                e_g = i * v_n
                sim_out['P_uns'].append(e_g)
                sim_out['q'].append(SOC_0)      # State of charge (%)
                sim_out['P_pv_exc'].append(0)   # Excess solar power (W)
            else:
                # Battery can be charged or discharged       
                # Calculate battery state of charge
                q1, q2, i_w = kb.capacity_step(q1_0, q2_0, k, c, qmax, i, 1)
                q0 = q1 + q2
                q1_0 = q1
                q2_0 = q2
                
                # Calculate solar energy wasted if max charging current is reached
                if i_w > 0:
                    e_s = i_w * v_n
                    sim_out['P_pv_exc'].append(e_s)
                else:
                    sim_out['P_pv_exc'].append(0)
                
                SOC_0 = q0/qmax*100
                sim_out['q'].append(SOC_0)   # State of charge (%)
                sim_out['P_uns'].append(0)   # Power unsupplied (W)
                
    #################################
    # PV-Battery-Generator topology #
    #################################
    elif is_gen and is_pv and is_batt:
        #######################################################################
        # Available control modes:                                            #
        #  1) Battery grid former, genset backup (DC coupled, cycle charging) #
        #  2) Mixed master, genset cycle charging (AC coupled)                #
        #  3) Mixed master, genset load following (AC coupled)                #
        #  4) Genset grid former, battery ramp control                        #
        #  TODO 5) Genset grid former, battery PV charge and cycle discharge       #
        #######################################################################
        sim_out['topo'] = (3, 'Solar PV-Battery-Generator')
        
        # Battery dominant control modes (1,2,3)
        if ctrl_mode in [1,2,3]:
            # Loop through each hour of the year
            cyc_charge = False          # Flag for cycle charging mode
            for i in range(8760):               
                # Calculate net battery current
                # Positive current denotes battery discharge
                if pv_cpl == 'DC':
                    # DC coupled PV
                    i_l = P_ld[i] / (v_n * eff_conv)                # Load current at DC side
                    i_s = P_pv[i] / v_n                    # Solar PV output current at output of charge controller
                    i_b = i_l - i_s                                 # Net battery current
                else:
                    # AC coupled PV
                    i_l = (P_ld[i] - P_pv[i]) / v_n        # Net load current at AC side
                    if i_l < 0:
                        # Battery charging
                        i_b = i_l * eff_conv
                    else:
                        # Battery discharging
                        i_b = i_l / eff_conv
                
                # Check if battery is under minimum SOC or it is in cycle charging mode
                if (SOC_0 < SOC_min) or cyc_charge:
                    # Check if there is enough PV to supply the load
                    if i_b > 0:
                        # Inadequate PV to supply the load
                        # Calculate energy required to be supplied by the generator 
                        if ctrl_mode == 1:
                            # DC coupled genset (Control mode 1): adjust for AC/DC charger loss
                            e_g = i_b * v_n / chg_eff
                        else:
                            # AC coupled genset (Control mode 2 or 3): adjust for bidirectional converter losses
                            e_g = i_b * v_n / eff_conv
                        
                        # Check if generator capacity is sufficient
                        if e_g > Pg_tot:
                            # Generator overloaded
                            sim_out['P_uns'].append(e_g - Pg_tot)
                            sim_out['P_gen'].append(Pg_tot)
                            i_b = 0
                        elif ctrl_mode == 3:
                            # Generator load-following mode (Control mode 3)
                            if e_g < Pg_min:
                                # Low load operation (battery charging with excess generator power)
                                sim_out['P_gen'].append(Pg_min)
                                i_b = -(Pg_min - e_g) * eff_conv / v_n 
                            else:
                                # Normal operation
                                sim_out['P_gen'].append(e_g)
                                i_b = 0
                        else:                
                            # Generator has excess capacity to supply battery
                            sim_out['P_uns'].append(0)
                            sim_out['P_gen'].append(Pg_tot)
                            
                            # Calculate excess generator current for battery charging
                            if ctrl_mode == 1:
                                # DC coupled gen (Control mode 1): adjust for AC/DC charger loss
                                i_b = -(Pg_tot - e_g) * chg_eff / v_n
                            else:
                                # AC coupled gen (Control mode 2): adjust for bidirectional converter losses
                                i_b = -(Pg_tot - e_g) * eff_conv / v_n                              
                            
                    else:
                        # Adequate PV to supply the load (and excess PV goes to battery)
                        sim_out['P_uns'].append(0)
                        sim_out['P_gen'].append(Pg_tot)
                        
                        # Calculate total battery charge current (with generator also online)
                        i_b = i_b - Pg_tot * chg_eff / v_n
                    
                    # Calculate battery state of charge
                    q1, q2, i_w = kb.capacity_step(q1_0, q2_0, k, c, qmax, i_b, 1)
                    q0 = q1 + q2
                    q1_0 = q1
                    q2_0 = q2
                    SOC_0 = q0/qmax*100
                    
                    # Calculate generator energy wasted if max charging current is reached
                    if i_w > 0:
                        e_exc = i_w * v_n
                        sim_out['P_gen_exc'].append(e_exc)
                    else:
                        sim_out['P_gen_exc'].append(0)
                    
                    sim_out['q'].append(SOC_0)      # State of charge (%)
                    sim_out['P_pv_exc'].append(0)   # Excess solar power (W)
                    
                    # For control modes 1 and 2 (cycle charging)
                    # If battery is below cycle charge SOC setpoint, keep generator in cycle charging mode
                    if SOC_0 < SOC_cyc and ctrl_mode in [1,2]:
                        cyc_charge = True
                    else:
                        cyc_charge = False
                  
                else:
                    # Generator not in operation
                    # Calculate battery state of charge
                    q1, q2, i_w = kb.capacity_step(q1_0, q2_0, k, c, qmax, i_b, 1)
                    q0 = q1 + q2
                    q1_0 = q1
                    q2_0 = q2
                    
                    # Calculate solar energy wasted if max charging current is reached
                    if i_w > 0:
                        e_s = i_w * v_n
                        sim_out['P_pv_exc'].append(e_s)
                    else:
                        sim_out['P_pv_exc'].append(0)
                    
                    SOC_0 = q0/qmax*100
                    sim_out['q'].append(SOC_0)      # State of charge (%)
                    sim_out['P_uns'].append(0)      # Power unsupplied (W)
                    sim_out['P_gen'].append(0)      # Generator output (W)
                    sim_out['P_gen_exc'].append(0)  # Excess generation (W)
        
        elif ctrl_mode == 4:
        #############################################################################################################
        # Control mode 4: Genset grid former, battery ramp control within specified time period
        # Between the start/stop time setpoints, the battery operates on ramp control as follows:
        #   - PV array has a firm power output setpoint. If PV output drops below the setpoint, then the battery 
        #     discharges to cover the difference
        #   - If the load is below the PV output setpoint, normal PV-generator operation takes place with excess 
        #     solar power charging the battery
        # Outside of the start/stop time setpoints, system operates as normal PV-generator system with
        # excess solar power charging the battery
        ##############################################################################################################
        
            # Loop through each hour of the year
            cyc_charge = False                      # Flag for cycle charging mode
            for i in range(8760):
                # Hour of the day
                h = np.mod(i+1,24)
                
                # If hour of the day is between start and stop time setpoints
                # AND the load is greater than the PV output setpoint
                # then activate solar/battery ramp/output control
                if (h >= t_set[0] and h < t_set[1] and P_ld[i] > p_set):
                    # Calculate net battery current
                    # Positive current denotes battery discharge
                    if pv_cpl == 'DC':
                        # DC coupled PV                        
                        i_s = P_pv[i] / v_n                    # Solar PV output current at output of charge controller
                        i_b = p_set / (v_n * eff_conv) - i_s            # Net battery current
                    else:
                        # AC coupled PV
                        i_net = (p_set - P_pv[i]) / v_n        # Net setpoint current at AC side
                        if i_net < 0:
                            # Battery charging
                            i_b = i_net * eff_conv
                        else:
                            # Battery discharging
                            i_b = i_net / eff_conv
                    
                    # Check if battery is under minimum SOC and net battery current > 0 (i.e. discharging)
                    p_def = 0
                    if (SOC_0 < SOC_min) and (i_b > 0):
                        # Battery under minimum SOC, do not discharge further
                        p_def = i_b * v_n *eff_conv       # Power deficit at AC side (relative to setpoint)
                        i_b = 0
                    
                    # Calculate generator loading`
                    P_uns = 0
                    if (p_set - p_def + Pg_min) > P_ld[i]:
                        # Low load conditions
                        sim_out['P_gen'].append(Pg_min)
                        sim_out['P_gen_exc'].append(Pg_min - P_ld[i] + p_set - p_def)
                    else:
                        # Load is above minimum generator loading
                        sim_out['P_gen_exc'].append(0)
                        if (Pg_tot + P_pv_out) < P_ld[i]:
                            # Generator under-capacity / overloaded
                            sim_out['P_gen'].append(Pg_tot)
                            P_uns = P_ld[i] - Pg_tot - (p_set - p_def)
                        else:
                            # Normal operation
                            sim_out['P_gen'].append(P_ld[i] - P_pv_out)
                    
                    sim_out['P_uns'].append(P_uns)
                    
                    # Calculate battery state of charge
                    q1, q2, i_w = kb.capacity_step(q1_0, q2_0, k, c, qmax, i_b, 1)
                    q0 = q1 + q2
                    q1_0 = q1
                    q2_0 = q2
                    
                    # Calculate solar energy wasted if max charging current is reached
                    if i_w > 0:
                        e_s = i_w * v_n
                        sim_out['P_pv_exc'].append(e_s)
                    else:
                        sim_out['P_pv_exc'].append(0)
                    
                    SOC_0 = q0/qmax*100
                    sim_out['q'].append(SOC_0)   # State of charge (%)
                    
                # Otherwise, normal PV-generator operation (with any excess PV charging the battery)
                else:
                    # PV output power at AC load side taking into account converter efficiencies
                    if pv_cpl == 'DC':
                        P_pv_out = P_pv[i] * eff_conv
                    else:
                        P_pv_out = P_pv[i]
                    
                    pv_exc = 0
                    if (P_pv_out + Pg_min) > P_ld[i]:
                        # Low load conditions
                        sim_out['P_uns'].append(0)
                        
                        if P_pv_out > 0 and Pg_min < P_ld[i]:
                            # Partial PV output used to charge battery
                            pv_exc = P_pv_out + Pg_min - P_ld[i]
                            sim_out['P_gen_exc'].append(0)
                            sim_out['P_gen'].append(Pg_min)
                        else:
                            sim_out['P_gen_exc'].append(Pg_min - P_ld[i])
                            sim_out['P_gen'].append(P_ld[i])
                            
                            if P_pv_out > 0 and Pg_min > P_ld[i]:
                                # All PV output curtailed / dumped
                                pv_exc = P_pv_out
                    else:
                        # Load is above minimum generator loading
                        sim_out['P_gen_exc'].append(0)
                        if (Pg_tot + P_pv_out) < P_ld[i]:
                            # Generator under-capacity / overloaded
                            sim_out['P_gen'].append(Pg_tot)
                            sim_out['P_uns'].append(P_ld[i] - Pg_tot - P_pv_out)
                        else:
                            # Normal operation
                            sim_out['P_gen'].append(P_ld[i] - P_pv_out)
                            sim_out['P_uns'].append(0)
                    
                    # Calculate excess PV current at DC side
                    if pv_cpl == 'DC':
                        i_b = -pv_exc / (v_n * eff_conv)
                    else:
                        i_b = -pv_exc / v_n * eff_conv
                    
                    # Calculate battery state of charge
                    q1, q2, i_w = kb.capacity_step(q1_0, q2_0, k, c, qmax, i_b, 1)
                    q0 = q1 + q2
                    q1_0 = q1
                    q2_0 = q2
                    
                    # Calculate solar energy wasted if max charging current is reached
                    if i_w > 0:
                        e_s = i_w * v_n
                        sim_out['P_pv_exc'].append(e_s)
                    else:
                        sim_out['P_pv_exc'].append(0)
                        
                    SOC_0 = q0/qmax*100
                    sim_out['q'].append(SOC_0)   # State of charge (%)
                    
        elif ctrl_mode == 5:
        #############################################################################################################
        # Control mode 5: Genset grid former, battery PV charge / cycle discharge
        # The generator forms the grid and supplies the load. The PV system supplies the load and charges the battery.
        # The battery discharges when it reaches its cycle charging setpoint until EOD, then waits to be charged again
        # by the PV system. The genset does not charge the battery.
        ##############################################################################################################
            pass
        
    return sim_out