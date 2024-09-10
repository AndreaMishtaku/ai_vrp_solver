prompt_template = """
Solve this Vehicle Routing Problem (VRP) given the following details:
Locations:
{locations}

Distances between nodes and depots which is the same in both directions:
{distances}

Vehicles and Depots:
{vehicle_depo}

Based on the above data, generate the most efficient routes that minimize the total distance traveled while meeting the demands at each location. Return the result in the specified JSON format.

"""
