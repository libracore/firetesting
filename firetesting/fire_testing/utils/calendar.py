# -*- coding: utf-8 -*-
# Copyright (c) 2018, libracore and contributors
# For license information, please see license.txt
#
# call the API from
#   /api/method/firetesting.fire_testing.utils.calendar.download_calendar
#
# SEURITY NOTICE: this exposes the public calendar on an open API. 
#       Make sure the above API call is blocked from the internet (only use in intranet).
#       E.g. when using an apache gateway proxy
#         ProxyPass /api/method/firetesting.fire_testing.utils.calendar.download_calendar !
#
from icalendar import Calendar, Event
from datetime import datetime
import frappe

def get_calendar():
    # check access
    
    if not
    # initialise calendar
    cal = Calendar()

    # set properties
    cal.add('prodid', '-//fire testing module//libracore//')
    cal.add('version', '2.0')

    # get data
    sql_query = """SELECT * FROM `tabEvent` WHERE `event_type` = 'Public'"""
    events = frappe.db.sql(sql_query, as_dict=True)
    # add events
    for erp_event in events:
	event = Event()
	event.add('summary', erp_event['subject'])
	event.add('dtstart', erp_event['starts_on'])
	if erp_event['ends_on']:
	    event.add('dtend', erp_event['ends_on'])
	event.add('dtstamp', erp_event['modified'])
	event.add('description', erp_event['description'])
	# add to calendar
	cal.add_component(event)
    
    return cal

@frappe.whitelist(allow_guest=True)
def download_calendar():
    frappe.local.response.filename = "calendar.ics"
    frappe.local.response.filecontent = (get_calendar()).to_ical()
    frappe.local.response.type = "download"
