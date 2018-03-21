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
            'items': ['Customer Test Request', 'Sample identification', 'Technical data sheet']
         },
         {
            'label': _('Tests'),
            'items': ['EN 50399', 'EN 60332 1 2', 'EN 61034 2', 'EN 60754 2']
         }
      ]
   }
