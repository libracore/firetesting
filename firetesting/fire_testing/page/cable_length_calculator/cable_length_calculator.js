frappe.pages['cable_length_calculator'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: __('Cable Length Calculator'),
		single_column: true
	});

	frappe.cable_length_calculator.make(page);
	frappe.cable_length_calculator.run(page);
    
    // add the application reference
    frappe.breadcrumbs.add("Fire Testing");
    
    // attach button handlers
    this.page.main.find(".btn-calculate").on('click', function() {
        var me = frappe.cable_length_calculator;
        
        // get diameter in mm
        var diameter = document.getElementById("diameter").value;

        if ((diameter != "") && (!isNaN(diameter))) {
            // calculate the mounting parameters
            frappe.call({
                method: 'firetesting.fire_testing.doctype.en_50399.en_50399.calculate_mounting',
                args: {
                    'diameter': diameter
                },
                callback: function(r) {
                    if (r.message) {
                        var parent = page.main.find(".mounting-results").empty();
                        $('<p>' + __("Number of cables") + ": " + r.message[0] + "<br>" + 
                            __("Width") + ": " + r.message[1] + " mm<br>" + 
                            __("Spacing") + ": " + r.message[2] + " mm<br>" + 
                            __("Required cable") + ": " + r.message[3] + ' m</p>').appendTo(parent);
                    } 
                }
            }); 
        } else {
            frappe.msgprint( __("Please insert a valid diameter") );
        }
               

    });
}

frappe.cable_length_calculator = {
	start: 0,
	make: function(page) {
		var me = frappe.cable_length_calculator;
		me.page = page;
		me.body = $('<div></div>').appendTo(me.page.main);
		var data = "";
		$(frappe.render_template('cable_length_calculator', data)).appendTo(me.body);      

	},
	run: function(page) {
 
	}
}
