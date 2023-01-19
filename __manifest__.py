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
        'views/contract.xml',
        'views/action.xml',


    ],

    'sequence': 1,
    'installable': True,
    'application': True,
    'auto_install': False,
}