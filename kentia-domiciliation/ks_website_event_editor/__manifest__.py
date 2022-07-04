# -*- coding: utf-8 -*-
{
    'name': "WEBSITE EVENT EDITOR",
    'summary': """
        Website Event Editor""",
    'description': """
        This module is used to edit from backoffice an event :
        - Content
        - Banner
        - SEO
        - Schedule blog publication        
    """,
    'author': "KASIA SARL",
    'website': "https://kasia.mg",
    'category': 'Website',
    'version': '0.1',
    'depends': ['base', 'website_event'],
    'data': [
        # views
        'views/event_event_views.xml',
        # data
        'data/event_cron.xml'
    ],
    'license': 'LGPL-3',
    'price': '15',
    'currency': 'EUR',
    'images': ['static/description/website_event_editor_v13.jpg'],
}
