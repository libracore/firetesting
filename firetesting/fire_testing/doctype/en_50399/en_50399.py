# -*- coding: utf-8 -*-
# Copyright (c) 2018, libracore GmbH and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import math

class EN50399(Document):
    def onload(self):
        """Runs when document is loaded (not created)"""
        pass

""" This function will import a transfer file content into the test record """
@frappe.whitelist()
def import_transfer_file(content, doc_name):
    # separate content into lines
    lines = content.split("\n")
    if len(lines) > 0:
        # find out if separator is tab or comma
        fields = lines[0].split('\t')
        if len(fields) > 16:
            separator = "\t"
        else:
            fields = content.split(',')
            if len(fields) > 16:
                separator = ","
            else:
                separator = ";"
                
        # read out values
        # initialise document
        doc = frappe.get_doc("EN 50399", doc_name)
        doc.date_of_test = assert_date(lines[5].split(separator)[1])
        doc.operator = lines[35].split(separator)[1]
        doc.pressure = lines[41].split(separator)[1]
        doc.relative_humidity = lines[42].split(separator)[1]
        doc.temperature = lines[43].split(separator)[1]

        raw = ""
        for line in lines:
            raw = raw + separator.join(line.split(separator)[2:]) + "\n"
            
        doc.logger_data = raw
        
        # store values
        doc.save()
        
    return { 'output': 'Transfer file imported' }

def assert_date(date_str):
    if "/" in date_str:
        # format as  in DD/MM/YYYY
        parts = date_str.split("/")
        return "{0}-{1}-{2}".format(parts[2], parts[1], parts[0])
    elif "." in date_str:
        # format as  in DD.MM.YYYY
        parts = date_str.split(".")
        return "{0}-{1}-{2}".format(parts[2], parts[1], parts[0])
    else:
        # format as  in YYYY-MM-DD
        return date_str
    
""" This function will export a transfer file from the test record """
@frappe.whitelist()
def export_transfer_file(doc_name):
    content = ""
    # initialise document
    doc = frappe.get_doc("EN 50399", doc_name)
    lines = doc.logger_data.split("\n")
    # define length of file to be at least 100 lines (or as many as data points)
    if (len(lines) - 1) > 100:
        length = len(lines) - 1
    else:
        length = 100
    # initialise lists for first two columns
    info_head_lines = [""] * length
    info_content_lines = [""] * length
    # initialise data for general information
    info_head_lines[0] = "General information"
    info_head_lines[2] = "Test"
    info_head_lines[3] = "Standard used"
    info_content_lines[3] = "EN 50399"
    info_head_lines[5] = "Date of test"
    info_content_lines[5] = get_normed_date(doc.date_of_test) #16/04/2015
    info_head_lines[7] = "Product"
    info_head_lines[8] = "Product Identification"
    material = frappe.get_doc("Material", doc.material)
    info_content_lines[8] = material.description
    info_head_lines[9] = "Specimen number"
    info_content_lines[9] = material.name
    info_head_lines[10] = "E' (MJ/m³)"
    #17.2
    info_head_lines[11] = "Sponsor"
    #Sponsor of test
    info_head_lines[12] = "Date of arrival"
    info_content_lines[12] = get_normed_date(material.date_of_arrival) #14/04/2015
    info_head_lines[13] = "Manufacturer"
    info_content_lines[13] = material.customer
    info_head_lines[14] = "Cable diameter (mm)"
    info_content_lines[14] = material.diameter
    info_head_lines[15] = "NMV (l/m)"
    #0.76
    info_head_lines[16] = "Largest conductor size (mm²)"
    #1
    info_head_lines[17] = "Total number of cables"
    #55
    info_head_lines[18] = "Number of layers"
    #1
    info_head_lines[19] = "Number of burners"
    #1
    info_head_lines[20] = "Mounting"
    #touching
    info_head_lines[21] = "Backing board on ladder? {Y/N}"
    if doc.backing_board == 1:
        info_content_lines[21] = "Yes"
    else:
        info_content_lines[21] = "No"
    info_head_lines[22] = "Backing board"
    #Supalux
    info_head_lines[23] = "Flame application time (s)"
    #1200
    info_head_lines[25] = "Specifications:"
    info_content_lines[25] = doc.test_apparatus
    info_head_lines[26] = "Flow profile kt (-)"
    #0.86
    info_head_lines[27] = "Probe constant kp (-)"
    #1.08
    info_head_lines[28] = "Duct diameter (m)"
    #0.4
    info_head_lines[29] = "O2 calibration delay time (s)"
    #24
    info_head_lines[30] = "CO2 calibration delay time (s)"
    #30
    info_head_lines[31] = "CO calibration delay time (s)"
    #30
    info_head_lines[33] = "Laboratory"
    info_head_lines[34] = "Laboratory name"
    info_content_lines[34] = frappe.defaults.get_global_default("company")
    info_head_lines[35] = "Operator"
    info_content_lines[35] = doc.operator
    info_head_lines[36] = "Filename"
    #C:\CAB_SOFT\DATA\CS_Demo.csv
    info_head_lines[37] = "Report identification"
    info_content_lines[37] = doc.title
    info_head_lines[40] = "Pre-test conditions"
    info_head_lines[41] = "Barometric pressure (Pa)"
    info_content_lines[41] = doc.pressure
    info_head_lines[42] = "Relative humidity (%)"
    info_content_lines[42] = doc.relative_humidity
    info_head_lines[43] = "Ambient temperature (°C)"
    info_content_lines[43] = doc.temperature
    info_head_lines[51] = "Conditioning"	
    info_head_lines[52] = "Conditioned? {Y/N}"
    #No
    info_head_lines[53] = "Conditioning temperature (°C)"
    #23
    info_head_lines[54] = "Conditioning RH (%)"
    #50
    info_head_lines[55] = "{Constant mass/fixed period}"
    #Fixed period
    info_head_lines[56] = "Time interval (hours)"
    info_head_lines[57] = "Mass 1 (g)"
    info_head_lines[58] = "Mass 2 (g)"
    info_head_lines[60] = "Comments"
    info_head_lines[61] = "Pre-test comments"
    #Comments entered before test
    info_head_lines[62] = "After-test comments"
    #After-test comments will be printed here
    info_head_lines[63] = "FDP flaming <= 10s {Y/N}"
    #No
    info_head_lines[64] = "FDP flaming > 10s {Y/N}"
    #No
    info_head_lines[65] = "Falling of specimen parts {Y/N}"
    #Yes
    info_head_lines[66] = "Smoke not entering hood {Y/N}"
    #No
    info_head_lines[67] = "Damage length (m)"
    info_content_lines[67] = str(doc.damage_zone_front / 1000)
    info_head_lines[75] = "HRR level (kW)"
    
    # combine general information and data vectors
    for i in range(0, length):
        content = (content + 
            "{0},{1},{2}\n".format(info_head_lines[i], info_content_lines[i], lines[i]))
        
    return { 'content': content }
    
def get_normed_date(date):
    # converts YYYY-MM-DD to DD/MM/YYYY
    if "-" in str(date):
        date_parts = str(date).split("-")
        return "{0}/{1}/{2}".format(date_parts[2], date_parts[1], date_parts[0])
    else:
        return date

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
    doc = frappe.get_doc("EN 50399", doc_name)
    
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
    # find start point: where burner output > 15 kW
    for i in range(1, len(raw_lines) - 1):
        fields = raw_lines[i].split(',')
        if float(fields[column_config.burner_output]) > 15:
            start_line_index = i
            break
    
    # compile the data vectors
    lines = "time (s),Gas MFM (mg/s),DPT (Pa),Transmission (%),O2 (%),CO2 (%),Amb T (K),T_Duct1 (K),T_Duct2 (K),T_Duct3 (K),CO (%),APT (kPa),Air MFM (mg/s),PDM (-),PDC (-)\n"
    lines = lines + "\n"
    for i in range(0, (1200/3) + 1):
        fields = raw_lines[start_line_index + i].split(',')
        lines = lines + "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14}\n".format(
            3 * i,                                              # 0 - time [sec]
            fields[column_config.gas_mfm],                      # 1 - Gas MFM [mg/s]
            fields[column_config.dpt],                          # 2 - DPT (deltaP) [Pa]
            fields[column_config.transmission],                 # 3 - Transmission [%]
            fields[column_config.o2],                           # 4 - O2 [%]
            fields[column_config.co2],                          # 5 - CO2 [%]
            kelvin(float(env_T)),                               # 6 - T (ambient) [K]
            kelvin(float(fields[column_config.t_duct_1])),      # 7 - T (duct, 1) [K]
            kelvin(float(fields[column_config.t_duct_2])),      # 8 - T (duct, 2) [K]
            -1,                           						# 9 - T (duct, 3) [K]
            (float(column_config.co) / 100000),                 # 10- CO [%]                                                                                                
            (float(env_P) / 1000),                              # 11- P (ambient) [kPa]
            -1,                                                 # 12- Air MFM [mg/s]
            -1,                                                 # 13- PDM
            -1,                                                 # 14- PDC                                                
            )
        
    # store output to document
    doc.logger_data = lines
    doc.save()
    
    # compute results
    output = calculate_results(doc_name)
    
    return output

""" This function will recalculate the results """
@frappe.whitelist()
def calculate_results(doc_name):
    # get parent document
    doc = frappe.get_doc("EN 50399", doc_name)
    
    # prepare data 
    lines = doc.logger_data.split('\n')
    
    # compute results 
    trace = ""
    # fraction of H2O
    env_rh = doc.relative_humidity
    env_P = doc.pressure
    env_T = doc.temperature
    if env_P == 0:
        env_P = 96000
    x_a_H2O = (float(env_rh) / 100) * (1 / float(env_P)) * (math.exp(23.2) / math.exp(3816/(kelvin(float(env_T))-46)))
    trace = trace + "x_a_H2O: {0}\n".format(x_a_H2O)
    # read constants
    if not doc.test_apparatus:
        return { 'output': 'Test apparatus not set' }
    apparatus = frappe.get_doc("Test Apparatus", doc.test_apparatus)
    kt = apparatus.en50399_kt
    kp = apparatus.en50399_kp
    d = apparatus.en50399_d
    A = math.pi * math.pow((d/2), 2)
    trace = trace + "kt: {0}, kp: {1}, A: {2} m2\n".format(kt, kp, A)
    initial_data_fields = lines[2].split(',')
    x_0_O2 = float(initial_data_fields[4])
    x_a_O2 = x_0_O2 * (1 - x_a_H2O)
    x_0_CO2 = float(initial_data_fields[5])
    q_burner = float(doc.burner_output)             # in kW
    E_1 = 17200                                     # in kJ/m3
    E_C3H8 = 16800                                  # in kJ/m3
    alpha = 1.105                                   # expansion factor
    # build up vectors and compute volume flow
    t = []                                          # time vector
    dp = []                                         # delta pressure [Pa]
    V = []                                          # volume flow vector
    t_gas = []                                      # exhaust gas temperature [K] (T duct 2)
    transmission = []                               # transmission [%]
    oxy_depletion = []                              # oxygen depletion factor [-]
    q = []                                          # heat release [kW]
    for i in range(2, len(lines)):
        fields = lines[i].split(',')
        if len(fields) > 1:
            t.append(int(fields[0]))
            dp.append(float(fields[2]))
            t_gas.append(float(fields[8]))
            transmission.append(float(fields[3]))
            diff = dp[-1] / t_gas[-1]
            if diff < 0:
                diff = 0
            # volume flow
            _v = 22.4 * (A * kt / kp) * math.sqrt(diff)
            V.append(_v)
            x_CO2 = float(fields[5])
            x_O2 = float(fields[4])
            _oxy_dep = (x_0_O2 * (1 - x_CO2) - x_O2 * (1 - x_0_CO2)) / (x_0_O2 * (1 - x_O2 - x_CO2))
            oxy_depletion.append(_oxy_dep)
            # heat release
            _q = E_1 * _v * x_a_O2 * (_oxy_dep / (_oxy_dep * (alpha - 1) + 1)) - (E_1 / E_C3H8) * q_burner
            q.append(_q)
            
    trace = trace + "t: {0}\n".format(t)
    trace = trace + "dp: {0}\n".format(dp)
    trace = trace + "trsm: {0}\n".format(transmission)
    trace = trace + "V: {0}\n".format(V)
    trace = trace + "oxy_dep: {0}\n".format(oxy_depletion)
    trace = trace + "q: {0}\n".format(q)
                
    # store output to document
    doc.calculation_trace = trace
    doc.kt = kt
    doc.kp = kp
    doc.a = A
    doc.trace = trace
    doc.save()
    
    return { 'output': 'Raw data imported and calulcated' }
    
def kelvin(temp):
    return temp + 273.15
