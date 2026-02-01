# Main window config
MAIN_WINDOW_TITLE = 'TextEditor'
MAIN_WINDOW_SIZE = '800x500'

# Notebook config for the "layout" function
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
