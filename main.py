#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2018 Julius Susanto. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""
CENTAUR: Hybrid Power System Simulation

Main window

Author: Julius Susanto
Last edited: January 2018
"""

import os, sys
from PyQt4 import QtGui

from gui.gui_solar import solar_ui
from gui.gui_loads import loads_ui
from gui.gui_battery import battery_ui
from gui.gui_gen import gen_ui
from gui.gui_project import project_ui
from gui.gui_sim import sim_ui

import matplotlib.backends.backend_tkagg
import gui.globals as globals

class Window(QtGui.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        
        globals.init()
        self.initUI()
        
    def initUI(self):
        """Set up and initialise main GUI window"""
        
        self.resize(1200, 750)
        self.centre()
        self.setWindowTitle('CENTAUR')
        self.setWindowIcon(QtGui.QIcon('media\sigma.png')) 
        
        """
        Tabs
        """
        tab_widget = QtGui.QTabWidget()
        tab1 = QtGui.QWidget()        
        tab2 = QtGui.QWidget() 
        tab3 = QtGui.QWidget()
        tab4 = QtGui.QWidget()
        tab5 = QtGui.QWidget()
        tab6 = QtGui.QWidget()
        self.tab_widget = tab_widget
        
        tab_widget.addTab(tab1, "Project")
        tab_widget.addTab(tab2, "Loads")
        tab_widget.addTab(tab3, "Solar PV") 
        tab_widget.addTab(tab4, "Battery") 
        tab_widget.addTab(tab5, "Genset") 
        tab_widget.addTab(tab6, "Simulation") 
        
        self.page1 = project_ui(tab1)
        self.page2 = loads_ui(tab2)
        self.page3 = solar_ui(tab3)
        self.page4 = battery_ui(tab4)
        self.page5 = gen_ui(tab5)
        self.page6 = sim_ui(tab6)
        
        self.page1.setup(self)
        self.page2.setup(self)
        self.page3.setup(self)
        self.page4.setup(self)
        self.page5.setup(self)
        self.page6.setup(self)
        
        self.pages = [self.page1, self.page2, self.page3, self.page4, self.page5]
        
        """
        Actions
        """
        exitAction = QtGui.QAction(QtGui.QIcon('media\exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)

        saveAsAction = QtGui.QAction(QtGui.QIcon('media\saveas.ico'), 'Save &As', self)
        saveAsAction.setShortcut('Ctrl+A')
        saveAsAction.setStatusTip('Save project as')
        saveAsAction.triggered.connect(self.save_as_fn)

        openAction = QtGui.QAction(QtGui.QIcon('media\open.ico'), '&Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open project')
        openAction.triggered.connect(self.open_fn)
        
        aboutAction = QtGui.QAction('&About CENTAUR', self)
        aboutAction.setStatusTip('About CENTAUR')
        aboutAction.triggered.connect(self.about_dialog)
        
        helpAction = QtGui.QAction('&User Manual', self)
        helpAction.setShortcut('F1')
        helpAction.setStatusTip('User documentation')
        helpAction.triggered.connect(self.user_manual)   
        
        """
        Menubar
        """
        menu_bar = QtGui.QMenuBar() 
        fileMenu = menu_bar.addMenu('&File')
        fileMenu.addAction(saveAsAction)
        fileMenu.addAction(openAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)
        helpMenu = menu_bar.addMenu('&Help')
        helpMenu.addAction(helpAction)
        helpMenu.addSeparator()
        helpMenu.addAction(aboutAction)

        """
        Status line.
        """
        self.status_message = QtGui.QStatusBar()        
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(menu_bar)
        vbox.addWidget(tab_widget) 
        vbox.addWidget(self.status_message)        
        self.setLayout(vbox)
        
    def centre(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def refresh_data(self):
        """Refresh each page with data from globals variables."""
        for p in self.pages:
            p.refresh_data()
    
    def show_status_message(self, message, error = False, beep = False):
        """Display a status message on the status line.
           If error is True the status text will be coloured red.
           If beep is True then the application will beep.
        """
        if(error):
            self.status_message.setStyleSheet('QStatusBar {color: red}')
        else:
            self.status_message.setStyleSheet('')
        if beep:
            QtGui.QApplication.beep()
        self.status_message.showMessage(message)
    
    def save_as_fn(self):
        """Function for the Save As action."""
        
        fname = QtGui.QFileDialog.getSaveFileName(self, "Save Data File As", "", "CENTAUR project files (*.ctr)")
        
        if fname:
            for p in self.pages:
                p.update_data()
            
            if globals.write_project_to_file(fname):
                self.show_status_message("Write to file " + fname + " successful.")
                self.refresh_data()                
            else:
                self.show_status_message("Failed to save " + fname + ".", error = True, beep = True)
        else:
            self.show_status_message("Save As cancelled.")                   
        
    def save_fn(self):    
        """Function for the Save action."""
        if globals.filename != "":
            if globals.write_project_to_file(globals.filename):                
                self.refresh_data()        
            else:
                self.show_status_message("Failed to save " + globals.filename + ".", error = True, beep = True)
        
    def open_fn(self):
        """Function for the Open action."""
        
        ##########################################################
        # TODO: Confirmation for opening file if data is unsaved #
        ##########################################################
        fname = QtGui.QFileDialog.getOpenFileName(self, "Open Data File", "", "CENTAUR project files (*.ctr)")
        if fname:
            if globals.load_project_from_file(fname):                
                self.refresh_data()
                self.show_status_message("File " + fname + " successfully loaded.")
            else:
                self.show_status_message("Failed to open " + fname + ".", error = True, beep = True)
        else:
            self.show_status_message("Open Data File cancelled.")
        
    def user_manual(self):
        """Launch user manual (Github link)"""
        os.system("start \"\" https://github.com/susantoj/CENTAUR/wiki")
    
    def about_dialog(self):
        """Show About dialog box"""
        QtGui.QMessageBox.about(self, "About CENTAUR",
                """<b>CENTAUR</b> is a hybrid power system simulation package.
                   <p>
                   Version: <b>v1.0<b><p>
                   <p>
                   <p>&copy; 2018 Julius Susanto</p>
                   <p>All rights reserved.</p>  
                   """)
    
def main():
    app = QtGui.QApplication(sys.argv)
    w = Window()
    w.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()