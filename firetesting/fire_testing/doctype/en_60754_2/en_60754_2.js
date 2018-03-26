// Copyright (c) 2018, libracore GmbH and contributors
// For license information, please see license.txt

frappe.ui.form.on('EN 60754 2', {
	refresh: function(frm) {
        // only allow to pull data when saved and in draft
        if ((!frm.doc.__islocal) && (frm.doc.docstatus == 0)) {
            frm.add_custom_button(__("Update composition table"), function() {
                fetch_components(frm);
            });   
            /* frm.add_custom_button(__("Re-calculate"), function() {
                update_calculation(frm);
            });   */
        }
        // allow to push results to the material record
        if (!frm.doc.__islocal) {
            frm.add_custom_button(__("Push results to material"), function() {
                push_results_to_material(frm);
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
        
        // set filters
        frm.fields_dict.ph_values.grid.get_field('material').get_query =
			function() {
				return {
					filters: {
						"type": "Component"
					}
				}
			};
        frm.fields_dict.conductivity_values.grid.get_field('material').get_query =
			function() {
				return {
					filters: {
						"type": "Component"
					}
				}
			};
	},
});

function fetch_components(frm) {
     // remove all rows
     cur_frm.get_field('composition_results').grid.grid_rows.forEach(function(row) {
         row.remove();
     });
     
     // get components
     frappe.call({
         "method": "frappe.client.get_list",
         "args": {
            "doctype": "Material Component", 
            "filters": {"parent": frm.doc.material},
            "fields": ["material_code", "mass"],
            "order_by": "idx"
         },
         "callback": function(r) {
                if (r.message != null) {
                    r.message.forEach(function(component) {
                        var child = cur_frm.add_child('composition_results');
                        frappe.model.set_value(child.doctype, child.name, 'material', component.material_code);
                        frappe.model.set_value(child.doctype, child.name, 'mass', component.mass);
                        cur_frm.refresh_field('composition_results');
                        resolve_material_data(frm);
                    });
                }
            }
    });

}

function resolve_material_data(frm) {
    // resolve material data
    cur_frm.get_field('composition_results').grid.grid_rows.forEach(function(row) {
        frappe.call({
            "method": "frappe.client.get",
            "args": {
                "doctype": "Material", 
                "name": row.doc.material
            },
            "callback": function(r) {
                if (r.message != null) {
                    frappe.model.set_value(row.doc.doctype, row.doc.name, 'article_number', r.message.material_code);
                    frappe.model.set_value(row.doc.doctype, row.doc.name, 'description', r.message.description);
                    frappe.model.set_value(row.doc.doctype, row.doc.name, 'ph', r.message.ph);
                    frappe.model.set_value(row.doc.doctype, row.doc.name, 'conductivity', r.message.conductivity);
                    frappe.model.set_value(row.doc.doctype, row.doc.name, 'reference', r.message.reference);   
                    frappe.model.set_value(row.doc.doctype, row.doc.name, 'is_metallic', r.message.is_metallic);   
                    cur_frm.refresh_field('composition_results');
                    update_calculation(frm);
                }
            }
        });
     });
}

function update_calculation(frm) {
    // calculate total weight
    var total_non_metallic_weight = 0.0;
    var components = frm.doc.composition_results;
    components.forEach(function (component) {
        if (!component.is_metallic) {
            total_non_metallic_weight += component.mass;
        }
    });
    
    // calculate weighted pH and conductivity
    var weighted_ph = 0.0;
    var weighted_conductivity = 0.0;
    components.forEach(function (component) {
        if (!component.is_metallic) {
            weighted_ph += (component.mass / total_non_metallic_weight) * component.ph;
            weighted_conductivity += (component.mass / total_non_metallic_weight) * component.conductivity;
        }
    });
    
    // output
    cur_frm.set_value('total_mass', total_non_metallic_weight);
    cur_frm.set_value('weighted_ph', weighted_ph);
    cur_frm.set_value('weighted_conductivity', weighted_conductivity);
}

/* this function is used to calculate the results and push them to the material record */
function push_results_to_material(frm) {
    var trace = "";
    
    var ph_values = frm.doc.ph_values;
    // create a list of all measured materials
    var materials = new Array();  
    ph_values.forEach(function(entry) {
        if (entry.material != null) {
            if (materials.indexOf(entry.material) == -1) {
                materials.push(entry.material);
            }
        } 
    });
    
    // calculate pH value per material
    var phs = new Array();
    materials.forEach(function(material) {
        var results = new Array(); 
        ph_values.forEach(function(entry) {
            if (entry.material == material) {
                results.push(entry.ph);
            } 
        });
        if (results.length > 2) {
            var avg = average(results);
            var stddev = standardDeviation(results);
            trace += material + ": pH " + avg  + " (+/- " + stddev + ")\n"; 
            phs.push(avg);
        } else {
            frappe.msgprint( __("Not sufficient measurements (pH) for {0} (at least 3 measurements required)").replace("{0}", material));
            phs.push(0);
        }        
    });
    
    // calculate conductivity value per material
    var conductivities = new Array();
    var conductivity_values = frm.doc.conductivity_values;
    materials.forEach(function(material) {
        var results2 = new Array(); 
        conductivity_values.forEach(function(entry) {
            if (entry.material == material) {
                results2.push(entry.conductivity);
            } 
        });
        if (results2.length > 2) {
            var avg2 = average(results2);
            var stddev2 = standardDeviation(results2);
            trace += material + ": conductivity " + avg2 + " (+/- " + stddev2 + ")\n"; 
            conductivities.push(avg2);
        } else {
            frappe.msgprint( __("Not sufficient measurements (conductivity) for {0} (at least 3 measurements required)").replace("{0}", material));
            conductivities.push(0);
        }        
    });
    
    // push results to material records
    for (i = 0; i < materials.length; i++) {
        if ((phs[i] != 0) && (conductivities[i] != 0)) {
            frappe.call({
                method: 'firetesting.fire_testing.doctype.material.material.update_measurements',
                args: { 
                    material: materials[i],
                    ph: phs[i],
                    conductivity: conductivities[i],
                    reference: frm.doc.name
                },
                callback: function(r) {
                    if (r.message) {
                        frappe.show_alert(r.message.output);
                    }
                }
            });
        }
    }
    
    // write output
    frm.set_value('raw', trace);
}

