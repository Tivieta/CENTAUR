#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2018 Julius Susanto. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""
CENTAUR: Hybrid Power System Simulation

Project Tab

Authors: Julius Susanto
Last edited: January 2018
"""

from PyQt4 import QtCore, QtGui
import numpy as np
import gui.globals as globals
import gui.utility as utility
                      
class project_ui(QtGui.QWidget): 
    
    def setup(self, window):
        """Set up and initialise project tab"""
        
        self.main_window = window        
        
        title1 = QtGui.QLabel('Project information')
        title1.setFont(QtGui.QFont('arial', weight=QtGui.QFont.Bold))
        
        label1 = QtGui.QLabel('Title:')
        self.edit_title = QtGui.QLineEdit()
        self.edit_title.setFixedWidth(300)
        
        label2 = QtGui.QLabel('Description:')
        self.edit_desc = QtGui.QTextEdit()
        
        title2 = QtGui.QLabel('System setup')
        title2.setFont(QtGui.QFont('arial', weight=QtGui.QFont.Bold))
        
        label3 = QtGui.QLabel('Hybrid system configuration:')
        self.combo_config = QtGui.QComboBox()
        self.combo_config.addItems(["Genset","PV-Genset","PV-Battery","PV-Battery-Genset"])
        
        label4 = QtGui.QLabel('Control mode:')
        self.combo_ctrl = QtGui.QComboBox()
        self.combo_ctrl.addItems(["Mode 1: Battery grid former, genset backup","Mode 2: Mixed master, genset cycle charging","Mode 3: Mixed master, genset load following","Mode 4: Genset grid former, battery ramp control"])
        
        layout = QtGui.QGridLayout()
        layout.addWidget(title1, 0, 0)
        layout.addWidget(label1, 1, 0)
        layout.addWidget(self.edit_title, 1, 1)
        layout.addWidget(label2, 2, 0)
        layout.addWidget(self.edit_desc, 2, 1)
        layout.addWidget(title2, 3, 0)
        layout.addWidget(label3, 4, 0)
        layout.addWidget(self.combo_config, 4, 1)
        layout.addWidget(label4, 5, 0)
        layout.addWidget(self.combo_ctrl, 5, 1)
        self.setLayout(layout)
        
        self.refresh_data() 
                
    def update_data(self):
        """Update global variables to match GUI fields"""
        globals.sys_data['proj_title'] = self.edit_title.text()
        globals.sys_data['proj_desc'] = self.edit_desc.toPlainText()
        globals.sys_data['sys_config'] = self.combo_config.currentIndex()
        globals.sys_data['ctrl_mode'] = self.combo_ctrl.currentIndex()
                     
    def refresh_data(self):
        """Update GUI fields to match global variables"""
        self.edit_title.setText(str(globals.sys_data['proj_title']))
        self.edit_desc.setText(str(globals.sys_data['proj_desc']))
        self.combo_config.setCurrentIndex(globals.sys_data['sys_config'])
        self.combo_ctrl.setCurrentIndex(globals.sys_data['ctrl_mode'])