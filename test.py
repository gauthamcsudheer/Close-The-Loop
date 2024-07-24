import itertools
from math import radians, sin, cos, sqrt, atan2
from geopy.geocoders import Nominatim

def haversine_distance(coord1, coord2):
    # Calculate the Haversine distance between two geographical coordinates
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    R = 6371.0  # Earth radius in kilometers

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c

    return distance

def total_distance(route):
    return sum(haversine_distance(route[i], route[i+1]) for i in range(len(route)-1)) + haversine_distance(route[-1], route[0])

def travelling_salesman(cities):
    shortest_route = None
    min_distance = float('inf')
    
    for perm in itertools.permutations(cities):
        current_distance = total_distance([city[1] for city in perm])
        if current_distance < min_distance:
            min_distance = current_distance
            shortest_route = perm
    
    return shortest_route, min_distance

def get_coordinates(city):
    geolocator = Nominatim(user_agent="tsp_solver")
    location = geolocator.geocode(city)
    if location:
        return (location.latitude, location.longitude)
    else:
        raise ValueError(f"Coordinates for city {city} not found")

# Example usage
cities_names = ["Thrissur", "Hyderabad", "Mumbai", "Delhi", "Hyderabad"]
cities_coords = [(city, get_coordinates(city)) for city in cities_names]

route, distance = travelling_salesman(cities_coords)
route_with_names = [city[0] for city in route]

print("Shortest route:", route_with_names)
print("Minimum distance (km):", distance)
