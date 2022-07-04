# -*- coding: utf-8 -*-
{
    'name': "WEBSITE BLOG EDITOR",
    'summary': """
        Website Blog Editor""",
    'description': """
        This module is used to edit from backoffice the blog post :
        - Content
        - Banner
        - SEO
        - Schedule blog publication        
    """,
    'author': "KASIA SARL",
    'website': "https://kasia.mg",
    'category': 'Website',
    'version': '0.1',
    'depends': ['base', 'website_blog'],
    'data': [
        # views
        'views/blog_post_views.xml',
        # data
        'data/blog_post_cron.xml'
    ],
    'license': 'LGPL-3',
    'price': '15',
    'currency': 'EUR',
    'images': ['static/description/banner_v12.jpg'],
}
