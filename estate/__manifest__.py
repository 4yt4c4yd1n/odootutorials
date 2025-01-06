{
    'name': 'Estate',
    'version': '1.0',
    'category': 'Sales/Estate',
    'sequence': 15,
    'summary': 'Estate',
    'description': "Realest estate",
    'website': 'https://www.odoo.com/page/crm',
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property.xml',
        'views/estate_menus.xml',
        'views/property_type.xml',
        'views/property_tag.xml',
        'views/property_offers.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}