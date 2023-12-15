import pandas as pd
import folium
import geopy
from geopy.distance import great_circle
import deap
import random
#import mlrose
import numpy as np
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

df_final_cities = pd.read_csv('/https://raw.githubusercontent.com/LDeYoung17/jingle-jam-2023/ds-work-branch/notebooks/final_cities.csv', encoding = "iso-8859-1")

def calculate_distance(location1, location2):
    return great_circle(location1, location2).mi

number_list = [0,1,2,3,4,5,6,7,8]

random.shuffle(number_list)
print(number_list)
df_final_cities['number'] = number_list

def fitness(route):
    total_distance = 0
    for i in range(len(route) - 1):

        location1 = route[i]
        location2 = route[i+1]

        lat_long_1 = (df_final_cities.loc[df_final_cities['number'] == location1, 'Latitude'].iloc[0], 
                      df_final_cities.loc[df_final_cities['number'] == location1, 'Longitude'].iloc[0])
        lat_long_2 = (df_final_cities.loc[df_final_cities['number'] == location2, 'Latitude'].iloc[0], 
                      df_final_cities.loc[df_final_cities['number'] == location2, 'Longitude'].iloc[0])

        total_distance += calculate_distance(lat_long_1, lat_long_2)
    return total_distance

def create_population():
    location_numbers = list(range(9))

    population_size = 10 
    population = []

    for pop_number in range(population_size):
        optimized_route = location_numbers[:]
        random.shuffle(optimized_route)
        population.append(optimized_route)
    return population


def selection_optimize(population, fitness_func, tournament_size=10):
    selected = []
    for j in range(len(population)):
        contenders = random.sample(population, tournament_size)
        winner = min(contenders, key=fitness_func)
        selected.append(winner)
    return selected

def ordered_crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    offspring = [None] * size
    offspring[start:end] = parent1[start:end]
    fill_values = [item for item in parent2 if item not in offspring]
    for i in range(size):
        if offspring[i] is None:
            offspring[i] = fill_values.pop(0)
    return offspring

def swap_mutation(route, mutation_rate):
    mutated_route = route[:]
    for i in range(len(route)):
        if random.random() < mutation_rate:
            swap_index = random.randint(0, len(route) - 1)
            mutated_route[i], mutated_route[swap_index] = mutated_route[swap_index], mutated_route[i]
    return mutated_route

num_generations = 250 
population_size = 10  
mutation_rate = 0.1  
best_route_per_generation = []

# Initialize population with random routes
selection_population = create_population()

for generation in range(num_generations):

    fitness_scores = [fitness(route) for route in selection_population]

    optimized_selection = selection_optimize(selection_population, fitness, tournament_size=5)

    next_generation = []
    while len(next_generation) < population_size:
        route_1, route_2 = random.sample(optimized_selection, 2)
        crossover_route = ordered_crossover(route_1, route_2)
        next_generation.append(crossover_route)

    population = [swap_mutation(route, mutation_rate) for route in next_generation]

    best_route = min(population, key=fitness)
    best_route_fitness = fitness(best_route)
    best_route_per_generation.append((best_route, best_route_fitness))

best_overall_route = min(best_route_per_generation, key=lambda x: x[1])
print(best_overall_route)

app = Dash(__name__)

app.layout = html.Div([
    html.H4('Polotical candidate voting pool analysis'),
    html.P("Select a candidate:"),
    dcc.RadioItems(
        id='candidate', 
        options=["Joly", "Coderre", "Bergeron"],
        value="Coderre",
        inline=True
    ),
    dcc.Graph(id="graph"),
])


@app.callback(
    Output("graph", "figure"), 
    Input("candidate", "value"))
def display_choropleth(candidate):
    df = px.data.election() # replace with your own data source
    geojson = px.data.election_geojson()
    fig = px.choropleth(
        df, geojson=geojson, color=candidate,
        locations="district", featureidkey="properties.district",
        projection="mercator", range_color=[0, 6500])
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig


app.run_server(debug=True)


