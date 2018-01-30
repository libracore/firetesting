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
    
    return { 'output': 'Transfer file imported' }

""" This function will export a transfer file from the test record """
@frappe.whitelist()
def export_transfer_file():
    content = "Transfer file placeholder"
    
    return { 'content': content }
