# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name" : "WhatsApp Live Chat",
    "author" : "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Website",
    "summary": """
   whatsapp live chat app, whatsapp chat by odoo website, client whatsup chat module
                    """,
    "description": """
    
Chat with your customers through WhatsApp, the most popular messaging app. Vital extension for your odoo website, which allows you to create stronger relationships with your customers by guiding and advising them in their purchases in real time.
Now your customers can chat with you at WhatsApp, directly from your odoo website to the mobile!! No need to add your mobile phone number to the mobile address book.
An online chat system provides customers immediate access to help. Wait times are often much less than a call center, and customers can easily multi-task while waiting.
This extension allows you to create a WhatsApp chat button, highly configurable, to show it in different parts of your site to chat with your customers through WhatsApp, the most popular messaging app.    
    
                    """,
    "version":"13.0.2",
    "depends" : ["base", "website", "portal"],
    "application" : True,
    "data" : [
        
              "data/whatsapp_data.xml",
              "views/whatsapp.xml",
              "views/res_config_settings_view.xml",
              "views/website_view.xml",
            
            ],
    "images": ["static/description/background.png", ],
    "auto_install": False,
    "installable" : True,
    "price": 25,
    "currency": "EUR"   
}
