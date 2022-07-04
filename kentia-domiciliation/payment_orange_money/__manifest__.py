# -*- coding: utf-8 -*-
{
    'name': 'Orange Money Payment Acquirer',
    'summary': 'Payment Acquirer : Orange Money Implementation',
    'description': """Payment Acquirer : Orange Money Implementation""",
    'category': 'Accounting',
    'version': '0.1',
    'depends': ['payment', 'website'],
    'website': 'https://kasia.mg',
    'author': "KASIA SARL",
    'license': 'OPL-1',
    'data': [
        'views/payment_views.xml',
        'views/payment_om_templates.xml',
        'data/payment_acquirer_data.xml',
    ],
    'installable': True,
    'price': '120',
    'currency': 'EUR',
}
