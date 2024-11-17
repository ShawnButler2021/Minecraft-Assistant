from mdp import MDP, Node
from testing_environments import PhysicalEnvironment


def base_model():
	model = MDP()
	names = [
		'coal',
		'iron',
		'gold',
		'diamond',
		'lava',
		'water',
		'empty'
		]

	nodes = [Node(name) for name in names]

	for node in nodes:
		node.add_action('wait', 0.01, -1)
		node.add_action('place_torch', 0.01, 2)
		node.add_action('craft', 0.01, 0)
		node.add_action('maintain_player', 0.01, 1)
		node.add_action('harvest_trees', 0.01, 1)
		node.balance_probabilities()
		model.add_node(node)

	return model

def ore_actions(mdp):
	names = [
		'coal',
		'iron',
		'gold',
		'diamond'
	]

	for name in names:
		n = mdp.get_node(name)
		n.add_action('mine', 0.01, 2)
		n.add_action('leave', 0.01, -1)
		n.add_action('pickup', 0.01, 3)
		n.balance_probabilities()
		mdp.replace_node(name, n)

def water_and_lava_actions(mdp):
	names = [
		'water',
		'lava'
	]

	for name in names:
		n = mdp.get_node(name)
		n.add_action('block', 0.01, 2)
		n.add_action('leave', 0.01, -1)
		n.balance_probabilities()
		mdp.replace_node(name, n)
	

def empty_actions(mdp):
	state_data = [
		['coal', 1],
		['iron', 2],
		['gold', 1],
		['diamond', 3],
		['water', 0],
		['lava', 0]
	]


	n = mdp.get_node('empty')
	for data in state_data:
		n.add_action('find '+ data[0], 0.01, data[1])
		n.add_action('move to ' + data[0], 0.01, data[1])
	n.balance_probabilities()
	mdp.replace_node(data, n)




print('Starting...')
model = base_model()
ore_actions(model)
water_and_lava_actions(model)
empty_actions(model)

model.print_action_space()