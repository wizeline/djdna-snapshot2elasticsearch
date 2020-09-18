import dash
import dash_bootstrap_components as dbc

external_stylesheets = [
    'https://unpkg.com/material-components-web@latest/dist/material-components-web.min.css',
    'https://fonts.googleapis.com/css?family=Roboto:300,400,500',
    'https://fonts.googleapis.com/icon?family=Material+Icons',
    dbc.themes.BOOTSTRAP,
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Dow Jones [Prototype]'
