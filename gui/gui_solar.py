#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2018 Julius Susanto. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""
CENTAUR: Hybrid Power System Simulation

Solar PV Tab

Authors: Julius Susanto
Last edited: January 2018
"""

from PyQt4 import QtCore, QtGui
import numpy as np
import gui.globals as globals
import gui.utility as utility
                      
class solar_ui(QtGui.QWidget): 
    
    def setup(self, window):
        """Set up and initialise solar PV tab"""
        
        self.main_window = window        
        
        title1 = QtGui.QLabel('Site Location')
        title1.setFont(QtGui.QFont('arial', weight=QtGui.QFont.Bold))
        
        label1 = QtGui.QLabel('Latitude:')
        label1.setFixedWidth(100)
        
        self.edit_lat = QtGui.QLineEdit()
        self.edit_lat.setFixedWidth(100)
        
        label2 = QtGui.QLabel('Longitude:')
        label2.setFixedWidth(100)
        
        self.edit_lon = QtGui.QLineEdit()
        self.edit_lon.setFixedWidth(100)
        
        title2 = QtGui.QLabel('Solar resource data')
        title2.setFont(QtGui.QFont('arial', weight=QtGui.QFont.Bold))
        
        update_button = QtGui.QPushButton("Update")
        update_button.setFixedWidth(80)
        
        headings = ['Ktm', 'Tamb']
        self.tableWidget = SolarTable(window, headings = headings, alternatingRowColors = True)
        self.tableWidget.setMinimumHeight(400)
        
        vline = QtGui.QFrame()
        vline.setFrameStyle(QtGui.QFrame.VLine | QtGui.QFrame.Sunken)
        
        title3 = QtGui.QLabel('Solar PV system')
        title3.setFont(QtGui.QFont('arial', weight=QtGui.QFont.Bold))
        
        label4a = QtGui.QLabel('PV array DC output:')
        label4b = QtGui.QLabel('Wp')
        
        self.edit_Pstc = QtGui.QLineEdit()
        self.edit_Pstc.setFixedWidth(100)
        
        label5 = QtGui.QLabel('PV system coupling:')
        self.pv_coupling = QtGui.QComboBox()
        self.pv_coupling.addItems(["AC","DC"])
        
        label6a = QtGui.QLabel('PV inverter AC output:')
        label6b = QtGui.QLabel('Wac')
        
        self.edit_Pinv = QtGui.QLineEdit()
        self.edit_Pinv.setFixedWidth(100)
        
        label7a = QtGui.QLabel('Power temperature coefficient:')
        label7b = QtGui.QLabel('pu/deg C')
        
        self.edit_gamma = QtGui.QLineEdit()
        self.edit_gamma.setFixedWidth(100)
        
        label8a = QtGui.QLabel('Enviromental derating factor:')
        label8b = QtGui.QLabel('pu')
        
        self.edit_ke = QtGui.QLineEdit()
        self.edit_ke.setFixedWidth(100)
        
        label9a = QtGui.QLabel('Manufacturer tolerance factor:')
        label9b = QtGui.QLabel('pu')
        
        self.edit_km = QtGui.QLineEdit()
        self.edit_km.setFixedWidth(100)
        
        label10a = QtGui.QLabel('Inverter / SCC efficiency:')
        label10b = QtGui.QLabel('pu')
        
        self.edit_eff = QtGui.QLineEdit()
        self.edit_eff.setFixedWidth(100)
        
        title4 = QtGui.QLabel('Solar PV Array Configuration')
        title4.setFont(QtGui.QFont('arial', weight=QtGui.QFont.Bold))
        
        label11a = QtGui.QLabel('Tilt angle:')
        label11b = QtGui.QLabel('degrees')
        
        self.edit_tilt = QtGui.QLineEdit()
        self.edit_tilt.setFixedWidth(100)
        
        label12a = QtGui.QLabel('Azimuth angle:')
        label12b = QtGui.QLabel('degrees')
        
        self.edit_azimuth = QtGui.QLineEdit()
        self.edit_azimuth.setFixedWidth(100)
        
        label13a = QtGui.QLabel('Albedo:')
        label13b = QtGui.QLabel('pu')
        
        self.edit_albedo = QtGui.QLineEdit()
        self.edit_albedo.setFixedWidth(100)
        
        layout = QtGui.QGridLayout()
        layout.addWidget(title1, 0, 0)
        layout.addWidget(label1, 1, 0)
        layout.addWidget(self.edit_lat, 1, 1)
        layout.addWidget(label2, 2, 0)
        layout.addWidget(self.edit_lon, 2, 1)
        layout.addWidget(title2, 3, 0, 1, 2)
        layout.addWidget(update_button, 3, 2)
        layout.addWidget(self.tableWidget, 4, 0, 10, 3)
        layout.addWidget(vline, 0, 4, 15, 4)
        
        layout.addWidget(title3, 0, 5)
        layout.addWidget(label4a, 1, 5)
        layout.addWidget(self.edit_Pstc, 1, 6)
        layout.addWidget(label4b, 1, 7)
        layout.addWidget(label5, 2, 5)
        layout.addWidget(self.pv_coupling, 2, 6)
        layout.addWidget(label6a, 3, 5)
        layout.addWidget(self.edit_Pinv, 3, 6)
        layout.addWidget(label6b, 3, 7)
        layout.addWidget(label7a, 4, 5)
        layout.addWidget(self.edit_gamma, 4, 6)
        layout.addWidget(label7b, 4, 7)
        layout.addWidget(label8a, 5, 5)
        layout.addWidget(self.edit_ke, 5, 6)
        layout.addWidget(label8b, 5, 7)
        layout.addWidget(label9a, 6, 5)
        layout.addWidget(self.edit_km, 6, 6)
        layout.addWidget(label9b, 6, 7)
        layout.addWidget(label10a, 7, 5)
        layout.addWidget(self.edit_eff, 7, 6)
        layout.addWidget(label10b, 7, 7)
        
        layout.addWidget(title4, 0, 8)
        layout.addWidget(label11a, 1, 8)
        layout.addWidget(self.edit_tilt, 1, 9)
        layout.addWidget(label11b, 1, 10)
        layout.addWidget(label12a, 2, 8)
        layout.addWidget(self.edit_azimuth, 2, 9)
        layout.addWidget(label12b, 2, 10)
        layout.addWidget(label13a, 3, 8)
        layout.addWidget(self.edit_albedo, 3, 9)
        layout.addWidget(label13b, 3, 10)
        self.setLayout(layout)
        
        self.refresh_data()
        
        self.edit_lat.editingFinished.connect(utility.create_validation_hook(self, self.edit_lat, "Latitude", -180, 180))       
        self.edit_lon.editingFinished.connect(utility.create_validation_hook(self, self.edit_lon, "Longitude", -180, 180))
        self.edit_Pstc.editingFinished.connect(utility.create_validation_hook(self, self.edit_Pstc, "PStc", 0, float("inf")))
        self.edit_Pinv.editingFinished.connect(utility.create_validation_hook(self, self.edit_Pinv, "Pinv", 0, float("inf")))
        self.edit_gamma.editingFinished.connect(utility.create_validation_hook(self, self.edit_gamma, "Gamma", 0, 1))
        self.edit_ke.editingFinished.connect(utility.create_validation_hook(self, self.edit_ke, "Ke", 0, 1))
        self.edit_km.editingFinished.connect(utility.create_validation_hook(self, self.edit_km, "Km", 0, 1))
        self.edit_eff.editingFinished.connect(utility.create_validation_hook(self, self.edit_eff, "Efficiency", 0, 1))
        self.edit_tilt.editingFinished.connect(utility.create_validation_hook(self, self.edit_tilt, "Tilt", 0, 90))
        self.edit_azimuth.editingFinished.connect(utility.create_validation_hook(self, self.edit_azimuth, "Azimuth", -180, 180))
        self.edit_albedo.editingFinished.connect(utility.create_validation_hook(self, self.edit_albedo, "Albedo", 0, 1))
        
        self.pv_coupling.currentIndexChanged.connect(self.update_coupling)
        update_button.clicked.connect(self.buttonClicked)
        self.tableWidget.itemChanged.connect(self.update_data_matrix)

    # TODO: Button doesn't do anything at the moment - make it goto NASA SSE and get data
    def buttonClicked(self, tableWidget):
        """Update PV resource button"""
        self.refresh_data()        
    
    def update_data(self):
        """Update global variables to match GUI fields"""
        globals.latitude = float(self.edit_lat.text())
        globals.longitude = float(self.edit_lon.text())
        globals.pv_data['P_stc'] = float(self.edit_Pstc.text())
        globals.pv_data['P_inv'] = float(self.edit_Pinv.text())
        globals.pv_data['gamma'] = float(self.edit_gamma.text())
        globals.pv_data['k_e'] = float(self.edit_ke.text())
        globals.pv_data['k_m'] = float(self.edit_km.text())
        globals.pv_data['eff_pv'] = float(self.edit_eff.text())
        globals.pv_data['tilt'] = float(self.edit_tilt.text())
        globals.pv_data['azimuth'] = float(self.edit_azimuth.text())
        globals.pv_data['albedo'] = float(self.edit_albedo.text())
    
    def update_coupling(self):
        """Update global variable for AC/DC coupling combo box"""
        if self.pv_coupling.currentIndex() == 0:
            globals.pv_data['pv_cpl'] = 'AC'
            self.edit_Pinv.setEnabled(True)
        else:
            globals.pv_data['pv_cpl'] = 'DC'
            self.edit_Pinv.setEnabled(False)
        
    def update_data_matrix(self, tableWidgetItem): 
        """Update PV resource matrix whenever table data is changed"""
        value = 0.0
        if tableWidgetItem.column() == 0:
            element = "Ktm"
            lower_bound = 0.0
            upper_bound = 1.0
            value = utility.validate(tableWidgetItem.text(), lower_bound, upper_bound, l_inclusive = False, u_inclusive = False)
        elif tableWidgetItem.column() == 1:
            element = "Tamb"
            lower_bound = -60.0
            upper_bound = 60.0
            value = utility.validate(tableWidgetItem.text(), lower_bound, upper_bound, l_inclusive = False, u_inclusive = False)
        
        if value is not False:   
            columns = [0,1]            
            column = columns[tableWidgetItem.column()]
            update_mapping = (globals.pv_resource[tableWidgetItem.row(), column] != value)            
            globals.pv_resource[tableWidgetItem.row(), column] = value
            
        else:
            self.main_window.show_status_message("Month " + str(tableWidgetItem.row() + 1) + " " + element +  ": Input value '" + tableWidgetItem.text() + "' out of bounds. (" + str(lower_bound) + " to " + str(upper_bound) + "). Value not set.", error = True, beep = True)
            self.tableWidget.itemChanged.disconnect()
            self.refresh_data()          
            self.tableWidget.itemChanged.connect(self.update_data_matrix)            
        
    def refresh_data(self):
        """Update GUI fields to match global variables"""
        self.edit_lat.setText(str(globals.latitude))
        self.edit_lon.setText(str(globals.longitude))
        self.tableWidget.fill_table(globals.pv_resource)
        if globals.pv_data['pv_cpl'] == 'AC':
            self.pv_coupling.setCurrentIndex(0)
            self.edit_Pinv.setEnabled(True)
        else:
            self.pv_coupling.setCurrentIndex(1)
            self.edit_Pinv.setEnabled(False)
        self.edit_Pstc.setText(str(globals.pv_data['P_stc']))
        self.edit_Pinv.setText(str(globals.pv_data['P_inv']))
        self.edit_gamma.setText(str(globals.pv_data['gamma']))
        self.edit_ke.setText(str(globals.pv_data['k_e']))
        self.edit_km.setText(str(globals.pv_data['k_m']))
        self.edit_eff.setText(str(globals.pv_data['eff_pv']))
        self.edit_tilt.setText(str(globals.pv_data['tilt']))
        self.edit_azimuth.setText(str(globals.pv_data['azimuth']))
        self.edit_albedo.setText(str(globals.pv_data['albedo']))
            
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