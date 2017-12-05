// Copyright (c) 2017, libracore GmbH and contributors
// For license information, please see license.txt

frappe.ui.form.on('Material', {
	refresh: function(frm) {
		// filter for crono based on customer link field
		cur_frm.fields_dict['crono'].get_query = function(doc) {
			return {
				filters: {
					"customer": frm.doc.customer
				}
			}
		}
	},
	setup: function(frm) {
		// in case of creating from crono, load customer
		if ((frm.doc.crono != null) && (frm.doc.crono != 'select')) {
			frappe.call({
				"method": "frappe.client.get",
				"args": {
					"doctype": "Crono",
					"name": frm.doc.crono
				},
				"callback": function(response) {
					var crono = response.message;

					if (crono) {
						frm.set_value('customer', crono.customer);
					} else {
						frappe.msgprint("Crono not found");
					}
				}
			});
		}
	},
	crono: function(frm) {
		// fetch customer when changing crono
		cur_frm.add_fetch('crono','customer','customer');
	}
});
