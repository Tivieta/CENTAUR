#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2018 Julius Susanto. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""
CENTAUR: Hybrid Power System Simulation

Generator Tab

Authors: Julius Susanto
Last edited: January 2018
"""

from PyQt4 import QtCore, QtGui
import numpy as np
import gui.globals as globals
import gui.utility as utility
                      
class gen_ui(QtGui.QWidget): 
    
    def setup(self, window):   
        """Set up and initialise generator tab"""
        
        self.main_window = window        
        
        title1 = QtGui.QLabel('Generator configuration')
        title1.setFont(QtGui.QFont('arial', weight=QtGui.QFont.Bold))
        
        label1 = QtGui.QLabel('No. generators:')
        self.edit_nGen = QtGui.QLineEdit()
        self.edit_nGen.setFixedWidth(100)
        
        label2a = QtGui.QLabel('Nominal capacity:')
        label2b = QtGui.QLabel('kW')
        
        self.edit_Pgen = QtGui.QLineEdit()
        self.edit_Pgen.setFixedWidth(100)
        
        label3a = QtGui.QLabel('Minimum generator loading:')
        label3b = QtGui.QLabel('pu')
        
        self.edit_Pmin = QtGui.QLineEdit()
        self.edit_Pmin.setFixedWidth(100)
        
        label4a = QtGui.QLabel('Specific fuel consumption:')
        label4b = QtGui.QLabel('litres/kWh')
        
        self.edit_sfc = QtGui.QLineEdit()
        self.edit_sfc.setFixedWidth(100)
        
        label5a = QtGui.QLabel('AC/DC charger efficiency:')
        label5b = QtGui.QLabel('pu (DC coupled only)')
        
        self.edit_ChgEff = QtGui.QLineEdit()
        self.edit_ChgEff.setFixedWidth(100)
        
        layout = QtGui.QGridLayout()
        layout.addWidget(title1, 0, 0)
        layout.addWidget(label1, 1, 0)
        layout.addWidget(self.edit_nGen, 1, 1)
        layout.addWidget(label2a, 2, 0)
        layout.addWidget(self.edit_Pgen, 2, 1)
        layout.addWidget(label2b, 2, 2)
        layout.addWidget(label3a, 3, 0)
        layout.addWidget(self.edit_Pmin, 3, 1)
        layout.addWidget(label3b, 3, 2)
        layout.addWidget(label4a, 4, 0)
        layout.addWidget(self.edit_sfc, 4, 1)
        layout.addWidget(label4b, 4, 2)
        layout.addWidget(label5a, 5, 0)
        layout.addWidget(self.edit_ChgEff, 5, 1)
        layout.addWidget(label5b, 5, 2)
        self.setLayout(layout)

        self.edit_nGen.editingFinished.connect(utility.create_validation_hook(self, self.edit_nGen, "Number of generators", 0, 9999))       
        self.edit_Pgen.editingFinished.connect(utility.create_validation_hook(self, self.edit_Pgen, "Generator nominal capacity", 0, 99999))
        self.edit_Pmin.editingFinished.connect(utility.create_validation_hook(self, self.edit_Pmin, "Generator minimum loading", 0, 1))
        self.edit_sfc.editingFinished.connect(utility.create_validation_hook(self, self.edit_sfc, "Specific fuel consumption", 0, 99999))
        self.edit_ChgEff.editingFinished.connect(utility.create_validation_hook(self, self.edit_ChgEff, "AC/DC charger efficiency", 0, 1))

        self.refresh_data()  
    
    def update_data(self):
        """Update global variables to match GUI fields"""
        globals.gen_data['n_gen'] = int(self.edit_nGen.text())
        globals.gen_data['P_gen'] = float(self.edit_Pgen.text())
        globals.gen_data['l_min'] = float(self.edit_Pmin.text())
        globals.gen_data['e_f'] = float(self.edit_sfc.text())
        globals.gen_data['chg_eff'] = float(self.edit_ChgEff.text())
                     
    def refresh_data(self):
        """Update GUI fields to match global variables"""
        self.edit_nGen.setText(str(globals.gen_data['n_gen']))
        self.edit_Pgen.setText(str(globals.gen_data['P_gen']))
        self.edit_Pmin.setText(str(globals.gen_data['l_min']))
        self.edit_sfc.setText(str(globals.gen_data['e_f']))
        self.edit_ChgEff.setText(str(globals.gen_data['chg_eff']))