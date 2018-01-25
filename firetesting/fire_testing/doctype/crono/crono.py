# -*- coding: utf-8 -*-
# Copyright (c) 2017, libracore GmbH and contributors
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
