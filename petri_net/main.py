from collections import deque

class Place:
    def __init__(self, id, tokens):
        self.id = id
        self.tokens = tokens

class Transition:
    def __init__(self, id, input_places, output_places):
        self.id = id
        self.input_places = input_places
        self.output_places = output_places

class Flow:
    def __init__(self, input_place_id, output_place_id, weight):
        self.input_place_id = input_place_id
        self.output_place_id = output_place_id
        self.weight = weight
def initialize_petri_net(places, transitions, flows, initial_marks):
    # Initialize the places with the given initial marks
    for i in range(len(places)):
        places[i].tokens = initial_marks[i]

def can_fire_transition(transition, places):
    # Check if the input places have enough tokens and the output places have room for more tokens
    for input_place_id in transition.input_places:
        if places[input_place_id].tokens < 1:
            return False
    for output_place_id in transition.output_places:
        if places[output_place_id].tokens >= 1:
            return False
    return True

def fire_transition(transition, places):
    # Remove tokens from input places and add tokens to output places
    for input_place_id in transition.input_places:
        places[input_place_id].tokens -= 1
    for output_place_id in transition.output_places:
        places[output_place_id].tokens += 1

def generate_reachability_graph(places, transitions, flows, initial_marks):
    state_queue = deque()
    visited_states = set()

    # Initialize the queue with the initial state
    initial_state = [place.tokens for place in places]
    state_queue.append(initial_state)
    visited_states.add(tuple(initial_state))

    while len(state_queue) > 0:
        current_state = state_queue.popleft()

        # Generate all possible successor states by firing enabled transitions
        for transition in transitions:
            if can_fire_transition(transition, [Place(place.id, place.tokens) for place in places]):
                successor_state = current_state.copy()
                fire_transition(transition, [Place(place.id, place.tokens) for place in places])
                successor_state = [place.tokens for place in places]

                # Enqueue the successor state if it has not been visited before
                if tuple(successor_state) not in visited_states:
                    state_queue.append(successor_state)
                    visited_states.add(tuple(successor_state))

    return visited_states

def is_sound(places, transitions, flows, initial_marks):
    reachability_graph = generate_reachability_graph(places, transitions, flows, initial_marks)
    return len(reachability_graph) < float('inf')

# Take user input for Petri net configuration
n_places = int(input("Enter the number of places: "))
places = []
for i in range(n_places):
    tokens = int(input(f"Enter the number of tokens in place {i}: "))
    places.append(Place(i, tokens))

n_transitions = int(input("Enter the number of transitions: "))
transitions = []
for i in range(n_transitions):
    input_places = list(map(int, input(f"Enter the input places for transition {i} (comma separated): ").split(',')))
    output_places = list(map(int, input(f"Enter the output places for transition {i} (comma separated): ").split(',')))
    transitions.append(Transition(i, input_places, output_places))

n_flows = int(input("Enter the number of flows: "))
flows = []
for i in range(n_flows):
    input_place_id, output_place_id, weight = map(int, input(f"Enter the input place, output place and weight for flow {i} (comma separated): ").split(','))
    flows.append(Flow(input_place_id, output_place_id, weight))

initial_marks = list(map(int, input("Enter the initial marks for each place (comma separated): ").split(',')))

# Initialize the Petri net with the given configuration
initialize_petri_net(places, transitions, flows, initial_marks)

# Check if the Petri net is sound
if is_sound(places, transitions, flows, initial_marks):
    print("Petri net is sound")
else:
    print("Petri net is not sound")

# Generate the reachability graph for the Petri net
reachability_graph = generate_reachability_graph(places, transitions, flows, initial_marks)
print("Reachability graph:")
for state in reachability_graph:
    print(state)