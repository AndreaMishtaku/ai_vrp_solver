prompt_template = """

Solve this Vehicle Routing Problem (VRP) when a request with demands that is  the quantity that needs to be delivered to each node is given as below:
{demands}
  - **Node**: The name of the node where the demand is required.
  - **Demand**: The quantity of goods to be delivered to the corresponding node.

The information you need for solving the problem:
List of nodes:
{nodes}
 - **Id**: The unique identifier for each node.
  - **Name**: Descriptive identifier.
  - **Latitude and longitude**: Coordinates .

List of depos that will supply the node:
{depos}
  - **Id**: The unique identifier for the depot, which will be the first and last node in every route.
  - **Name**: Descriptive identifier of the depot.
  - **Latitude and longitude**: Coordinates.
  - **Capacity**: The maximum load that can be handled by the depot.

List of edges that keeps the distance between two nodes:
{edges}
  - **Start_Node_Id**: The id of the node where the edge begins.
  - **End_Node_Id**: The id of the node where the edge ends.
  - **Distance**: The distance between  nodes .

List of vehicles that have a specific capacity and a unique identifier:
{vehicles}
  - **Plate**: The license plate of the vehicle, which serves as its identifier.
  - **Capacity**: The maximum load the vehicle can carry (important for ensuring the vehicle’s route stays within capacity limits).


Using the provided data, your task is to generate the most efficient set of routes for the available vehicles. Each route must start and end at the depot, satisfy all node demands, and ensure that no vehicle exceeds its capacity.
- **Route Optimization**: Minimize the total distance traveled by all vehicles combined.
- **Constraints**: Ensure that each vehicle’s load does not exceed its capacity and that all demands are met.
- **Response**: Ensure that response to be a json with this schema.
    ```
    {schema}
    ```
"""
