{
    'name': 'Agreement',
    'category': 'agreement',
    'version': '1.0',
    'description': "Договоры",
    'maintainer': 'admin',
    'depends': [
        'base', 'mail'
    ],
    'qweb': [
    ],

    'data': [
        'data/sequence.xml',
        'data/cron.xml',
        'security/security.xml',
        'views/handbook.xml',
        'views/contract.xml',
        'views/action.xml',
        'security/ir.model.access.csv',


    ],

    'sequence': 1,
    'installable': True,
    'application': True,
    'auto_install': False,
}