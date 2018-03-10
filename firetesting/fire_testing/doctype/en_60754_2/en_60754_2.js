// Copyright (c) 2018, libracore GmbH and contributors
// For license information, please see license.txt

frappe.ui.form.on('EN 60754 2', {
	refresh: function(frm) {
        // only allow to pull data when saved and in draft
        if ((!frm.doc.name.startsWith("New")) && (frm.doc.docstatus == 0)) {
            frm.add_custom_button(__("Update composition table"), function() {

            });      
        }
        // allow to push results to the material record
        frm.add_custom_button(__("Push results to material"), function() {

        });  
	},
    onload: function(frm) { 
        // check if this is a new entry
        if (frm.doc.name.startsWith("New")) {
            // create title based on crono
            if (frm.doc.crono != null) {
                // define test name / title
                var crono_number = frm.doc.crono.split("-");
                if (crono_number.length > 1) {
                    var title = "LSFIRE / " + crono_number[1] + " / 13";
                } else {
                    var title = "LSFIRE / " + frm.doc.crono + " / 13";
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
	},
});
