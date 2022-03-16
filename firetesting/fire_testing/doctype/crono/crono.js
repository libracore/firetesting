// Copyright (c) 2017-2018, libracore GmbH and contributors
// For license information, please see license.txt

frappe.ui.form.on('Crono', {
    refresh: function(frm) {
        //Filter for sales_order based on customer link field
        cur_frm.fields_dict['sales_order'].get_query = function(doc) {
            return {
                filters: {
                    "customer": frm.doc.customer
                }
            }
        };
        cur_frm.fields_dict['classification'].get_query = function(doc) {
        return {
            filters: {
            "customer": frm.doc.customer
            }
        }
        };
        cur_frm.fields_dict['material'].get_query = function(doc) {
        return {
            filters: {
            "customer": frm.doc.customer,
            "type": ["!=", "Component"]
            }
        }
        };
                
        // provide lock & unlock for system manager and crono manager
        if ((frappe.user.has_role("System Manager")) || (frappe.user.has_role("Crono Manager"))) {
            if(frm.doc.docstatus==0) {
            frm.add_custom_button(__("Lock"), function() {
                lock(frm);
                });
            } else {
            frm.add_custom_button(__("Unlock"), function() {
                unlock(frm);
                });
            }
        }
        
        // check if this is a new document
        if (frm.doc.__islocal) {
        if ((frm.doc.sales_order != null) && (frm.doc.sales_order != 'select')) {
            // in case of creating from sales order
            frappe.call({
                "method": "frappe.client.get",
                "args": {
                    "doctype": "Sales Order",
                    "name": frm.doc.sales_order
                },
                "callback": function(response) {
                    var so = response.message;
                    if (so) {
                        frm.set_value('customer', so.customer);
                        console.log(so);
                        frm.set_value('sample_name', so.material);
                        frm.set_value('test_methods', so.test_methods);
                    } else {
                        frappe.msgprint("Sales order not found");
                    }
                }
            });
        }
        else if ((frm.doc.classification != null) && (frm.doc.classification != 'select')) {
            // in case of creating from classification
            frappe.call({
                "method": "frappe.client.get",
                "args": {
                "doctype": "Classification",
                "name": frm.doc.classification
                },
                "callback": function(response) {
                var classification = response.message;
                if (classification) {
                    frm.set_value('customer', classification.customer);
                    frm.set_value('sales_order', classification.sales_order);
                } else {
                    frappe.msgprint("Classification not found");
                }
                }
            });
        }
        }
    },
    sales_order: function(frm) {
        cur_frm.add_fetch('sales_order','material','sample_name'); 
        cur_frm.add_fetch('sales_order','customer','customer');
        cur_frm.add_fetch('sales_order','test_methods','test_methods'); 
    },
    classification: function(frm) {
        // classification has changed, fetch sales order and customer
        cur_frm.add_fetch('classification','sales_order','sales_order');
        cur_frm.add_fetch('classification','customer','customer');
    }
});

// lock crono
function lock(frm) {
    frappe.call({
        method: 'firetesting.fire_testing.doctype.crono.crono.lock',
        args: { 
            'doc': frm.doc.name
        },
        callback: function(r) {
            // refresh
            location.reload();
        }
    });
}

// unlock crono
function unlock(frm) {
    frappe.call({
        method: 'firetesting.fire_testing.doctype.crono.crono.unlock',
        args: { 
            'doc': frm.doc.name
        },
        callback: function(r) {
            // refresh
            location.reload();
        }
    });
}
