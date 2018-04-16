from frappe import _

def get_data():
   return {
      'fieldname': 'material',
      'transactions': [
         {
            'label': _('Crono'),
            'items': ['Crono']
         },
         {
            'label': _('Cable tests'),
            'items': ['EN 50399', 'EN 60332 1 2', 'EN 61034 2', 'EN 60754 2']
         }
      ]
   }
