prompt_template = """

Solve this Vehicle Routing Problem (VRP) given the following details:
The information you need for solving the problem:

### List of locations
  - **Id**: The unique identifier for the location
  - **Name**: Descriptive identifier. (For example name of the city)
  - **Latitude and longitude**: Coordinates.
  - **Capacity**: Only for depot attribute which specifies maximum quantity a depo can handle.
  - **Demand**: Required quantity from a normal node.

Info with the indexes that locations represent in the distance matrix and location details:
Format ('Node'|'Depo') (id): (name) with ('demand'|'capacity') integer
{locations}

### Distances between locacions
- Format (start_node_id) to (end_node_id) : (distance)
{distances}


### Vehicles
  - **Plate**: The license plate of the vehicle, which serves as its identifier.
  - **Capacity**: The maximum load the vehicle can carry (important for ensuring the vehicle’s route stays within capacity limits).

Info about each vehicle and its depot:
{vehicle_depo}

### Task
Using the provided data, your objective is to generate the most efficient set of routes for the available vehicles. Each route must:
- Start and end at a designated depot.
- Satisfy all node demands.
- Ensure no vehicle exceeds its capacity.
- Take the shortest path possible by taking into consideration vehicle capacity and node demand.

### Response
Dont give any extra explanation about the problem, answer directly with json output.
Ensure that response to be a json with this schema.
    ```
    {schema}
    ```
"""
