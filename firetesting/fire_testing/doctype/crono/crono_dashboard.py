from frappe import _

def get_data():
   return {
      'fieldname': 'crono',
      'transactions': [
         {
            'label': _('Documents'),
            'items': ['Customer Test Request', 'Sample identification', 'Technical data sheet', 'Crono Verification']
         },
         {
            'label': _('Cable tests'),
            'items': ['EN 50399', 'EN 60332 1 2', 'EN 61034 2', 'EN 60754 2']
         }
      ]
   }
