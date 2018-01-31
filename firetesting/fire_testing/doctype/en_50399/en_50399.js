// Copyright (c) 2018, libracore GmbH and contributors
// For license information, please see license.txt

frappe.ui.form.on('EN 50399', {
	refresh: function(frm) {
        // add menu buttons
        frm.page.add_menu_item(__("Export transfer file"), function() {
            // create a transfer file from record
            export_transfer_file(frm);
		});
        frm.page.add_menu_item(__("Import data from transfer file"), function() {
            // load data from transfer file
            import_transfer_file(frm);
		});        
        // add utility buttons
        frm.add_custom_button(__("Load raw data"), function() {
            read_raw_data(frm);
        });
	},
    setup: function(frm) { 
		// create title based on crono
		if (frm.doc.crono != null) {
            // define test name / title
			var title = "LSF-" + frm.doc.crono + "-10";
			//frappe.msgprint(title);
			cur_frm.set_value("title", title);
            // get customer (from cache)
            cur_frm.add_fetch('crono','customer','customer');
            // read material
            get_material(frm);
		}
		else {
			frappe.msgprint({
				title: __("Crono app"),
				message: __("Please create tests only from Crono dashboard"),
				indicator: 'red'
			});
		}
	}
});

function get_material(frm) {
    frappe.call({
        method: 'firetesting.fire_testing.doctype.crono.crono.get_material',
        args: { 
            'doc': frm.doc.crono
        },
        callback: function(r) {
            if (r.message) {
                if (r.message.material_name == "no material defined!") {
                    frappe.msgprint({
                        title: __("Crono app"),
                        message: __("Material not found. Please create a material in the crono first."),
                        indicator: 'red'
                    });
                } else {
                    frm.set_value('material', r.message.material_name);
                }
            }
        }
    });
}

function read_raw_data(frm) {
    var d = new frappe.ui.Dialog({
    	'title': 'Read raw data',
    	'fields': [
            {'fieldname': 'ht', 'fieldtype': 'HTML'}
        ],
        primary_action: function() {
            // hide form
            d.hide();
            // get file object
            var file = document.getElementById("input_file").files[0];
            // and read the file to the form
            read_file(frm, file);

        }
    });
    
    d.fields_dict.ht.$wrapper.html('<input type="file" id="input_file" />');
    
    d.show();
}

function read_file(frm, file) {
    // read the file 
    var content = "";
    if (file) {
        // create a new reader instance
        var reader = new FileReader();
        // assign load event to process the file
        reader.onload = function (event) {           
            // read file content
            content = event.target.result;

            // write content to form raw field
            cur_frm.set_value('logger_data', content);
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

function import_transfer_file(frm) {
    var d = new frappe.ui.Dialog({
    	'title': 'Import transfer file (CSV)',
    	'fields': [
            {'fieldname': 'ht', 'fieldtype': 'HTML'}
        ],
        primary_action: function() {
            // hide form
            d.hide();
            // get file object
            var file = document.getElementById("input_file").files[0];
            // and read the file to the form
            read_import_file(frm, file);

        }
    });
    
    d.fields_dict.ht.$wrapper.html('<input type="file" id="input_file" />');
    
    d.show();
}

function read_import_file(frm, file) {
    // read the file 
    var content = "";
    if (file) {
        // create a new reader instance
        var reader = new FileReader();
        // assign load event to process the file
        reader.onload = function (event) {           
            // read file content
            content = event.target.result;

            // import content
            frappe.call({
                method: 'firetesting.fire_testing.doctype.en_50399.en_50399.import_transfer_file',
                args: { 
                    'content': content
                },
                callback: function(r) {
                    if (r.message) { 
                        assign_imported_values(r.message.data);
                        frappe.msgprint(r.message.output);                        
                    }
                }
            });
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

function assign_imported_values(data) {
    cur_frm.set_value("date_of_test", data.date_of_test);
    cur_frm.set_value("operator", data.operator);
    cur_frm.set_value("logger_data", data.raw);
    cur_frm.set_value("temperature", data.env_temperature);
    cur_frm.set_value("pressure", data.env_pressure);
    cur_frm.set_value("relative_humidity", data.env_humidity);            
}

function export_transfer_file(frm) {
    // export transfer file
    frappe.call({
        method: 'firetesting.fire_testing.doctype.en_50399.en_50399.export_transfer_file',
        args: {
            'doc_name': frm.doc.name
        },
        callback: function(r) {
            if (r.message) { 
                download("transfer.csv", r.message.content);
            }
        }
    });
}

function download(filename, content) {
  var element = document.createElement('a');
  element.setAttribute('href', 'data:application/octet-stream;charset=utf-8,' + encodeURIComponent(content));
  element.setAttribute('download', filename);

  element.style.display = 'none';
  document.body.appendChild(element);

  element.click();

  document.body.removeChild(element);
}
