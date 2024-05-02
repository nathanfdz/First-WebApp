# Import packages-----------------------------------------------------------------
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
from dash.exceptions import PreventUpdate
from dash.dependencies import State

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

    #1
    html.Div(className='row', children=[
        html.Div(className='six columns', children=[
            dash_table.DataTable(data=df.to_dict('records'), page_size=11, style_table={'overflowX': 'auto'})
        ]),
        html.Div(className='six columns', children=[
            dcc.Graph(figure={}, id='histo-chart-final')
        ])
    ]),
    #2
html.Div(className='row', children='La boite à moustache',
            style={'textAlign': 'center', 'color': 'black', 'fontSize': 20}),
html.Div([
    dcc.Checklist(['Asia', 'Europe', 'Africa','Americas', 'Oceania'],
                inline=True,
                id='my-checklist'
                )
],style={'textAlign': 'center'}),

html.Div(className='row', children=[
    dcc.Graph(id="box")
]),


    #3
    html.Div([
    html.H2("Graphique linéaire"),
    dcc.Graph(id="graph"),
    html.Div(id="pb-result")
],style={'textAlign': 'center', 'color': 'black', 'fontSize': 20})

    ])

#calcul de la moyenne d'espérence de vie de chaque continent-----------------------------------------------------------------
moyenne_asia = df[df['continent'] == 'Asia']['lifeExp'].mean()
print(moyenne_asia)


moyenne_Europe = df[df['continent'] == 'Europe']['lifeExp'].mean()
print(moyenne_Europe)

moyenne_Africa = df[df['continent'] == 'Africa']['lifeExp'].mean()
print(moyenne_Africa)

moyenne_Americas = df[df['continent'] == 'Americas']['lifeExp'].mean()
print(moyenne_Americas)

moyenne_Oceania = df[df['continent'] == 'Oceania']['lifeExp'].mean()
print(moyenne_Oceania)

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

#graphique 3
@app.callback(
    Output("pb-result", "children"),
    [Input("graph", "clickData")]
)
def update_output(click_data):
    if click_data:
        # Si des données de clic sont disponibles
        continent = click_data["points"][0]["x"]
        # Récupérez le continent correspondant au clic
        selected_continent = continent
        # Filtrer les données pour le continent sélectionné
        filtered_df = df[df["continent"] != selected_continent]
        # Créer le nouveau graphique sans le continent sélectionné
        fig = px.line(
            filtered_df,
            x="continent",
            y="lifeExp",
            color="country",
            markers=True,
            title="Life Expectancy for Countries with High Population",
        )
        fig.update_layout(title=dict(x=0.5))
        return dcc.Graph(figure=fig)
    else:
        # Si aucun clic n'a été détecté, afficher le graphique initial
        fig = px.line(
            df,
            x="continent",
            y="lifeExp",
            color="country",
            markers=True,
            title="Life Expectancy for Countries with High Population",
        )
        fig.update_layout(title=dict(x=0.5))
        return dcc.Graph(figure=fig)

# Exécutez l'application-----------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
