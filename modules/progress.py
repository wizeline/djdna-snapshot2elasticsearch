import dash_html_components as html
import dash_bootstrap_components as dbc

class Progress():
    def __init__(self, label, value):
        self.label = label
        self.value = value

    def create(self):
        return html.Div([
                dbc.Row([
                    dbc.Col(self.label.capitalize(), width=2, style={ 'textAlign':'right', 'padding-top':'0.5%'}),
                    dbc.Col(dbc.Progress(id=self.label), width=8, style={'padding-top' : '1%'})
                ])
            ]
        )
