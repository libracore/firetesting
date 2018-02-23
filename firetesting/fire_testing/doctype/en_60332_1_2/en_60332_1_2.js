// Copyright (c) 2018, libracore GmbH and contributors
// For license information, please see license.txt

frappe.ui.form.on('EN 60332 1 2', {
	refresh: function(frm) {

	},
    onload: function(frm) { 
        // check if this is a new entry
        if (frm.doc.name.startsWith("New")) {
            // create title based on crono
            if (frm.doc.crono != null) {
                // define test name / title
                var crono_number = frm.doc.crono.split("-");
                if (crono_number.length > 1) {
                    var title = "LSF-" + crono_number[1] + "-11";
                } else {
                    var title = "LSF-" + frm.doc.crono + "-11";
                }
                //frappe.msgprint(title);
                cur_frm.set_value("title", title);
                // get customer
                get_customer(frm);
                // read material
                get_material(frm);
            }
            else {
                frappe.msgprint({
                    title: __("Crono app"),
                    message: __("Please create tests only from the Crono dashboard"),
                    indicator: 'red'
                });
            }
        }
	}
});
