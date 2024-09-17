def generate_response_from_edges(edges, nodes, node_id):
    responses = []
    # Create a dictionary for quick lookup of nodes by their id
    nodes_dict = {node['id'].strip(): node for node in nodes}
    print("nodes_dict>>>>>>", nodes_dict)

    for edge in edges:
        start_node_id = edge.get("start").strip()
        target_node_id = edge.get("to").strip()

        print(f"Checking edge from {start_node_id} to {target_node_id}")

        if start_node_id == node_id.strip():
            print(f"Matched start_node_id: {start_node_id} with node_id: {node_id}")

            # Get the data of the target node
            target_node = nodes_dict.get(target_node_id)
            print(f"target_node_id>>>> {target_node_id}")
            print(f"target_node>>>> {target_node}")

            if target_node:
                responses.append(target_node['data'].get('label', 'No data available'))
            else:
                print(f"Node with ID {target_node_id} not found in nodes_dict.")

    return responses if responses else ["Default response"]


def convert_flow_to_intents(chatbot_flow_data):
    nodes = chatbot_flow_data.get("nodes", [])
    edges = chatbot_flow_data.get("edges", [])

    # Ensure nodes are properly included in the dictionary
    nodes_dict = {node['id'].strip(): node for node in nodes}
    print("nodes_dict for intents>>>>>>", nodes_dict)

    intents = []
    for node in nodes:
        node_id = node.get("id").strip()
        patterns = [node['data'].get('label', '')]

        # Generate responses based on the edges
        responses = generate_response_from_edges(edges, nodes, node_id)

        intent = {
            "tag": node_id,
            "patterns": patterns,
            "responses": responses,
            "context_set": "",  # Can be adjusted based on your needs
        }
        intents.append(intent)

    return {"intents": intents}
