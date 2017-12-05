// Copyright (c) 2017, libracore GmbH and contributors
// For license information, please see license.txt

frappe.ui.form.on('Crono', {
	refresh: function(frm) {
		//Filter for sales_order based on customer link field
		cur_frm.fields_dict['sales_order'].get_query = function(doc) {
			return {
				filters: {
					"customer": frm.doc.customer
				}
			}
		};
                cur_frm.fields_dict['classification'].get_query = function(doc) {
                        return {
                                filters: {
                                        "customer": frm.doc.customer
                                }
                        }
                };
	},
	setup: function(frm) {
		if (!frm.doc.sales_order) {
			// in case of creating from sales order
			cur_frm.add_fetch('sales_order','customer','customer');
		}
		else if (!frm.doc.classification) {
			// in case of creating from classification
			cur_frm.add_fetch('classification','sales_order','sales_order');
			cur_frm.add_fetch('classification','customer','customer');
		}
	},
	sales_order: function(frm) {
		//cur_frm.add_fetch('sales_order','material','material');
	}
});
