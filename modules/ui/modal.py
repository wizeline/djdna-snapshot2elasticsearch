import dash_bootstrap_components as dbc
import dash_html_components as html

from dash.dependencies import Output, Input, State, MATCH

class Modal:
  def __init__(self, title, body, index):
    self.title = title 
    self.body = body
    self.index = index

  def create(self):
    return dbc.Modal([
            dbc.ModalHeader(self.title),
            dbc.ModalBody(self.body, style={'text-align' : 'justify', 'white-space' : 'pre-line'}),
            dbc.ModalFooter(
                html.Button([
                    html.Span('CLOSE', className='mdc-button__label')
                ], className='mdc-button mdc-button--raised', id={'index' : self.index, 'role' : 'close'}),
            )
        ],
        id={'index': self.index, 'role': 'modal'},
        className='modal-dialog-scrollable',
    )

def set_toggle_modal(app):
    '''
    Sets the callback to control the behavior of the modal.
    '''
    @app.callback(
    Output({'index': MATCH, 'role': 'modal'}, "is_open"),
    [Input({'index': MATCH, 'role': 'open'}, "n_clicks"), Input({'index': MATCH, 'role': 'close'}, "n_clicks")],
    [State({'index': MATCH, 'role': 'modal'}, "is_open")])
    def toggle_modal(n1, n2, is_open):
        if n1 or n2:
            return not is_open
        return is_open
