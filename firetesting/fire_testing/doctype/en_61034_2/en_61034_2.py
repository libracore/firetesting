# -*- coding: utf-8 -*-
# Copyright (c) 2018, libracore GmbH and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class EN610342(Document):
	pass

@frappe.whitelist()
def convert_data(raw, doc_name, env_T=20, env_P=96000, env_rh=50):
    # get parent document
    doc = frappe.get_doc("EN 61034 2", doc_name)
    
    # prepare input data
    raw_lines = raw.split('\n')

    # TODO import raw data
    
    return
