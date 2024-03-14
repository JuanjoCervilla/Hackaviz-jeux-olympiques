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
              html.H1("Jeux Olympiques Paris 2024"),
              html.Img(src=app.get_asset_url("logo_jo.png"))],
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
            html.Div(id='title-analysis-card',
                     children=[html.H2( id='header_session')]),
            html.Br(),
            
            html.Div(id='title-indicator-card', 
                     children = [
                            html.H5('Lieu'),
                            html.H5('Capacité'),
                            html.H5('Date'),
                             ]
                     ),
            html.Div(id='indicator-card', 
                     children = [
                            html.H2( id = 'lieu_KPI'),
                            html.H2( id = 'capacité_KPI'),
                            html.H2( id = 'date_KPI'),
                             ]
                     ),
            
            html.Br(),
            html.Br(),
            html.Br(),
            
            html.Div(id='phases-prices-card', children=[
                    html.H4( id = 'title_session'),
                    html.H4(id='title_price'),
                    dash_table.DataTable(id = 'listing_phase_info',
                                            style_cell={'textAlign': 'center'},
                                            style_as_list_view=True, 
                                            style_header={ 'backgroundColor': 'rgb(210, 210, 210)', 'color': 'black','fontWeight': 'bold'},
                                            style_cell_conditional=[{'if': {'column_id': 'Session'},'fontWeight': 'bold'}],
                                            style_data_conditional=[ {'if': {'row_index': 'odd'},'backgroundColor': 'rgb(240, 240, 240)',}],
                                            #page_size=4,
                                            #fixed_rows={'headers': True},
                                            style_table={'overflowX': 'auto'}  
                                            ),
                    dcc.Graph(id='bar_chart_prices',figure = {}),   
                ]),                              

            html.Br(),
            
            html.Div(id = 'restau-card', children = [
                html.Div(id='info-restau-card', children=[
                    
                    html.Div(id='filter-restau-card', children=[
                        html.H3('Filtre pour le type de restaurant'),
                        html.H3(id='distance-restau'),
                        dcc.Dropdown(
                            id='Dropdown_TypeRestau',
                            clearable=False,
                            optionHeight = 25,
                            maxHeight = 150,
                            placeholder= 'Sélectionnez une session',
                            multi=True,
                            ),
                                    
                        dcc.RangeSlider(id = 'RangeSlider_Distance', min=0, max=1500, value=[0, 300],
                                        tooltip={"placement": "bottom", "always_visible": True}),
                        
                    ]),
                    
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    
                    html.Div(id='analysis-restau-card', children=[
                        html.H3('Liste des restaurants disponibles'),
                        html.H3('Type de restaurant selon les critères'),
                        dash_table.DataTable(id = 'listing_restau',
                            style_cell={'textAlign': 'center'},
                            style_as_list_view=True, 
                            style_header={ 'backgroundColor': 'rgb(210, 210, 210)', 'color': 'black','fontWeight': 'bold'},
                            style_cell_conditional=[{'if': {'column_id': 'Etablissement'},'fontWeight': 'bold'}],
                            style_data_conditional=[ {'if': {'row_index': 'odd'},'backgroundColor': 'rgb(240, 240, 240)',}],
                            page_size=4
                            ),
                        dcc.Graph(id='donut_chart_typeRestau',figure = {})                        
                    ]),
                    
                ]),
                html.Div(id='map-restau-card', children=[
                    html.H1('map here')  
                    ]),
            ]),
        ],
    ) 



app.layout  = html.Div(
    id='app-container',
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

#Callback for Dropdown Options Disciplines
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

#Callback for Dropdown Value Disciplines
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


#Callback for Dropdown Options Epreuves
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

#Callback for Dropdown Value Epreuves
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

#Callback for dropdown options session  
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

#Callback for dropdown value session 
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
    
    return f"Analyse de Session {session} "

#callback lieu_KPI
@app.callback(
    Output("lieu_KPI", "children"),
    Input("Dropdown_Session", "value")
)
def update_first_piechart_graph(session):
    
    df = df_jo.copy()
    df = df[df['Session'] == session]
    df.reset_index(inplace=True, drop=True)
    lieu = df.Lieu[0]
    
    return f"📍 {lieu} "

#callback date_KPI
@app.callback(
    Output("date_KPI", "children"),
    Input("Dropdown_Session", "value")
)
def update_first_piechart_graph(session):
    
    df = df_jo.copy()
    df = df[df['Session'] == session]
    df.reset_index(inplace=True, drop=True)
    date = df.Date_Début[0]
    
    return f"🗓️ {date} "

# #Callback capacity KPI
@app.callback(
    Output("capacité_KPI", "children"),
    Input("Dropdown_Session", "value")
)
def update_first_piechart_graph(session):
    
    df = df_jo.copy()
    df = df[df['Session'] == session]
    df.reset_index(inplace=True, drop=True)
    capacity = int(df.capacité[0])
    
    return f"🏟️ {capacity} "

#callback title session for phase
@app.callback(
    Output("title_session", "children"),
    Input("Dropdown_Session", "value")
)
def update_first_piechart_graph(session):
    
    return f"Phases compris dans la session {session}"

#callback title session for phase
@app.callback(
    Output("title_price", "children"),
    Input("Dropdown_Session", "value")
)
def update_first_piechart_graph(session):
    
    return f"Prix par category pour la session {session} "


# Callback listing phase
@app.callback(
    Output("listing_phase_info", "data"),
    Output("listing_phase_info", "columns"),
    Input("Dropdown_Session", "value")
)
def update_datatable(session):

    df = df_jo.copy()
    df = df[df['Session'] == session]
    
    df = df[['Phase', 'Heure_Début', 'Heure_Fin']]
    columns = [{'id': c, 'name': c} for c in df.columns]

    return df.to_dict('records'), columns

#callback barchart prices
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
    df.columns = ['Category', 'Price']
    df = df.dropna()

    fig = px.bar(df, x='Category', y='Price', width=800, height=400)
                                                                                                      
    return fig

# #Callback capacity KPI
@app.callback(
    Output("distance-restau", "children"),
    Input("Dropdown_Session", "value")
)
def update_first_piechart_graph(session):
    
    df = df_jo.copy()
    df = df[df['Session'] == session]
    df.reset_index(inplace=True, drop=True) 
    lieu = df.Lieu[0]
    
    return f"Filtre pour la distance par rappport à {lieu} "


#Callback for Dropdown Options TypeRestau
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

#Callback for Dropdown Value TypeRestau
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

    return typeRestau

#Callback for listing_restau
@app.callback(
    Output("listing_restau", "data"),
    Output("listing_restau", "columns"),
    Input("Dropdown_Session", "value"),
    Input("Dropdown_TypeRestau", "value"),
    Input("RangeSlider_Distance", "value"),
)
def update_datatable(session, typeRestau, distance):

    df = df_jo.copy()
    df = df[df['Session'] == session]
    df.reset_index(inplace=True, drop=True)
    lieu = df.Lieu[0]
    
    df_restaurant = df_restau.copy()
    df_restaurant = df_restaurant[df_restaurant['Lieu'] == lieu]
    df_restaurant = df_restaurant[df_restaurant['Type'].isin(typeRestau)]
    df_restaurant = df_restaurant[(df_restaurant['distance'] >= distance[0]) & (df_restaurant['distance'] <= distance[1])]
    
    df_restaurant = df_restaurant[['Etablissement', 'adresse', 'premiere_activité']]
    columns = [{'id': c, 'name': c} for c in df_restaurant.columns]

    return df_restaurant.to_dict('records'), columns

#callback donut chart typeRestau
@app.callback(
    Output("donut_chart_typeRestau", "figure"),
    Input("Dropdown_Session", "value"),
    Input("Dropdown_TypeRestau", "value"),
    Input("RangeSlider_Distance", "value")
)
def update_first_piechart_graph(session, typeRestau, distance):
    
    df = df_jo.copy()
    df = df[df['Session'] == session]
    df.reset_index(inplace=True, drop=True)
    lieu = df.Lieu[0]                                                                               
    
    df_restaurant = df_restau.copy()
    df_restaurant = df_restaurant[df_restaurant['Lieu'] == lieu]
    df_restaurant = df_restaurant[df_restaurant['Type'].isin(typeRestau)]
    df_restaurant = df_restaurant[(df_restaurant['distance'] >= distance[0]) & (df_restaurant['distance'] <= distance[1])]
    
    type_counts = df_restaurant['Type'].value_counts()
    
    type_counts_df = pd.DataFrame({'Type': type_counts.index, 'Count': type_counts.values})

    fig = px.pie(type_counts_df, values='Count', names='Type', hole=0.7)
    fig.update_layout(showlegend=False)
    return fig



if __name__=='__main__':
    app.run_server(debug=True, port=3000)