# -*- coding: utf-8 -*-
# Copyright (c) 2017-2018, libracore GmbH and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Crono(Document):
    pass

@frappe.whitelist()
def lock(doc):
    frappe.db.sql("UPDATE `tabCrono` SET `docstatus` = 1 WHERE `name` = '{0}'".format(doc))
    return

@frappe.whitelist()
def unlock(doc):
    frappe.db.sql("UPDATE `tabCrono` SET `docstatus` = 0 WHERE `name` = '{0}'".format(doc))
    return

@frappe.whitelist()
def get_material(doc):
    material_name = frappe.get_value("Crono", doc, 'material')
    if material_name:
        return { 'material_name': material_name }
    else:
        return { 'material_name': "no material defined!" }

@frappe.whitelist()
def get_customer(doc):
    customer_name = frappe.get_value("Crono", doc, 'customer')
    if customer_name:
        return { 'customer_name': customer_name }
    else:
        return { 'customer_name': "no customer defined!" }
