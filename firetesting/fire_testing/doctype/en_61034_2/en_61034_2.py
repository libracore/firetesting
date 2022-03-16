# -*- coding: utf-8 -*-
# Copyright (c) 2018, libracore GmbH and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _
from statistics import mean

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
    """
    def convert_data(self, raw):       
        # prepare input data
        raw_lines = raw.split('\n')
        """ field definition: 
            0: date (dd.mm.yyy)	
            1: time (hh:mm:ss)
            2: temperature [°C] (float)
            3: sensor [mV] (float)
            4: transmittance [%] (percent)
        """ 	
        # configuration of columns of raw file
        column_config = { 
            'date': 0,
            'time': 1,
            'sensor': 3, 
            'temperature': 2, 
            'transmittance': 4
        }
        
        # compile the data vectors
        time = []
        transmittance = []
        temperature = []
        min_transmittance = 100
        max_temperature = 0
        end_time = 0
        # first data in row 8
        separator = "\t"
        fields = raw_lines[8].split(separator)
        if len(fields) < 5:
            # try comma as separator
            separator = ";"
            fields = raw_lines[8].split(separator)
            if len(fields) < 5:
                # try semicolon as separator
                separator = ","
                fields = raw_lines[8].split(separator)
        if len(fields) < 5:
            # fields not found, invalid input
            return { 'output' : "Invalid input format" }
        starting_temperature = get_value(fields[column_config['temperature']], 1)
        for i in range(8, len(raw_lines)):
            fields = raw_lines[i].split(separator)
            if len(fields) > 4:
                # start time has a 120 sec offset
                _time = ((i - 8) * 3) - 120
                # stop after 40 minutes
                if _time > (40 * 60):
                    continue
                end_time = _time
                time.append(end_time)
                _transmittance = get_value(fields[column_config['transmittance']], 2)
                transmittance.append(_transmittance)
                if _transmittance < min_transmittance:
                    min_transmittance = _transmittance
                _temperature = get_value(fields[column_config['temperature']], 1)
                temperature.append(_temperature)
                if _temperature > max_temperature:
                    max_temperature = _temperature

        # thin out data for chart (only 1 data point per minute, 1/20)
        time_short = ""
        transmittance_short = ""
        temperature_short = ""
        for i in range(0, len(time), 20):
            time_short += "{0},".format((time[i]/60))
            transmittance_short += "{0},".format(transmittance[i])
            temperature_short += "{0},".format(temperature[i])
           
        time_short = time_short[:-1]
        transmittance_short = transmittance_short[:-1]
        temperature_short = temperature_short[:-1]
        incident_light_intensity = mean(transmittance[0:39])      # first 120 sec (40 datapoints à 3 sec)
        min_intensity = min_transmittance / incident_light_intensity
        result_amd2 = min_intensity ** (40 / (self.number_of_cables * self.diameter))
        
        # store output to document
        self.raw_time = time_short
        self.raw_transmittance = transmittance_short
        self.raw_temperature = temperature_short
        self.min_transmittance = min_transmittance
        self.incident_light_intensity = incident_light_intensity
        self.min_intensity = 100 * min_intensity                    # in percent
        if self.diameter <= 20: 
            self.result = self.min_intensity
        else:
            self.result = 100 * result_amd2                             # in percent
        self.starting_temperature = starting_temperature
        self.maximum_temperature = max_temperature
        self.end_time = end_time
        self.save()
        
        return { 'output': 'Raw data imported and calculated' }

    def reset_submit(self):
        # this function will reset the submit status
        sql_query = """UPDATE `tabEN 61034 2` SET `docstatus` = 0 WHERE `name` = '{name}'""".format(name=self.name)
        frappe.db.sql(sql_query)
        new_comment = frappe.get_doc({'doctype': 'Communication'})
        new_comment.comment_type = "Comment"
        new_comment.content = "Document submit reset"
        new_comment.reference_doctype = "EN 61034 2"
        new_comment.status = "Linked"
        new_comment.reference_name = self.name
        new_comment.save()
        return
        
# this function parses a decimal string value to a float
def get_value(value, decimals=2):
    try:
        _value = round(float(value), decimals)
    except ValueError:
        _value = round(float(value.replace(',', '.')), decimals)
    return _value

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
