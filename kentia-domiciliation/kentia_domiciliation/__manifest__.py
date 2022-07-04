# -*- coding: utf-8 -*-
{
    'name': "KENTIA DOMICILIATION",

    'summary': """
        Backend Customization
        """,

    'description': """
        Backend Customization
    """,

    'author': "KASIA SARL",
    'website': "https://kasia.mg",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'contacts',
        'crm',
        'sale_management',
        'subscription_management',
        'om_account_accountant',
        'invoice_bulk_mailing',
        'ks_website_blog_editor',
        'ks_website_event_editor',
    ],
    'data': [
        #security
        'security/ir.model.access.csv',
        # data
        'data/ir_sequence_data.xml',
        'data/template_mail.xml',
        'data/ir_cron_mail.xml',
        # views
        'views/report_layout.xml',
        'views/action_manager.xml',
        'views/res_partner_views.xml',
        'views/product_template_views.xml',
        'views/sale_order_views.xml',
        'views/subscription_subscription_views.xml',
        'views/account_move_inherit_views.xml',
        'views/account_declaration_views.xml',
        'reports/report_saleorder_templates.xml',
        'reports/report_invoice_templates.xml',
    ],
}