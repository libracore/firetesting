// Copyright (c) 2017, libracore GmbH and contributors
// For license information, please see license.txt

frappe.ui.form.on('Test request', {
	refresh: function(frm) {

	}
});

// normal field change on crono does not work on the initial set
function loadCustomer() {
	cur_frm.add_fetch('crono', 'customer', 'customer');
};

// mutation observer for crono changes
var cronoObserver = new MutationObserver(function(mutations) {
     mutations.forEach(function(mutation) {
  	loadCustomer();
     });
});
var target=document.querySelector('div[data-fieldname="crono"] .control-input-wrapper .control-value');
var options = {
     attributes: true,
     characterData: true
};
cronoObserver.observe(target, options);
