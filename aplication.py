##############################################################################
########################## INTRODUCTION ######################################
##############################################################################

## PACKAGES
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
from datetime import datetime as dt

df_jo = pd.read_csv('./data/paris_2024_traite.csv')
df_restau = pd.read_csv('./data/restaurants_proximité.csv')

## APLICATION AND SERVER
from app import app

##############################################################################
################################ LAYOUT ######################################
##############################################################################

############################### CONTROL SIDE ###################################

header = dbc.Card([
    html.Div(
    id="banner",
    className="banner",
    children=[html.Img(src=app.get_asset_url("paris_2024.png")),
              html.H1("Jeux Olympiques Paris 2024", className="text-center"),
              html.Img(src=app.get_asset_url("logo_jo.png")),],
        ),
])

def generate_control_card():
    """
    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card",
        children=[
            html.P("Sélectionnez le type de jeux"),
            dcc.RadioItems(
                id='RadioItems_Jeux',
                value = list(df_jo.Jeux.unique())[0],
                options=[{'label': str(x), 'value': x} for x in df_jo.Jeux.unique()],
                # inline=True,
                labelStyle={'display': 'inline-block',
                            'background' : '#66B2FF',
                            'padding': '0.4rem 1.1rem',
                            'border-radius':'0.3rem',
                            'margin' : '0.7rem',
                            },
            ),
            html.Br(),
            html.P("Sélectionnez le Genre de la discipline"),
            dcc.RadioItems(
                        id='RadioItems_Genre',
                        value='Hommes',
                        options= [{'label': 'Hommes', 'value': 'Hommes'}, {'label': 'Femmes', 'value': 'Femmes'},{'label': 'Mixte', 'value': 'Mixte'}],#[{'label': x, 'value': x} for x in df_jo.Genre.unique()],
                        labelStyle={'display': 'inline-block',
                                    'background' : '#CCE5FF',
                                    'padding': '0.3rem 0.5rem',
                                    'border-radius':'0.3rem',
                                    'margin' : '0.5rem',
                                    },
                        style={'font-size': 15}
                        ),
            html.Br(),
            html.P("Sélectionnez la discipline"),
            dcc.Dropdown(
                id = 'Dropdown_Discipline' ,
                options= df_jo.Discipline.unique(),
                placeholder= 'Sélectionnez une discipline',
                multi= False,
                clearable=False
            ),
            html.Br(),
            html.P("Sélectionnez l'épreuve"),
            dcc.Dropdown(
                id='Dropdown_Epreuve',
                options= df_jo.Épreuve.unique(),
                clearable=False,
                placeholder= 'Sélectionnez une épreuve',
                multi=False,
            ),
            html.Br(),
            html.P("Select Check-In Time"),
            dcc.DatePickerRange(
                id="date-picker-select",
                display_format = "DD / MM / YY" ,
            ),
        ],
    )

app.layout = html.Div(
    id="app-container",
    children=[
        header,
        html.Div(
            id="left-column",
            className="four columns",
            children=[generate_control_card()]
        )
    ]
)

##############################################################################
############################## CALLBACK ######################################
##############################################################################

#Callback for Disciplines
@app.callback(
    Output("Dropdown_Discipline", "options"),
    Input("RadioItems_Jeux", "value"),
    Input("RadioItems_Genre", "value"),
)
def options_dropdown_category(jeux, genre):

    df = df_jo.copy()
    df = df[df['Jeux'] == jeux]
    df = df[df['Genre'] == genre]

    disciplines = list(df.Discipline.unique())
    disciplines.sort() 

    return [{'label': x, 'value': x} for x in disciplines]


@app.callback(
    Output("Dropdown_Discipline", "value"),
    Input("RadioItems_Jeux", "value"),
    Input("RadioItems_Genre", "value"),
)
def values_dropdown_category(jeux, genre):

    df = df_jo.copy()
    df = df[df['Jeux'] == jeux]
    df = df[df['Genre'] == genre]
    
    disciplines = list(df.Discipline.unique())
    disciplines.sort() 

    return disciplines[0]


#Callback for Epreuves
@app.callback(
    Output("Dropdown_Epreuve", "options"),
    Input("RadioItems_Jeux", "value"),
    Input("RadioItems_Genre", "value"),
    Input("Dropdown_Discipline", "value"),
)
def options_dropdown_category(jeux, genre, discipline):

    df = df_jo.copy()
    df = df[df['Jeux'] == jeux]
    df = df[df['Genre'] == genre]
    df = df[df['Discipline'] == discipline]

    epreuves = list(df.Épreuve.unique())
    epreuves.sort() 

    return [{'label': x, 'value': x} for x in epreuves]


@app.callback(
    Output("Dropdown_Epreuve", "value"),
    Input("RadioItems_Jeux", "value"),
    Input("RadioItems_Genre", "value"),
    Input("Dropdown_Discipline", "value"),
)
def values_dropdown_category(jeux, genre, discipline):

    df = df_jo.copy()
    df = df[df['Jeux'] == jeux]
    df = df[df['Genre'] == genre]
    df = df[df['Discipline'] == discipline]
    
    epreuves = list(df.Épreuve.unique())
    epreuves.sort() 

    return epreuves[0]


# #Callback for Start Date calendar
@app.callback(
    Output("date-picker-select", "start_date"),
    Input("RadioItems_Jeux", "value"),
    Input("RadioItems_Genre", "value"),
    Input("Dropdown_Discipline", "value"),
    Input("Dropdown_Epreuve", "value"),
)
def options_dropdown_category(jeux, genre, discipline, epreuve):

    df = df_jo.copy()
    df = df[df['Jeux'] == jeux]
    df = df[df['Genre'] == genre]
    df = df[df['Discipline'] == discipline]
    df = df[df['Épreuve'] == epreuve]

    return dt.strptime(df['Date_Début'].min(), '%m-%d-%Y') 

#Callback for Max Start Date calendar
@app.callback(
    Output("date-picker-select", "min_date_allowed"),
    Input("RadioItems_Jeux", "value"),
    Input("RadioItems_Genre", "value"),
    Input("Dropdown_Discipline", "value"),
    Input("Dropdown_Epreuve", "value"),
)
def options_dropdown_category(jeux, genre, discipline, epreuve):

    df = df_jo.copy()
    df = df[df['Jeux'] == jeux]
    df = df[df['Genre'] == genre]
    df = df[df['Discipline'] == discipline]
    df = df[df['Épreuve'] == epreuve]
    
    return dt.strptime(df['Date_Début'].min(), '%m-%d-%Y') 


#Callback for End Date calendar
@app.callback(
    Output("date-picker-select", "end_date"),
    Input("RadioItems_Jeux", "value"),
    Input("RadioItems_Genre", "value"),
    Input("Dropdown_Discipline", "value"),
    Input("Dropdown_Epreuve", "value"),
)
def options_dropdown_category(jeux, genre, discipline, epreuve):

    df = df_jo.copy()
    df = df[df['Jeux'] == jeux]
    df = df[df['Genre'] == genre]
    df = df[df['Discipline'] == discipline]
    df = df[df['Épreuve'] == epreuve]

    return dt.strptime(df['Date_Début'].max(), '%m-%d-%Y')

# #Callback for Max End Date calendar
@app.callback(
    Output("date-picker-select", "max_date_allowed"),
    Input("RadioItems_Jeux", "value"),
    Input("RadioItems_Genre", "value"),
    Input("Dropdown_Discipline", "value"),
    Input("Dropdown_Epreuve", "value"),
)
def options_dropdown_category(jeux, genre, discipline, epreuve):

    df = df_jo.copy()
    df = df[df['Jeux'] == jeux]
    df = df[df['Genre'] == genre]
    df = df[df['Discipline'] == discipline]
    df = df[df['Épreuve'] == epreuve]

    return dt.strptime(df['Date_Début'].max(), '%m-%d-%Y')

# #Callback for Initial_Visible_Month
@app.callback(
    Output("date-picker-select", "initial_visible_month"),
    Input("RadioItems_Jeux", "value"),
    Input("RadioItems_Genre", "value"),
    Input("Dropdown_Discipline", "value"),
    Input("Dropdown_Epreuve", "value"),
)
def options_dropdown_category(jeux, genre, discipline, epreuve):

    df = df_jo.copy()
    df = df[df['Jeux'] == jeux]
    df = df[df['Genre'] == genre]
    df = df[df['Discipline'] == discipline]
    df = df[df['Épreuve'] == epreuve]

    return dt.strptime(df['Date_Début'].min(), '%m-%d-%Y')


if __name__=='__main__':
    app.run_server(debug=True, port=3000)