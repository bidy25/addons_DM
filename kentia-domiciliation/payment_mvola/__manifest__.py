# -*- coding: utf-8 -*-
{
    'name': 'Mvola Payment Acquirer',
    'summary': 'MVOLA Payment Acquirer',
    'description': """MVOLA Payment Acquirer""",
    'category': 'Accounting',
    'version': '2.0',
    'depends': ['payment','website'],
    'website': 'https://kasia.mg',
    'author': "KASIA SARL",
    'license': 'OPL-1',
    'data': [
        'views/payment_views.xml',
        'views/payment_mvola_templates.xml',
        'data/payment_acquirer_data.xml',
    ],
    'installable': True,
    'price': '120',
    'currency': 'EUR',
}
