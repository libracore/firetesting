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

function get_customer(frm) {
    frappe.call({
        method: 'firetesting.fire_testing.doctype.crono.crono.get_customer',
        args: { 
            'doc': frm.doc.crono
        },
        callback: function(r) {
            if (r.message) {
                if (r.message.customer_name == "no customer defined!") {
                    frappe.msgprint({
                        title: __("Crono app"),
                        message: __("Customer not found. Please enter the customer reference in the crono first."),
                        indicator: 'red'
                    });
                } else {
                    frm.set_value('customer', r.message.customer_name);
                }
            }
        }
    });
}
