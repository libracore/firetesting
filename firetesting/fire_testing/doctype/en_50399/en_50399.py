# -*- coding: utf-8 -*-
# Copyright (c) 2018, libracore GmbH and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class EN50399(Document):
    def onload(self):
        """Runs when document is loaded (not created)"""
        pass

""" This function will import a transfer file content into the test record """
@frappe.whitelist()
def import_transfer_file(content):
    # separate content into lines
    lines = content.split("\n")
    data = {}
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

        data['date_of_test'] = assert_date(lines[5].split(separator)[1])
        data['operator'] = lines[35].split(separator)[1]
        data['env_pressure'] = lines[41].split(separator)[1]
        data['env_humidity'] = lines[42].split(separator)[1]
        data['env_temperature'] = lines[43].split(separator)[1]

        raw = ""
        for line in lines:
            raw = raw + separator.join(line.split(separator)[2:]) + "\n"
        data['raw'] = raw
        
    return { 'output': 'Transfer file imported', 'data': data }

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
