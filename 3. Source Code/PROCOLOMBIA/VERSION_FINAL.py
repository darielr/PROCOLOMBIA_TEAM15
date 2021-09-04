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

tpl = dl.templates.DbcRow(app, title="PR", left_cols=4, figure_template=True)# theme=dbc.themes.SUPERHERO)

template=tpl

server = app.server
app.config["suppress_callback_exceptions"] = True

# This loads the "flatly" themed figure template templates from dash-bootstrap-templates library,
# adds it to plotly.io and makes it the default.

load_figure_template("Flaty")

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    'color': 'rgb(179,166,166)',
    'background-color': 'rgb(242,242,242)'
    }


sidebar = html.Div(
    [
        #html.H2("Sidebar", className="display-4"),
        html.Img(src=app.get_asset_url('pro_colombia_logo (1).png'), style={'height':'20%', 'width':'100%'}, ),
        html.Hr(),
        html.P(
            "Menu", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Statistics Analysis", href="/page-1", active="exact"),
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
                dbc.NavLink("USA_Topic_Modeling", href="/page-12", active=False, style= {'display': 'none'}),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)


navbar = dbc.NavbarSimple(
    children=[
        html.A( dbc.Row(
                [
                    dbc.Col(html.Img(src=app.get_asset_url('LOGO.png'), height="30px")),
                                   ],
                align="center",
                no_gutters=True,
            ),
             ),
        dbc.NavItem(dbc.NavLink("Page 1", href="/page-1")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Page 2", href="/page-2"),
                dbc.DropdownMenuItem("Page 3", href="/page-3"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    
    brand="PROCOLOMBIA",
    brand_href="https://procolombia.co/en",
    color="dark",
    dark=True,
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
                dbc.Button("More information", outline=True, color="success", href="https://www.linkedin.com/in/angiaparicio/"),
            ]
        ),
    ],
    style={"width": "9rem", 'height':'50%'},
)

card_dariel = dbc.Card(
    [
        dbc.CardImg(src=app.get_asset_url('dariel.jpeg'), style={'height':'100%', 'width':'100%'}, top=True),
        dbc.CardBody(
            [
                html.H4("Dariel Rincones", className="card-title"),
                html.P(
                    "Software Developer",
                    className="card-text",
                ),
                dbc.Button("More information", outline=True, color="success", href='https://www.linkedin.com/in/dariel-alfonso-rincones-rivas-1b401536/'),
            ]
        ),
    ],
    style={"width": "9rem", 'height':'50%'},
)

card_daniel = dbc.Card(
    [
        dbc.CardImg(src=app.get_asset_url('daniel.jpeg'), style={'height':'100%', 'width':'100%'}, top=True),
        dbc.CardBody(
            [
                html.H4("Daniel Romero", className="card-title"),
                html.P(
                    "Industrial Engineer",
                    className="card-text",
                ),
                dbc.Button("More information", outline=True, color="success", href='https://www.linkedin.com/in/daniel-romero-rodriguez-226bb213/'),
            ]
        ),
    ],
    style={"width": "9rem", 'height':'50%'},
)


card_carlos = dbc.Card(
    [
        dbc.CardImg(src=app.get_asset_url('carlos.jpeg'),  style={'height':'100%', 'width':'100%'}, top=True),
        dbc.CardBody(
            [
                html.H4("Carlos Lopez", className="card-title"),
                html.P(
                    "Industrial Engineer",
                    className="card-text",
                ),
                dbc.Button("More information", outline=True, color="success", href='www.linkedin.com/in/carlos-eduardo-lópez-ramos'),
            ]
        ),
    ],
    style={"width": "9rem", 'height':'50%'},
)

card_german = dbc.Card(
    [
        dbc.CardImg(src=app.get_asset_url('german.jpeg'), style={'height':'100%', 'width':'100%'}, top=True),
        dbc.CardBody(
            [
                html.H4("German Puertas", className="card-title"),
                html.P(
                    "Industrial Engineer",
                    className="card-text",
                ),
                dbc.Button("More information", outline=True, color="success", href='https://www.linkedin.com/in/germ%C3%A1n-puertas-a420b113'),
            ]
        ),
    ],
    style={"width": "9rem", 'height':'50%'},
)


card_manuel = dbc.Card(
    [
        dbc.CardImg(src=app.get_asset_url('manuel.jpeg'),  style={'height':'100%', 'width':'100%'}, top=True),
        dbc.CardBody(
            [
                html.H4("Manuel Arias", className="card-title"),
                html.P(
                    "Electronic Engineer",
                    className="card-text",
                ),
                dbc.Button("More information", outline=True, color="success", className="mr-1", href='https://www.linkedin.com/in/manuel-arias-6a292962'),
            ]
        ),
    ],
    style={"width": "8rem", 'height':'50%'},
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
                    "Sequence of n words in a tweet",
                    className="card-text",
                ),
                dbc.Button("View details", color="danger", href="/page-4", outline=True, ),
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
                    "Determine if a tweet is positive, neutral or negative",
                    className="card-text",
                ),
                dbc.Button("View details", color="warning", href="/page-5", outline=True, ),
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
                    "Classify tweets in different topics",
                    className="card-text",
                ),
                dbc.Button("View details", color="success", href="/page-6", outline=True, ),
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
                    "Sequence of n words in a tweet",
                    className="card-text",
                ),
                dbc.Button("View details", color="danger", href="/page-7", outline=True, ),
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
                    "Determine if a tweet is positive, neutral or negative",
                    className="card-text",
                ),
                dbc.Button("View details", color="warning", href="/page-8", outline=True, ),
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
                    "Classify tweets in different topics",
                    className="card-text",
                ),
                dbc.Button("View details", color="success", href="/page-9" , outline=True,),
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
                    "Sequence of n words in a tweet",
                    className="card-text",
                ),
                dbc.Button("View details", color="danger", href="/page-10", outline=True ),
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
                    "Determine if a tweet is positive, neutral or negative",
                    className="card-text",
                ),
                dbc.Button("View details", color="warning", href="/page-11" ,outline=True ),
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
                    "Classify tweets in different topics",
                    className="card-text",
                ),
                dbc.Button("View details", color="success", href="/page-12" , outline=True,),
            ]
        ),
    ],
    style={'width': '100%',  'marginTop': '20'},
))
])
])

tabs =  html.Div([
        dbc.Tabs(
    [   
        dbc.Tab(tab1_content, label="Canada"),
        dbc.Tab(tab2_content, label="United Kingdom"),
        dbc.Tab(tab3_content, label="United States"),    
    ])
    ])


####################################################################### DATA fdimarkets
path_data='data/'
full_path=os.path.join(path_data, 'clean_fdimarkets.csv')
fdimarkets  = pd.read_csv(full_path,sep = ';', encoding='latin-1')

source_country=fdimarkets['SRC_CTRY'].unique()
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


CONTENT_STYLE = {
    "margin-left": "50",
    "margin-right": "0",
    'marginTop': '5',
    'marginBottom': '10',
    
    'backgroundColor':'#EBEBEB',
    
}
content = html.Div(id="page-content", style={ "margin-left": "17rem", "margin-right": "0rem", 'marginBottom': '0rem',})

app.layout = html.Div([dcc.Location(id="url"),sidebar, content,

     #  
        
    
  #  html.Div(id='tabs-content-classes',  style={ "margin-left": "15rem", "margin-right": "1rem", "padding": "2rem 1rem", 'backgroundColor':'#EBEBEB'})
]
)
  
@app.callback(Output('page-content', 'children'),
               [Input('url', 'pathname')]
              )
              
def render_content(pathname):
 if pathname == "/":
             return  html.Div([ 
             html.Img(src=app.get_asset_url('Imagen2.jpg'), style={'height':'1%', 'width':'100%'} ),
             html.Hr(),
             html.Div([dbc.Row([dbc.Col(dbc.Card(
    [
        dbc.CardImg(src=app.get_asset_url('logo-fdi-markets.png'),  top=True, style={'height':'1%', 'width':'100%'} ),
        dbc.CardBody(
            [
                html.H4("Statistics Analysis", className="card-title"),
                html.P(
                    'Here you can find descriptive visualizations about investments in the world obtained from the cross-border investment monitor from the Financial Times (fDi markets)',
                    className="card-text",
                ),
                dbc.Button("View details", color="success", href="/page-1" , outline=True,),
            ]
        ),
    ],
    style={'width': '100%',  'marginTop': '20', 'backgroundColor':'rgb(179,205,227)'}
)), 
       dbc.Col(dbc.Card(
    [
        dbc.CardImg(src=app.get_asset_url('arreglada_twitter.png'), top=True),
        dbc.CardBody(
            [
                html.H4("Models", className="card-title"),
                html.P(
                    'Here you can find model results with Twitter as data source ',
                    className="card-text",
                ),
                dbc.Button("View details", color="success", href="/page-2" , outline=True,),
            ]
        ),
    ],
    style={'width': '100%',  'marginTop': '20', 'backgroundColor':'rgb(179,205,227)'},
)), 

             ])
             ], style={'backgroundColor':'rgb(242,242,242)'}),
             html.Img(src=app.get_asset_url('Colombia.jpg'), style={'height':'3%', 'width':'100%'}),
             html.Div([ 
             dbc.Row([ dbc.Col(html.Img(src=app.get_asset_url('procolombia.png'), style={'height':'70%', 'width':'70%'})),
             dbc.Col(html.Img(src=app.get_asset_url('emp-logo-colombia.png'), style={'height':'70%', 'width':'90%'})),
             dbc.Col(html.Img(src=app.get_asset_url('DS4A_LatAm_logo@2x.png'), style={'height':'70%', 'width':'100%'}))
             ])
             ], style={'background-color': '#ABBAEA', 'marginBottom': '5' }),
             ], style={'background-image': 'Imagen2.jpg'})
            
 if pathname == "/page-1":
             return html.Div([ html.H3('Global Investment Analysis'),
             html.Hr(), 
             html.Div([html.P('The following map shows the total investments that each country has made from 2012 to 2021 in order to show those countries that over time    have a high degree of investment that can be targeted for Colombia. In the next slider you can select the year you want to consult.'),],style={'backgroundColor':'rgb(179,205,227)'}) ,              
             dcc.Slider(
             id='year-slider',
             min=fdimarkets['YEAR'].min(),
             max=fdimarkets['YEAR'].max(),
             value=fdimarkets['YEAR'].max(),
             marks={str(year): str(year) for year in fdimarkets['YEAR'].unique()},
             step=None,
            
             ),  
                    
            dbc.Row([
            dbc.Col(dcc.Graph(id='map1'), lg=12),
                   ]),
            html.Hr(),
            html.Div([html.P('In the following scatter charts you will be able to visualize the sectors in which the countries invested their capital in the respective year and the jobs they generated according to capital.'),],style={'backgroundColor':'rgb(179,205,227)'}),
            html.Div([
            html.Label('Select investor country'),
            dcc.Dropdown(
                id='source_country',
                options=[{'label': i, 'value': i} for i in source_country],
                #placeholder="Select a c",
                value='India', 
                
                
            )], style={'width': '30%', 'display': 'inline-block', }),             
            dbc.Row([
            dbc.Col(dcc.Graph(id='scatter'), lg=6),
            dbc.Col(dcc.Graph(id='jobs'), lg=6)
             ]),  
             
            html.Hr(), 
            html.Div([html.P('In the bar chart you will be able to visualize the internal and external investments in each destination region.'),],style={'backgroundColor':'rgb(179,205,227)'}),               
            html.Div([
            html.Label('Select a destination region'),
            dcc.Dropdown(
                id='region',
                options=[{'label': i, 'value': i} for i in region],
                value='Asia'
            )], style={'width': '30%', 'display': 'inline-block'}),   
            
            dbc.Row([
            dbc.Col(dcc.Graph(id='cap_inv2'), lg=12),
                   ]),                  
                                                     
            html.Img(src=app.get_asset_url('Colombia.jpg'), style={'height':'1%', 'width':'100%'}), 
            html.Div([ 
            dbc.Row([ dbc.Col(html.Img(src=app.get_asset_url('procolombia.png'), style={'height':'70%', 'width':'70%'})),
            dbc.Col(html.Img(src=app.get_asset_url('emp-logo-colombia.png'), style={'height':'70%', 'width':'90%'})),
            dbc.Col(html.Img(src=app.get_asset_url('DS4A_LatAm_logo@2x.png'), style={'height':'70%', 'width':'100%'}))
            ])
            ], style={'background-color': '#ABBAEA', 'marginBottom': '5' })
            ]),
     
 if pathname == "/page-2":
    return  html.Div([html.Img(src=app.get_asset_url('countries.jpg'), style={'height':'1%', 'width':'100%'}), 
    tabs, html.Div([html.Img(src=app.get_asset_url('Colombia.jpg'), style={'height':'3%', 'width':'100%'}), 
    html.Div([ dbc.Row([ dbc.Col(html.Img(src=app.get_asset_url('procolombia.png'), style={'height':'70%', 'width':'70%'})),
            dbc.Col(html.Img(src=app.get_asset_url('emp-logo-colombia.png'), style={'height':'70%', 'width':'90%'})),
            dbc.Col(html.Img(src=app.get_asset_url('DS4A_LatAm_logo@2x.png'), style={'height':'70%', 'width':'100%'}))
            ])
            ], style={'background-color': '#ABBAEA', 'marginBottom': '5' })])])
        
 if pathname == "/page-3":
   return  html.Div([html.H3('Data Science Team'),
             html.Hr(), cards, html.Div([html.Img(src=app.get_asset_url('Colombia.jpg'), style={'height':'3%', 'width':'100%'}), 
   html.Div([ dbc.Row([ dbc.Col(html.Img(src=app.get_asset_url('procolombia.png'), style={'height':'70%', 'width':'70%'})),
            dbc.Col(html.Img(src=app.get_asset_url('emp-logo-colombia.png'), style={'height':'70%', 'width':'90%'})),
            dbc.Col(html.Img(src=app.get_asset_url('DS4A_LatAm_logo@2x.png'), style={'height':'70%', 'width':'100%'}))
            ])
            ], style={'background-color': '#ABBAEA', 'marginBottom': '5' })])])
        
 if pathname == "/page-4":
   return   html.Div([
            html.H3('Descriptive Analysis'),
            html.Hr(),
            html.Div([html.P('This descriptive analysis presents the word cloud obtained from the twitters for Canada, where the main filter was Colombia, and the respective n-grams'), ],style={'backgroundColor':'rgb(179,205,227)'}),
            html.Img(src=app.get_asset_url('Canada_wordcloud1.png'), style={'height':'50%', 'width':'70%', 'textAlign': 'center'}),
            html.Hr(), html.Div([ dbc.Row([
            dbc.Col(
                [
                    dbc.Row(
                        dbc.Col(html.Iframe(src=app.get_asset_url('Canada_barchartOnegram.html'), style={"height": "398px", "width": "100%"}))
                    ),
                    dbc.Row(
                        dbc.Col(html.Iframe(src=app.get_asset_url('Canada_barchartBigram.html'), style={"height": "398px", "width": "100%"}))
                    )
                ],
                width=6
            ),
           dbc.Col(html.Iframe(src=app.get_asset_url('Canada_barchartTrigram.html'), style={"height": "800px", "width": "100%"})),
        ]
        )
        ]),
            html.Hr(),
            dbc.Button("Learn more about n-grams", color="danger", href="https://towardsdatascience.com/understanding-word-n-grams-and-n-gram-probability-in-natural-language-processing-9d9eef0fa058"), 
            dbc.Button("Come back ", color="warning", href="/page-2"),
            ]), html.Img(src=app.get_asset_url('Colombia.jpg'), style={'height':'3%', 'width':'100%'}), html.Div([ 
            dbc.Row([ dbc.Col(html.Img(src=app.get_asset_url('procolombia.png'), style={'height':'70%', 'width':'70%'})),
            dbc.Col(html.Img(src=app.get_asset_url('emp-logo-colombia.png'), style={'height':'70%', 'width':'90%'})),
            dbc.Col(html.Img(src=app.get_asset_url('DS4A_LatAm_logo@2x.png'), style={'height':'70%', 'width':'100%'}))
            ])
            ], style={'background-color': '#ABBAEA', 'marginBottom': '5' })
 if pathname == "/page-5":
   return   html.Div([
            html.H3('Sentiment Analysis'),
            html.Hr(),
            html.Div([html.P('Sentiment analysis is the most common text classification tool that analyzes an incoming message and tells whether the underlying sentiment is positive, negative, or neutral. In this case, this sentiment about Colombia is analyzed using Canadian tweets.'), ],style={'backgroundColor':'rgb(179,205,227)'}),
            html.Iframe(src=app.get_asset_url('Canada_figsentiment.html'), style={"height": "600px", "width": "49%"}),
            html.Iframe(src=app.get_asset_url('Canada_sentimentbar.html'), style={"height": "600px", "width": "49%"}),
            html.Hr(),
            dbc.Button("Learn more about Sentiment analysis", color="danger", href="https://towardsdatascience.com/sentiment-analysis-concept-analysis-and-applications-6c94d6f58c17"), 
            dbc.Button("Come back ", color="warning", href="/page-2"),
            ]), html.Div([ html.Img(src=app.get_asset_url('Colombia.jpg'), style={'height':'3%', 'width':'100%'}), 
            html.Div([ dbc.Row([ dbc.Col(html.Img(src=app.get_asset_url('procolombia.png'), style={'height':'70%', 'width':'70%'})),
            dbc.Col(html.Img(src=app.get_asset_url('emp-logo-colombia.png'), style={'height':'70%', 'width':'90%'})),
            dbc.Col(html.Img(src=app.get_asset_url('DS4A_LatAm_logo@2x.png'), style={'height':'70%', 'width':'100%'}))
            ])
            ], style={'background-color': '#ABBAEA', 'marginBottom': '5' })
            ]),  
            
            
 if pathname == "/page-6":
   return   html.Div([
            html.H3('Topic Modeling'),
            html.Hr(),
            html.Div([html.P("In this section, you will be able to visualize and interact with the clusters obtained using the unsupervised machine learning technique known as topic modeling for Canada's word clouds."), ],style={'backgroundColor':'rgb(179,205,227)'}),
            html.Iframe(src=app.get_asset_url('Canada_lda.html'), style={"height": "900px", "width": "100%"}),
            html.Hr(),
            dbc.Button("Learn more about topic modeling", color="danger", href="https://monkeylearn.com/blog/introduction-to-topic-modeling/"), 
            dbc.Button("Come back ", color="warning", href="/page-2"),
            ]), html.Div([ html.Img(src=app.get_asset_url('Colombia.jpg'), style={'height':'3%', 'width':'100%'}), 
            html.Div([ dbc.Row([ dbc.Col(html.Img(src=app.get_asset_url('procolombia.png'), style={'height':'70%', 'width':'70%'})),
            dbc.Col(html.Img(src=app.get_asset_url('emp-logo-colombia.png'), style={'height':'70%', 'width':'90%'})),
            dbc.Col(html.Img(src=app.get_asset_url('DS4A_LatAm_logo@2x.png'), style={'height':'70%', 'width':'100%'}))
            ])
            ], style={'background-color': '#ABBAEA', 'marginBottom': '5' })
            ]),
            
            
 if pathname == "/page-7":
   return   html.Div([
            html.H3('Descriptive Analysis'),
            html.Hr(),
            html.Div([html.P('This descriptive analysis presents the word cloud obtained from the twitters for United Kingdom, where the main filter was Colombia, and the respective n-grams'), ],style={'backgroundColor':'rgb(179,205,227)'}),
            html.Img(src=app.get_asset_url('UK_wordcloud1.png'), style={'height':'50%', 'width':'70%', 'textAlign': 'center'}),
            html.Hr(), html.Div([ dbc.Row([
            dbc.Col(
                [
                    dbc.Row(
                        dbc.Col(html.Iframe(src=app.get_asset_url('UK_barchartOnegram.html'), style={"height": "398px", "width": "100%"}))
                    ),
                    dbc.Row(
                        dbc.Col(html.Iframe(src=app.get_asset_url('UK_barchartBigram.html'), style={"height": "398px", "width": "100%"}))
                    )
                ],
                width=6
            ),
           dbc.Col(html.Iframe(src=app.get_asset_url('UK_barchartTrigram.html'), style={"height": "800px", "width": "100%"})),
        ]
        )
        ]),
            html.Hr(),
            
            dbc.Button("Learn more about n-grams", color="danger", href="https://towardsdatascience.com/understanding-word-n-grams-and-n-gram-probability-in-natural-language-processing-9d9eef0fa058"), 
            dbc.Button("Come back ", color="warning", href="/page-2"),
            ]), html.Div([ html.Img(src=app.get_asset_url('Colombia.jpg'), style={'height':'3%', 'width':'100%'}), 
             html.Div([ dbc.Row([ dbc.Col(html.Img(src=app.get_asset_url('procolombia.png'), style={'height':'70%', 'width':'70%'})),
            dbc.Col(html.Img(src=app.get_asset_url('emp-logo-colombia.png'), style={'height':'70%', 'width':'90%'})),
            dbc.Col(html.Img(src=app.get_asset_url('DS4A_LatAm_logo@2x.png'), style={'height':'70%', 'width':'100%'}))
            ])
            ], style={'background-color': '#ABBAEA', 'marginBottom': '5' })
            ])
 if pathname == "/page-8":
   return   html.Div([
            html.H3('Sentiment Analysis'),
            html.Hr(),
            html.Div([html.P('Sentiment analysis is the most common text classification tool that analyzes an incoming message and tells whether the underlying sentiment is positive, negative, or neutral. In this case, this sentiment about Colombia is analyzed using UK tweets.'), ],style={'backgroundColor':'rgb(179,205,227)'}),
            html.Iframe(src=app.get_asset_url('UK_figsentiment.html'), style={"height": "600px", "width": "49%"}),
            html.Iframe(src=app.get_asset_url('UK_sentimentbar.html'), style={"height": "600px", "width": "49%"}),
            html.Hr(),
            dbc.Button("Learn more about Sentiment Analysis", color="danger", href="https://towardsdatascience.com/sentiment-analysis-concept-analysis-and-applications-6c94d6f58c17"), 
            dbc.Button("Come back ", color="warning", href="/page-2"),
            ]), html.Div([ html.Img(src=app.get_asset_url('Colombia.jpg'), style={'height':'3%', 'width':'100%'}), 
            html.Div([ dbc.Row([ dbc.Col(html.Img(src=app.get_asset_url('procolombia.png'), style={'height':'70%', 'width':'70%'})),
            dbc.Col(html.Img(src=app.get_asset_url('emp-logo-colombia.png'), style={'height':'70%', 'width':'90%'})),
            dbc.Col(html.Img(src=app.get_asset_url('DS4A_LatAm_logo@2x.png'), style={'height':'70%', 'width':'100%'}))
            ])
            ], style={'background-color': '#ABBAEA', 'marginBottom': '5' })
            ]),
            
            
 if pathname == "/page-9":
   return   html.Div([
            html.H3('Topic Modeling'),
            html.Hr(),
            html.Div([html.P("In this section, you will be able to visualize and interact with the clusters obtained using the unsupervised machine learning technique known as topic modeling for United Kingdom's word clouds."), ],style={'backgroundColor':'rgb(179,205,227)'}),
            html.Iframe(src=app.get_asset_url('UK_lda.html'), style={"height": "900px", "width": "100%"}),
            html.Hr(),
            dbc.Button("Learn more about topic modeling", color="danger", href="https://monkeylearn.com/blog/introduction-to-topic-modeling/"), 
            dbc.Button("Come back ", color="warning", href="/page-2"),
            ]), html.Div([ html.Img(src=app.get_asset_url('Colombia.jpg'), style={'height':'3%', 'width':'100%'}), 
            html.Div([ dbc.Row([ dbc.Col(html.Img(src=app.get_asset_url('procolombia.png'), style={'height':'70%', 'width':'70%'})),
            dbc.Col(html.Img(src=app.get_asset_url('emp-logo-colombia.png'), style={'height':'70%', 'width':'90%'})),
            dbc.Col(html.Img(src=app.get_asset_url('DS4A_LatAm_logo@2x.png'), style={'height':'70%', 'width':'100%'}))
            ])
            ], style={'background-color': '#ABBAEA', 'marginBottom': '5' })
            ])
          
 if pathname == "/page-10":
   return   html.Div([
            html.H3('Descriptive Analysis'),
            html.Hr(),
            html.Div([html.P('This descriptive analysis presents the word cloud obtained from the twitters for United States, where the main filter was Colombia, and the respective n-grams'), ],style={'backgroundColor':'rgb(179,205,227)'}),
            html.Img(src=app.get_asset_url('USA_wordcloud1.png'), style={'height':'50%', 'width':'70%', 'textAlign': 'center'}),
            html.Hr(), html.Div([ dbc.Row([
            dbc.Col(
                [
                    dbc.Row(
                        dbc.Col(html.Iframe(src=app.get_asset_url('USA_barchartOnegram.html'), style={"height": "398px", "width": "100%"}))
                    ),
                    dbc.Row(
                        dbc.Col(html.Iframe(src=app.get_asset_url('USA_barchartBigram.html'), style={"height": "398px", "width": "100%"}))
                    )
                ],
                width=6
            ),
           dbc.Col(html.Iframe(src=app.get_asset_url('USA_barchartTrigram.html'), style={"height": "800px", "width": "100%"})),
        ]
        )
        ]),
            html.Hr(),
            
            dbc.Button("Learn more about n-grams", color="danger", href=""), 
            dbc.Button("Come back ", color="warning", href="/page-2"),
            ]), html.Div([ html.Img(src=app.get_asset_url('Colombia.jpg'), style={'height':'3%', 'width':'100%'}), 
            html.Div([ dbc.Row([ dbc.Col(html.Img(src=app.get_asset_url('procolombia.png'), style={'height':'70%', 'width':'70%'})),
            dbc.Col(html.Img(src=app.get_asset_url('emp-logo-colombia.png'), style={'height':'70%', 'width':'90%'})),
            dbc.Col(html.Img(src=app.get_asset_url('DS4A_LatAm_logo@2x.png'), style={'height':'70%', 'width':'100%'}))
            ])
            ], style={'background-color': '#ABBAEA', 'marginBottom': '5' })
            ])
 if pathname == "/page-11":
   return   html.Div([
            html.H3('Sentiment Analysis'),
            html.Hr(),
            html.Div([html.P('Sentiment analysis is the most common text classification tool that analyzes an incoming message and tells whether the underlying sentiment is positive, negative, or neutral. In this case, this sentiment about Colombia is analyzed using USA tweets.'), ],style={'backgroundColor':'rgb(179,205,227)'}),
            html.Iframe(src=app.get_asset_url('USA_figsentiment.html'), style={"height": "600px", "width": "49%"}),
            html.Iframe(src=app.get_asset_url('USA_sentimentbar.html'), style={"height": "600px", "width": "49%"}),
            html.Hr(),
            dbc.Button("Learn more about Sentiment Analysis", color="danger", href="https://towardsdatascience.com/sentiment-analysis-concept-analysis-and-applications-6c94d6f58c17"), 
            dbc.Button("Come back ", color="warning", href="/page-2"),
            ]), html.Div([ html.Img(src=app.get_asset_url('Colombia.jpg'), style={'height':'3%', 'width':'100%'}), 
            html.Div([ dbc.Row([ dbc.Col(html.Img(src=app.get_asset_url('procolombia.png'), style={'height':'70%', 'width':'70%'})),
            dbc.Col(html.Img(src=app.get_asset_url('emp-logo-colombia.png'), style={'height':'70%', 'width':'90%'})),
            dbc.Col(html.Img(src=app.get_asset_url('DS4A_LatAm_logo@2x.png'), style={'height':'70%', 'width':'100%'}))
            ])
            ], style={'background-color': '#ABBAEA', 'marginBottom': '5' })
            ]),
                        
            
 if pathname == "/page-12":
   return   html.Div([
            html.H3('Topic Modeling'),
            html.Hr(),
            html.Div([html.P("In this section, you will be able to visualize and interact with the clusters obtained using the unsupervised machine learning technique known as topic modeling for United States' word clouds."), ],style={'backgroundColor':'rgb(179,205,227)'}),
            html.Iframe(src=app.get_asset_url('USA_lda.html'), style={"height": "900px", "width": "100%"}),
            html.Hr(),
            dbc.Button("Learn more about topic modeling", color="danger", href="https://monkeylearn.com/blog/introduction-to-topic-modeling/"), 
            dbc.Button("Come back ", color="warning", href="/page-2"),
            ]), html.Div([ html.Img(src=app.get_asset_url('Colombia.jpg'), style={'height':'3%', 'width':'100%'}), 
            html.Div([ dbc.Row([ dbc.Col(html.Img(src=app.get_asset_url('procolombia.png'), style={'height':'70%', 'width':'70%'})),
            dbc.Col(html.Img(src=app.get_asset_url('emp-logo-colombia.png'), style={'height':'70%', 'width':'90%'})),
            dbc.Col(html.Img(src=app.get_asset_url('DS4A_LatAm_logo@2x.png'), style={'height':'70%', 'width':'100%'}))
            ])
            ], style={'background-color': '#ABBAEA', 'marginBottom': '5' })
            ]),
                         
            
@app.callback(dash.dependencies.Output('map1', 'figure'),
    [dash.dependencies.Input('year-slider', 'value')])
def update_figure(selected_year):
    filtered_df = clean_fdimarkets_map[clean_fdimarkets_map['YEAR'] == selected_year]
    map1 = px.choropleth(filtered_df, locations='SRC_ISO3', color="CAP_INV", hover_name="SRC_CTRY", projection="natural earth", scope='world',)
   # map1.update_traces(customdata=filtered_df[filtered_df['SECTOR'] == xaxis_column_sector]['PAIS'])
    map1.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')
    return  map1
         
           
       
@app.callback(dash.dependencies.Output('scatter', 'figure'),
    [dash.dependencies.Input('year-slider', 'value'),
     dash.dependencies.Input('source_country', 'value')])
def scatter(selected_year, source_country): 
    
    filtered_df = fdimarkets[fdimarkets['YEAR'] == selected_year] 
    filtered_df = filtered_df[filtered_df['SRC_CTRY'] == source_country]
    scatter_fig = px.scatter(filtered_df, x='CAP_INV', y='INDUST_SECTOR', size_max=70
    ).update_traces(marker_opacity=0.5, marker_size=12)      
    return scatter_fig

@app.callback(dash.dependencies.Output('jobs', 'figure'),
    [dash.dependencies.Input('year-slider', 'value'),
    dash.dependencies.Input('source_country', 'value')])
def jobs(selected_year, source_country ): 
    
    filtered_df = fdimarkets[fdimarkets['YEAR'] == selected_year] 
    filtered_df = filtered_df[filtered_df['SRC_CTRY'] == source_country]
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

@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
        
   # Start the server
if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port="8010", debug=True)
