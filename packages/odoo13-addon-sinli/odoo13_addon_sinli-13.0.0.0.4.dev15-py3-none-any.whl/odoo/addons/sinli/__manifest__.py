# -*- coding: utf-8 -*-
######################################################################################
#
#         License**
#
########################################################################################
{
    'name': 'Integración de sinli en Odoo',
    'version': '13.0.0.0.3',
    'summary': 'Módulo para la integración de sinli en Odoo.',
    'description': 'Módulo para la integración de sinli en Odoo.',
    'category': 'Industries',
    'author': 'Colectivo DEVCONTROL',
    'author_email': 'devcontrol@zici.fr',
    'maintainer': 'Colectivo DEVCONTROL',
    'company': 'Colectivo DEVCONTROL',
    'website': 'https://framagit.org/devcontrol',
    'depends': ['sale', 'gestion_editorial'],
    "external_dependencies": {"python" : [
        "sinli",
        "python-stdnum"
    ]},
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_sinli_view.xml',
        'views/res_config_settings_sinli_view.xml',
        'views/export_libro_view.xml',
        'views/download_file.xml',
        'views/sinli_message_view.xml',
        'views/sinli_dialog_view.xml',
        'views/export_purchase_order_view.xml',
        'wizards/export_sinli/export_sinli.xml'
    ],
    'images': ['static/description/logo-devcontrol.png'],
    'license': 'OPL-1',
    'price': 0,
    'currency': 'EUR',
    'installable': True,
    'application': False,
    'auto_install': False,
}
