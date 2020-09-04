import dash_html_components as html

footer = (
    html.Div([
        html.Div([
            html.P('At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum schmidt.', className='mdc-typography')
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
