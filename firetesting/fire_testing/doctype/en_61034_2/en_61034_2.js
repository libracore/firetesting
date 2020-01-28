// Copyright (c) 2018, libracore GmbH and contributors
// For license information, please see license.txt

frappe.ui.form.on('EN 61034 2', {
	refresh: function(frm) {
        // only place buttons on saved draft documents
        if ((frm.doc.docstatus == 0) && (!frm.doc.__islocal)) { 
            // add utility buttons
            frm.add_custom_button(__("Load raw data"), function() {
                read_raw_data(frm);
            });
            frm.add_custom_button(__("Calculate mounting"), function() {
                // set mounting parameters
                set_mounting(frm);
            });
        }
        // add reset button if submitted and user is Crono Approver
        if ((frm.doc.docstatus == 1) && (frappe.user.has_role("Crono Approver"))) {
            frm.add_custom_button(__("Reset submit"), function() {
                // reset
                frappe.call({
                    method: 'reset_submit',
                    doc: frm.doc,
                    callback: function(response) {
                        location.reload();
                    }
                });
            });
        }
	},
    onload: function(frm) { 
        // check if this is a new entry
        if (frm.doc.__islocal) {
            // create title based on crono
            if (frm.doc.crono != null) {
                // define test name / title
                var crono_number = frm.doc.crono.split("-");
                if (crono_number.length > 1) {
                    var title = "LSFIRE / " + crono_number[1] + " / 12";
                } else {
                    var title = "LSFIRE / " + frm.doc.crono + " / 12";
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

function read_raw_data(frm) {
    // clean file browser cache
    if (document.getElementById("input_file")) {
        document.getElementById("input_file").outerHTML = "";
    }
    
    var d = new frappe.ui.Dialog({
    	'title': 'Read raw data (txt)',
    	'fields': [
            {'fieldname': 'ht', 'fieldtype': 'HTML'}
        ],
        primary_action: function() {
            // hide form
            d.hide();
            // get file object
            var file = document.getElementById("input_file").files[0];            
            // and read the file to the form
            read_raw_file(frm, file);

        }
    });
    
    d.fields_dict.ht.$wrapper.html('<p>' + __("Please select the raw data file (txt format).") + '</p>' +
        '<p>' + __("Data needs to contain time, temperature and transmittance") + '</p>' +
        '<input type="file" id="input_file" />');
    
    d.show();
}

function read_raw_file(frm, file) {
    // read the file 
    var content = "";
    if (file) {
        /* create new reader instance */
        var reader = new FileReader();
        reader.onload = function(e) {
            /* read the file */
            var data = e.target.result;

            convert_raw_data(frm, data);
        }
        // assign an error handler event
        reader.onerror = function (event) {
            frappe.msgprint(__("Error reading file"), __("Error"));
        }
        reader.readAsText(file, "UTF-8"); 
    }
    else
    {
        frappe.msgprint(__("Please select a file."), __("Information"));
    }
}

function convert_raw_data(frm, raw) {
    frappe.call({
        method: 'convert_data',
        doc: frm.doc,
        args: { 
            'raw': raw
        },
        callback: function(r) {
            if (r.message) {
                frappe.show_alert(r.message.output);
                refresh_field(['raw_time', 'raw_transmittance', 'raw_temperature',
                    'min_transmittance', 'starting_temperature', 'maximum_temperature',
                    'end_time', 'incident_light_intensity', 'min_intensity', 'result']);
            }
        }
    });
}

/* define the mounting parameters */
function set_mounting(frm) {
    frappe.call({
        method: 'set_mounting',
        doc: frm.doc,
        callback: function(response) {
            refresh_field(['number_of_bundles', 'number_of_cables', 'rotation']);
                        
            // show a short information
            frappe.show_alert( __("Mounting collected"));
        }
    }); 
}
