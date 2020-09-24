import base64
import dash_html_components as html

def load_image(image_path):
    encoded_image = base64.b64encode(open(image_path,'rb').read()) 
    return 'data:image/svg+xml;base64,{}'.format(encoded_image.decode())

logo_header = (
    html.Header([
        html.Div([
            html.Section([
                html.Div([
                    html.A([
                        html.Img(
                        src=load_image('resources/images/dev_platform_one_line_full_color.svg'), width='345px')
                    ], id='top')
                ]),
            ], className='mdc-top-app-bar__section mdc-top-app-bar__section--align-start'),
            html.Section([
                html.Img( src=load_image('resources/images/dj-prototypes-logo.svg') )
            ], className='mdc-top-app-bar__section mdc-top-app-bar__section--align-end', role='toolbar')
        ], className='mdc-top-app-bar__row')
    ], className='mdc-top-app-bar')
)

title = (
    html.Div([
        html.H1(
            'Company Risk Monitoring', 
            className='mdc-typography--headline1 mdc-theme--primary', 
            style={'margin-top' : '72px', 'margin-bottom' : '72px'}
        ),
    ])
)
