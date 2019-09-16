// Copyright (c) 2018, libracore GmbH and contributors
// For license information, please see license.txt

frappe.ui.form.on('Crono Verification', {
	refresh: function(frm) {
        // check if this is a new entry
        if (frm.doc.__islocal) {
            // create title based on crono
            if (frm.doc.crono != null) {
                // define title
                var title = "Verification " + frm.doc.crono;

                cur_frm.set_value('title', title);
                // get customer
                get_customer(frm);
                // read material
                get_material(frm);
            }
            else {
                frappe.msgprint({
                    title: __("Crono app"),
                    message: __("Please create verification records only from the Crono dashboard"),
                    indicator: 'red'
                });
            }
        }
	},
    validate: function(frm) {
        if (frm.doc.shape == "Circular") {
            var diameter = frm.doc.declared_diameter;
            var diameter_min = 0.9 * diameter;
            var diameter_max= 1.1 * diameter;
            frm.set_value('declared_diameter_min', diameter_min);
            frm.set_value('declared_diameter_max', diameter_max);
        } else {
            var diameter1 = frm.doc.major_axis_diameter;
            var diameter2 = frm.doc.minor_axis_diameter;
            var diameter1_min = 0.9 * diameter1;
            var diameter1_max= 1.1 * diameter1;
            var diameter2_min = 0.9 * diameter2;
            var diameter2_max= 1.1 * diameter2;
            frm.set_value('major_axis_diameter_min', diameter1_min);
            frm.set_value('major_axis_diameter_max', diameter1_max);
            frm.set_value('minor_axis_diameter_min', diameter2_min);
            frm.set_value('minor_axis_diameter_max', diameter2_max);
        } 
    }
});
