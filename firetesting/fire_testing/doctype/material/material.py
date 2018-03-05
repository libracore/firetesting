# -*- coding: utf-8 -*-
# Copyright (c) 2017, libracore GmbH and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

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

