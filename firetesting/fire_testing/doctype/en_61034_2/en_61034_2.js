// Copyright (c) 2018, libracore GmbH and contributors
// For license information, please see license.txt

frappe.ui.form.on('EN 61034 2', {
	refresh: function(frm) {
        // add utility buttons
        frm.add_custom_button(__("Load raw data"), function() {
            read_raw_data(frm);
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
                    var title = "LSF-" + crono_number[1] + "-12";
                } else {
                    var title = "LSF-" + frm.doc.crono + "-12";
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
    var d = new frappe.ui.Dialog({
    	'title': 'Read raw data (xlsx)',
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
    
    d.fields_dict.ht.$wrapper.html('<p>' + __("Please select the raw data file (xlsx format).") + '</p>' +
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
            /* load the workbook */
            var workbook = XLSX.read(data, {type: 'binary'});
            var first_sheet_name = workbook.SheetNames[0];
            /* convert content to csv */
            var csv = XLSX.utils.sheet_to_csv(workbook.Sheets[first_sheet_name]);
            /* write content to form raw field */
            convert_raw_data(frm, csv);
        }
        // assign an error handler event
        reader.onerror = function (event) {
            frappe.msgprint(__("Error reading file"), __("Error"));
        }
        reader.readAsBinaryString(file); 
    }
    else
    {
        frappe.msgprint(__("Please select a file."), __("Information"));
    }
}

function convert_raw_data(frm, raw) {
    frappe.call({
        method: 'firetesting.fire_testing.doctype.en_61034_2.en_61034_2.convert_data',
        args: { 
            'raw': raw,
            'doc_name': frm.doc.name
        },
        callback: function(r) {
            if (r.message) {
                reload_dialog(__("Import completed"), __(r.message.output));
            }
        }
    });
}
