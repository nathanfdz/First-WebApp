# Import packages-----------------------------------------------------------------
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate
from dash.dependencies import State


# ici
# Incorporate data-----------------------------------------------------------------
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

# Initialisez l'application - incorporez du CSS-----------------------------------------------------------------
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)


# Mise en page de l'app-----------------------------------------------------------------
app.layout = html.Div([
    #titre de ma page
    html.Div(className='row', children='My First WebApp in Python with Data, Graph, and Controls',
            style={'textAlign': 'center', 'color': 'blue', 'fontSize': 30}),

    #trait en dessous du titre
    html.Hr(),


    #div pour boutons radio
    html.Div(className='row', children=[
        dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'],
                    value='pop',
                    inline=True,#permet de mettre de façon horizontale mes boutons radio
                    id='my-radio-buttons-final')
    ],style={'textAlign': 'center'}),

    #Diagramme en baton
    html.Div(className='row', children=[
        html.Div(className='six columns', children=[
            dash_table.DataTable(data=df.to_dict('records'), page_size=11, style_table={'overflowX': 'auto'})
        ]),
        html.Div(className='six columns', children=[
            dcc.Graph(figure={}, id='histo-chart-final')
        ])
    ]),

    #trait en dessous du titre
    html.Hr(),

    #Boite à moustache
html.Div(className='row', children='Box plot',
            style={'textAlign': 'center', 'color': 'black', 'fontSize': 20}),
html.Div([
    dcc.Checklist(options=['Asia', 'Europe', 'Africa','Americas', 'Oceania'],
                inline=True,
                value=['Europe'],
                id='my-checklist'
                )
],style={'textAlign': 'center'}),

html.Div(className='row', children=[
    dcc.Graph(id="box")
]),

html.Hr(),

#diagramme circulaire
html.Div([
    html.Div("Diagramme Circulaire"),
    dcc.Graph(figure={},id='pie-chart')
], style={'textAlign': 'center', 'color': 'black', 'fontSize': 20})

    ])



# Ajouter des contrôles pour créer l'interaction1-----------------------------------------------------------------
#graphique 2
@app.callback(
        Output(component_id='box',component_property='figure'),
        Input(component_id='my-checklist',component_property='value')
)

def generate_plot_box(selected_values):
    if selected_values is None:
        raise PreventUpdate# Empêche la mise à jour du graphique si aucune valeur n'est sélectionnée dans la checklist
    # Filtrer le DataFrame en fonction des valeurs sélectionnées dans la checklist
    filtered_df = df[df['continent'].isin(selected_values)]
    # Créer le graphique en boîte avec Plotly Express
    fig = px.box(filtered_df, x='continent', y='pop')
    return fig


# graphique 1
@callback(
    Output(component_id='histo-chart-final', component_property='figure'),
    Input(component_id='my-radio-buttons-final', component_property='value')
)
def update_graph(col_chosen):
    fig = px.histogram(df, x='continent', y=col_chosen, histfunc='avg')
    return fig


#diagramme circulaire
def update_pie_chart(selected_category):
    # Créer un diagramme circulaire avec Plotly Express
    fig = px.pie(df, values='continent', names='pop', title='Diagramme Circulaire',color_discrete_sequence=px.colors.sequential.RdBu)
    return fig


# Exécutez l'application-----------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
