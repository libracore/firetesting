from frappe import _

def get_data():
   return {
      'fieldname': 'classification',
      'transactions': [
         {
            'label': _('Related records'),
            'items': ['Crono']
         },
         {
            'label': _('Information'),
            'items': ['Annex A']
         }
      ]
   }
