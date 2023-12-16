import pandas as pd
import geopy
from geopy.distance import great_circle
import random
import numpy as np
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import json
import plotly.graph_objects as go
from dash.dependencies import Output

df_final_cities = pd.read_csv('/https://raw.githubusercontent.com/LDeYoung17/jingle-jam-2023/ds-work-branch/notebooks/final_cities.csv', encoding = "iso-8859-1")

def calculate_distance(location1, location2):
    return great_circle(location1, location2).mi

number_list = [0,1,2,3,4,5,6,7,8]

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

baseline_route = [0,1,2,3,4,5,6,7,8]

baseline_model = fitness(baseline_route)

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

best_of_routes = best_overall_route[0]
optimized_route_data = []

for k in best_of_routes:
    city_row = df_final_cities[df_final_cities['number'] == k]
    city_data = {
        'city': city_row['City'].iloc[0],
        'latitude': city_row['Latitude'].iloc[0],
        'longitude': city_row['Longitude'].iloc[0]
    }
    optimized_route_data.append(city_data)

df_optimized_route = pd.DataFrame(optimized_route_data)

mapbox_access_token = open(".mapbox_token").read()

app = Dash(__name__)

app.layout = html.Div([
    html.H4('Mapping Deliveries Around the World'),
    dcc.RadioItems(
        id='map', 
        options=["Scatter", "Route Map"],
        value="Route Map",
        inline=True
    ),
    dcc.Graph(id="graph"),

])


@app.callback(
    Output("graph", "figure"),
    Input("map", "value")) 


def display_trace_scattermapbox(selected_map):
    if selected_map == 'Route Map':
        fig = go.Figure(go.Scattermapbox(
        ))

        fig.add_trace(go.Scattermapbox(
            mode = "markers+lines",
            lon = df_final_cities['Longitude'],
            lat = df_final_cities['Latitude'],
            text = df_final_cities['City'],
            name='Baseline Route',
            marker = {'size': 10})),

        fig.add_trace(go.Scattermapbox(
            mode = "markers+lines",
            lon = df_optimized_route['longitude'],
            lat = df_optimized_route['latitude'],
            text = df_optimized_route['city'],
            name = 'Optimized Route',
            marker = {'size': 10}))

        fig.update_layout(
            margin ={'l':0,'t':0,'b':0,'r':0},
            mapbox = {
                'center': {'lon': 10, 'lat': 10},
                'style': "open-street-map",
                'center': {'lon': -20, 'lat': -20},
                'zoom': 1})
    elif selected_map == 'Scatter':
        fig = go.Figure(go.Scattermapbox(
            lat=df_final_cities['Latitude'],
            lon=df_final_cities['Longitude'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=9
            ),
            text=df_final_cities['City'],
        ))

        fig.update_layout(
            autosize=True,
            hovermode='closest',
            mapbox=dict(
                accesstoken=mapbox_access_token,
                bearing=0,
                center=dict(
                    lat=38.92,
                    lon=-77.07, 
            ),
            pitch=0,
            zoom=1
            ),
        )
    return fig


app.run_server(debug=True)


data_to_convert = {
    "data_config": {
        "csv_file_path": "/Users/admin/Desktop/GitHub/new_repos/jingle-jam-2023/notebooks/final_cities.csv",
        "number_list": number_list,
        "population_size": 10,
        "num_generations": 250,
        "mutation_rate": 0.1
    },
    "best_route": {
        "route": best_overall_route[0],
        "fitness": best_overall_route[1],
        "baseline_model": baseline_model,
        "baseline_route": baseline_route
    },
    "optimized_route_data": optimized_route_data,
    "dash_app_layout": {
        "title": "Mapping Deliveries Around the World",
        "radio_items_options": ["Route Map", "Scatter"],
        "default_value": "Route Map"
    }
}

json_data = json.dumps(data_to_convert, indent=4)

with open('output.json', 'w') as json_file:
    json.dump(data_to_convert, json_file, indent=4)
