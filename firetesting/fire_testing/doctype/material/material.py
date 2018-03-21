# -*- coding: utf-8 -*-
# Copyright (c) 2017, libracore GmbH and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _

class Material(Document):
    def get_usage(self):
        # get material that uses this component
        sql_query = ("SELECT `parent` " +
                    "FROM `tabMaterial Component` " +
                    "WHERE `material_code` = '{0}'".format(self.name))
        records = frappe.db.sql(sql_query, as_dict=True)
        materials = []
        for record in records:
            materials.append(frappe.get_doc("Material", record['parent']))
        return {'materials': materials }

""" This function is used to update measurement results of materials.
    Data is pushed here from the EN 60754-2 client script 
"""
@frappe.whitelist()
def update_measurements(material, ph, conductivity, reference):
    # initialise document
    doc = frappe.get_doc("Material", material)
    if not doc:
        return { 'output': _('Material {0} not found').format(material) }
    doc.ph = ph
    doc.conductivity = conductivity
    doc.reference = reference
    doc.save()
    return { 'output': _('Material {0} successfully updated').format(material) }
