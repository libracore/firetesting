from frappe import _

def get_data():
   return {
      'fieldname': 'crono',
      'transactions': [
         {
            'label': _('Tests'),
            'items': ['Test 10', 'Test 11', 'Test 12', 'Test 13']
         }
      ]
   }