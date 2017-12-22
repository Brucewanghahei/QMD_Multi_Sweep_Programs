"""Written by Bruce Wang.
    Inspired and helped by Johnathon Vannucci.
    Contact wdmzcjwq@gmail.com if you have any questions"""

"""To compile the .ui file into .py file, it is very simple. Do the following stpes:
   1. Open Command Proment (Terminal if you are using mac), using 'cd' to get the directory that contains the .ui file
   2. Type "pyuic4 -x filename.ui -o filename.py"
   3. If nothing strange happens, it means a .py file is successfully created in the same directory contains your original .ui file
   4. Do not change any of the code in the .py file because recomling any new changes in the .ui file will delete your changes"""

# Import os library
import os, inspect

# These are the modules required for the guiqwt widgets.
# Import plot widget base class
from guiqwt.pyplot import *
from guiqwt.plot import CurveWidget
from guiqwt.builder import make

import string

# Import system library
import sys

# Import datetime
from datetime import datetime
now = datetime.now()

# Import the visa library
try:
    import visa
    visa_available = True
except:
    visa_available = False

# Import numpy library
import numpy

# Import pylab library 
# It contains some functions necessary to create some of the functions in the used in the plots
from pylab import *

# It makes the text format looks pretty and well-designed
from textwrap import wrap

# Adding navigation toolbar to the figure
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

# Import the PyQt4 modules for all the commands that control the GUI.
# Importing as from "Module" import * implies that everything from that module is not part of this module.
# You do not need to put the module name before its commands
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# This is very important because it imports the GUI created earlier using Qt Designer
# To import the GUI from another python file, it is very simple. Just following the following steps:
# 1. Create an empyty file called __init__.py in the same directory as the GUI file
# 2. If the GUI file and __init__.py file are in the same directory as this file, just type "from .GUIfilename import classname"
# 3. If the GUI file and __init__.py file are in the sub file of this file, then type "from subfilename.GUIfilename import classname"
# classname is the name of the class in the GUI file, usually it should be 'Ui_MainWindow'
from Sub_Scripts.GUI import Ui_MainWindow

# To get the screen dimensions (in pixels) using the standard Python library.
from win32api import GetSystemMetrics
screen_res = [GetSystemMetrics (0), GetSystemMetrics (1)]

import subprocess

from Sub_Scripts.Keithley import Keithley
from Sub_Scripts.Agilent import Agilent
from Sub_Scripts.Magnet import Magnet


continue_check = True
# The class that controls all the operations of the GUI. This is the self class that contains all the functions that control the GUI.
class MyForm(QMainWindow):
    
    # The __init__ function is what is everything the user wants to be initialized when the class is called.
    # Here we shall define the trig functions to corresponding variables.
    # Note that the "self" variable means that the function is part of the class and can be called inside and outside the class.(Although __init__ is special.)
    def __init__(self, parent = None):
        
        self.collect_data_thread = Collect_data()

        # Standard GUI code
        QWidget.__init__(self, parent)

        # All the GUI data and widgets in the Ui_MainWindow() class is defined to self.ui
        # Thus to do anything on the GUI, the commands must go through this variable
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.connect(self.ui.pushButton_update_1, SIGNAL('clicked()'), lambda : self.Update("visa1", self.ui.comboBox_visa_1))
        self.connect(self.ui.pushButton_update_2_1, SIGNAL('clicked()'), lambda : self.Update("visa2_1", self.ui.comboBox_visa_2_1))
        self.connect(self.ui.pushButton_update_2_2, SIGNAL('clicked()'), lambda : self.Update("visa2_2", self.ui.comboBox_visa_2_2))
        self.connect(self.ui.pushButton_update_2_3, SIGNAL('clicked()'), lambda : self.Update("visa2_3", self.ui.comboBox_visa_2_3))
        self.connect(self.ui.pushButton_update_2_4, SIGNAL('clicked()'), lambda : self.Update("visa2_4", self.ui.comboBox_visa_2_4))
        self.connect(self.ui.pushButton_update_2_5, SIGNAL('clicked()'), lambda : self.Update("visa2_5", self.ui.comboBox_visa_2_5))
        self.connect(self.ui.pushButton_update_2_6, SIGNAL('clicked()'), lambda : self.Update("visa2_6", self.ui.comboBox_visa_2_6))
        self.connect(self.ui.pushButton_update_2_7, SIGNAL('clicked()'), lambda : self.Update("visa2_7", self.ui.comboBox_visa_2_7))
        self.connect(self.ui.pushButton_update_2_8, SIGNAL('clicked()'), lambda : self.Update("visa2_8", self.ui.comboBox_visa_2_8))
        self.connect(self.ui.pushButton_update_2_9, SIGNAL('clicked()'), lambda : self.Update("visa2_9", self.ui.comboBox_visa_2_9))
        self.connect(self.ui.pushButton_update_2_10, SIGNAL('clicked()'), lambda : self.Update("visa2_10", self.ui.comboBox_visa_2_10))
        self.connect(self.ui.pushButton_select_1, SIGNAL('clicked()'), lambda : self.Select(self.ui.label_condition_1, "visa1", self.visa1, self.ui.comboBox_device_1, self.ui.comboBox_visa_1, self.ui.label_visa_1, [self.ui.pushButton_select_1, self.ui.pushButton_close_1], self.ui.textEdit_input_1))
        self.connect(self.ui.pushButton_select_2_1, SIGNAL('clicked()'), lambda : self.Select(self.ui.label_condition_2, "visa2_1", self.visa2_1, self.ui.comboBox_device_2, self.ui.comboBox_visa_2_1, self.ui.label_visa_2_1, [self.ui.pushButton_select_2_1, self.ui.pushButton_close_2_1], self.ui.textEdit_input_2))
        self.connect(self.ui.pushButton_select_2_2, SIGNAL('clicked()'), lambda : self.Select(self.ui.label_condition_2, "visa2_2", self.visa2_2, self.ui.comboBox_device_2, self.ui.comboBox_visa_2_2, self.ui.label_visa_2_2, [self.ui.pushButton_select_2_2, self.ui.pushButton_close_2_2], self.ui.textEdit_input_2))
        self.connect(self.ui.pushButton_select_2_3, SIGNAL('clicked()'), lambda : self.Select(self.ui.label_condition_2, "visa2_3", self.visa2_3, self.ui.comboBox_device_2, self.ui.comboBox_visa_2_3, self.ui.label_visa_2_3, [self.ui.pushButton_select_2_3, self.ui.pushButton_close_2_3], self.ui.textEdit_input_2))
        self.connect(self.ui.pushButton_select_2_4, SIGNAL('clicked()'), lambda : self.Select(self.ui.label_condition_2, "visa2_4", self.visa2_4, self.ui.comboBox_device_2, self.ui.comboBox_visa_2_4, self.ui.label_visa_2_4, [self.ui.pushButton_select_2_4, self.ui.pushButton_close_2_4], self.ui.textEdit_input_2))
        self.connect(self.ui.pushButton_select_2_5, SIGNAL('clicked()'), lambda : self.Select(self.ui.label_condition_2, "visa2_5", self.visa2_5, self.ui.comboBox_device_2, self.ui.comboBox_visa_2_5, self.ui.label_visa_2_5, [self.ui.pushButton_select_2_5, self.ui.pushButton_close_2_5], self.ui.textEdit_input_2))
        self.connect(self.ui.pushButton_select_2_6, SIGNAL('clicked()'), lambda : self.Select(self.ui.label_condition_2, "visa2_6", self.visa2_6, self.ui.comboBox_device_2, self.ui.comboBox_visa_2_6, self.ui.label_visa_2_6, [self.ui.pushButton_select_2_6, self.ui.pushButton_close_2_6], self.ui.textEdit_input_2))
        self.connect(self.ui.pushButton_select_2_7, SIGNAL('clicked()'), lambda : self.Select(self.ui.label_condition_2, "visa2_7", self.visa2_7, self.ui.comboBox_device_2, self.ui.comboBox_visa_2_7, self.ui.label_visa_2_7, [self.ui.pushButton_select_2_7, self.ui.pushButton_close_2_7], self.ui.textEdit_input_2))
        self.connect(self.ui.pushButton_select_2_8, SIGNAL('clicked()'), lambda : self.Select(self.ui.label_condition_2, "visa2_8", self.visa2_8, self.ui.comboBox_device_2, self.ui.comboBox_visa_2_8, self.ui.label_visa_2_8, [self.ui.pushButton_select_2_8, self.ui.pushButton_close_2_8], self.ui.textEdit_input_2))
        self.connect(self.ui.pushButton_select_2_9, SIGNAL('clicked()'), lambda : self.Select(self.ui.label_condition_2, "visa2_9", self.visa2_9, self.ui.comboBox_device_2, self.ui.comboBox_visa_2_9, self.ui.label_visa_2_9, [self.ui.pushButton_select_2_9, self.ui.pushButton_close_2_9], self.ui.textEdit_input_2))
        self.connect(self.ui.pushButton_select_2_10, SIGNAL('clicked()'), lambda : self.Select(self.ui.label_condition_2, "visa2_10", self.visa2_10, self.ui.comboBox_device_2, self.ui.comboBox_visa_2_10, self.ui.label_visa_2_10, [self.ui.pushButton_select_2_10, self.ui.pushButton_close_2_10], self.ui.textEdit_input_2))
        self.connect(self.ui.pushButton_close_1, SIGNAL('clicked()'), lambda : self.Close(self.ui.label_condition_1, "visa1", self.visa1, self.ui.label_visa_1, [self.ui.pushButton_select_1, self.ui.pushButton_close_1], self.ui.textEdit_input_1))
        self.connect(self.ui.pushButton_close_2_1, SIGNAL('clicked()'), lambda : self.Close(self.ui.label_condition_2, "visa2_1", self.visa2_1, self.ui.label_visa_2_1, [self.ui.pushButton_select_2_1, self.ui.pushButton_close_2_1], self.ui.textEdit_input_2))
        self.connect(self.ui.pushButton_close_2_2, SIGNAL('clicked()'), lambda : self.Close(self.ui.label_condition_2, "visa2_2", self.visa2_2, self.ui.label_visa_2_2, [self.ui.pushButton_select_2_2, self.ui.pushButton_close_2_2], self.ui.textEdit_input_2))
        self.connect(self.ui.pushButton_close_2_3, SIGNAL('clicked()'), lambda : self.Close(self.ui.label_condition_2, "visa2_3", self.visa2_3, self.ui.label_visa_2_3, [self.ui.pushButton_select_2_3, self.ui.pushButton_close_2_3], self.ui.textEdit_input_2))
        self.connect(self.ui.pushButton_close_2_4, SIGNAL('clicked()'), lambda : self.Close(self.ui.label_condition_2, "visa2_4", self.visa2_4, self.ui.label_visa_2_4, [self.ui.pushButton_select_2_4, self.ui.pushButton_close_2_4], self.ui.textEdit_input_2))
        self.connect(self.ui.pushButton_close_2_5, SIGNAL('clicked()'), lambda : self.Close(self.ui.label_condition_2, "visa2_5", self.visa2_5, self.ui.label_visa_2_5, [self.ui.pushButton_select_2_5, self.ui.pushButton_close_2_5], self.ui.textEdit_input_2))
        self.connect(self.ui.pushButton_close_2_6, SIGNAL('clicked()'), lambda : self.Close(self.ui.label_condition_2, "visa2_6", self.visa2_6, self.ui.label_visa_2_6, [self.ui.pushButton_select_2_6, self.ui.pushButton_close_2_6], self.ui.textEdit_input_2))
        self.connect(self.ui.pushButton_close_2_7, SIGNAL('clicked()'), lambda : self.Close(self.ui.label_condition_2, "visa2_7", self.visa2_7, self.ui.label_visa_2_7, [self.ui.pushButton_select_2_7, self.ui.pushButton_close_2_7], self.ui.textEdit_input_2))
        self.connect(self.ui.pushButton_close_2_8, SIGNAL('clicked()'), lambda : self.Close(self.ui.label_condition_2, "visa2_8", self.visa2_8, self.ui.label_visa_2_8, [self.ui.pushButton_select_2_8, self.ui.pushButton_close_2_8], self.ui.textEdit_input_2))
        self.connect(self.ui.pushButton_close_2_9, SIGNAL('clicked()'), lambda : self.Close(self.ui.label_condition_2, "visa2_9", self.visa2_9, self.ui.label_visa_2_9, [self.ui.pushButton_select_2_9, self.ui.pushButton_close_2_9], self.ui.textEdit_input_2))
        self.connect(self.ui.pushButton_close_2_10, SIGNAL('clicked()'), lambda : self.Close(self.ui.label_condition_2, "visa2_10", self.visa2_10, self.ui.label_visa_2_10, [self.ui.pushButton_select_2_10, self.ui.pushButton_close_2_10], self.ui.textEdit_input_2))
        
        self.axes_1 = None
        self.axes_2 = None
        self.parameters_1 = []
        self.parameters_2 = []
        self.Values_1 = []
        self.Values_2 = []
        self.connect(self.ui.pushButton_plot_1, SIGNAL('clicked()'), lambda : self.Plot_step(self.ui.textEdit_steps_1, self.ui.label_steps_1, self.ui.mplwidget_1, self.axes_1, self.ui.label_condition_1, self.parameters_1, self.Values_1, self.ui.pushButton_clear_1))
        self.connect(self.ui.pushButton_plot_2, SIGNAL('clicked()'), lambda : self.Plot_step(self.ui.textEdit_steps_2, self.ui.label_steps_2, self.ui.mplwidget_2, self.axes_2, self.ui.label_condition_2, self.parameters_2, self.Values_2, self.ui.pushButton_clear_2))
        self.connect(self.ui.pushButton_clear_1, SIGNAL('clicked()'), lambda : self.Clear(self.ui.mplwidget_1, self.axes_1, self.Values_1, self.ui.textEdit_steps_1, self.ui.label_condition_1, self.ui.label_steps_1, self.ui.pushButton_clear_1))
        self.connect(self.ui.pushButton_clear_2, SIGNAL('clicked()'), lambda : self.Clear(self.ui.mplwidget_2, self.axes_2, self.Values_2, self.ui.textEdit_steps_2, self.ui.label_condition_2, self.ui.label_steps_2, self.ui.pushButton_clear_2))
      
        #self.connect(self.ui.pushButton_Start, SIGNAL('clicked()'), self.start)
        #self.connect(self.ui.pushButton_Stop, SIGNAL('clicked()'), self.collect_data_thread.stop)
        #self.connect(self.ui.pushButton_Pause, SIGNAL('clicked()'), self.collect_data_thread.pause)
        #self.connect(self.collect_data_thread, SIGNAL("curve_plot"), self.curvePlots_update)
        #self.connect(self.collect_data_thread, SIGNAL("print"), self.Print_data)
        
        #self.connect(self.ui.textEdit, SIGNAL('textChanged ()'), lambda : self.start_font("C"))
    
        self.Update("visa1", self.ui.comboBox_visa_1)
        self.Update("visa2_1", self.ui.comboBox_visa_2_1)
        self.Update("visa2_2", self.ui.comboBox_visa_2_2)
        self.Update("visa2_3", self.ui.comboBox_visa_2_3)
        self.Update("visa2_4", self.ui.comboBox_visa_2_4)
        self.Update("visa2_5", self.ui.comboBox_visa_2_5)
        self.Update("visa2_6", self.ui.comboBox_visa_2_6)
        self.Update("visa2_7", self.ui.comboBox_visa_2_7)
        self.Update("visa2_8", self.ui.comboBox_visa_2_8)
        self.Update("visa2_9", self.ui.comboBox_visa_2_9)
        self.Update("visa2_10", self.ui.comboBox_visa_2_10)
        
        #self.curve_1 = self.make_curveWidgets(self.ui.curvewidget_1, "r", "black", titles = ["Plot 1", "X (x)", "Y (y)"])

        self.ui.mplwidget_1 = self.make_mplToolBar(self.ui.mplwidget_1, self.ui.widget_1)
        self.ui.mplwidget_2 = self.make_mplToolBar(self.ui.mplwidget_2, self.ui.widget_2)
        
        self.visa1 = None
        self.visa2_1 = None
        self.visa2_2 = None
        self.visa2_3 = None
        self.visa2_4 = None
        self.visa2_5 = None
        self.visa2_6 = None
        self.visa2_7 = None
        self.visa2_8 = None
        self.visa2_9 = None
        self.visa2_10 = None
        
        # Set the visa names of the tabWidget
        # font = QFont()
        # font.setPointSize(8)
        # self.ui.tabWidget_visa.setFont(font)
        # self.ui.tabWidget_visa.setTabText(0, "Visa Name 1")
        # self.ui.tabWidget_visa.setTabText(1, "Visa Name 2")
        # self.ui.tabWidget_visa.setTabText(2, "Visa Name 3")
        # self.ui.tabWidget_visa.setTabText(3, "Visa Name 4")
        # self.ui.tabWidget_visa.setTabText(4, "Visa Name 5")
        # self.ui.tabWidget_visa.setTabText(5, "Visa Name 6")
        # self.ui.tabWidget_visa.setTabText(6, "Visa Name 7")
        # self.ui.tabWidget_visa.setTabText(7, "Visa Name 8")
        # self.ui.tabWidget_visa.setTabText(8, "Visa Name 9")
        # self.ui.tabWidget_visa.setTabText(8, "Visa Name 10")
        
        # Input parameters by string
        # Remember to keep the last one as "Comments: ..." so that the program could see that as an end.
        self.input_string = []
        # self.input_string.append("00 Parameter: 1\n")
        # self.input_string.append("01 Parameter: 1\n")
        # self.input_string.append("02 Parameter: 1\n")
        # self.input_string.append("03 Parameter: 1\n")
        # self.input_string.append("04 Parameter: 1\n")
        # self.input_string.append("05 Parameter: 1\n")
        # self.input_string.append("06 Parameter: 1\n")
        # self.input_string.append("07 Parameter: 1\n")
        # self.input_string.append("08 Parameter: 1\n")
        # self.input_string.append("09 Parameter: 1\n")
        # self.input_string.append("10 Parameter: 1\n")
        # self.input_string.append("11 Parameter: 1\n")
        # self.input_string.append("12 Parameter: 1\n")
        # self.input_string.append("13 Comments: ")
        
        self.Visa_addresses = [["None", "None"], ["Yokogawa GS200", "YOKOGAWA"], ["Agilent 34460A", "Agilent Technologies"], ["Keithley 2450", "KEITHLEY INSTRUMENTS INC."], ["Network Analyzer", "Rohde-Schwarz"], ["Magnet Model 430", "AMERICAN MAGNETICS INC."]]
        self.Visa_input = [["Yokogawa GS200", "Output(Voltage/Current): ", "Measure(Voltage/Current/Resistance/Power): ", "Voltage Limit(Value/Manual): ", "Current Limit(Value/Manual): ", "Output Scaling: "], ["Keithley 2450", "Output(Voltage/Current): ", "Measure(Voltage/Current/Resistance/Power): ", "Voltage Limit(Value/Manual): ", "Current Limit(Value/Manual): ", "Output Scaling: "], ["Agilent 34460A", "Lock-in: ", "Lock-in Sensitivity: ", "Additional Gain: "], ["Magent", "Field Sweep: "]]
    
    def Update(self, signal, comboBoxVisa):
        rm = visa.ResourceManager()
        try:
            alls = rm.list_resources()
        except:
            alls = "No Visa Available."
        if signal == "visa1":
            self.ui.comboBox_visa_1.clear()
        elif signal == "visa2_1":
            self.ui.comboBox_visa_2_1.clear()
        elif signal == "visa2_2":
            self.ui.comboBox_visa_2_2.clear()
        elif signal == "visa2_3":
            self.ui.comboBox_visa_2_3.clear()
        elif signal == "visa2_4":
            self.ui.comboBox_visa_2_4.clear()
        elif signal == "visa2_5":
            self.ui.comboBox_visa_2_5.clear()
        elif signal == "visa2_6":
            self.ui.comboBox_visa_2_6.clear()
        elif signal == "visa2_7":
            self.ui.comboBox_visa_2_7.clear()
        elif signal == "visa2_8":
            self.ui.comboBox_visa_2_8.clear()
        elif signal == "visa2_9":
            self.ui.comboBox_visa_2_9.clear()
        elif signal == "visa2_10":
            self.ui.comboBox_visa_2_10.clear()
        
        for temp in alls:
            if signal == "visa1":
                self.ui.comboBox_visa_1.addItem(temp)
            elif signal == "visa2_1":
                self.ui.comboBox_visa_2_1.addItem(temp)
            elif signal == "visa2_2":
                self.ui.comboBox_visa_2_2.addItem(temp)
            elif signal == "visa2_3":
                self.ui.comboBox_visa_2_3.addItem(temp)
            elif signal == "visa2_4":
                self.ui.comboBox_visa_2_4.addItem(temp)
            elif signal == "visa2_5":
                self.ui.comboBox_visa_2_5.addItem(temp)
            elif signal == "visa2_6":
                self.ui.comboBox_visa_2_6.addItem(temp)
            elif signal == "visa2_7":
                self.ui.comboBox_visa_2_7.addItem(temp)
            elif signal == "visa2_8":
                self.ui.comboBox_visa_2_8.addItem(temp)
            elif signal == "visa2_9":
                self.ui.comboBox_visa_2_9.addItem(temp)
            elif signal == "visa2_10":
                self.ui.comboBox_visa_2_10.addItem(temp)
    
    def Select(self, label_condition, signal, visa_chosen, comboBoxDevice, comboBoxVisa, lineEditVisa, selectClose, textEdit_input):
        visa_address = str(comboBoxVisa.currentText())
        rm = visa.ResourceManager()
        rm.list_resources()
        inst = rm.open_resource(visa_address)
        if not self.Check(inst):
            try:
                inst = rm.open_resource(visa_address, baud_rate = 115200)
            except:
                label_condition.setText("Invalid visa address.")
                lineEditVisa.setText("None.")
                visa_chosen = False
        
        if self.Check(inst):
            visa_name = inst.query("*IDN?")
            name_list = visa_name.split(',')
            first_name = name_list[0]
            print first_name
            if self.is_same(comboBoxDevice, first_name):
                if signal == "visa1":
                    lineEditVisa.setText(visa_name)
                    selectClose[0].setEnabled(False)
                    selectClose[1].setEnabled(True)
                    self.visa1 = inst
                elif signal == "visa2_1":
                    lineEditVisa.setText(visa_name)
                    selectClose[0].setEnabled(False)
                    selectClose[1].setEnabled(True)
                    self.visa2_1 = inst
                elif signal == "visa2_2":
                    lineEditVisa.setText(visa_name)
                    selectClose[0].setEnabled(False)
                    selectClose[1].setEnabled(True)
                    self.visa2_2 = inst
                elif signal == "visa2_3":
                    lineEditVisa.setText(visa_name)
                    selectClose[0].setEnabled(False)
                    selectClose[1].setEnabled(True)
                    self.visa2_3 = inst
                elif signal == "visa2_4":
                    lineEditVisa.setText(visa_name)
                    selectClose[0].setEnabled(False)
                    selectClose[1].setEnabled(True)
                    self.visa2_4 = inst
                elif signal == "visa2_5":
                    lineEditVisa.setText(visa_name)
                    selectClose[0].setEnabled(False)
                    selectClose[1].setEnabled(True)
                    self.visa2_5 = inst
                elif signal == "visa2_6":
                    lineEditVisa.setText(visa_name)
                    selectClose[0].setEnabled(False)
                    selectClose[1].setEnabled(True)
                    self.visa2_6 = inst
                elif signal == "visa2_7":
                    lineEditVisa.setText(visa_name)
                    selectClose[0].setEnabled(False)
                    selectClose[1].setEnabled(True)
                    self.visa2_7 = inst
                elif signal == "visa2_8":
                    lineEditVisa.setText(visa_name)
                    selectClose[0].setEnabled(False)
                    selectClose[1].setEnabled(True)
                    self.visa2_8 = inst
                elif signal == "visa2_9":
                    lineEditVisa.setText(visa_name)
                    selectClose[0].setEnabled(False)
                    selectClose[1].setEnabled(True)
                    self.visa2_9 = inst
                elif signal == "visa2_10":
                    lineEditVisa.setText(visa_name)
                    selectClose[0].setEnabled(False)
                    selectClose[1].setEnabled(True)
                    self.visa2_10 = inst
                label_condition.setText("Visa is selected succefully!")
                for i in range(0, len(self.Visa_input)):
                    if self.Visa_input[i][0] == str(comboBoxDevice.currentText()):
                        for j in range(1, len(self.Visa_input[i])):
                            textEdit_input.append(self.Visa_input[i][j])
            else:
                device_name = str(comboBoxDevice.currentText())
                if device_name == "None":
                    label_condition.setText("No device is chosen.")    
                else:
                    label_condition.setText("Invalid " + str(comboBoxDevice.currentText()) + " address.")
        else:
            label_condition.setText("Invalid " + str(comboBoxDevice.currentText()) + " address.")
            lineEditVisa.setText("None.")
            visa_chosen = False
    
    def is_same(self, comboBoxDevice, first_name):
        name = str(comboBoxDevice.currentText())
        for i in range(0, len(self.Visa_addresses)):
            if self.Visa_addresses[i][0] == name:
                if first_name == self.Visa_addresses[i][1]:
                    return True
        return False 
        
    def Close(self, label_condition, signal, visa_chosen, lineEditVisa, selectClose, textEdit_input):
        label_condition.setText('Visa address is closed')
        lineEditVisa.setText('')
        selectClose[0].setEnabled(True)
        selectClose[1].setEnabled(False)
        if signal == "visa1":
            visa_chosen.close()
            self.visa1 = None
        elif signal == "visa2_1":
            visa_chosen.close()
            self.visa2_1 = None
        elif signal == "visa2_2":
            visa_chosen.close()
            self.visa2_2 = None
        elif signal == "visa2_3":
            visa_chosen.close()
            self.visa2_3 = None
        elif signal == "visa2_4":
            visa_chosen.close()
            self.visa2_4 = None
        elif signal == "visa2_5":
            visa_chosen.close()
            self.visa2_5 = None
        elif signal == "visa2_6":
            visa_chosen.close()
            self.visa2_6 = None
        elif signal == "visa2_7":
            visa_chosen.close()
            self.visa2_7 = None
        elif signal == "visa2_8":
            visa_chosen.close()
            self.visa2_8 = None
        elif signal == "visa2_9":
            visa_chosen.close()
            self.visa2_9 = None
        elif signal == "visa2_10":
            visa_chosen.close()
            self.visa2_10 = None
        textEdit_input.clear()
        
    def Check(self, inst):
        try:
            inst.ask("*IDN?")
            valid = True
        except:
            valid = False
        return valid
    
    def Plot_step(self, textEdit_steps, label_step, mplwidget, axes, label_condition, parameters, Values, pushButton_clear):
        first_available = True
        self.data_available = False
        
        if textEdit_steps.toPlainText() == '':
            label_condition.setText('Please enter start point.')
        else:
            parameters = []
            Values = []
            
            para = str(textEdit_steps.toPlainText())
            para = map(str, para.split('\n'))
            start_point = para[0].split(' ')
            if start_point[0] == 'Start' and len(start_point) == 2:
                if len(para) == 1:
                    first_available = False
                    label_condition.setText('Invalid values enter Peaks and Steps.')
                else:
                    for i in range(1, len(para)):
                        if para[i] != '':
                            try:
                                para[i] = map(float, para[i].split(','))
                                if len(para[i]) != 3:
                                    label_condition.setText('Invalid values entered. Please check line #' + str(i + 1) + '.')
                                    first_available = False
                                    break
                                elif para[i][1] != math.floor(para[i][1]) or para[i][1] < 1:
                                    label_condition.setText('Please enter an integer repeat value in line #' + str(i + 1) + '.')
                                    first_available = False
                                    break
                                else:
                                    parameters.append(para[i])
                                    label_condition.setText('')
                            except Exception, e:
                                first_available = False
                                label_condition.setText('Invalid values entered. Please check line #' + str(i + 1) + '.')
                                break
            else:
                first_available = False
                label_condition.setText('Invalid start point.')
            
            if first_available:   
                repeat_sub_values = []
                
                start = float(start_point[1])
                step = parameters[0][0]
                repeat = int(math.floor(parameters[0][1]))
                peak = parameters[0][2]
                if peak != start and step == 0:
                    label_condition.setText('Invalid values entered. Please check line #' + str(1) + '.')
                else:
                    if peak < start and step > 0:
                        step = -1 * step
                    sub_values = numpy.arange(start, peak + step, step, dtype = 'float')
                    if abs(sub_values[len(sub_values) - 1]) > abs(peak):
                        sub_values[len(sub_values) - 1] = peak
                    if len(parameters) == 1:
                        end = len(sub_values)
                    else:
                        end = len(sub_values) - 1
                    for i in range(0, end):
                        for j in range(0, repeat):
                            repeat_sub_values.append(sub_values[i])
                    Values.append(repeat_sub_values)
                    for i in range(1, len(parameters)):
                        repeat_sub_values = []
                        start = peak
                        step = parameters[i][0]
                        repeat = int(math.floor(parameters[i][1]))
                        peak = parameters[i][2]
                        if peak != start and step == 0:
                            label_condition.setText('Invalid values entered. Please check line #' + str(i + 1) + '.')
                            break
                        elif para[i][1] != math.floor(para[i][1]):
                            label_condition.setText('Please enter an integer repeat value in line #' + str(i + 1) + '.')
                            first_available = False
                            break
                        else:
                            if peak < start and step > 0:
                                step = -1 * step
                            sub_values = numpy.arange(start, peak + step, step, dtype = 'float')
                            if abs(sub_values[len(sub_values) - 1]) > abs(peak):
                                sub_values[len(sub_values) - 1] = peak
                            if i == len(parameters) - 1:
                                end = len(sub_values)
                            else:
                                end = len(sub_values) - 1
                            for i in range(0, end):
                                for j in range(0, repeat):
                                    repeat_sub_values.append(sub_values[i])
                            Values.append(repeat_sub_values)
                            
                    self.data_available = True
                    self.Plot(label_step, mplwidget, axes, Values)
                    label_condition.setText('Array has been plotted')
                    pushButton_clear.setEnabled(True)
    
    def Plot(self, label, mplwidget, axes, Values):
        x_value = []
        y_value = []
        item = 0
        for i in range(0, len(Values)):
            for j in range(0, len(Values[i])):
                x_value.append(item)
                x_value.append(item + 1)
                y_value.append(Values[i][j])
                y_value.append(Values[i][j])
                item += 1
        
        label.setText(str(item))
        axes = self.plot_reset(axes, mplwidget)
        axes.plot(x_value, y_value, marker = '.', linestyle = '-')
        axes.grid()
        axes.set_title("Data File Plot")
        axes.set_xlabel("Steps")
        axes.set_ylabel("Values")
        mplwidget.draw()
    
    def Clear(self, mplwidget, axes, Values, textEdit_steps, label_condition, label_step, pushButton_clear):
        self.data_available = False
        axes = self.plot_reset(axes, mplwidget)
        axes.grid()
        mplwidget.draw()
        Values = []
        textEdit_steps.clear()
        label_condition.setText('')
        label_step.setText('')
        pushButton_clear.setEnabled(False)
        
    def make_curveWidgets(self, curvewidget, color, markerColor, titles):
        curve_temp = make.curve([], [], color = color, marker = "o", markerfacecolor = markerColor, markersize = 5)
        curvewidget.plot.add_item(curve_temp)
        curvewidget.plot.set_antialiasing(True)
        curvewidget.plot.set_titles(titles[0], titles[1], titles[2])
        return curve_temp
    
    def make_mplToolBar(self, mplwidget, widget):
        canvas_mpl = FigureCanvas(mplwidget.figure)
        canvas_mpl.setParent(widget)
        # This is the toolbar widget for the import canvas
        mpl_toolbar = NavigationToolbar(canvas_mpl, mplwidget)
        vbox_ = QVBoxLayout()
        # The matplotlib canvas
        vbox_.addWidget(canvas_mpl)
        # The matplotlib toolbar
        vbox_.addWidget(mpl_toolbar)
        widget.setLayout(vbox_)
        return canvas_mpl
    
    def mplPlots(self):
        self.ui.mplwidget_1.draw()
        self.ui.mplwidget_2.draw()

    def plot_reset(self, axes, mplwidget):
        mplwidget.figure.clear()
        axes = mplwidget.figure.add_subplot(111)
        return axes
    
    def plot_data(self, axes, x, y, titles, mplwidget):
        axes = self.plot_reset(axes, mplwidget)
        axes.plot(x, y, marker = '.', linestyle = '-')
        axes.grid()
        axes.set_title(titles[0])
        axes.set_xlabel(titles[1])
        axes.set_ylabel(titles[2])
        mplwidget.draw()
        
    def start(self):
        instruments = [self.visa1, self.visa2, self.visa3, self.visa4, self.visa5]
        curves = [self.curve_1, self.curve_2, self.curve_3, self.curve_4]
        curveWidgets =[self.ui.curvewidget_1, self.ui.curvewidget_2, self.ui.curvewidget_3, self.ui.curvewidget_4]
        go_on = True
        
        inputted_string = str(self.ui.textEdit.toPlainText())
        input_data = inputted_string.split("Comments:")
        comments = input_data[1]
        
        input_data = input_data[0].split("\n")
        
        inputted_data = []
        
        for i in range(0, len(input_data)):
            for j in range(0, len(self.input_string)):
                if len(input_data[i].split(self.input_string[j].split(":")[0])) > 1:
                    inputted_data.append(input_data[i].split(self.input_string[j].split(":")[0])[1].replace(":", "").replace(" ", ""))
                    print inputted_data
        
        #Make Array
        
        array_start = float(inputted_data[1])
        array_step = float(inputted_data[3])
        array_stop = float(inputted_data[4])
        double_lin = inputted_data[5].upper()
        
        if array_start < array_stop:
            array_1 = numpy.arange(array_start, array_stop + array_step, array_step)
        elif array_start > array_stop:
            array_1 = numpy.arange(array_stop, array_start + array_step, array_step)[::-1]
        
        
        if double_lin == "Y":
            array_2 = array_1[::-1]
            array_sweep = numpy.append(array_1, array_2)
        else:
             array_sweep = array_1
        
        run_program = True
        for i in range(0, len(inputted_data)):
            try:
                if self.inputted_data[i] != inputted_data[i]:
                    run_program = False
                    self.start_font("C")
            except:
                run_program = False
                self.start_font("C")
        
        for i in range(0, len(array_sweep)):
            try:
                if self.array_sweep[i] != array_sweep[i]:
                    run_program = False
                    self.start_font("C")
            except:
                run_program = False
                self.start_font("C")
        
        if not run_program:
            self.inputted_data = inputted_data
            self.array_sweep = array_sweep
            self.ui.curvewidget_1.plot.set_titles("Magnetic Field Steps", "Steps", "Field (T)")
            self.curve_1.set_data(range(0, len(self.array_sweep)), self.array_sweep)
            self.ui.curvewidget_1.plot.do_autoscale()
            self.curve_1.plot().replot()
            self.start_font("S")
            
        elif run_program:
            if str(self.ui.pushButton_Start.text()) == "Start":
                self.start_font("C")
                self.collect_data_thread.input(self.ui, instruments, curves, curveWidgets, go_on, inputted_data, comments, array_sweep, inputted_string, self.input_string)
            else:
                self.start_font("S")

    def curvePlots_update(self, curveInfo):
        curveWidget = curveInfo[0]
        curve = curveInfo[1]
        curveWidget.plot.do_autoscale()
        curve.plot().replot()
    
    def Print_data(self, display_text):
        
        font = QFont()
        font.setPointSize(8)
        self.ui.textEditDisplay.setFont(font)
        self.ui.textEditDisplay.setText(display_text)
    
    def Switch_scale(self, num):
        temp = abs(num)
        if temp >= 1E9:
            scale = [1E-9, "G"]
        elif temp >= 1E6 and temp < 1E9:
            scale = [1E-6, "M"]
        elif temp >= 1E3 and temp < 1E6:
            scale = [1E-3, "k"]
        elif temp >= 1 and temp < 1000:
            scale = [1, ""]
        elif temp >= 1E-3 and temp < 1:
            scale = [1E3, "m"]
        elif temp >= 1E-6 and temp < 1E-3:
            scale = [1E6, "u"]
        elif temp >= 1E-9 and temp < 1E-6:
            scale = [1E9, "n"]
        elif temp < 1E-9:
            scale = [1E12, "p"]
        return scale
    
    def closeEvent(self, event):
        quit_msg = "Do you want to quit the program?"
        reply = QMessageBox.question(self, "Message", quit_msg, QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
            
class Collect_data(QThread):
    def __init__(self, parent = None):
        QThread.__init__(self, parent)
        self.exiting = False

    def input(self, ui, instruments, curves, curveWidgets, go_on, inputted_data, comments, array_sweep, inputted_string, input_string):
        self.ui = ui
        self.lockin_visa = instruments[0]
        self.keithley_visa = instruments[1]
        self.magnet_visa = instruments[2]
        self.curves = curves
        self.curveWidgets = curveWidgets
        self.go_on = go_on
        self.inputted_string = inputted_string
        self.input_string = input_string
        
        
        self.run_num = str(inputted_data[0])
        self.sweep_rate = float(inputted_data[2])
        self.lockin_sens = float(inputted_data[6])
        self.currBias_resis = float(inputted_data[7])
        self.lockin_voltage = float(inputted_data[8])
        self.currBias_curr = self.lockin_voltage/self.currBias_resis
        self.volt_gain = float(inputted_data[9])
        self.user = str(inputted_data[10])
        self.file_name = str(inputted_data[11])
        self.timeStamp = str(inputted_data[12]).upper()
        self.comments = comments
        self.Array = array_sweep
        
        self.Gate_Volt = []
        self.Gate_Curr = []
        self.Field = []
        self.Device_Volt = []
        self.Device_Curr = []
        self.Device_Cond = []
        self.Device_Resis = []
        
        #self.run()
        self.start()
    
    def stop(self):
        self.stop_collecting = True
        self.pause_collecting = False
        self.ui.label_condition.setText('Stopped.')
        self.ui.pushButton_Start.setEnabled(True)
        self.ui.pushButton_Pause.setEnabled(False)
        self.ui.pushButton_Stop.setEnabled(False)
    
    def pause(self):
        if self.pause_collecting:
            self.read_textEditIn()
            self.ui.label_condition.setText('Running...')
            self.ui.pushButton_Pause.setText("Pause")
            self.pause_collecting = False
        else:
            self.ui.label_condition.setText('Paused. Click continue to run.')
            self.ui.pushButton_Pause.setText("Continue")
            self.pause_collecting = True
            
    def run(self):
        import time
        
        if self.timeStamp == "Y":
            file_name = self.run_num + "_" + self.file_name + "_" + str(time.ctime().replace(":", "-").replace(" ", "_"))
        else:
            file_name = self.run_num + "_" + self.file_name
            
        self.write_file = open(file_name + ".txt", 'a')
        self.write_file.write("User: " + self.user + "\n\n")
        self.write_file.write(self.inputted_string + "\n\n")
        self.write_file.write("Collected Data\n")
        self.write_file.write("Time, Field, Gate Voltage, Gate Current, Device Voltage, Device Current, Device Conductane, Device Resistance\n")
        self.write_file.write("s, T, V, A, V, A, S, Ohms\n")
        


        self.t_plot = []
        date_value = []
        date_and_time = []
        self.s_value = []
        temp = 0
        start_time = time.time()
        
        Magnet().Conf_ramp_rate_field(self.magnet_visa, self.sweep_rate)
        Magnet().Ramp(self.magnet_visa)
        
        
        self.pause_collecting = False
        self.stop_collecting = False
        self.ui.pushButton_Start.setEnabled(False)
        self.ui.pushButton_Pause.setEnabled(True)
        self.ui.pushButton_Stop.setEnabled(True)
        
        while True:
            if self.go_on:
                if self.stop_collecting:
                    self.ui.label_condition.setText('Reading stoped.')
                    break
                
                if self.pause_collecting:
                    self.ui.label_condition.setText('Reading paused.')                  
                    
                else:
                    if temp == len(self.Array):
                        self.ui.label_condition.setText('Scan complete.')
                        break
                    
                    
                    self.ui.label_condition.setText('Reading...')
                    
                    #start_time = time.time()
                    
                    print self.Array[temp]
                    Magnet().Conf_field(self.magnet_visa, self.Array[temp])
                    Magnet().Ramp(self.magnet_visa)
                    
                    temp_field = None
                    while temp_field != "Set":
                        if self.stop_collecting:
                            break
                        time.sleep(0.1)
                        Magnet().Magnet_field(self.magnet_visa)
                        temp_field = float(Magnet().Read(self.magnet_visa))
                        print temp_field
                        print abs(temp_field - self.Array[temp])
                        if abs(temp_field - self.Array[temp]) < 1e-8:
                            curr_field = temp_field
                            temp_field = "Set"
                    
                    
                    #Keithley().set_voltage(self.keithley_visa, self.Array[temp])
                    #Keithley().read_data_write(self.keithley_visa)
                    #gate_data = Keithley().read_data_read(self.keithley_visa)
                    #while float(gate_data[0]) > 1e10:
                        #Keithley().read_data_write(self.keithley_visa)
                        #gate_data = Keithley().read_data_read(self.keithley_visa)
                    
                    Keithley().read_data_write(self.keithley_visa)
                    gate_data = Keithley().read_data_read(self.keithley_visa)
                    Agilent().read_data_write(self.lockin_visa)
                    DeviceVolt = float(Agilent().read_data_read(self.lockin_visa))
                    
                    DeviceVolt = DeviceVolt*self.lockin_sens/(10.0*self.volt_gain)
                    
                    end_time = time.time()
                    self.during = end_time - start_time
                    self.t_plot.append(self.during)
                    
                    self.write_file.write(str(self.during) + "," + str(curr_field)+ "," + str(float(gate_data[0])) + "," + str(float(gate_data[1])) + "," + str(DeviceVolt)+ "," + str(self.currBias_curr) + "," + str(self.currBias_curr/DeviceVolt) + "," + str(DeviceVolt/self.currBias_curr)+ "\n")
                    
                    self.Gate_Volt.append(float(gate_data[0]))
                    self.Gate_Curr.append(float(gate_data[1])*1e12) #pA
                    self.Field.append(curr_field) #T
                    self.Device_Curr.append(self.currBias_curr*1e9) #nA
                    self.Device_Volt.append(DeviceVolt*1e6) #uV
                    self.Device_Resis.append(DeviceVolt/self.currBias_curr*1e-3) #kOhms
                    self.Device_Cond.append(self.currBias_curr/DeviceVolt*1e6) #uS
                    
                    self.s_value.append(temp)
                    
                    self.setup_plot(self.curveWidgets[0], self.curves[0], [self.s_value, self.Field], ["Magnetic Field Steps", "Steps", "Field (T)"])
                    self.setup_plot(self.curveWidgets[1], self.curves[1], [self.Field, self.Device_Cond], ["Device Conductance", "Field (T)", "Conductance (uS)"])
                    self.setup_plot(self.curveWidgets[2], self.curves[2], [self.Field, self.Device_Volt], ["Device Voltage", "Field (T)", "Voltage (uV)"])
                    self.setup_plot(self.curveWidgets[3], self.curves[3], [self.Field, self.Device_Curr], ["Device Current", "Field (T)", "Current (nA)"])
                    
                    
                    display_text = ""
                    display_text = display_text + "Time: " + str(round(self.during, 3)) + " s\n\n"
                    display_text = display_text + "Field: " + str(round(float(curr_field), 3)) + " T\n"
                    display_text = display_text + "Gate Voltage: " + str(round(float(gate_data[0]), 3)) + " V\n"
                    display_text = display_text + "Gate Current: " + str(round(float(gate_data[1])*1e12, 3)) + " pA\n\n"
                    display_text = display_text + "Device Voltage: " + str(round(DeviceVolt*1e6, 3)) + " uV\n"
                    display_text = display_text + "Device Current: " + str(round(self.currBias_curr*1e9, 3)) + " nA\n"
                    display_text = display_text + "Device Resistance: " + str(round(DeviceVolt/self.currBias_curr*1e-3, 3)) + " kOhms\n"
                    display_text = display_text + "Device Conductance: " + str(round(self.currBias_curr/DeviceVolt*1e6, 3)) + " uS\n"
                    
                    self.emit(SIGNAL("print"), display_text) #, self.during, float(self.data[0]), float(self.data[1]))
                    
                    now = datetime.datetime.now()
                    date = '%s-%s-%s' % (now.year, now.month, now.day)
                    current_time = '%s:%s:%s' % (now.hour, now.minute, now.second)
                    self.date_and_time = date + ' ' + current_time
                    date_value.append(self.date_and_time)
                    
                    temp += 1
        
        Magnet().Pause(self.magnet_visa)
        self.ui.pushButton_Start.setEnabled(True)
        self.ui.pushButton_Pause.setEnabled(False)
        self.ui.pushButton_Stop.setEnabled(False)
        self.write_file.close()
        
        file_par = open("parameters.txt", "w").write(str(self.ui.textEdit.toPlainText()))
        file_par.close()
        
    def setup_plot(self, curveWidget, curve, data, titles):
        curveWidget.plot.set_titles(titles[0], titles[1], titles[2])
        curve.set_data(data[0], data[1])
        self.emit(SIGNAL("curve_plot"), [curveWidget, curve])
    
    def plot_reset(self, axes, mplwidget):
        mplwidget.figure.clear()
        axes = mplwidget.figure.add_subplot(111)
        return axes
        
    def read_textEditIn(self):
        inputted_string = str(self.ui.textEdit.toPlainText())
        input_data = inputted_string.split("Comments:")
        comments = input_data[1]
        
        input_data = input_data[0].split("\n")
        
        inputted_data = []
        
        for i in range(0, len(input_data)):
            for j in range(0, len(self.input_string)):
                if len(input_data[i].split(self.input_string[j].split(":")[0])) > 1:
                    inputted_data.append(input_data[i].split(self.input_string[j].split(":")[0])[1].replace(":", "").replace(" ", ""))
        
        if self.lockin_sens != float(inputted_data[6]):
            self.lockin_sens = float(inputted_data[6])
            self.write_file.write("\nNew Lock-in Sens: " + str(self.lockin_sens) + "\n\n")
        if self.currBias_resis != float(inputted_data[7]):
            self.currBias_resis = float(inputted_data[7])
            self.currBias_curr = self.lockin_voltage/self.currBias_resis
            self.write_file.write("\nNew Current Bias Resistor: " + str(self.currBias_resis) + "\n\n")
        if self.lockin_voltage != float(inputted_data[8]):
            self.lockin_voltage = float(inputted_data[8])
            self.currBias_curr = self.lockin_voltage/self.currBias_resis
            self.write_file.write("\nNew Lock-in Voltage Output: " + str(self.lockin_voltage) + "\n\n")
        if self.volt_gain != float(inputted_data[9]):
            self.volt_gain = float(inputted_data[9])
            self.write_file.write("\nNew Lock-in Voltage Gain: " + str(self.volt_gain) + "\n\n")
        
    
    
    def Switch_scale(self, num):
        temp = abs(num)
        if temp >= 1E9:
            scale = [1E-9, "G"]
        elif temp >= 1E6 and temp < 1E9:
            scale = [1E-6, "M"]
        elif temp >= 1E3 and temp < 1E6:
            scale = [1E-3, "k"]
        elif temp >= 1 and temp < 1000:
            scale = [1, ""]
        elif temp >= 1E-3 and temp < 1:
            scale = [1E3, "m"]
        elif temp >= 1E-6 and temp < 1E-3:
            scale = [1E6, "u"]
        elif temp >= 1E-9 and temp < 1E-6:
            scale = [1E9, "n"]
        elif temp < 1E-9:
            scale = [1E12, "p"]
            
        return scale
    
    def __del__(self):
        self.exiting = True
        self.wait()
# The if statement is to check whether this module is the self module and in case that it is imported by another module
# If it is the self module then it starts the GUI under if condition
# This in case it is being imported, then it will not immediately start the GUI upon being imported
if __name__ == "__main__":
    # Opens the GUI
    app = QApplication(sys.argv)
    myapp = MyForm()

    # Shows the GUI
    myapp.show()

    # Exits the GUI when the x button is clicked
    sys.exit(app.exec_())
        
        

        
