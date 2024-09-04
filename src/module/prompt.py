prompt_template = """

Solve this Vehicle Routing Problem (VRP) given the following details:
**Demands**:
{demands}
  - **Node**: The name of the node where the demand is required.
  - **Demand**: The quantity of goods to be delivered to the corresponding node.

The information you need for solving the problem:
List of locations:
{locations}
  - **Id**: The unique identifier for the location
  - **Name**: Descriptive identifier. (For example name of the city)
  - **Latitude and longitude**: Coordinates.
  - **Capacity**: Only for depot attribute which specifies maximum quantity a depo can handle.

List of edges that keeps the distance between two nodes:
{edges}
  - **Start Node**: The id of the node where the edge begins.
  - **End Node **: The id of the node where the edge ends.
  - **Distance**: The distance between  nodes .

List of vehicles that have a specific capacity and a unique identifier:
{vehicles}
  - **Plate**: The license plate of the vehicle, which serves as its identifier.
  - **Capacity**: The maximum load the vehicle can carry (important for ensuring the vehicle’s route stays within capacity limits).

### Task
Using the provided data, your objective is to generate the most efficient set of routes for the available vehicles. Each route must:
- Start and end at a designated depot.
- Satisfy all node demands.
- Ensure no vehicle exceeds its capacity.


### Response
Ensure that response to be a json with this schema.
    ```
    {schema}
    ```
"""
