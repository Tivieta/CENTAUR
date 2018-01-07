#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2018 Julius Susanto. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""
CENTAUR: Hybrid Power System Simulation

Simulation Tab

Authors: Julius Susanto
Last edited: January 2018
"""

from PyQt4 import QtCore, QtGui
import numpy as np
import matplotlib.pyplot as plt
import gui.globals as globals
import gui.utility as utility
from engine.chron_sim import run_sim
                      
class sim_ui(QtGui.QWidget): 
    
    def setup(self, window):   
        """Set up and initialise simulation tab"""
        
        self.main_window = window        
        
        run_button = QtGui.QPushButton("Run")
        run_button.setFixedWidth(80)
        
        title1 = QtGui.QLabel('Output Window')
        title1.setFont(QtGui.QFont('arial', weight=QtGui.QFont.Bold))
        
        clear_button = QtGui.QPushButton("Clear")
        clear_button.setFixedWidth(80)
        
        font = QtGui.QFont("Courier New",10)
        self.textBox = QtGui.QTextEdit()
        self.textBox.setReadOnly(True)
        self.textBox.setFont(font)
        self.textBox.setMinimumSize(QtCore.QSize(1000,400))
        
        title2 = QtGui.QLabel('Plot Outputs')
        title2.setFont(QtGui.QFont('arial', weight=QtGui.QFont.Bold))
        
        self.combo_plot = QtGui.QComboBox()
        self.combo_plot.setFixedWidth(150)
        plot_button = QtGui.QPushButton("Plot")
        
        layout = QtGui.QGridLayout()
        layout.addWidget(run_button, 0, 0)
        layout.addWidget(title1, 1, 0)
        layout.addWidget(clear_button, 1, 1)
        layout.addWidget(self.textBox, 2, 0, 3, 8)
        layout.addWidget(title2, 5, 0)
        layout.addWidget(self.combo_plot, 6, 0)
        layout.addWidget(plot_button, 6, 1)
        
        self.setLayout(layout)

        run_button.clicked.connect(self.runBtnClicked)
        clear_button.clicked.connect(self.clear_fn)
        plot_button.clicked.connect(self.plotBtnClicked)
        
        # Clear output window
        self.textBox.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.textBox.customContextMenuRequested.connect(self.textbox_menu)
    
    def textbox_menu(self, point):
        """ Custom context menu for output window """
        menu = self.textBox.createStandardContextMenu(point)
        
        # Include clear log action
        clearLog = QtGui.QAction('Clear output window', self)
        clearLog.setStatusTip('Clear output window')
        clearLog.triggered.connect(self.clear_fn)
        
        menu.addAction(clearLog)
        menu.exec_(self.textBox.viewport().mapToGlobal(point))
    
    def write(self, msg):
        """ Function to write messages into output window """
        self.textBox.insertPlainText(str(msg))
    
    def clear_fn(self):
        """ Function to clear output window """
        self.textBox.clear()
    
    def runBtnClicked(self):
        """ Run simulation engine """
        self.write('Running simulation...\n')
        
        for p in self.main_window.pages:
            p.update_data()
        
        # Build up input dictionaries from global data
        pv_dict = globals.pv_data
        pv_dict['Ktm'] = globals.pv_resource[:,0].tolist()
        pv_dict['T_amb'] = globals.pv_resource[:,1].tolist()
        
        batt_dict = globals.batt_data
        batt_dict['T'] = globals.batt_char[:,0].tolist()
        batt_dict['I'] = globals.batt_char[:,1].tolist()
        
        gen_dict = globals.gen_data
        
        load_dict = {
            'l_sum' : globals.loads[:,0].tolist(),
            'l_win' : globals.loads[:,1].tolist(),
            'sigma_s' : globals.load_sigma[0], 
            'sigma_w' : globals.load_sigma[1]
        }
        
        self.combo_plot.clear()
        self.combo_plot.addItem('Load Demand')
        sys_dict = globals.sys_data
        sys_dict['lat'] = globals.latitude
        if sys_dict['sys_config'] in [0, 1, 3]:
            sys_dict['is_gen'] = True
            self.combo_plot.addItem('Generator Output')
        else:
            sys_dict['is_gen'] = False
        
        if sys_dict['sys_config'] in [1, 2, 3]:
            sys_dict['is_pv'] = True
            self.combo_plot.addItem('Solar PV Output')
        else:
            sys_dict['is_pv'] = False
            
        if sys_dict['sys_config'] in [2, 3]:
            sys_dict['is_batt'] = True
            self.combo_plot.addItem('Battery SoC')
        else:
            sys_dict['is_batt'] = False
            
        self.sim_out = run_sim(sys_dict,pv_dict,batt_dict,gen_dict,load_dict)
        
        topo = self.sim_out['topo']
        P_ld = self.sim_out['P_ld']
        E_tot = sum(P_ld)/1000
        E_uns = sum(self.sim_out['P_uns'])

        if topo[0] in [0,1,3]:
            E_gen = sum(self.sim_out['P_gen'])
            E_gen_exc = sum(self.sim_out['P_gen_exc'])
        else:
            E_gen = 0
            
        if topo[0] in [1,2,3]:
            G0 = self.sim_out['G0']
            P_pv = self.sim_out['P_pv']
            E_exc = sum(self.sim_out['P_pv_exc'])
            E_sol = sum(P_pv) - E_exc

        if topo[0] in [2,3]:
            q = self.sim_out['q']
            E_bat = E_tot - (E_gen + E_uns) / 1000
        else:
            q = np.zeros(8761)
                    
        self.write('--------------------------------------\n')
        self.write('SYSTEM SUMMARY\n')
        self.write('--------------------------------------\n')
        self.write('Topology: ' + topo[1] +'\n')
        if topo[0] == 3:
            if sys_dict['ctrl_mode'] == 0:
                ctrl_mode = 'Battery grid former, genset backup (cycle charging, DC coupled)'
            elif sys_dict['ctrl_mode'] == 1:
                ctrl_mode = 'Mixed master, genset cycle charging (AC coupled)'
            elif sys_dict['ctrl_mode'] == 2:
                ctrl_mode = 'Mixed master, genset load following (AC coupled)'
            elif sys_dict['ctrl_mode'] == 3:
                ctrl_mode = 'Genset grid former (AC coupled), battery ramp-rate support'
            elif sys_dict['ctrl_mode'] == 4:
                ctrl_mode = 'Genset grid former (AC coupled), battery charged by PV and cycle discharged'
            self.write('Control mode: ' + ctrl_mode + '\n')
        if topo[0] in [1,2,3]:
            self.write('Solar PV system capacity: ' + str(pv_dict['P_stc']/1000) + ' kWp (' + pv_dict['pv_cpl'] + ' coupled)\n')
        if topo[0] in [2,3]:
            self.write('Battery system capacity: ' + str(batt_dict['C_nom'] * batt_dict['n_batt'] * batt_dict['v_dc'] /1000) + ' kWh\n')
        if topo[0] in [0,1,3]:
            self.write('Generator capacity: ' + str(gen_dict['n_gen']) + ' x ' + str(gen_dict['P_gen']) + ' kW units = '+ str(gen_dict['n_gen'] * gen_dict['P_gen']) + ' kW total\n')
        self.write('\n')
        self.write('--------------------------------------\n')
        self.write('SIMULATION RESULTS\n')
        self.write('--------------------------------------\n')
        self.write('SYSTEM LOAD \n')
        self.write('----------- \n')
        self.write('Total energy demand: ' + str(round(E_tot,2)) + ' kWh\n')
        self.write('Energy unsupplied: ' + str(round(E_uns/1000,2)) + ' kWh (' + str(round(E_uns/1000/E_tot *100,2)) + '% of overall demand)\n')
        if topo[0] in [1,2,3]:
            self.write('\n')
            self.write('SOLAR PV SYSTEM \n')
            self.write('--------------- \n')
            self.write('Total GHI: ' + str(round(sum(self.sim_out['G0'])/1000,2)) + ' kWh/m2 per year\n')
            self.write('Total solar PV system output: ' + str(round(sum(P_pv)/1000,2)) + ' kWh (including inverter/SCC losses)\n')
            self.write('Useful solar PV energy: ' + str(round(E_sol/1000,2)) + ' kWh (' + str(round(E_sol/sum(P_pv)*100,2)) + '% of total solar output)\n')
            self.write('Excess solar PV energy: ' + str(round(E_exc/1000,2)) + ' kWh (' + str(round(E_exc/sum(P_pv)*100,2)) + '% of total solar output)\n')

        if topo[0] in [2,3]:
            self.write('\n')
            self.write('BATTERY SYSTEM \n')
            self.write('-------------- \n')
            self.write('Load supplied by PV/battery system: ' + str(round(E_bat,2)) + ' kWh (' + str(round(E_bat/E_tot *100,2)) + '% of overall demand)\n')
        if topo[0] in [0,1,3]:
            self.write('\n')
            self.write('GENERATOR \n')
            self.write('--------- \n')
            self.write('Load supplied by generator: ' + str(round(E_gen/1000,2)) + ' kWh (' + str(round(E_gen/1000/E_tot *100,2)) + '% of overall demand)\n')
            self.write('Excess generation: ' + str(round(E_gen_exc/1000,2)) + ' kWh (' + str(round(E_gen_exc/(E_gen+E_gen_exc)*100,2)) + '% of total generator output)\n')
            self.write('Fuel used by generator: ' + str(round((E_gen+E_gen_exc)/1000 * gen_dict['e_f'],2)) + ' litres\n')
        
        self.main_window.show_status_message('Simulation complete...')
    
    def plotBtnClicked(self):
        """ Plot result outputs """
        if plt.fignum_exists(1):
            # Do nothing if a plot is already open
            QtGui.QMessageBox.warning(self, 'Warning', "A plot is already open. Please close to create a new plot.", QtGui.QMessageBox.Ok)
        else:
            fig = plt.figure(1, facecolor='white', figsize=(16,7))
            if self.combo_plot.currentText() == 'Battery SoC':
                q = self.sim_out['q']
                # Reshape q into 2d matrix (24 x 365)
                q2d = np.reshape(np.matrix(q[1:]), (-1,24)).T
                plt.title('Battery state of charge (%)')
                
            elif self.combo_plot.currentText() == 'Generator Output':
                q = np.array(self.sim_out['P_gen']) / 1000
                q2d = np.reshape(np.matrix(q), (-1,24)).T
                plt.title('Generator Output (kW)')
                
            elif self.combo_plot.currentText() == 'Solar PV Output':
                q = self.sim_out['P_pv']
                q2d = np.reshape(np.matrix(q), (-1,24)).T
                plt.title('Solar PV Output (Wp)')
            
            elif self.combo_plot.currentText() == 'Load Demand':
                q = self.sim_out['P_ld']
                q2d = np.reshape(np.matrix(q), (-1,24)).T
                plt.title('Load Demand (W)')
            
            try:
                plt.ylabel('Hour of the day')
                plt.xlabel('Day of the year')
                plt.imshow(q2d, aspect='auto', cmap='jet')
                plt.colorbar()
                plt.show()
            except:
                self.main_window.show_status_message('Error opening plot...')
                plt.close()