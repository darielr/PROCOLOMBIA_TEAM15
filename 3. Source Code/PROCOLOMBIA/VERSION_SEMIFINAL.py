import dash
import dash_labs as dl
import os
import plotly.express as px
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from dash.dependencies import Input, Output, State
import base64
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud , STOPWORDS, ImageColorGenerator
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from plotly.offline import plot
import random


from dash_bootstrap_templates import load_figure_template

app = dash.Dash(__name__, plugins=[dl.plugins.FlexibleCallbacks()])

tpl = dl.templates.DbcRow(app, title="PR", left_cols=4, figure_template=True)  #, theme=dbc.themes.SUPERHERO)

template=tpl

server = app.server
app.config["suppress_callback_exceptions"] = True

# This loads the "flatly" themed figure template templates from dash-bootstrap-templates library,
# adds it to plotly.io and makes it the default.

#load_figure_template("Superhero")

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    
}


sidebar = html.Div(
    [
        #html.H2("Sidebar", className="display-4"),
        html.Img(src=app.get_asset_url('LOGOPROCOLOMBIA.png'), style={'height':'20%', 'width':'100%'}),
        html.Hr(),
        html.P(
            "Menu", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Statistic analysis", href="/page-1", active="exact"),
                dbc.NavLink("Models", href="/page-2", active="exact"),
                dbc.NavLink("About us", href="/page-3", active="exact"),
                dbc.NavLink("Canada_Descriptive_Analysis", href="/page-4", active=False, style= {'display': 'none'}),
                dbc.NavLink("Canada_Sentiment", href="/page-5", active=False, style= {'display': 'none'}),
                dbc.NavLink("Canada_Topic_Modeling", href="/page-6", active=False, style= {'display': 'none'}),
                dbc.NavLink("UK_Descriptive_Analysis", href="/page-7", active=False, style= {'display': 'none'}),
                dbc.NavLink("UK_Sentiment", href="/page-8", active=False, style= {'display': 'none'}),
                dbc.NavLink("UK_Topic_Modeling", href="/page-9", active=False, style= {'display': 'none'}),
                dbc.NavLink("USA_Descriptive_Analysis", href="/page-10", active=False, style= {'display': 'none'}),
                dbc.NavLink("USA_Sentiment", href="/page-11", active=False, style= {'display': 'none'}),
                dbc.NavLink("USA_Topic_Modeling", href="/page-11", active=False, style= {'display': 'none'}),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)
######################################################## CARDS
card_angi = dbc.Card(
    [
        dbc.CardImg(src=app.get_asset_url('IMG_1040.JPG'), style={'height':'100%', 'width':'100%'}, top=True),
        dbc.CardBody(
            [
                html.H4("Angi Aparicio", className="card-title"),
                html.P(
                    "Geologists",
                    className="card-text",
                ),
                dbc.Button("Go somewhere", outline=True, color="success", href="https://www.linkedin.com/in/angiaparicio/"),
            ]
        ),
    ],
    style={"width": "10rem"},
)

card_dariel = dbc.Card(
    [
        dbc.CardImg(src=app.get_asset_url(''), style={'height':'50%', 'width':'50%'}, top=True),
        dbc.CardBody(
            [
                html.H4("Dariel", className="card-title"),
                html.P(
                    "Geologists",
                    className="card-text",
                ),
                dbc.Button("Go somewhere", outline=True, color="success"),
            ]
        ),
    ],
    style={"width": "10rem"},
)

card_daniel = dbc.Card(
    [
        dbc.CardImg(src=app.get_asset_url('daniel.jpeg'), style={'height':'100%', 'width':'100%'}, top=True),
        dbc.CardBody(
            [
                html.H4("Daniel Romero", className="card-title"),
                html.P(
                    "Geologists",
                    className="card-text",
                ),
                dbc.Button("Go somewhere", outline=True, color="success"),
            ]
        ),
    ],
    style={"width": "10rem"},
)


card_carlos = dbc.Card(
    [
        dbc.CardImg(src=app.get_asset_url('carlos.jpeg'),  style={'height':'80%', 'width':'100%'}, top=True),
        dbc.CardBody(
            [
                html.H4("Carlos Lopez", className="card-title"),
                html.P(
                    "Geologists",
                    className="card-text",
                ),
                dbc.Button("Go somewhere", outline=True, color="success"),
            ]
        ),
    ],
    style={"width": "10rem"},
)

card_german = dbc.Card(
    [
        dbc.CardImg(src=app.get_asset_url('manuel.jpeg'), style={'height':'160%', 'width':'100%'}, top=True),
        dbc.CardBody(
            [
                html.H4("German", className="card-title"),
                html.P(
                    "Geologists",
                    className="card-text",
                ),
                dbc.Button("Go somewhere", outline=True, color="success"),
            ]
        ),
    ],
    style={"width": "10rem"},
)


card_manuel = dbc.Card(
    [
        dbc.CardImg(src=app.get_asset_url(''), top=True),
        dbc.CardBody(
            [
                html.H4("Manuel", className="card-title"),
                html.P(
                    "Geologists",
                    className="card-text",
                ),
                dbc.Button("Go somewhere", outline=True, color="success", className="mr-1", href='https://www.linkedin.com/in/germ%C3%A1n-puertas-a420b113/'),
            ]
        ),
    ],
    style={"width": "10rem"},
)
cards = dbc.Row(
    [
        dbc.Col(card_angi, width="auto"),
        dbc.Col(card_dariel, width="auto"),
        dbc.Col(card_daniel, width="auto"),
        dbc.Col(card_carlos, width="auto"),
        dbc.Col(card_german, width="auto"),
        dbc.Col(card_manuel, width="auto")
        
    ]
)

######################################################## CARDS DESCRIPTIVE, SENTIMENT, TOPIC MODELING
tab1_content = html.Div([
        dbc.Row([
        dbc.Col(dbc.Card([
        dbc.CardImg(src=app.get_asset_url('descriptive_analysis.jpg'), top=True),
        dbc.CardBody(
            [
                html.H4("Descriptive Analysis", className="card-title"),
                html.P(
                    "xxx",
                    className="card-text",
                ),
                dbc.Button("Go somewhere", color="danger", href="/page-4" ),
            ]
        ),
    ],
     style={'width': '100%', 'marginTop': '20'},
)),

    dbc.Col( dbc.Card(
    [
        dbc.CardImg(src=app.get_asset_url('sentiment_analysis.jpeg'), top=True),
        dbc.CardBody(
            [
                html.H4("Sentiment Analysis", className="card-title"),
                html.P(
                    "xxx",
                    className="card-text",
                ),
                dbc.Button("Go somewhere", color="warning", href="/page-5" ),
            ]
        ),
    ],
    style={'width': '100%', 'marginTop': '20'},
)),

    dbc.Col(dbc.Card(
    [
        dbc.CardImg(src=app.get_asset_url('topic_modeling.png'), top=True),
        dbc.CardBody(
            [
                html.H4("Topic Modeling", className="card-title"),
                html.P(
                    "xxx",
                    className="card-text",
                ),
                dbc.Button("Go somewhere", color="success", href="/page-6" ),
            ]
        ),
    ],
    style={'width': '100%',  'marginTop': '20'},
))
])
])


######################################################  TABS

tab2_content = html.Div([
        dbc.Row([
        dbc.Col(dbc.Card([
        dbc.CardImg(src=app.get_asset_url('descriptive_analysis.jpg'), top=True),
        dbc.CardBody(
            [
                html.H4("Descriptive Analysis", className="card-title"),
                html.P(
                    "xxx",
                    className="card-text",
                ),
                dbc.Button("Click here", color="danger", href="/page-7" ),
            ]
        ),
    ],
     style={'width': '100%', 'marginTop': '20'},
)),

    dbc.Col( dbc.Card(
    [
        dbc.CardImg(src=app.get_asset_url('sentiment_analysis.jpeg'), top=True),
        dbc.CardBody(
            [
                html.H4("Sentiment Analysis", className="card-title"),
                html.P(
                    "xxx",
                    className="card-text",
                ),
                dbc.Button("Click here", color="warning", href="/page-8" ),
            ]
        ),
    ],
    style={'width': '100%', 'marginTop': '20'},
)),

    dbc.Col(dbc.Card(
    [
        dbc.CardImg(src=app.get_asset_url('topic_modeling.png'), top=True),
        dbc.CardBody(
            [
                html.H4("Topic Modeling", className="card-title"),
                html.P(
                    "xxx",
                    className="card-text",
                ),
                dbc.Button("Click here", color="success", href="/page-9" ),
            ]
        ),
    ],
    style={'width': '100%',  'marginTop': '20'},
))
])
])
tab3_content = html.Div([
        dbc.Row([
        dbc.Col(dbc.Card([
        dbc.CardImg(src=app.get_asset_url('descriptive_analysis.jpg'), top=True),
        dbc.CardBody(
            [
                html.H4("Descriptive Analysis", className="card-title"),
                html.P(
                    "xxx",
                    className="card-text",
                ),
                dbc.Button("Click here", color="danger", href="/page-4" ),
            ]
        ),
    ],
     style={'width': '100%', 'marginTop': '20'},
)),

    dbc.Col( dbc.Card(
    [
        dbc.CardImg(src=app.get_asset_url('sentiment_analysis.jpeg'), top=True),
        dbc.CardBody(
            [
                html.H4("Sentiment Analysis", className="card-title"),
                html.P(
                    "xxx",
                    className="card-text",
                ),
                dbc.Button("Click here", color="warning", href="/page-5" ),
            ]
        ),
    ],
    style={'width': '100%', 'marginTop': '20'},
)),

    dbc.Col(dbc.Card(
    [
        dbc.CardImg(src=app.get_asset_url('topic_modeling.png'), top=True),
        dbc.CardBody(
            [
                html.H4("Topic Modeling", className="card-title"),
                html.P(
                    "xxx",
                    className="card-text",
                ),
                dbc.Button("Click here", color="success", href="/page-6" ),
            ]
        ),
    ],
    style={'width': '100%',  'marginTop': '20'},
))
])
])

tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Canada"),
        dbc.Tab(tab2_content, label="United Kingdom"),
        dbc.Tab(tab3_content, label="United States"),
        
           
    
    ]
)


####################################################################### DATA fdimarkets
path_data='data/'
full_path=os.path.join(path_data, 'clean_fdimarkets.csv')
fdimarkets  = pd.read_csv(full_path,sep = ';', encoding='latin-1')

available_indicators=fdimarkets['SUBSECTOR'].unique()
region=fdimarkets['SRC_REGION'].unique()
latin_america=fdimarkets['SRC_REGION'].unique()

# Add 0s to NA in Flags to groupby
fdimarkets['SRC_AMERLAT_CARIBE'] = fdimarkets['SRC_AMERLAT_CARIBE'].fillna(0)
fdimarkets['DSTN_AMERLAT_CARIBE'] = fdimarkets['DSTN_AMERLAT_CARIBE'].fillna(0)

# Calculate groupby to graph the map

#clean_fdimarkets_map = fdimarkets.groupby(['SRC_CTRY',
 #      'DSTN_CTRY','YEAR', 'SRC_CAPITAL', 'SRC_LAT',
  #     'SRC_LON', 'SRC_ID', 'SRC_ISO2', 'SRC_ISO3', 'SRC_REGION',
  #     'SRC_AMERLAT_CARIBE', 'DSTN_CAPITAL', 'DSTN_LAT', 'DSTN_LON', 'DSTN_ID',
  #     'DSTN_ISO2', 'DSTN_ISO3', 'DSTN_REGION', 'DSTN_AMERLAT_CARIBE'],as_index=False).agg({'CAP_INV':'sum','JOBSCREATED':'sum'})

clean_fdimarkets_map = fdimarkets.groupby(['SRC_CTRY',
       'YEAR', 'SRC_CAPITAL', 'SRC_LAT',
       'SRC_LON', 'SRC_ID', 'SRC_ISO2', 'SRC_ISO3', 'SRC_REGION',
       'SRC_AMERLAT_CARIBE'],as_index=False).agg({'CAP_INV':'sum','JOBSCREATED':'sum'})


####################################################################### DATA gazelle
full_path=os.path.join(path_data, 'clean_gazelle.csv')
gazelle  = pd.read_csv(full_path,sep = ';', encoding='latin-1')




colors = ['rgb(0, 0, 100)']
CONTENT_STYLE = {
    "margin-left": "10",
    "margin-right": "10",
    'marginTop': '5',
    'marginBottom': '20',
    'padding': '6px 0px 0px 8px',
    'backgroundColor':'#F7FBFE',
}
content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = dbc.Container([dcc.Location(id="url"),sidebar, content,

    dcc.Store(id="store"),
       # html.H1("PROCOLOMBIA"),
       html.Img(src=app.get_asset_url('image2.jpg'), style={'height':'3%', 'width':'100%'}),
        html.Hr(),
        dbc.Button(
            "Regenerate graphs",
            color="primary",
            block=True,
            id="button",
            className="mb-3"),
    
    
    html.Div(id='tabs-content-classes')
]
)
  
@app.callback(Output('tabs-content-classes', 'children'), 
               [Input('url', 'pathname')]
              )
              
def render_content(pathname):
# if pathname == "/":
#            return simple_jumbotron
            
 if pathname == "/page-1":
            return html.Div([                                   
            dcc.Slider(
             id='year-slider',
             min=fdimarkets['YEAR'].min(),
             max=fdimarkets['YEAR'].max(),
             value=fdimarkets['YEAR'].max(),
             marks={str(year): str(year) for year in fdimarkets['YEAR'].unique()},
             step=None
    ),  
    
            html.Div([
            dcc.Dropdown(
                id='latin_america',
                options=[{'label': i, 'value': i} for i in latin_america],
                value='1'
            )], style={'width': '49%', 'display': 'inline-block'}), 
            
                     
            html.H3('Investiment map'),
                       
            dbc.Row([
            dbc.Col(dcc.Graph(id='map1', hoverData={'points': [{'customdata': ''}]}), lg=10),
                   ]),
            html.Hr(),
                         
            dbc.Row([
            dbc.Col(dcc.Graph(id='scatter'), lg=6),
            dbc.Col(dcc.Graph(id='jobs'), lg=6)
             ]),  
             
            html.Hr(), 
            html.H3('Investiment'),                  
            html.Div([
            dcc.Dropdown(
                id='region',
                options=[{'label': i, 'value': i} for i in region],
                value='Asia'
            )], style={'width': '49%', 'display': 'inline-block'}),   
            
            dbc.Row([
            dbc.Col(dcc.Graph(id='cap_inv2', hoverData={'points': [{'customdata': 'Malasia'}]}), lg=12),
                   ]),                  
                                                     
        ])
     
 if pathname == "/page-2":
    return  tabs,
        
 if pathname == "/page-3":
   return  cards,       
        
 if pathname == "/page-4":
   return   html.Div([
            html.H3('Descriptive Analysis'),
            html.P("XXXX.", className="lead"),
            html.Img(src=app.get_asset_url('Canada_wordcloud1.png'), style={'height':'100%', 'width':'100%'}),
            html.Hr(),
            html.Iframe(src=app.get_asset_url('Canada_barchartOnegram.html'), style={"height": "600px", "width": "49%"}),
            html.Iframe(src=app.get_asset_url('Canada_barchartBigram.html'), style={"height": "600px", "width": "49%"}),
            html.Hr(),
            html.Iframe(src=app.get_asset_url('Canada_barchartTrigram.html'), style={"height": "600px", "width": "49%"}),
            dbc.Button("Learn more", color="danger", href=""),
            dbc.Button("Come back ", color="danger", href="/page-2"),
            ])

 if pathname == "/page-5":
   return   html.Div([
            html.H3('Sentiment Analysis'),
            html.P("XXXX.", className="lead"),
            html.Iframe(src=app.get_asset_url('Canada_figsentiment.html'), style={"height": "600px", "width": "49%"}),
            html.Iframe(src=app.get_asset_url('Canada_sentimentbar.html'), style={"height": "600px", "width": "49%"}),
            ])
            
            
 if pathname == "/page-6":
   return   html.Div([
            html.H3('Topic Modeling'),
            html.P("XXXX.", className="lead"),
            html.Iframe(src=app.get_asset_url('Canada_lda.html'), style={"height": "950px", "width": "115%"})
            ])
            
            
@app.callback(dash.dependencies.Output('map1', 'figure'),
    [dash.dependencies.Input('year-slider', 'value'),])
def update_figure(selected_year):
    filtered_df = fdimarkets[fdimarkets['YEAR'] == selected_year]
    map1 = px.choropleth(filtered_df, locations='SRC_ISO3', color="CAP_INV", hover_name="SRC_CTRY", projection="natural earth", scope='world',)
    map1.update_traces(customdata=filtered_df['SRC_CTRY']),
    map1.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')
    return  map1
         
  
           
       
@app.callback(dash.dependencies.Output('scatter', 'figure'),
    [dash.dependencies.Input('map1', 'hoverData')])
def scatter( hoverData ): 
    
  #  filtered_df = fdimarkets[fdimarkets['YEAR'] == selected_year] 
   # customdata=filtered_df[filtered_df['SRC_CTRY']]
    filtered_df = fdimarkets[fdimarkets['SRC_CTRY'] == hoverData['points'][0]['customdata']]   
    scatter_fig = px.scatter(filtered_df, x='CAP_INV', y='INDUST_SECTOR', size_max=70
    ).update_traces(marker_opacity=0.5, marker_size=12)      
    return scatter_fig

@app.callback(dash.dependencies.Output('jobs', 'figure'),
    [dash.dependencies.Input('year-slider', 'value')])
def jobs(selected_year ): 
    filtered_df = fdimarkets[fdimarkets['YEAR'] == selected_year] 
    jobs = px.scatter(filtered_df, x='JOBSCREATED', y='INDUST_SECTOR', size_max=70, color='CAP_INV', color_continuous_scale='Viridis',
    ).update_traces(marker_opacity=0.5, marker_size=12)
    return jobs
 
    
@app.callback(dash.dependencies.Output('cap_inv2', 'figure'),
    [dash.dependencies.Input('year-slider', 'value'),
     dash.dependencies.Input('region', 'value')])
def cap_inv(selected_year, region): 
    filtered_df = fdimarkets[fdimarkets['YEAR'] == selected_year]
    filtered_df = filtered_df[filtered_df['DSTN_REGION'] == region]
    cap_inv2 =  go.Figure(data=[go.Bar(name='Outward', x=filtered_df['SRC_CTRY'], y=filtered_df['CAP_INV'],  offsetgroup=0), go.Bar(name='Inward', x=filtered_df['DSTN_CTRY'], y=filtered_df['CAP_INV'],  offsetgroup=1,
    marker_color='lightsalmon')])
    return cap_inv2


        
   # Start the server
if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port="8040", debug=True)
