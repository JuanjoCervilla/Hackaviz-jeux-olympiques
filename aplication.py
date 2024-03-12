##############################################################################
########################## INTRODUCTION ######################################
##############################################################################

## PACKAGES
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
from datetime import datetime as dt

df_jo = pd.read_csv('./data/paris_2024_traite.csv')
df_restau = pd.read_csv('./data/restaurants_proximité.csv')

## APLICATION AND SERVER
from app import app


import plotly.graph_objects as go


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

generate_control_card = html.Div(
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
                optionHeight = 25,
                clearable=False
            ),
            html.Br(),
            html.P("Sélectionnez l'épreuve"),
            dcc.Dropdown(
                id='Dropdown_Epreuve',
                options= df_jo.Épreuve.unique(),
                clearable=False,
                optionHeight = 25,
                placeholder= 'Sélectionnez une épreuve',
                multi=False,
            ),
            html.Br(),
            html.P("Sélectionnez les horaires de recherche"),
            dcc.DatePickerRange(
                id="date-picker-select",
                display_format = "DD / MM / YY" ,
            ),
            html.Br(),
            html.Br(),
            html.P("Quelles sont les sessions disponibles selon ces critères ?"),
            dash_table.DataTable(id = 'listing_session_info',
                                    style_cell={'textAlign': 'center'},
                                    style_as_list_view=True, 
                                    style_header={ 'backgroundColor': 'rgb(210, 210, 210)', 'color': 'black','fontWeight': 'bold'},
                                    style_cell_conditional=[{'if': {'column_id': 'Session'},'fontWeight': 'bold'}],
                                    style_data_conditional=[ {'if': {'row_index': 'odd'},'backgroundColor': 'rgb(240, 240, 240)',}],
                                    page_size=4
                                    ),
            html.Br(),
            html.P("Finalment, sélectionnez le code de la session"),
            dcc.Dropdown(
                    id='Dropdown_Session',
                    # options= df_jo.Session.unique(),
                    clearable=False,
                    optionHeight = 25,
                    maxHeight = 150,
                    placeholder= 'Sélectionnez une session',
                    multi=False,
                    ),        
        ],
    ) 

analysis_card = html.Div(
        id="analysis-card",
        children=[
            html.H1( id='header_session' ),
            dcc.Graph(id='indicator_capacity',figure = {}),
            html.P( id = 'title_session'),
            dash_table.DataTable(id = 'listing_phase_info',
                                    style_cell={'textAlign': 'center'},
                                    style_as_list_view=True, 
                                    style_header={ 'backgroundColor': 'rgb(210, 210, 210)', 'color': 'black','fontWeight': 'bold'},
                                    style_cell_conditional=[{'if': {'column_id': 'Session'},'fontWeight': 'bold'}],
                                    style_data_conditional=[ {'if': {'row_index': 'odd'},'backgroundColor': 'rgb(240, 240, 240)',}],
                                    page_size=4
                                    ),
            dcc.Graph(id='bar_chart_prices',figure = {}),
            dcc.Dropdown(
                id='Dropdown_TypeRestau',
                clearable=False,
                optionHeight = 25,
                maxHeight = 150,
                placeholder= 'Sélectionnez une session',
                multi=True,
                ),  
                       
        ],
    ) 



app.layout  = html.Div(
    id='app-layout',
    children=[
        
    header,
    
    html.Div(
        id = 'content-body',
        children=[
            generate_control_card,
            analysis_card
        ]
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
def options_dropdown(jeux, genre, discipline, epreuve):

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
def options_dropdown(jeux, genre, discipline, epreuve):

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
def options_dropdown(jeux, genre, discipline, epreuve):

    df = df_jo.copy()
    df = df[df['Jeux'] == jeux]
    df = df[df['Genre'] == genre]
    df = df[df['Discipline'] == discipline]
    df = df[df['Épreuve'] == epreuve]

    return dt.strptime(df['Date_Début'].min(), '%m-%d-%Y')

# Callback listing session
@app.callback(
    Output("listing_session_info", "data"),
    Output("listing_session_info", "columns"),
    Input("RadioItems_Jeux", "value"),
    Input("RadioItems_Genre", "value"),
    Input("Dropdown_Discipline", "value"),
    Input("Dropdown_Epreuve", "value"),
    Input("date-picker-select", "start_date"),
    Input("date-picker-select", "end_date"),
)
def update_datatable(jeux, genre, discipline, epreuve, start_date, end_date):

    df = df_jo.copy()
    df = df[df['Jeux'] == jeux]
    df = df[df['Genre'] == genre]
    df = df[df['Discipline'] == discipline]
    df = df[df['Épreuve'] == epreuve]
    
    start_date = start_date.split('T')[0]
    start_date = dt.strptime(start_date, '%Y-%m-%d')
    start_date = start_date.strftime('%m-%d-%Y')
    
    end_date = end_date.split('T')[0]
    end_date = dt.strptime(end_date, '%Y-%m-%d')
    end_date = end_date.strftime('%m-%d-%Y')

    df = df[(df_jo['Date_Début'] >= start_date) & (df['Date_Début'] <= end_date)]

    
    df = df[['Session', 'Discipline','Lieu']]
    columns=[{'id': c, 'name': c} for c in df.columns]


    return df.to_dict('records'), columns

#Callback for dropdown section 
@app.callback(
    Output("Dropdown_Session", "options"),
    Input("RadioItems_Jeux", "value"),
    Input("RadioItems_Genre", "value"),
    Input("Dropdown_Discipline", "value"),
    Input("Dropdown_Epreuve", "value"),
    Input("date-picker-select", "start_date"),
    Input("date-picker-select", "end_date"),
)
def update_datatable(jeux, genre, discipline, epreuve, start_date, end_date):

    df = df_jo.copy()
    df = df[df['Jeux'] == jeux]
    df = df[df['Genre'] == genre]
    df = df[df['Discipline'] == discipline]
    df = df[df['Épreuve'] == epreuve]
    
    start_date = start_date.split('T')[0]
    start_date = dt.strptime(start_date, '%Y-%m-%d')
    start_date = start_date.strftime('%m-%d-%Y')
    end_date = end_date.split('T')[0]
    end_date = dt.strptime(end_date, '%Y-%m-%d')
    end_date = end_date.strftime('%m-%d-%Y')

    df = df[(df_jo['Date_Début'] >= start_date) & (df['Date_Début'] <= end_date)]

    sessions = list(df.Session.unique())
    sessions.sort() 

    return [{'label': x, 'value': x} for x in sessions]

#Callback for dropdown session 
@app.callback(
    Output("Dropdown_Session", "value"),
    Input("RadioItems_Jeux", "value"),
    Input("RadioItems_Genre", "value"),
    Input("Dropdown_Discipline", "value"),
    Input("Dropdown_Epreuve", "value"),
    Input("date-picker-select", "start_date"),
    Input("date-picker-select", "end_date"),
)
def update_datatable(jeux, genre, discipline, epreuve, start_date, end_date):

    df = df_jo.copy()
    df = df[df['Jeux'] == jeux]
    df = df[df['Genre'] == genre]
    df = df[df['Discipline'] == discipline]
    df = df[df['Épreuve'] == epreuve]
    
    start_date = start_date.split('T')[0]
    start_date = dt.strptime(start_date, '%Y-%m-%d')
    start_date = start_date.strftime('%m-%d-%Y')
    end_date = end_date.split('T')[0]
    end_date = dt.strptime(end_date, '%Y-%m-%d')
    end_date = end_date.strftime('%m-%d-%Y')

    df = df[(df_jo['Date_Début'] >= start_date) & (df['Date_Début'] <= end_date)]

    sessions = list(df.Session.unique())
    sessions.sort() 

    return sessions[0]

#callback header session
@app.callback(
    Output("header_session", "children"),
    Input("Dropdown_Session", "value")
)
def update_first_piechart_graph(session):
    
    return f"Analyse de session {session} "

#Callback capacity KPI
@app.callback(
    Output("indicator_capacity", "figure"),
    Input("Dropdown_Session", "value")
)
def update_first_piechart_graph(session):
    
    df = df_jo.copy()
    df = df[df['Session'] == session]
    df.reset_index(inplace=True, drop=True)
    
    fig = go.Figure()

    fig.add_trace(go.Indicator(
    title = "Capacité",
    mode = "number",
    value = df.capacité[0],
    number = {'prefix': "🏟️ ", 'valueformat': '.g'},
    domain = {'row': 0, 'column': 0}))

    fig.update_layout(
        grid = {'rows': 1, 'columns': 1, 'pattern': "independent"})
                                                                                           
    return fig

#callback title session for phase
@app.callback(
    Output("title_session", "children"),
    Input("Dropdown_Session", "value")
)
def update_first_piechart_graph(session):
    
    return f"Quels sont les phases compris dans ce session {session} ?"


# Callback listing phase
@app.callback(
    Output("listing_phase_info", "data"),
    Output("listing_phase_info", "columns"),
    Input("Dropdown_Session", "value")
)
def update_datatable(session):

    df = df_jo.copy()
    df = df[df['Session'] == session]
    
    df = df[['Session', 'Phase', 'Heure_Début', 'Heure_Fin']]
    columns = [{'id': c, 'name': c} for c in df.columns]

    return df.to_dict('records'), columns

#callback barchart
@app.callback(
    Output("bar_chart_prices", "figure"),
    Input("Dropdown_Session", "value")
)
def update_first_piechart_graph(session):
    
    df = df_jo.copy()
    df = df[df['Session'] == session]
    df = df[['Catégorie_First', 'Catégorie_A', 'Catégorie_B', 'Catégorie_C', 'Catégorie_D', 'Catégorie_E+', 'Catégorie_E', 'Catégorie_First_PFR', 'Catégorie_A_PFR', 'Catégorie_B_PFR']]
    sf = df.iloc[0, :]
    df = sf.to_frame()
    df.reset_index(inplace=True)
    df.columns = ['Category', 'Value']
    df = df.dropna()

    fig = px.bar(df, x='Category', y='Value')
                                                                                                      
    return fig


#Callback for TypeRestau
@app.callback(
    Output("Dropdown_TypeRestau", "options"),
    Input("Dropdown_Session", "value"),
)
def options_dropdown_category(session):

    df = df_jo.copy()
    df = df[df['Session'] == session]
    df.reset_index(inplace=True, drop=True)
    lieu = df.Lieu[0]
    
    df_restaurant = df_restau.copy()
    df_restaurant = df_restaurant[df_restaurant['Lieu'] == lieu]

    typeRestau = list(df_restaurant.Type.unique())
    typeRestau.sort() 

    return [{'label': x, 'value': x} for x in typeRestau]


@app.callback(
    Output("Dropdown_TypeRestau", "value"),
    Input("Dropdown_Session", "value"),
)
def values_dropdown_category(session):

    df = df_jo.copy()
    df = df[df['Session'] == session]
    df.reset_index(inplace=True, drop=True)
    lieu = df.Lieu[0]
    
    df_restaurant = df_restau.copy()
    df_restaurant = df_restaurant[df_restaurant['Lieu'] == lieu]

    typeRestau = list(df_restaurant.Type.unique())
    typeRestau.sort() 

    return typeRestau[0]




if __name__=='__main__':
    app.run_server(debug=True, port=3000)