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
        
        if (frm.doc.type == "Component") {
            frm.add_custom_button(__("Show Usage"), function() {
                show_usage(frm);
            });
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
    onload: function(frm) {
        // set filters
        frm.fields_dict.components.grid.get_field('material_code').get_query =
			function() {
				return {
					filters: {
						"type": "Component"
					}
				}
			};  
    },
	crono: function(frm) {
		// fetch customer when changing crono
		cur_frm.add_fetch('crono','customer','customer');
	}
});

function show_usage(frm) {
    frappe.call({
        method: 'get_usage',
        doc: frm.doc,
        callback: function(r) {
           var d = new frappe.ui.Dialog({
                'fields': [
                    {'fieldname': 'ht', 'fieldtype': 'HTML'}
                ]
            });
            var output = "";
            if (r.message.materials.length > 0) {
                output = frappe.render_template('material_table', r.message);
            } else {
                output = ('<p class="text-muted">' + __("No materials found.") + '</p>');
            }
            d.fields_dict.ht.$wrapper.html(output);
            d.show();
        }
    });
}
