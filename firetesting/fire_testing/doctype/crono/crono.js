// Copyright (c) 2017, libracore GmbH and contributors
// For license information, please see license.txt

frappe.ui.form.on('Crono', {
	refresh: function(frm) {
		cur_frm.fields_dict['quotation_number'].get_query = function(doc) {
			return {
				filters: {
					"customer": frm.doc.customer
				}
			}
		}
		cur_frm.add_fetch('quotation_number','transaction_date','quotation_exit');
	},
	
	crono_status: function(frm) {
		if(!cur_frm.doc.material_receive && cur_frm.doc.crono_status=='Work in progress') {
			cur_frm.set_value('crono_status', '');
			frappe.msgprint('For status work in progress, the material must be available!');
		}
		if(!cur_frm.doc.material_receive && cur_frm.doc.crono_status=='Finish') {
			cur_frm.set_value('crono_status', '');
			frappe.msgprint('For status Finish, the material must be available!');
		}
		if(!cur_frm.doc.quotation_exit && cur_frm.doc.crono_status!='') {
			cur_frm.set_value('crono_status', '');
			frappe.msgprint('At first, a quotation must be done!');
		}
	}
});
