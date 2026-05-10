# Used at editor.py for window config.
MAIN_WINDOW_TITLE = 'RNoTe'
MAIN_WINDOW_SIZE = '800x500'

# Used at main_menu.py for the "about" dialog.
FIRST_INFO = '项目开源在：https://github.com/SkyElysium/RNoTe'
SECOND_INFO = '''\n
Licensed Under the MIT License.
Copyright (c) 2025 SkyElysium.
'''

ISSUE_URL = 'https://github.com/SkyElysium/RNoTe/issues/new'

# Used at custom_notebook.py for the "layout" function.
CUSTOM_NOTEBOOK_STYLE = [('CustomNotebook.tab',
{
    'sticky': 'nswe',
    'children': [
        ('CustomNotebook.padding',
        {
            'side': 'top',
            'sticky': 'nswe',
            'children': [
                ('CustomNotebook.focus',
                {
                    'side': 'top',
                    'sticky': 'nswe',
                    'children': [
                        ('CustomNotebook.label',
                        {
                            'side': 'left',
                            'sticky': ''
                        }), ('CustomNotebook.close',
                        {
                            'side': 'right',
                            'sticky': ''
                        })
                    ]
                })
            ]
        })
    ]
})]

CUSTOM_X_SCROLLBAR_STYLE = [
    (
        "Custom.Horizontal.TScrollbar.trough",
        {
            "children": [
                (
                    "Custom.Horizontal.TScrollbar.thumb",
                    {
                        "unit": "1",
                        "children": [
                            ("Custom.Horizontal.TScrollbar.grip", {"sticky": ""})
                        ],
                        "sticky": "nswe",
                    },
                )
            ],
            "sticky": "we",
        },
    )
]
