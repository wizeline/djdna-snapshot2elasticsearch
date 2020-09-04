import dash_html_components as html

class Progress():
    def __init__(self, value):
        self.value = value

    def create(self):
        return html.Div([
            html.Div([
                html.Div(className='mdc-linear-progress__buffer-bar')
            ],className='mdc-linear-progress__buffer'),
            html.Div([
                html.Span(className='mdc-linear-progress__bar-inner')
            ], 
            className='mdc-linear-progress__bar mdc-linear-progress__primary-bar', 
            style={'transform': 'scaleX({})'.format(self.value)})
        ], role='progressbar', className='mdc-linear-progress')
        