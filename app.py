import dash
import dash_bootstrap_components as dbc


# app = dash.Dash(external_stylesheets=[dbc.themes.CYBORG])
external_stylesheets = [dbc.themes.ZEPHYR, dbc.icons.BOOTSTRAP]
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.LUX])
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=external_stylesheets, title='Jeux Olympiques Dashboard')


