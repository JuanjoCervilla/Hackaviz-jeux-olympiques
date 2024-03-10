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

############################### FIRST CARD ###################################

first_card = dbc.Card(
    [
        dbc.CardBody(
            [
                ################## FIRST ROW ##################
                dbc.Row(
                    [
                        #Having more space on the left side
                        dbc.Col(
                            [],
                            width=1,
                        ),
                        
                        #RadioItems for type of Jeux
                        dbc.Col(
                            [
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
                            ],
                            width=3,
                        ),                        
                        
                        #Dropdown for Discipline
                        dbc.Col(
                            [
                                #html.Label('Discipline', style = {'font-weight': 'bold', 'font-size': 16}),
                                dcc.Dropdown(
                                    id = 'Dropdown_Discipline' ,
                                    options= df_jo.Discipline.unique(),
                                    #value = ['Jan'],
                                    placeholder= 'Sélectionnez une discipline',
                                    multi= False,
                                    clearable=False
                                ),
                            ],
                            width=3,
                            className="text-center",
                        ),
                        
                        dbc.Col(
                            [
                            html.Br(),
                            html.P("Select Check-In Time"),
                            dcc.DatePickerRange(
                                id="date-picker-select",
                                start_date=dt(2024, 8, 1),
                                end_date=dt(2024, 8, 5),
                                min_date_allowed=dt(2024, 8, 1),
                                max_date_allowed=dt(2024, 8, 31),
                                initial_visible_month=dt(2024, 8, 1),
                            ),
                            ]
                        )
                        
                    ]
                ),
                                
                 ################## SECOND ROW ##################
                dbc.Row(
            [
                # Having more space between dropdowns
                dbc.Col(
                    [],
                    width=1,
                ),
                
                #RadioItems for Genre
                dbc.Col(
                [
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
                ],
                    width=3,
                ),
                
                # Dropdown for épreuve                
                dbc.Col(
                            [
                                #html.Label('Épreuve', style = {'font-weight': 'bold', 'font-size': 16}),
                                dcc.Dropdown(
                                    id='Dropdown_Epreuve',
                                    options= df_jo.Épreuve.unique(),
                                    clearable=False,
                                    placeholder= 'Sélectionnez une épreuve',
                                    multi=False,
                                ),
                            ],
                            width=3,
                            className="text-center",
                        ),              
            ],
        ),     
            ]
        )
    ]
)

header = dbc.Card([
    html.Div(
    id="banner",
    className="banner",
    children=[html.Img(src=app.get_asset_url("paris_2024.png")),
              html.H1("Jeux Olympiques Paris 2024", className="text-center"),
              html.Img(src=app.get_asset_url("logo_jo.png")),],
        ),
])

app.layout = html.Div([
    header,
    first_card
])


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


#Callback for Disciplines

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



if __name__=='__main__':
    app.run_server(debug=True, port=3000)