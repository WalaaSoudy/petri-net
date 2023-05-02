'''
This code defines a class called PetriNet that represents a Petri Net,
which is a type of directed graph used for modeling concurrent systems.
The class has the following attributes: places (a list of strings representing the places in the Petri Net), transitions
(a list of strings representing the transitions in the Petri Net), flows (a list of tuples representing the arcs in the Petri Net)
,and initial_marking (a dictionary representing the initial marking of the Petri Net).

The PetriNet class also has two methods: is_sound and generate_reachability_graph.
The is_sound method checks if the Petri Net is sound by verifying that all transitions have at least one input place.
The generate_reachability_graph method generates the reachability graph of the Petri Net,
which is a directed graph representing all possible states of the Petri Net.

The code prompts the user to input the Petri Net details such as the places,
transitions, flows, and initial marking, and creates a PetriNet object. It then checks if the Petri Net is sound
and generates the reachability graph. If the user chooses to draw the reachability graph,
it uses the NetworkX library and Matplotlib to visualize the graph. If the user chooses not to draw the graph,
it prints the reachability set for each node.

To run the code,
save it as a Python file (e.g., petri_net.py) and run it using a Python interpreter.
The interpreter will prompt the user to input the Petri Net details,
and the code will generate and display the reachability graph if the user chooses to do so.
'''

import networkx as nx
import matplotlib.pyplot as plt

class PetriNet:
    def __init__(self, places, transitions, flows, initial_marking):
        self.places = places
        self.transitions = transitions
        self.flows = flows
        self.initial_marking = initial_marking

    def is_sound(self):
        inputs = {}
        outputs = {}

        # Iterate over all flows and populate inputs and outputs
        for flow in self.flows:
            if flow[1] not in inputs:
                inputs[flow[1]] = set()
            inputs[flow[1]].add(flow[0])

            if flow[0] not in outputs:
                outputs[flow[0]] = set()
            outputs[flow[0]].add(flow[1])

        # Check if there are any transitions that have no inputs
        for t in self.transitions:
            if t not in inputs:
                return False

        return True

    def generate_reachability_graph(self):
        # We will use NetworkX library to generate the reachability graph.
        G = nx.DiGraph()
        for place in self.places:
            G.add_node(place, label=place)
        for transition in self.transitions:
            G.add_node(transition, label=transition)
        for flow in self.flows:
            G.add_edge(flow[0], flow[1], weight=1)
        # Compute the reachability set for each node using depth-first search.
        for node in G.nodes:
            reachability_set = set()
            self.dfs(node, reachability_set, G)
            G.nodes[node]['reachability_set'] = reachability_set
        return G

    def dfs(self, node, reachability_set, G):
        reachability_set.add(node)
        for neighbor in G.neighbors(node):
            if neighbor not in reachability_set:
                self.dfs(neighbor, reachability_set, G)

# Take input for Petri Net
print("Please input the Petri Net:")
places = input("Places: ").split(",")
transitions = input("Transitions: ").split(",")
flows_input = input("Flows (format: place1->transition1,transition1->place2,...): ")
flows = []
for flow in flows_input.split(","):
    flow_parts = flow.split("->")
    flows.append((flow_parts[0], flow_parts[1]))
print(flows)  # Debugging line
initial_marking_input = input("Initial marking (format: place1=marking1,place2=marking2,...): ")
initial_marking = {}
for marking in initial_marking_input.split(","):
    marking_parts = marking.split("=")
    initial_marking[marking_parts[0]] = int(marking_parts[1])

# Create Petri net object
pn = PetriNet(places, transitions, flows, initial_marking)

# Check soundness
if pn.is_sound():
    print("Petri is sound")
else:
    print("Petri Net is not sound.")


G = pn.generate_reachability_graph()

# Draw or print reachability graph
if input("Do you want to draw the reachability graph? (y/n) ") == "y":
    pos = nx.spring_layout(G)
    node_labels = nx.get_node_attributes(G, 'label')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_nodes(G, pos, nodelist=G.nodes(), node_color='r')
    nx.draw_networkx_labels(G, pos, labels=node_labels)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='b')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.show()
else:
    for node in G.nodes:
        print(node, G.nodes[node]['reachability_set'])


