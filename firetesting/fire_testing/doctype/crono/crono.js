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
		if ((frm.doc.sales_order != null) && (frm.doc.sales_order != 'select')) {
			// in case of creating from sales order
			frappe.call({
                                "method": "frappe.client.get",
                                "args": {
                                        "doctype": "Sales Order",
                                        "name": frm.doc.sales_order
                                },
                                "callback": function(response) {
                                        var so = response.message;
                                        if (so) {
                                                frm.set_value('customer', so.customer);
                                        } else {
                                                frappe.msgprint("Sales order not found");
                                        }
                                }
                        });
		}
		else if ((frm.doc.classification != null) && (frm.doc.classification != 'select')) {
			// in case of creating from classification
			frappe.call({
                                "method": "frappe.client.get",
                                "args": {
                                        "doctype": "Classification",
                                        "name": frm.doc.classification
                                },
                                "callback": function(response) {
                                        var classification = response.message;
                                        if (classification) {
                                                frm.set_value('customer', classification.customer);
						frm.set_value('sales_order', classification.sales_order);
                                        } else {
                                                frappe.msgprint("Sales order not found");
                                        }
                                }
                        });
		}
	},
	sales_order: function(frm) {
		//cur_frm.add_fetch('sales_order','material','material');
		cur_frm.add_fetch('sales_order','customer','customer');
	},
	classification: function(frm) {
		// classification has changed, fetch sales order and customer
		cur_frm.add_fetch('classification','sales_order','sales_order');
		cur_frm.add_fetch('classification','customer','customer');
	}
});
