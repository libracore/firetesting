# Copyright (c) 2018, libracore GmbH and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import datetime

def execute(filters=None):
	# prepare week
	sql_query = "SELECT DATE_SUB(CURDATE(), INTERVAL WEEKDAY(CURDATE()) DAY) AS `LastMonday`"
	monday_date = frappe.db.sql(sql_query, as_dict=True)[0]['LastMonday']
	tuesday_date = monday_date + datetime.timedelta(days=1)
	wednesday_date = monday_date + datetime.timedelta(days=2)
	thursday_date = monday_date + datetime.timedelta(days=3)
	friday_date = monday_date + datetime.timedelta(days=4)
	
	# prepare grid
	columns = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
	data = [[monday_date, tuesday_date, wednesday_date, thursday_date, friday_date], 
	   [get_day(monday_date), 
	    get_day(tuesday_date), 
	    get_day(wednesday_date), 
	    get_day(thursday_date), 
	    get_day(friday_date)]]
	return columns, data

def get_day(date):
	# get full day events
	sql_query = """SELECT * 
		    FROM `tabEvent` 
		    WHERE `event_type` = 'Public' 
		      AND DATE(`starts_on`) = '{0}' 
		    ORDER BY `all_day` DESC""".format(date)
	events = frappe.db.sql(sql_query, as_dict=True)
	str_events = ""
	for event in events:
		if not event.all_day:
			try:
				str_events += "{0}:{1:02d} - {2}:{3:02d}<br>".format(
					event.starts_on.hour, event.starts_on.minute,
					event.ends_on.hour, event.ends_on.minute)
			except:
				pass
		str_events += "{0}<br>".format(event.subject)
		if event.description:
			str_events += "{0}<br>".format(event.description)
		str_events += "<br>"
	return str_events
			
