# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "firetesting"
app_title = "Fire Testing"
app_publisher = "libracore GmbH"
app_description = "Tools for fire testing labs"
app_icon = "octicon octicon-flame"
app_color = "red"
app_email = "info@libracore.com"
app_license = "GPL"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/firetesting/css/firetesting.css"
# app_include_js = "/assets/firetesting/js/firetesting.js"

# include js, css files in header of web template
# web_include_css = "/assets/firetesting/css/firetesting.css"
# web_include_js = "/assets/firetesting/js/firetesting.js"

# for desk css
app_include_css = ["/assets/css/firetesting.min.css"]

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
doctype_js = {
    "EN 50399" :   ["public/js/xlsx.full.min.js", "public/js/fire-common.js"],
    "EN 61034 2" : "public/js/fire-common.js",
    "EN 60332 1 2" :  "public/js/fire-common.js",
    "EN 60754 2" :    "public/js/fire-common.js",
    "Crono Verification" : "public/js/fire-common.js",
	"Sales Order": "public/js/sales_order.js"
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "firetesting.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "firetesting.install.before_install"
# after_install = "firetesting.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "firetesting.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"firetesting.tasks.all"
# 	],
# 	"daily": [
# 		"firetesting.tasks.daily"
# 	],
# 	"hourly": [
# 		"firetesting.tasks.hourly"
# 	],
# 	"weekly": [
# 		"firetesting.tasks.weekly"
# 	]
# 	"monthly": [
# 		"firetesting.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "firetesting.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "firetesting.event.get_events"
# }

