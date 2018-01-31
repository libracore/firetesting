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
def export_transfer_file():
    content = "Transfer file placeholder"
    
    return { 'content': content }
