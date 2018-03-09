# -*- coding: utf-8 -*-
# Copyright (c) 2018, libracore GmbH and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _

class EN610342(Document):
    def set_mounting(self):
        if not self.material:
            frappe.msgprint( _("Please select a material") )
            return
        
        material = frappe.get_doc("Material", self.material)
        if material.diameter and (not material.diameter == 0):
            number_of_bundles, number_of_cables, rotation = calculate_mounting(material.diameter)
        else:
            frappe.msgprint( _("Invalid diameter. Please check material.") )
            return
            
        self.number_of_bundles = number_of_bundles
        self.number_of_cables = number_of_cables
        self.rotation = rotation
        self.save()
        return

""" This function is used to import and normalise data from the data logger 
    raw: string with the data
    doc_name: name of this document record
    env_T: environmental temperature, in °C
    env_P: environmental pressure, in Pa
    env_rh: environmental relative humidity, in %
"""
@frappe.whitelist()
def convert_data(raw, doc_name, env_T=20, env_P=96000, env_rh=50):
    # get parent document
    doc = frappe.get_doc("EN 61034 2", doc_name)
    
    # prepare input data
    raw_lines = raw.split('\n')
    """ field definition: (V1)          (V2)
        A-0: full time					full time
        B-1: T3 (duct) [°C]				0.0 - TAMB_50399
        C-2: Flow Cavi 					0.1 - Tduct1_50399 {T duct 1}
        D-3: Fumi Cavi					0.2 - Tduct3_50399 {T duct 2}
        E-4: T1 (duct) [°C]				0.5 - Flow_50399 {DPT}
        F-5: T2 (duct) [°C]				0.6 - SMOKE_50399 {transmission}
        G-6: O2 [%]						0.7 - AirIN_50399
        H-7: CO2 [%]					0.8 - T_IN_50399
        I-8: CO [%]						1.0 - Gas O2 {O2}
        J-9: Gas						1.1 - Gas CO2 {CO2}
        K-10: Gas						1.2 - Gas CO {CO}
        L-11: Burner output (Q) [kW]	1.4 - Gas used
        M-12: T (duct) [°C]				80.1 - Gas_Burner_50399 {gad mfm}
        N-13: Flow duct					80.2 - Qburner_50399 {Q burner}
        O-14: RHR calib					80.3 - Tduct_50399
        P-15: RHR test					80.4 - FlowDuct_50399
        Q-16: CO ppm					80.10 - RHR_Cal_50399
        R-17: Smoke [%]					80.11 - RHR_Test_50399
        S-18:							80.12 - CO_net_50399
        T-19:							80.13 - Epthane_RHR_50399
        U-20:							80.14 - Meth_RHR_50399
        V-21:							80.15 - Flow_IN_50399
        W-22:							80.16 - air_IN_50399
        X-23:
        Y-24:
        Z-25:
    """ 	
    # configuration of columns of raw file
    column_config = { 
        'time': 0,
        'burner_output': 13, 
        'gas_mfm': 12, 
        'dpt': 4,
        'transmission': 5,
        'o2': 8,
        'co2': 9,
        'amb_t': -1,
        't_duct_1': 2,
        't_duct_2': 3,
        't_duct_3': -1,
        'co': 10,
        'apt': -1,
        'air_mfm': -1,
        'pdm': -1,
        'pdc': -1
    }
    
    # compile the data vectors
    time = ""
    transmittance = ""
    temperature = ""
    min_transmittance = 100
    max_temperature = 0
    end_time = 0
    fields = raw_lines[1].split(',')
    starting_temperature = fields[column_config['t_duct_1']]
    for i in range(1, len(raw_lines)):
        fields = raw_lines[i].split(',')
        if len(fields) > 4:
            end_time = i * 3
            time += "{0},".format(end_time)
            _transmittance = fields[column_config['transmission']]
            transmittance += "{0},".format(_transmittance)
            if _transmittance < min_transmittance:
                min_transmittance = _transmittance
            _temperature = fields[column_config['t_duct_1']]
            temperature += "{0},".format(_temperature)
            if _temperature > max_temperature:
                max_temperature = _temperature
            
    # remove trailing comma
    time = time[:-1]
    transmittance = transmittance[:-1]
    temperature = temperature[:-1]
    
    # thin out data for chart (only 1 data point per minute, 1/20)
    times = time.split(',')
    transmittances = transmittance.split(',')
    temperatures = temperature.split(',')
    time = ""
    transmittance = ""
    temperature = ""
    for i in range(0, len(times), 20):
        time += "{0},".format(times[i])
        transmittance += "{0},".format(transmittances[i])
        temperature += "{0},".format(temperatures[i])
        
    # remove trailing comma
    time = time[:-1]
    transmittance = transmittance[:-1]
    temperature = temperature[:-1]
            
    # store output to document
    doc.raw_time = time
    doc.raw_transmittance = transmittance
    doc.raw_temperature = temperature
    doc.min_transmittance = min_transmittance
    doc.starting_temperature = starting_temperature
    doc.maximum_temperature = max_temperature
    doc.end_time = end_time
    doc.save()
    
    return { 'output': 'Raw data imported and calculated' }
    
@frappe.whitelist()
def calculate_mounting(diameter=5.0):
    diameter = float(diameter)
    if diameter <= 5:
        number_of_bundles = int(45 / (3 * diameter))
        number_of_cables = 7 * number_of_bundles
        rotation_20 = int(20 * diameter)
        rotation_30 = int(30 * diameter)
        rotation = "{0} - {1} mm".format(rotation_20, rotation_30)
    else:
        number_of_bundles = 0
        if (diameter > 40):
            number_of_cables = 1
        elif (diameter > 20):
            number_of_cables = 2
        elif (diameter > 10):
            number_of_cables = 3
        else:
            number_of_cables = int(45/diameter)
        rotation = "-"
    return number_of_bundles, number_of_cables, rotation
