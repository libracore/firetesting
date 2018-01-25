// Copyright (c) 2018, libracore GmbH and contributors
// For license information, please see license.txt

frappe.ui.form.on('EN 50399', {
	refresh: function(frm) {

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
