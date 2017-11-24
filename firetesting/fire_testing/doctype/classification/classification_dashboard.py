from frappe import _

def get_data():
   return {
      'fieldname': 'classification',
      'transactions': [
         {
            'label': _('Cronos'),
            'items': ['Crono']
         }
         {
            'label': _('Information'),
            'items': ['Annex A']
         }
      ]
   }
