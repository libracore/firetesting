// Copyright (c) 2017, libracore GmbH and contributors
// For license information, please see license.txt

frappe.ui.form.on('Crono', {
	refresh: function(frm) {
		//Filter for quotation_number based on customer link field
		cur_frm.fields_dict['quotation_number'].get_query = function(doc) {
			return {
				filters: {
					"customer": frm.doc.customer
				}
			}
		}
		//Filter for sales_order based on customer link field
		cur_frm.fields_dict['sales_order'].get_query = function(doc) {
			return {
				filters: {
					"customer": frm.doc.customer
				}
			}
		}
		//Fetch value transaction_date into field quotation_exit from quotation based quotation_number
		cur_frm.add_fetch('quotation_number','transaction_date','quotation_exit');
		
	},
	
	crono_status: function(frm) {
		//Work i progress only when material received
		if(!cur_frm.doc.material_receive && cur_frm.doc.crono_status=='Work in progress') {
			cur_frm.set_value('crono_status', '');
			frappe.msgprint('For status work in progress, the material must be available!');
		}
		//Finish only when material received
		if(!cur_frm.doc.material_receive && cur_frm.doc.crono_status=='Finish') {
			cur_frm.set_value('crono_status', '');
			frappe.msgprint('For status Finish, the material must be available!');
		}
		//Check if a quotation is linked 
		if(!cur_frm.doc.quotation_exit && cur_frm.doc.crono_status!='') {
			cur_frm.set_value('crono_status', '');
			frappe.msgprint('At first, a quotation must be done!');
		}
		//Check if a sales order is linked
		if(!cur_frm.doc.sales_order && cur_frm.doc.crono_status!='' && cur_frm.doc.crono_status!='Backlog') {
			cur_frm.set_value('crono_status', '');
			frappe.msgprint('At first, a sales order must exist!');
		}
	},
	//Set prop. "set_only_once" after save
	validate: function(frm) {
		if(cur_frm.doc.sales_order) {
			cur_frm.set_df_property('sales_order','set_only_once',1);
		}
		if(cur_frm.doc.red_standard_selection) {
			cur_frm.set_df_property('red_standard_selection','set_only_once',1);
		}
		if(cur_frm.doc.material_receive) {
			cur_frm.set_df_property('material_receive','set_only_once',1);
		}
	},
	//Set/remove mandatory from material based on material receive date
	material_receive: function(frm) {
		if(!cur_frm.doc.material_receive) {
			cur_frm.set_df_property('material','reqd',0);
		}else{
			cur_frm.set_df_property('material','reqd',1);
		}
	}
});
