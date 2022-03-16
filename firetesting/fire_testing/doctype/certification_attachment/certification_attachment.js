// Copyright (c) 2022, libracore GmbH and contributors
// For license information, please see license.txt

frappe.ui.form.on('Certification Attachment', {
    refresh: function(frm) {
        if (frm.doc.__islocal) {
            cur_frm.set_value('date', frappe.datetime.get_today());
        }
    }
});
