from frappe import _

def get_data():
   return {
      'fieldname': 'crono',
      'transactions': [
         {
            'label': _('Tests'),
            'items': ['EN 50399', 'Test 11', 'Test 12', 'Test 13']
         },
         {
            'label': _('Documents'),
            'items': ['Test request', 'Sample identification', 'Technical data sheet']
         },
         {
            'label': _('Records'),
            'items': ['Material']
         }
      ]
   }
