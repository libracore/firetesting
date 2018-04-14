// Copyright (c) 2017, libracore GmbH and contributors
// For license information, please see license.txt

frappe.ui.form.on('Material', {
	refresh: function(frm) {      
	    if (frm.doc.type == "Component") {
		frm.add_custom_button(__("Show Usage"), function() {
		    show_usage(frm);
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
