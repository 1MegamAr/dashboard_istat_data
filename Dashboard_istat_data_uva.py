import dash
from dash import dcc, html, Input, Output, State, Dash
import dash_bootstrap_components as dbc
import pandas as pd
from pandas_geojson import read_geojson
import plotly.express as px









################################   line provincie     ###############################################################
df = pd.read_csv('df_provincie_06_22_bar.csv')


dropdown_provincie = html.Div([
    dcc.Dropdown(
        id='city-dropdown',
        options=[{'label': city, 'value': city} for city in df['Territorio'].unique()],
        #placeholder="Seleziona una provincia",
        value='Agrigento',
        style = {'width':'100%'}
    ),
    dcc.Graph(id='production-graph')
])








#####################################   line regioni    ####################################################


df_reg = pd.read_csv('df_reg_barplot.csv')



dropdown_reg = html.Div([
    dcc.Dropdown(
        id='region-dropdown',
        options=[{'label': region, 'value': region} for region in df_reg['Territorio'].unique()],
        value='Abruzzo',
        #placeholder="Seleziona una regione",
    ),
    dcc.Graph(id='production-graph1')
])

####################################### map provincie    ####################################################

df_map = pd.read_csv("df_provincie_06_22_bar_map.csv")

pd.set_option('display.float_format', lambda x: '%.2f' % x)


counties_prov = read_geojson('map_provincie.geojson')   

prov_id_map = {}

for feature in counties_prov['features']:
    feature['id'] = feature['properties']['prov_istat_code_num']
    prov_id_map[feature['properties']['prov_name']] = feature['id']
    

df_map['id'] = df_map['Territorio'].apply(lambda x: prov_id_map[x])



dropdown_map_prov = html.Div([
    dcc.Dropdown(
        id='map_prov-dropdown',
        options=[{'label': map_prov, 'value': map_prov} for map_prov in df_map['Anno'].unique()],
        #value='2022',
        placeholder="Seleziona un anno"
    ),
    dcc.Graph(id='production-graph2')
])



##################################  map regioni  ##############################################################

df_map_reg = pd.read_csv("df_reg_bar_map.csv")

pd.set_option('display.float_format', lambda x: '%.2f' % x)


counties_reg = read_geojson('map_regioni.geojson')   

reg_id_map = {}

for feature in counties_reg['features']:
    feature['id'] = feature['properties']['reg_istat_code_num']
    reg_id_map[feature['properties']['reg_name']] = feature['id']
    

df_map_reg['id'] = df_map_reg['Territorio'].apply(lambda x: reg_id_map[x])



dropdown_map_reg = html.Div([
    dcc.Dropdown(
        id='map_reg-dropdown',
        options=[{'label': map_reg, 'value': map_reg} for map_reg in df_map_reg['Anno'].unique()],
        #value='2022',
        placeholder="Seleziona un anno"
    ),
    dcc.Graph(id='production-graph3')
])


########################### bar provincie ###########################################


fig4 = px.bar(df_map,
             x = 'Territorio',
             y = 'Quintali',
             color = "Anno",
             hover_data= ['Quintali','Var.%','Classifica'],
             #width=1000,
             height=600,
             title='Produzione per provincia (Produzione raccolta) ',
             labels={'value': 'Quintali'}
)

bar_prov = html.Div(
    children =[
        dcc.Graph(id ='production-graph4', figure = fig4 )
    ]
)
 
############################## bar regioni ######################################
fig5 = px.bar(df_map_reg,
             x = 'Territorio',
             y = 'Quintali',
             color = "Anno",
             hover_data= ['Quintali','Var.%','Classifica'],
             #width=1000,
             height=600,
             title='Produzione per regione (Produzione raccolta) ',
             labels={'value': 'Quintali'}
)

bar_reg = html.Div(
    children =[
        dcc.Graph(id ='production-graph5', figure = fig5 )
    ]
)



######################################### app layout ###################################
app = dash.Dash(name = __name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

navbar = dbc.Row(
    dbc.Col(
        dbc.NavbarSimple(
    children=[
        
        dbc.NavItem(dbc.NavLink("Mario Pilo", href="https://www.linkedin.com/feed/?trk=404_page")),
        dbc.NavItem(dbc.NavLink("Istat", href="http://dati.istat.it/Index.aspx?QueryId=33706")),
        dbc.NavItem(dbc.NavLink("Plotly", href="https://plotly.com/")),
        dbc.DropdownMenu(
            nav=True,
            in_navbar=True,
            label="Collegamenti",
            children=[
                dbc.DropdownMenuItem('Python', href="https://www.python.org/"),
                dbc.DropdownMenuItem('Pandas', href="https://pandas.pydata.org/"),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem('Dash', href="https://plotly.com/dash/"),
            ],
        ),
    ],
    brand="Dashboard Istat Data Uva da Vino",
    brand_href="https://www.linkedin.com/feed/?trk=404_page",
    sticky="top",
    color="dark",
    dark=True,
    ),
    sm = 12, lg = 12, md= 12, xs =12, xl =12)
)

h1_regioni = html.Div(
    children = 
    [
        html.H1('Regioni')
    ],
    style = {'align-items': 'center'}
)  





#################### griglia #######################################################

grid = html.Div(
    dbc.Container([
        dbc.Row([
            dbc.Col(dropdown_map_reg,
                sm = 12, md= 12, lg = 6,  xs =12, xl =6),
            dbc.Col(dropdown_reg,
                sm = 12, md= 12, lg = 6,  xs =12, xl =6)
        ]),
        html.Br(),
        html.Br(),
        
        dbc.Row([
            dbc.Col(dropdown_map_prov,
                sm = 12, md= 12, lg = 6,  xs =12, xl =6),
            dbc.Col(dropdown_provincie,
                sm = 12, md= 12, lg = 6,  xs =12, xl =6)
    ]),
        html.Br(), 
        html.Br(),
        
        dbc.Row([
            dbc.Col(bar_reg,
                sm = 12, md= 12, lg = 6,  xs =12, xl =6),
            dbc.Col(bar_prov,
                sm = 12, md= 12, lg = 6,  xs =12, xl =6)]),
        html.Br(),
        html.Br()
    ],
    fluid = True)
)
  






############################# callback prov line #######################################################################
@app.callback(
    dash.dependencies.Output('production-graph', 'figure'),
    [dash.dependencies.Input('city-dropdown', 'value')])
def update_graph(selected_city):
    df_filtered = df[df['Territorio'] == selected_city]
    
    fig = px.line(df_filtered, x='Anno',
                  y='Quintali',
                  hover_data = ['Var.%', 'Classifica'],
                  #width = 500,
                  height = 600,
                  markers = True)
    
    fig.update_layout(title='Trend Provincie (2006 - 2022) {}'.format(selected_city))
    return fig



######################### callback reg line ##############################################################


@app.callback(
    dash.dependencies.Output('production-graph1', 'figure'),
    [dash.dependencies.Input('region-dropdown', 'value')])
def update_graph(selected_region):
    df_reg_filtered = df_reg[df_reg['Territorio'] == selected_region]
    
    fig1 = px.line(df_reg_filtered,
                   
                x='Anno',
                y='Quintali',
                hover_data = ['Var.%', 'Classifica'],
                #width = 500,
                height = 600,
                markers = True)
    
    fig1.update_layout(title='Trend Regioni (2013 - 2022) {}'.format(selected_region))
    return fig1



######################## callback map prov ##################################

@app.callback(
    dash.dependencies.Output('production-graph2', 'figure'),
    [dash.dependencies.Input('map_prov-dropdown', 'value')])
def update_graph(selected_year):
    df_map_filtered = df_map[df_map['Anno'] == selected_year]
    
    fig2 = px.choropleth_mapbox(df_map_filtered,
                    geojson= counties_prov,
                    locations = 'id',
                    color= 'Quintali',
                    color_continuous_scale= "dense",
                    range_color=(df_map["Quintali"].min(), df_map["Quintali"].max()),
                    hover_name = 'Territorio',
                    hover_data = ['Anno','Quintali', 'Var.%', 'Classifica'],
                    mapbox_style= 'white-bg',
                    title= 'Mappa produzione per provincie 2022',
                    #width=1000,
                    height=600,
                    center = {'lat':42, 'lon': 13},
                    zoom =2.8)

    fig2.update_layout(margin={"r":30,"t":35,"l":35,"b":30})
    
    fig2.update_layout(title='Mappa delle provincie {}'.format(selected_year))
    return fig2





#####################################  callback map regioni  ######################################################################

@app.callback(
    dash.dependencies.Output('production-graph3', 'figure'),
    [dash.dependencies.Input('map_reg-dropdown', 'value')])
def update_graph(selected_year):
    df_map_filtered = df_map_reg[df_map_reg['Anno'] == selected_year]
    
    fig3 = px.choropleth_mapbox(df_map_filtered,
                    geojson= counties_reg,
                    locations = 'id',
                    color= 'Quintali',
                    color_continuous_scale= "reds",
                    range_color=(df_map_reg["Quintali"].min(), df_map_reg["Quintali"].max()),
                    hover_name = 'Territorio',
                    hover_data = ['Anno','Quintali', 'Var.%', 'Classifica'],
                    mapbox_style= 'white-bg',
                    title= 'Mappa produzione per regioni 2022',
                    #width=1000,
                    height=600,
                    center = {'lat':42, 'lon': 13},
                    zoom =2.8)

    fig3.update_layout(margin={"r":30,"t":35,"l":35,"b":30})
    
    fig3.update_layout(title='Mappa delle regioni {}'.format(selected_year))
    return fig3

######################################################################################################################






#########################################################################################################
app.layout = html.Div(children =
                      [
    navbar,
    html.Br(),
    html.Br(),                      
    grid,
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br()
    ]
    
)


if __name__ == '__main__':
    app.run_server(debug = False)
