import dash_bootstrap_components as dbc

from modules.modal import Modal

class ListItem():
    def __init__(self, heading, text, id):
        self.heading = heading
        self.text = text
        self.id = id

    def create(self):
        return dbc.ListGroupItem([
            dbc.Row([
                dbc.Col(dbc.ListGroupItemText(self.heading)),
                dbc.Col(dbc.Button('Read article', {'index': self.id, 'role': 'open'} ))
            ]),
            Modal(self.heading, self.text, self.id).create()
        ])
