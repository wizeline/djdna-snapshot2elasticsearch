import dash_html_components as html

footer = (
    html.Div([
        html.Div([
            html.P('This app and the information contained herein is not intended to be a source of investment advice or credit analysis with respect to the material presented; it is intended to be used and must be used for informational purposes only. None of the authors, contributors, administrators or anyone else connected with Dow Jones, in any way whatsoever, can be responsible for your use of the information contained in or linked from this app.', className='mdc-typography')
        ], className='mdc-layout-grid__cell--span-10'),
        html.Div([
            html.A([
                html.Span('VISIT DEV PORTAL', className='mdc-button__label')
            ],
                className='mdc-button mdc-button--raised',
                href='https://developer.dowjones.com/site/global/home/index.gsp'
            )
        ], className='mdc-layout-grid__cell--span-2 mdc-layout-grid__cell--align-middle')
    ], className='mdc-layout-grid__inner')
)
