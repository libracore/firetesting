try {
  cur_frm.dashboard.add_transactions([
    {
        'label': 'Fire testing',
        'items': [
            'Classification', 'Crono'
        ]
    }
]);
} catch { /* do nothing for older versions */ }