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
        
        if (frm.doc.docstatus == 0) {
            // add utility buttons
            frm.add_custom_button(__("Load results from ELAB"), function() {
                read_elab(frm);
            });
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
        }
        
        // check if this is a new entry
        if (frm.doc.__islocal) {
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
        
        // prepare charts
        loadCharts(frm);
	}
});

function loadCharts(frm) {
    /* heat release  */
    displayChart('chartHRR', 
        'https://data.libracore.ch/server-side-charts/api/en_50399.php' +
        '?x[0]=' + frm.doc.data_time +
        '&y[0]=' + frm.doc.data_hrr + 
        '&legend[0]=' + frm.doc.title +
        '&title=HRR' + 
        '&scale=0,1200,0,' + frm.doc.chart_hrr_y_max);
    displayChart('chartTHR', 
        'https://data.libracore.ch/server-side-charts/api/en_50399.php' +
        '?x[0]=' + frm.doc.data_time +
        '&y[0]=' + frm.doc.data_thr + 
        '&legend[0]=' + frm.doc.title +
        '&title=THR' + 
        '&scale=0,1200,0,' + frm.doc.chart_thr_y_max);  
    /* smoke production */
    displayChart('chartSPR', 
        'https://data.libracore.ch/server-side-charts/api/en_50399.php' +
        '?x[0]=' + frm.doc.data_time +
        '&y[0]=' + frm.doc.data_spr + 
        '&legend[0]=' + frm.doc.title +
        '&title=SPR' + 
        '&scale=0,1200,0,' + frm.doc.chart_spr_y_max); 
    displayChart('chartTSP', 
        'https://data.libracore.ch/server-side-charts/api/en_50399.php' +
        '?x[0]=' + frm.doc.data_time +
        '&y[0]=' + frm.doc.data_tsp + 
        '&legend[0]=' + frm.doc.title +
        '&title=TSP' + 
        '&scale=0,1200,0,' + frm.doc.chart_tsp_y_max); 
        
    /* Transmittance */
    displayChart('chartTransmittance',
        'https://data.libracore.ch/server-side-charts/api/en_50399.php' +
        '?x[0]=' + frm.doc.data_time +
        '&y[0]=' + frm.doc.data_transmission + 
        '&legend[0]=' + frm.doc.title +
        '&title=Transmittance' + 
        '&scale=0,1200,0,' + frm.doc.chart_transmittance_y_max); 
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
            {'fieldname': 'ht', 'fieldtype': 'HTML'},
            {'fieldname': 'ignore_shift', 'fieldtype': 'Check', 'label': __('Ignore individual shifts'), 'default': 1}
        ],
        primary_action: function() {
            // get values
            var data = d.get_values();
            // hide form
            d.hide();
            // get file object
            
            var file = document.getElementById("input_file").files[0];
            // and read the file to the form
            read_raw_file(frm, file, data.ignore_shift);

        },
        primary_action_label: __('Load raw data')
    });
    
    d.fields_dict.ht.$wrapper.html('<p>' + __("Please select the raw data file (xlsx format).") + '</p>' +
        '<p>' + __("The first row should contain column headers (ID,0.0 - TAMB_50399,0.1 - Tduct1_50399,...), the second column and onwards the data") + '</p>' +
        '<input type="file" id="input_file" />');
    
    d.show();
}

function read_raw_file(frm, file, ignore_shift) {
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
            convert_raw_data(frm, csv, ignore_shift);
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

function convert_raw_data(frm, raw, ignore_shift) {
    frappe.call({
        method: 'firetesting.fire_testing.doctype.en_50399.en_50399.convert_data',
        args: { 
            'raw': raw,
            'doc_name': frm.doc.name,
            'ignore_individual_shifts': ignore_shift
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
    // clean file browser cache
    if (document.getElementById("input_file")) {
        document.getElementById("input_file").outerHTML = "";
    }
    
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

        },
        primary_action_label: __('Import file')
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

/* read ELAB files */
function read_elab(frm) {
    // clean file browser cache
    if (document.getElementById("elab_file")) {
        document.getElementById("elab_file").outerHTML = "";
    }
    
    var d = new frappe.ui.Dialog({
        'title': 'Read ELAB (xlsx)',
        'fields': [
            {'fieldname': 'ht', 'fieldtype': 'HTML'}
        ],
        primary_action: function() {
            // get values
            var data = d.get_values();
            // hide form
            d.hide();
            // get file object
            var file = document.getElementById("elab_file").files[0];

            // and read the file to the form
            load_elab(frm, file);

        },
        primary_action_label: __('Load ELAB')
    });

    d.fields_dict.ht.$wrapper.html('<p>' + __("Please select the ELAB data file (xlsx format).") + '</p>' +
        '<p>' + __("The file needs to contain an <i>export</i> tab with the transfer information.") + "</p>" +
        '<input type="file" id="elab_file" />');

    d.show();
}

function load_elab(frm, file) {
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
            var export_sheet_name = workbook.SheetNames['export'];
            /* convert content to csv */
            var csv = XLSX.utils.sheet_to_csv(workbook.Sheets[export_sheet_name]);
            /* write content to form trace field */
            cur_frm.set_value('calculation_trace', csv);
            var crono = workbook.Sheets['export']['A2'].v;
            if (("CRONO-" + crono) != frm.doc.crono) {
            frappe.msgprint( __("Crono validation failed: invalid Crono number.") );
	    } else {
            var success = true;
            /* Input data */
            try {
                cur_frm.set_value('operator', workbook.Sheets['export']['B2'].v);
                var test_date_str = String(workbook.Sheets['export']['C2'].v);
                var test_date_parts = test_date_str.split("-");
                cur_frm.set_value('date_of_test', 
                    (test_date_parts[2] + "-" + test_date_parts[1] + "-" + test_date_parts[0]));
                cur_frm.set_value('test_apparatus', workbook.Sheets['export']['D2'].v);
                cur_frm.set_value('temperature', workbook.Sheets['export']['E2'].v);
                cur_frm.set_value('pressure', workbook.Sheets['export']['F2'].v);
                cur_frm.set_value('relative_humidity', workbook.Sheets['export']['G2'].v);
                cur_frm.set_value('damage_zone_front', workbook.Sheets['export']['H2'].v);
                cur_frm.set_value('damage_zone_back', workbook.Sheets['export']['I2'].v);
                cur_frm.set_value('time_after_combustion', 
                    (String(workbook.Sheets['export']['J2'].v)).replace("<", "&lt;").replace(">", "&gt;"));
                cur_frm.set_value('dripping', 
                    (String(workbook.Sheets['export']['K2'].v)).replace("<", "&lt;").replace(">", "&gt;"));
                cur_frm.set_value('daily_check_file_name', workbook.Sheets['export']['AF2'].v);
            }
            catch (err) {
                frappe.msgprint( __("Error parsing input data: ") + err.message, __("Error"));
                success = false;
            }
            /* Vectors */
            try {
                var time_str = workbook.Sheets['export']['L2'].v;
                for (var r = 3; r <= 402; r++) {
                    time_str += "," + workbook.Sheets['export']['L' + r].v;
                }
                cur_frm.set_value('data_time', time_str);
                var hrr_str = workbook.Sheets['export']['M2'].v;
                for (var r = 3; r <= 402; r++) {
                    hrr_str += "," + workbook.Sheets['export']['M' + r].v;
                }
                cur_frm.set_value('data_hrr', hrr_str);
                var thr_str = workbook.Sheets['export']['N2'].v;
                for (var r = 3; r <= 402; r++) {
                    thr_str += "," + workbook.Sheets['export']['N' + r].v;
                }
                cur_frm.set_value('data_thr', thr_str);
                var transmission_str = workbook.Sheets['export']['O2'].v;
                for (var r = 3; r <= 402; r++) {
                    transmission_str += "," + workbook.Sheets['export']['O' + r].v;
                }
                cur_frm.set_value('data_transmission', transmission_str);
                var spr_str = workbook.Sheets['export']['P2'].v;
                for (var r = 3; r <= 402; r++) {
                    spr_str += "," + workbook.Sheets['export']['P' + r].v;
                }
                cur_frm.set_value('data_spr', spr_str);
                var tsp_str = workbook.Sheets['export']['Q2'].v;
                for (var r = 3; r <= 402; r++) {
                    tsp_str += "," + workbook.Sheets['export']['Q' + r].v;
                }
                cur_frm.set_value('data_tsp', tsp_str);
            }
            catch (err) {
                frappe.msgprint( __("Error parsing vectors: ") + err.message, __("Error"));
                success = false;                
            }
            
            /* Results */
            try {
                cur_frm.set_value('kt', workbook.Sheets['export']['R2'].v);
                cur_frm.set_value('hrr_max', workbook.Sheets['export']['S2'].v);
                cur_frm.set_value('chart_hrr_y_max', workbook.Sheets['export']['S2'].v);
                cur_frm.set_value('hrr_max_time', workbook.Sheets['export']['T2'].v);
                cur_frm.set_value('transmittance_min', workbook.Sheets['export']['U2'].v);
                cur_frm.set_value('transmittance_min_time', workbook.Sheets['export']['V2'].v);
                cur_frm.set_value('spr_max', workbook.Sheets['export']['W2'].v);
                if (Number(workbook.Sheets['export']['W2'].v) < 1) {
                    cur_frm.set_value('chart_spr_y_max', '1');
                } else {
                    cur_frm.set_value('chart_spr_y_max', workbook.Sheets['export']['W2'].v);
                }
                cur_frm.set_value('spr_max_time', workbook.Sheets['export']['X2'].v);
                cur_frm.set_value('peak_hrr', workbook.Sheets['export']['S2'].v);
                cur_frm.set_value('thr_1200s', workbook.Sheets['export']['Y2'].v);
                cur_frm.set_value('chart_thr_y_max', workbook.Sheets['export']['Y2'].v);                
                cur_frm.set_value('figra', workbook.Sheets['export']['Z2'].v);
                cur_frm.set_value('peak_spr', workbook.Sheets['export']['W2'].v);
                cur_frm.set_value('tsp_1200s', workbook.Sheets['export']['AA2'].v);
                cur_frm.set_value('chart_tsp_y_max', workbook.Sheets['export']['AA2'].v);
                cur_frm.set_value('flame_spread', workbook.Sheets['export']['AB2'].v);
                cur_frm.set_value('class_general', workbook.Sheets['export']['AC2'].v);
                cur_frm.set_value('class_smoke', workbook.Sheets['export']['AD2'].v);
                cur_frm.set_value('class_dripping', workbook.Sheets['export']['AE2'].v);
                cur_frm.set_value('chart_transmittance_y_max', '100');
            }
            catch (err) {
                frappe.msgprint( __("Error parsing results: ") + err.message, __("Error"));
                success = false;                
            }
            
            if (success) {
                frappe.msgprint( __("ELAB data imported.") , __("Success"));
            } 
            
            /* fetch test apparatus parameters */
            frappe.call({
                "method": "frappe.client.get",
                "args": {
                    "doctype": "Apparatus",
                    "name": frm.doc.test_apparatus
                },
                "callback": function(response) {
                    var test_apparatus = response.message;

                    if (test_apparatus) {
                        cur_frm.set_value('kp', test_apparatus.en50399_kp);
                        cur_frm.set_value('e1', 17200);
                        cur_frm.set_value('radius_of_tube', (test_apparatus.en50399_d / 2));
                    } else {
                        frappe.msgprint("Test Apparatus not found");
                    }
                }
            });
	    }

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

