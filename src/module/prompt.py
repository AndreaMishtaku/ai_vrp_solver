from langchain.prompts import PromptTemplate

prompt_template = """
Given the following input in JSON format:

Input JSON:
{request_payload}

The input JSON will always have the following structure:
{
    "demands": [
        {
        "node": "string",    # The name of the node (e.g., a city)
        "demand": integer    # The demand value associated with the node
        }
    ],
    "depo_vehicle": [
        {
        "depo": "string",    # The name of the depot
        "plate": "string"    # The vehicle's license plate number
        }
    ] 
}

Please process this input and return the result in the following JSON format:

Desired JSON Format:
{
    "routes":[
        {
        "plate": "string",      # Plate of the vehicle
        "route": Array<int>,    # Array with id of nodes visited,
        "load":  integer,       # Total load transported from the vehicle 
        "distance": integer,    # Distance covered from vehicle through nodes specified in route array
        }
    ],
    "total_distance": integer,  # Sum of distances in routes array
    "total_load": integer,    # Sum of loads in routes array

}

Your JSON Response:
"""




prompt = PromptTemplate(
    input_variables=["request_payload"],
    template=prompt_template
)