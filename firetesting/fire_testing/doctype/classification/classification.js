// Copyright (c) 2017, libracore GmbH and contributors
// For license information, please see license.txt

frappe.ui.form.on('Classification', {
	refresh: function(frm) {
		//Filter for sales_order based on customer link field
		cur_frm.fields_dict['sales_order'].get_query = function(doc) {
			return {
				filters: {
					"customer": frm.doc.customer
				}
			}
		};
        
        // check if this is a new record
        if (frm.doc.__islocal) {
            var last_route = frappe.route_history.slice(-2, -1)[0];
            // last_route is a array with ["Form", "Crono", "CRONO-00003"]
            if (last_route[1] == "Crono") {
               // coming from a Crono
               get_info(frm, last_route[2]);
            } else {
                // coming from sales order: fetch customer from sales order
                cur_frm.add_fetch('sales_order','customer','customer');
            }
        }
        
	} 
});

function get_info(frm, crono) {
    frappe.call({
        "method": "frappe.client.get",
        "args": {
            "doctype": "Crono",
            "name": crono
        },
        "callback": function(response) {
            var crono = response.message;

            if (crono) {
                frm.set_value('customer', crono.customer);
                frm.set_value('sales_order', crono.sales_order);
            } else {
                frappe.msgprint("Crono not found");
            }
        }
    });
}
