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
					"name": "Test 10",
					"label": _("Test 10 - EN 50399 Burner"),
					"description": _("Test 10 - EN 50399 Burner")
				},
				{
					"type": "doctype",
					"name": "Test 11",
					"label": _("Test 11 - EN 60332-1-2 Flame propagation"),
					"description": _("Test 11 - EN 60332-1-2 Flame propagation")
				},
				{
					"type": "doctype",
					"name": "Test 12",
					"label": "Test 12 - EN 61034-2 Smoke density",
					"description": _("Test 12 - EN 61034-2 Smoke density")
				},
				{
					"type": "doctype",
					"name": "Test 13",
					"label": _("Test 13 - EN 60754-2 Accidity"),
					"description": _("Test 13 - EN 60754-2 Accidity")
				}
			]
		}
	]
