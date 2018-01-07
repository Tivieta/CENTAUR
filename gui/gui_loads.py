#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2018 Julius Susanto. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""
CENTAUR: Hybrid Power System Simulation

Loads Tab

Authors: Julius Susanto
Last edited: January 2018
"""

from PyQt4 import QtCore, QtGui
import numpy as np
import gui.globals as globals
import gui.utility as utility
                      
class loads_ui(QtGui.QWidget): 
    
    def setup(self, window):   
        """Set up and initialise loads tab"""
        
        self.main_window = window        
        
        title1 = QtGui.QLabel('Load variability')
        title1.setFont(QtGui.QFont('arial', weight=QtGui.QFont.Bold))
        
        label1 = QtGui.QLabel('Summer Dispersion:')
        label1.setFixedWidth(100)
        
        self.edit_sigma_s = QtGui.QLineEdit()
        self.edit_sigma_s.setFixedWidth(100)
        
        label2 = QtGui.QLabel('Winter Dispersion:')
        label2.setFixedWidth(100)
        
        self.edit_sigma_w = QtGui.QLineEdit()
        self.edit_sigma_w.setFixedWidth(100)
        
        title2 = QtGui.QLabel('Hourly load data')
        title2.setFont(QtGui.QFont('arial', weight=QtGui.QFont.Bold))
        
        headings = ['Summer (kW)', 'Winter (kW)']
        self.tableWidget = SolarTable(window, headings = headings, alternatingRowColors = True)
        self.tableWidget.setMinimumHeight(500)
        vheadings = ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']
        self.tableWidget.setRowCount(len(vheadings)) 
        self.tableWidget.setVerticalHeaderLabels(vheadings)
        
        layout = QtGui.QGridLayout()
        layout.addWidget(title1, 0, 0)
        layout.addWidget(label1, 1, 0)
        layout.addWidget(self.edit_sigma_s, 1, 1)
        layout.addWidget(label2, 2, 0)
        layout.addWidget(self.edit_sigma_w, 2, 1)
        layout.addWidget(title2, 3, 0, 1, 2)
        layout.addWidget(self.tableWidget, 4, 0, 10, 3)
        self.setLayout(layout)

        self.edit_sigma_s.editingFinished.connect(utility.create_validation_hook(self, self.edit_sigma_s, "Summer dispersion", 0, 99999))
        
        self.edit_sigma_w.editingFinished.connect(utility.create_validation_hook(self, self.edit_sigma_w, "Winter dispersion", 0, 99999))
        
        self.tableWidget.itemChanged.connect(self.update_data_matrix)

        self.refresh_data()  
    
    def update_data(self):
        """Update global variables to match GUI fields"""
        globals.load_sigma[0] = float(self.edit_sigma_s.text())
        globals.load_sigma[1] = float(self.edit_sigma_w.text())
           
    def update_data_matrix(self, tableWidgetItem): 
        """Update load matrix whenever table data is changed"""
        value = 0.0
        if tableWidgetItem.column() == 0:
            element = "Summer Load"
            lower_bound = 0.0
            upper_bound = 999999
            value = utility.validate(tableWidgetItem.text(), lower_bound, upper_bound, l_inclusive = True, u_inclusive = False)
        elif tableWidgetItem.column() == 1:
            element = "Winter Load"
            lower_bound = 0.0
            upper_bound = 999999
            value = utility.validate(tableWidgetItem.text(), lower_bound, upper_bound, l_inclusive = True, u_inclusive = False)
        
        if value is not False:   
            columns = [0,1]            
            column = columns[tableWidgetItem.column()]
            update_mapping = (globals.loads[tableWidgetItem.row(), column] != value)            
            globals.loads[tableWidgetItem.row(), column] = value
            #tableWidgetItem.setText(str(value))
            
        else:
            self.main_window.show_status_message(element + " Hour " + str(tableWidgetItem.row()) + ": Input value '" + tableWidgetItem.text() + "' out of bounds. (" + str(lower_bound) + " to " + str(upper_bound) + "). Value not set.", error = True, beep = True)
            self.tableWidget.itemChanged.disconnect()
            self.refresh_data()          
            self.tableWidget.itemChanged.connect(self.update_data_matrix)            
        
    def refresh_data(self):
        """Update GUI fields to match global variables"""
        self.edit_sigma_s.setText(str(globals.load_sigma[0]))
        self.edit_sigma_w.setText(str(globals.load_sigma[1]))
        self.tableWidget.fill_table(globals.loads)
            
class SolarTable(utility.CentaurTable): 
    """Modified version of LowFi table specifically for the Right Of Way tab."""

    def signal_mapping(signal_mapper):
        self.signal_mapper = signal_mapper

    def fill_table(self, data):
        """Fill table from 2D list or numpy array."""
        if len(data) > 0:
            if isinstance(data, np.ndarray):
                data = data.tolist()
            data_rows = len(data)
            data_columns = len(data[0])
            
            if data_columns > 0:
                self.setRowCount(data_rows)
                for r in range(0, data_rows):
                    # Update real columns
                    for c in range(2):
                        item = QtGui.QTableWidgetItem()                        
                        item.setText(str(data[r][c]))      
                        self.setItem(r, c, item)