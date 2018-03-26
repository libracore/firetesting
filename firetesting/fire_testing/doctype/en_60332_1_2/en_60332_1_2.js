// Copyright (c) 2018, libracore GmbH and contributors
// For license information, please see license.txt

frappe.ui.form.on('EN 60332 1 2', {
	refresh: function(frm) {
        frm.add_custom_button(__("Calculate"), function() {
            calculate(frm);
        });
	},
    onload: function(frm) { 
        // check if this is a new entry
        if (frm.doc.__islocal) {
            // create title based on crono
            if (frm.doc.crono != null) {
                // define test name / title
                var crono_number = frm.doc.crono.split("-");
                if (crono_number.length > 1) {
                    var title = "LSFIRE / " + crono_number[1] + " / 11";
                } else {
                    var title = "LSFIRE / " + frm.doc.crono + " / 11";
                }
                //frappe.msgprint(title);
                cur_frm.set_value("title", title);
                // get customer
                get_customer(frm);
                // read material
                get_material(frm);
                // create 5 measurement rows
                /* for (i = 0; i < 5; i++) { // does not work because measurements does not yet exist
                    var child = cur_frm.add_child(measurements);
                }*/
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

function calculate(frm) {
    var measurements = frm.doc.measurements;
    var start = new Array();
    var end = new Array();
    measurements.forEach(function(entry) {
        if (entry.start != null) {
            start.push(entry.start);
        }
        if (entry.end != null) {
            end.push(entry.end);
        }
    });
    var average_start = average(start);
    var average_end = average(end);
    var flame_spread = average_end - average_start;
    cur_frm.set_value("average_start", average_start);
    cur_frm.set_value("average_end", average_end); 
    cur_frm.set_value("start_uncertainty", standardDeviation(start));
    cur_frm.set_value("end_uncertainty", standardDeviation(end));     
    cur_frm.set_value("flame_spread", flame_spread);
    if (flame_spread <= 425) {
        cur_frm.set_value("has_passed", 1);
    }
    else {
        cur_frm.set_value("has_passed", 0);
    }
}
