# -*- coding: utf-8 -*-
# Copyright (c) 2018, libracore GmbH and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import math
from frappe import _

class EN50399(Document):
    def onload(self):
        """Runs when document is loaded (not created)"""
        pass
        
    def set_mounting(self):
        if not self.material:
            frappe.msgprint( _("Please select a material") )
            return
        
        material = frappe.get_doc("Material", self.material)
        if material.diameter and (not material.diameter == 0):
            number_of_cables, width, spacing, request_length = calculate_mounting(material.diameter)
        else:
            frappe.msgprint( _("Invalid diameter. Please check material.") )
            return
            
        self.material_length = width
        self.number_of_cables = number_of_cables
        self.spacing = spacing
        self.required_cable = request_length
        self.save()
        return

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
        if float(fields[column_config['burner_output']]) > 15:
            start_line_index = i
            break
    
    # compile the data vectors
    lines = "time (s),Gas MFM (mg/s),DPT (Pa),Transmission (%),O2 (%),CO2 (%),Amb T (K),T_Duct1 (K),T_Duct2 (K),T_Duct3 (K),CO (%),APT (kPa),Air MFM (mg/s),PDM (-),PDC (-)\n"
    lines = lines + "\n"
    for i in range(0, (1200/3) + 1):
        fields = raw_lines[start_line_index + i].split(',')
        lines = lines + "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14}\n".format(
            3 * i,                                              # 0 - time [sec]
            fields[column_config['gas_mfm']],                   # 1 - Gas MFM [mg/s]
            fields[column_config['dpt']],                       # 2 - DPT (deltaP) [Pa]
            fields[column_config['transmission']],              # 3 - Transmission [%]
            fields[column_config['o2']],                        # 4 - O2 [%]
            fields[column_config['co2']],                       # 5 - CO2 [%]
            kelvin(float(env_T)),                               # 6 - T (ambient) [K]
            kelvin(float(fields[column_config['t_duct_1']])),   # 7 - T (duct, 1) [K]
            kelvin(float(fields[column_config['t_duct_2']])),   # 8 - T (duct, 2) [K]
            -1,                           						# 9 - T (duct, 3) [K]
            (float(column_config['co']) / 100000),              # 10- CO [%]                                                                                                
            (float(env_P) / 1000),                              # 11- P (ambient) [kPa]
            -1,                                                 # 12- Air MFM [mg/s]
            -1,                                                 # 13- PDM
            -1,                                                 # 14- PDC                                                
            )
    
    # determine transmission baseline in first 60 seconds (20 readings)
    i0 = 0.0
    for i in range(1, 21):
        fields = raw_lines[i].split(',')
        i0 = i0 + float(fields[column_config['transmission']])
    i0 = i0 / 20
    
    # store output to document
    doc.logger_data = lines
    doc.i0 = i0
    doc.raw_data_cutoff = start_line_index
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
    if doc.logger_data == None:
        frappe.msgprint( _("Please make sure that all data is available (missing logger data)") )
        return
    lines = doc.logger_data.split('\n')
    column_config = { 'time': 0,
        'gas_mfm': 1,
        'dpt': 2,
        'transmission': 3,
        'o2': 4,
        'co2': 5,
        't_amb': 6,
        't_duct_1': 7,
        't_duct_2': 8,
        't_duct_3': 9,
        'co': 10,
        'p_amb': 11,
        'air_mfm': 12,
        'pdm': 13,
        'pdc': 14
    }

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
    x_0_O2 = (float(initial_data_fields[column_config['o2']]) / 100)
    x_a_O2 = x_0_O2 * (1 - x_a_H2O)
    x_0_CO2 = (float(initial_data_fields[column_config['co2']]) / 100)
    trace = trace + "x_0_O2: {0}, x_a_O2: {1}, x_0_CO2: {2}\n".format(
        x_0_O2, x_a_O2, x_0_CO2)
    q_burner = float(doc.burner_output)             # in kW
    E_1 = 17200                                     # in kJ/m3
    E_C3H8 = 16800                                  # in kJ/m3
    alpha = 1.105                                   # expansion factor
    i0 = doc.i0                                     # transmission baseline
    # build up vectors and compute volume flow
    time = []                                       # time vector
    dp = []                                         # delta pressure [Pa]
    V = []                                          # volume flow vector
    t_gas = []                                      # exhaust gas temperature [K] (T duct 2)
    transmission = []                               # transmission [%]
    min_transmission = 100                          # minimal transmission
    min_transmission_time = 0                       # time of minimal transmission
    oxy_depletion = []                              # oxygen depletion factor [-]
    q = []                                          # heat release [kW]
    thr = []                                        # total heat release [MJ]
    peak_hrr = 0.0                                  # peak heat release [kW]
    peak_hrr_time = 0                               # time of hrr peak [s]
    k = []											# smoke production extinction coefficient
    spr = []                                        # smoke production
    tsp = []                                        # total smoke production [m2]
    peak_spr = 0.0                                  # peak smoke production [m2/s]
    peak_spr_time = 0                               # time of smoke production peak
    for i in range(2, len(lines)):
        fields = lines[i].split(',')
        if len(fields) > 1:
            _time = int(fields[column_config['time']])
            time.append(_time)
            _dp = float(fields[column_config['dpt']])
            dp.append(_dp)
            _t_gas = (float(fields[column_config['t_duct_2']]) + 
                float(fields[column_config['t_duct_2']])) / 2.0
            t_gas.append(_t_gas)
            # transmission
            _transmission = float(fields[column_config['transmission']])
            if _transmission < min_transmission:
                min_transmission = _transmission
                min_transmission_time = _time
            transmission.append(_transmission)
            _diff = _dp / _t_gas
            if _diff < 0:
                _diff = 0
            # volume flow
            _v = 22.4 * (A * kt / kp) * math.sqrt(_diff)
            V.append(_v)
            x_CO2 = (float(fields[column_config['co2']])) / 100
            x_O2 = (float(fields[column_config['o2']])) / 100
            _oxy_dep = (x_0_O2 * (1 - x_CO2) - x_O2 * (1 - x_0_CO2)) / (x_0_O2 * (1 - x_O2 - x_CO2))
            oxy_depletion.append(_oxy_dep)
            # heat release
            _q = E_1 * _v * x_a_O2 * (_oxy_dep / (_oxy_dep * (alpha - 1) + 1)) - (E_1 / E_C3H8) * q_burner
            if _q < 0:
                _q = 0                  # prevent negative heat values
            q.append(_q)
            if len(thr) == 0:            # define current THR
                _thr = (3 * _q) / 1000
            else:
                _thr = thr[-1] + (3 * _q / 1000)
            thr.append(_thr)
            if _q > peak_hrr:
                peak_hrr = _q           # update peak_hrr
                peak_hrr_time = _time
            # smoke production
            _k = (1 / d) * math.log(i0 / _transmission)
            k.append(_k)
            _spr = _k * _v
            if _spr < 0:
                _spr = 0                # prevent negative smoke production
            spr.append(_spr)
            if len(tsp) == 0:           # define current TSP
                _tsp = 3 * _spr
            else:
                _tsp = tsp[-1] + 3 * _spr
            tsp.append(_tsp)
            if _spr > peak_spr:
                peak_spr = _spr
                peak_spr_time = _time

    # compute floating averages and FIGRA
    hrr_av = []                                 # in kW
    figra = []                                  # in W/s
    figra_max = 0.0                             # in W/s
    for i in range(0,len(time)):
        # hrr_av from symmetrical average (see EN 50399 G.1)
        if time[i] == 0:                        # t = 0 sec
            _hrr_av = 0
        elif time[i] == 3:                   # t = 3 sec
            _hrr_av = (q[0] + q[1] + q[2]) / 3
        elif time[i] == 6:                   # t = 6 sec
            _hrr_av = (q[0] + q[1] + q[2] + q[3] + q[4]) / 5
        elif time[i] == 9:                   # t = 9 sec
            _hrr_av = (q[0] + q[1] + q[2] + q[3] + q[4] + q[5] + q[6]) / 7
        elif time[i] == 12:                   # t = 12 sec
            _hrr_av = (q[0] + q[1] + q[2] + q[3] + q[4] + q[5] + q[6] + q[7] + q[8]) / 9
        elif time[i] == 1200:                        # t = 1200 sec
            _hrr_av = q[i]
        elif time[i] == 1197:                   # t = 1197 sec
            _hrr_av = (q[i-1] + q[i] + q[i+1]) / 3
        elif time[i] == 1194:                   # t = 1194 sec
            _hrr_av = (q[i-2] + q[i-1] + q[i] + q[i+1] + q[i+2]) / 5
        elif time[i] == 1191:                   # t = 1191 sec
            _hrr_av = (q[i-3] + q[i-2] + q[i-1] + q[i] + q[i+1] + q[i+2] + q[i+3]) / 7
        elif time[i] == 1188:                   # t = 1188 sec
            _hrr_av = (q[i-4] + q[i-3] + q[i-2] + q[i-1] + q[i] + q[i+1] + q[i+2] + q[i+3] + q[i+4]) / 9
        else:
            _hrr_av = (0.5 * q[i-5] + q[i-4] + q[i-3] + q[i-2] + q[i-1] + q[i] + q[i+1] + q[i+2] + q[i+3] + q[i+4] + 0.5 * q[i+5]) / 10
        hrr_av.append(_hrr_av)
        # figra: honor critiera
        if (_hrr_av > 3) and (thr[i] > 0.4):
            _figra = 1000 * (_hrr_av / time[i])
        else:
            _figra = 0
        figra.append(_figra)
        if _figra > figra_max:                  # check maximal figra
            figra_max = _figra

    trace = trace + "time: {0}\n".format(time)
    trace = trace + "dp: {0}\n".format(dp)
    trace = trace + "trsm: {0}\n".format(transmission)
    trace = trace + "V: {0}\n".format(V)
    trace = trace + "oxy_dep: {0}\n".format(oxy_depletion)
    trace = trace + "q (=hrr): {0}\n".format(q)
    trace = trace + "k: {0}\n".format(k)
    trace = trace + "spr: {0}\n".format(spr)
    trace = trace + "hrr_av: {0}\n".format(hrr_av)    
    trace = trace + "figra: {0}\n".format(figra)    
    trace = trace + "Peak HRR: {0} ({4} sec), THR: {1}, Peak SPR: {2} ({5} sec), TSP: {3}\n".format(
        peak_hrr, thr[-1], peak_spr, tsp[-1], peak_hrr_time, peak_spr_time)

    # process data for charts
    time_data_str = ""
    transmission_data_str = ""
    hrr_data_str = ""
    thr_data_str = ""
    spr_data_str = ""
    tsp_data_str = ""
    for i in range(0, len(time)):
        time_data_str = time_data_str + "{0},".format(time[i])
        transmission_data_str = transmission_data_str + "{0:.3f},".format(transmission[i])
        hrr_data_str = hrr_data_str + "{0:.3f},".format(hrr_av[i])
        thr_data_str = thr_data_str + "{0:.3f},".format(thr[i])
        spr_data_str = spr_data_str + "{0:.3f},".format(spr[i])
        tsp_data_str = tsp_data_str + "{0:.3f},".format(tsp[i])

    time_data_str = time_data_str[:-1]          # remove trailing comma
    transmission_data_str = transmission_data_str[:-1]
    hrr_data_str = hrr_data_str[:-1]
    thr_data_str = thr_data_str[:-1]
    spr_data_str = spr_data_str[:-1]
    tsp_data_str = tsp_data_str[:-1]

    # compute flame spread
    if doc.damage_zone_front > doc.damage_zone_back:
        doc.flame_spread = float(doc.damage_zone_front) / 100.0
    else:
        doc.flame_spread = float(doc.damage_zone_back) / 100.0
                
    # store output to document
    # result section
    doc.peak_hrr = peak_hrr
    doc.peak_spr = peak_spr
    doc.thr_1200s = thr[-1]
    doc.tsp_1200s = tsp[-1]
    doc.figra = figra_max
    # trace and processing
    doc.calculation_trace = trace
    doc.kt = kt
    doc.kp = kp
    doc.a = A
    doc.radius_of_tube = d / 2
    doc.e1 = E_1
    doc.trace = trace
    doc.data_time = time_data_str
    doc.data_transmission = transmission_data_str
    doc.data_hrr = hrr_data_str
    doc.data_thr = thr_data_str
    doc.data_spr = spr_data_str
    doc.data_tsp = tsp_data_str
    doc.hrr_max = peak_hrr
    doc.hrr_max_time = peak_hrr_time
    doc.transmittance_min = min_transmission
    doc.transmittance_min_time = min_transmission_time
    doc.spr_max = peak_spr
    doc.spr_max_time = peak_spr_time
    
    doc.save()
    
    return { 'output': 'Raw data imported and calculated' }
    
def kelvin(temp):
    return temp + 273.15

@frappe.whitelist()
def calculate_mounting(diameter=5.0):
    diameter = float(diameter)
    if diameter <= 5:
        d = round(diameter, 1)
        n = int(100 / (d * d))
        number_of_cables = "15 x {0:.0f}".format(n)
        n = 15 * n
        width = round(10*15 + 10*14, 1)
        spacing = 10
    elif diameter >= 20:
        n = int(320 / (round(diameter, 0) + 20))
        number_of_cables = "{0:.0f}".format(n)
        spacing = 20
        width = round(diameter * n + (n - 1) * spacing, 1)
    else:
        spacing = round(diameter, 1)
        n = int((300 + round(diameter, 0)) / (2 * round(diameter, 0)))
        number_of_cables = "{0:.0f}".format(n)
        width = round(diameter * n + (n - 1) * spacing, 1)
    # define length of cable required [m]
    request_length = round(3.7 * n, 2)
    return number_of_cables, width, spacing, request_length
