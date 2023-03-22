{
    'name': 'Fetch So',
    'version': '16.0.1.0.0',
    'sequence': '-12',
    'summary': 'Fetch sale order',
    'description': 'Fetch sale order',

    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'website': 'https://www.cybrosys.com',
    'maintainer': 'Cybrosys Techno Solutions',
    'support': 'Cybrosys Techno Solutions',

    'category': 'sale',

    'depends': ['base', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/transfer_view.xml',
    ],

    'license': 'LGPL-3',

    'installable': True,
    'application': True,

}
