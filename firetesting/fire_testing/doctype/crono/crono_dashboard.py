from frappe import _

def get_data():
   return {
      'fieldname': 'crono',
      'transactions': [
         {
            'label': _('Records'),
            'items': ['Material']
         },

         {
            'label': _('Documents'),
            'items': ['Test request', 'Sample identification', 'Technical data sheet']
         },
         {
            'label': _('Tests'),
            'items': ['EN 50399', 'Test 11', 'Test 12', 'Test 13']
         }
      ]
   }
