// Copyright (c) 2017, libracore GmbH and contributors
// For license information, please see license.txt

frappe.ui.form.on('Test 10', {
	refresh: function(frm) {

	},
	setup: function(frm) {
		// create title based on crono
		if (frm.doc.crono != null) {
			var title = "LSF-" + frm.doc.crono + "-10";
			frappe.msgprint(title);
			cur_frm.set_value("title", title);
		}
		else {
			frappe.msgprint({
				title: __('Crono app'),
				message: __('Please create tests only from Crono dashboard'),
				indicator: 'red'
			});
		}
	}
});
