import dash_html_components as html
import dash_bootstrap_components as dbc

class Progress():
    def __init__(self, label, value):
        self.label = label
        self.value = value

    def create(self):
        return html.Div([
                dbc.Row([
                    dbc.Col(self.label.capitalize(), width=1, style={ 'textAlign':'right'}),
                    dbc.Col(dbc.Progress(id=self.label), width=4),
                ])
            ]
        )