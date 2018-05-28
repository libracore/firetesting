# -*- coding: utf-8 -*-
# Copyright (c) 2018, libracore and contributors
# For license information, please see license.txt
import icalendar

def get_calendar():
    # initialise calendar
    cal = Calendar()
    from datetime import datetime

    # set properties
    cal.add('prodid', '-//libracore fire testing module//mxm.dk//')
    cal.add('version', '2.0')

    # one sample event
    import pytz
    event = Event()
    event.add('summary', 'Python meeting about calendaring')
    event.add('dtstart', datetime(2005,4,4,8,0,0,tzinfo=pytz.utc))
    event.add('dtend', datetime(2005,4,4,10,0,0,tzinfo=pytz.utc))
    event.add('dtstamp', datetime(2005,4,4,0,10,0,tzinfo=pytz.utc))
    # add to calendar
    cal.add_component(event)
    
    return cal
