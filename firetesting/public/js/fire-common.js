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

function reload_dialog(title, message) {
    var d = new frappe.ui.Dialog({
    	'title': title,
    	'fields': [
            {'fieldname': 'ht', 'fieldtype': 'HTML'}
        ],
        primary_action: function() {
            // hide form
            d.hide();
            // reload form
            location.reload();
        },
        primary_action_label: __('OK')
    });
    
    d.fields_dict.ht.$wrapper.html('<p>' + message + '</p>');
    
    d.show();
}

function standardDeviation(values){
  var avg = average(values);
  
  var squareDiffs = values.map(function(value){
    var diff = value - avg;
    var sqrDiff = diff * diff;
    return sqrDiff;
  });
  
  var avgSquareDiff = average(squareDiffs);

  var stdDev = Math.sqrt(avgSquareDiff);
  return stdDev;
}

function average(values){
  var sum = values.reduce(function(sum, value){
    return sum + value;
  }, 0);

  var avg = sum / values.length;
  return avg;
}

// access protection: remove sections
function access_protection() {
    if (!frappe.user.has_role("Limited Access")) {
        // disable all attachments
        var styleSheet = document.createElement("style");
        styleSheet.innerText = ".attachment-row { display: none; }";
        document.head.appendChild(styleSheet);
        
        // show public files
        setTimeout(function () {
            var files = document.getElementsByClassName("attachment-row");
            for (var i = 0; i < files.length; i++) {
                if (!files[i].innerHTML.includes("private")) {
                    files[i].style.display = "block";
                }
            }
        }, 500);
    } 
}

// access protection triggers
frappe.ui.form.on("Customer", {
    refresh(frm) { 
        $('.form-heatmap').hide();
        $('.form-stats').hide();
        if (!frappe.user.has_role("Limited Access")) {
            $('.form-dashboard').hide();
        }
        access_protection(); }
});
frappe.ui.form.on("Crono", {
    refresh(frm) { access_protection(); }
});
frappe.ui.form.on("Certification Attachment", {
    refresh(frm) { access_protection(); }
});
frappe.ui.form.on("Inspection Attachment", {
    refresh(frm) { access_protection(); }
});
