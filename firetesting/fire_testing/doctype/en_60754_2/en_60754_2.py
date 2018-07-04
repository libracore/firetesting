# -*- coding: utf-8 -*-
# Copyright (c) 2018, libracore GmbH and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class EN607542(Document):
    def reset_submit(self):
        # this function will reset the submit status
        sql_query = """UPDATE `tabEN 60754 2` SET `docstatus` = 0 WHERE `name` = '{name}'""".format(name=self.name)
        frappe.db.sql(sql_query)
        new_comment = frappe.get_doc({'doctype': 'Communication'})
        new_comment.comment_type = "Comment"
        new_comment.content = "Document submit reset"
        new_comment.reference_doctype = "EN 60754 2"
        new_comment.status = "Linked"
        new_comment.reference_name = self.name
        new_comment.save()
        return
	
