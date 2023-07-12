# -*- coding: utf-8 -*-
{
    'name': "Aterra",
    'version': '1.0',
    'description': "Aterra Card Game",
    'summary': "Aterra Card Game",

    'author': "Joseph Maiarana",
    'website': "www.WarforAterra.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'App',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web','website'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/aterra_card.xml',
        'views/res_partner_view.xml',
    ],
    'qweb': [
        'static/src/xml/aterra_card.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'images': [
        'aterra/static/description/Aterra_Logo_Nebula_Back_White_1.1.png',
    ],
    'installable': True,
    'application': True,
    'installable': True,
    'auto_install': False,

    'assets': {
        'web.assets_frontend': [
            "aterra/static/src/css/aterra_card.css",
        ]
    },
    'icon': "aterra/static/description/Aterra_dragon_icon.png",

}
