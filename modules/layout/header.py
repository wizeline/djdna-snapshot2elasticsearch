import base64
import dash_html_components as html

def load_image(image_path):
    encoded_image = base64.b64encode(open(image_path,'rb').read()) 
    return 'data:image/svg+xml;base64,{}'.format(encoded_image.decode())

logo_header = (
    html.Div([
        html.A(id='top', className='mdc-layout-grid__cell--span-12'),
        html.Div([ 
            html.Img(
                src=load_image('./resources/images/dev_platform_one_line_full_color.svg'), width='345px')
            ], className='mdc-layout-grid__cell--span-6'),
        html.Div([
            html.Img(
                src=load_image('resources/images/dj-prototypes-logo.svg'))
            ], className='mdc-layout-grid__cell--span-6', style={ 'textAlign' : 'right' })
    ], className='mdc-layout-grid__inner')
)

title = (
    html.Div([
        html.H1(
            'Company Risk Monitoring', 
            className='mdc-typography--headline1 mdc-theme--primary', 
            style={'margin-top' : '64px'}
        ),
    ])
)
