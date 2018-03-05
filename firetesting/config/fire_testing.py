from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Main records"),
			"icon": "fa fa-book",
			"items": [
				{
					"type": "doctype",
					"name": "Classification",
					"description": _("Classification records.")
				},
				{
					"type": "doctype",
					"name": "Crono",
					"description": _("Crono records.")
				},
				{
					"type": "doctype",
					"name": "Material",
					"description": _("Material database.")
				}
			]
		},
		{
			"label": _("Tests"),
			"icon": "fa fa-flask",
			"items": [
				{
					"type": "doctype",
					"name": "EN 50399",
					"label": _("Test 10 - EN 50399 Burner"),
					"description": _("Test 10 - EN 50399 Burner")
				},
				{
					"type": "doctype",
					"name": "EN 60332 1 2",
					"label": _("Test 11 - EN 60332-1-2 Flame propagation"),
					"description": _("Test 11 - EN 60332-1-2 Flame propagation")
				},
				{
					"type": "doctype",
					"name": "EN 61034 2",
					"label": "Test 12 - EN 61034-2 Smoke density",
					"description": _("Test 12 - EN 61034-2 Smoke density")
				},
				{
					"type": "doctype",
					"name": "EN 60754 2",
					"label": _("Test 13 - EN 60754-2 Acidity"),
					"description": _("Test 13 - EN 60754-2 Acidity")
				}
			]
		},
		{
			"label": _("Reference documents"),
			"icon": "fa fa-file-text",
			"items": [
				{
					"type": "doctype",
					"name": "Test request",
					"label": _("Test request"),
					"description": _("Test request"),
				},
				{
					"type": "doctype",
					"name": "Sample identification",
					"label": _("Sample identification"),
					"description": _("Sample identification"),
				},
				{
					"type": "doctype",
					"name": "Technical data sheet",
					"label": _("Technical data sheet"),
					"description": _("Technical data sheet"),
				},
				{
					"type": "doctype",
					"name": "EXAP calculation",
					"label": _("EXAP calculation"),
					"description": _("EXAP calculation")
				}
			]
		},
		{
			"label": _("Reports"),
			"icon": "fa fa-file-text-o",
			"items": [
				{
					"type": "report",
                    "doctype": "Material",
					"name": "Unidentified material",
					"label": _("Unidentified material"),
					"description": _("Unidentified material"),
				}
			]
		},
		{
			"label": _("Configuration"),
			"icon": "fa fa-cogs",
			"items": [
				{
					"type": "doctype",
					"name": "Test Apparatus",
					"label": _("Test Apparatus"),
					"description": _("Test Apparatus"),
				},
                {
					"type": "doctype",
					"name": "Laboratory",
					"label": _("Laboratory"),
					"description": _("Laboratory"),
				},
                {
					"type": "doctype",
					"name": "Picture Description",
					"label": _("Picture Description"),
					"description": _("Picture Description"),
				}
			]
		},
		{
			"label": _("Tools"),
			"icon": "fa fa-wrench",
			"items": [
				{
					"type": "page",
					"name": "cable_length_calculator",
					"label": _("Cable Length Calculator"),
					"description": _("Cable Length Calculator"),
				}
			]
		}       
	]
