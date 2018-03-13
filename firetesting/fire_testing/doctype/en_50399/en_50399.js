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
        frm.add_custom_button(__("Re-calculate"), function() {
            recalculate(frm);
        });
        frm.add_custom_button(__("Calculate mounting"), function() {
            // set mounting parameters
            set_mounting(frm);
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
                    var title = "LSFIRE / " + crono_number[1] + " / 10";
                } else {
                    var title = "LSFIRE / " + frm.doc.crono + " / 10";
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
        
        // prepare charts
        loadCharts(frm);
	}
});

function loadCharts(frm) {
    /* heat release  */
    displayChart('chartHRR', 
        'https://data.libracore.ch/server-side-charts/api/scientific_chart.php' +
        '?x[0]=' + frm.doc.data_time +
        '&y[0]=' + frm.doc.data_hrr + 
        '&legend=' + frm.doc.title +
        '&title=HRR' + 
        '&scale=0,1200,0,' + frm.doc.hrr_max);
    displayChart('chartTHR', 
        'https://data.libracore.ch/server-side-charts/api/scientific_chart.php' +
        '?x[0]=' + frm.doc.data_time +
        '&y[0]=' + frm.doc.data_thr + 
        '&legend=' + frm.doc.title +
        '&title=THR' + 
        '&scale=0,1200,0,' + frm.doc.thr_1200s);  
    /* smoke production */
    displayChart('chartSPR', 
        'https://data.libracore.ch/server-side-charts/api/scientific_chart.php' +
        '?x[0]=' + frm.doc.data_time +
        '&y[0]=' + frm.doc.data_spr + 
        '&legend=' + frm.doc.title +
        '&title=SPR' + 
        '&scale=0,1200,0,' + frm.doc.spr_max); 
    displayChart('chartTSP', 
        'https://data.libracore.ch/server-side-charts/api/scientific_chart.php' +
        '?x[0]=' + frm.doc.data_time +
        '&y[0]=' + frm.doc.data_tsp + 
        '&legend=' + frm.doc.title +
        '&title=TSP' + 
        '&scale=0,1200,0,' + frm.doc.tsp_1200s); 
        
    /* Transmittance */
    displayChart('chartTransmittance',
        'https://data.libracore.ch/server-side-charts/api/scientific_chart.php' +
        '?x[0]=' + frm.doc.data_time +
        '&y[0]=' + frm.doc.data_transmission + 
        '&legend=' + frm.doc.title +
        '&title=Transmittance' + 
        '&scale=0,1200,0,100'); 
}

function displayChart(container, source) {
    let _img = document.getElementById(container);
    var Img = new Image;
    Img.onload = function() {
        _img.src = this.src;
    }
    Img.src = source;
}

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
        '<p>' + __("The first row should contain column headers (ID,0.0 - TAMB_50399,0.1 - Tduct1_50399,...), the second column and onwards the data") + '</p>' +
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
            //cur_frm.set_value('logger_data', csv);
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
        method: 'firetesting.fire_testing.doctype.en_50399.en_50399.convert_data',
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

function recalculate(frm) {
    frappe.call({
        method: 'firetesting.fire_testing.doctype.en_50399.en_50399.calculate_results',
        args: { 
            'doc_name': frm.doc.name
        },
        callback: function(r) {
            if (r.message) {
                reload_dialog(__("Re-calculation completed"), __(r.message.output));
            }
        }
    });
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
                    'content': content,
                    'doc_name': frm.doc.name
                },
                callback: function(r) {
                    if (r.message) { 
                        reload_dialog(__("Import completed"), __(r.message.output));
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

/* define the mounting parameters */
function set_mounting(frm) {
    frappe.call({
        method: 'set_mounting',
        doc: frm.doc,
        callback: function(response) {
            refresh_field(['material_length', 'number_of_cables', 'spacing', 'required_cable']);
                        
            // show a short information
            frappe.show_alert( __("Mounting collected"));
        }
    }); 
}
