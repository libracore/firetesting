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
	
	quotation: function(frm) {
		
	}
});
