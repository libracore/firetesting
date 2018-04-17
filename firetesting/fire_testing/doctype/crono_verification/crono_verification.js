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

                cur_frm.set_value("title", title);
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

	}
});
