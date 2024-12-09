import mdp
import testing_environments as te
from helper_functions import *
import pickle


# model setup ==========================
def set_ore_state(mdp_model):
	names = [
		'coal',
		'iron',
		'gold',
		'diamond'
	]

	for name in names:
		n = mdp_model.get_node(name)
		n.add_action('mine', 0.01, 2)
		n.add_action('leave', 0.01, -1)
		n.add_action('pickup', 0.01, 3)
		n.balance_probabilities()

def set_water_and_lava_states(mdp_model):
	names = [
		'water',
		'lava'
	]

	for name in names:
		n = mdp_model.get_node(name)
		n.add_action('block', 0.01, 2)
		n.add_action('leave', 0.01, -1)
		n.balance_probabilities()

def set_empty_state(mdp_model):
	state_data = [
		['coal', 1],
		['iron', 2],
		['gold', 1],
		['diamond', 3],
		['water', 0],
		['lava', 0]
	]


	n = mdp_model.get_node('empty')
	for data in state_data:
		n.add_action('move_to_' + data[0], 0.01, data[1])
		n.balance_probabilities()

def create_mining_model():
	names = [
		'empty',
		'coal',
		'iron',
		'gold',
		'diamond',
		'lava',
		'water'
		]
	model = mdp.create_base_model(names)

	for name in names:
		node = model.get_node(name)
		node.add_action('wait', 0.01, -1)
		node.add_action('place_torch', 0.01, 2)
		node.add_action('craft', 0.01, 0)
		node.add_action('maintain_player', 0.01, 1)
		node.add_action('harvest_trees', 0.01, 1)

	set_ore_state(model)
	set_water_and_lava_states(model)
	set_empty_state(model)

	return model

# ======================================

# crafting =============================
def craft_action_logic(inventory, action, counts):
	craft_stick = action == 'stick' and can_craft_sticks(counts[1])
	craft_pickaxe = action == 'pickaxe' and can_craft_pickaxe(counts)

	if craft_pickaxe:
		inventory.remove_from_inventory(('wood',3))
		inventory.remove_from_inventory(('sticks',2))
		inventory.add_to_inventory(('axe', 1))
		return True
	if craft_stick:
		inventory.remove_from_inventory(('wood',2))
		inventory.add_to_inventory(('sticks', 4))
		return True
	return False

# ======================================

def is_change_action(model, action):
	action = action.split('_')
	state = action[-1]
	action = action[0]

	match action:
		case 'leave':
			model.move_to_state('empty')
		case 'move':
			model.move_to_state(state)
		case 'block':
			model.move_to_state('empty')

def train_model(model, inventory, epochs, verbose):
	reward_data = []
	for i in range(1, epochs+1):
		if verbose: 
			print(f'Epoch {i}')
			model.print_current_information()

		# get count/physical data
		wood_count = get_wood_count(inventory)
		stick_count = get_stick_count(inventory)
		counts = (wood_count,stick_count)


		# get states & actions
		curr_state = model.get_current_node().get_state_name()
		action, reward = model.take_action()
		if verbose: print('Taken action:', action, '\n')

		if is_change_action(model, action): continue
		
		# special actions
		if action == 'craft':
			x = craft_action_logic(inventory,action,counts)
			if x: continue	# if craft chosen and 
							# model doesn't have
							# material, restart loop
		if action == 'pickup':
			player_inventory.add_to_inventory((curr_state, 1))



		model.add_to_reward(reward)
		reward_data.append(model.return_current_rewards())
		# value iteration policy


	return model, reward_data


if __name__ == '__main__':
	m = create_mining_model()
	player_inventory = te.Inventory()

	#m.print_action_space()
	m, rewards = train_model(m, player_inventory, 100, True)

	#with open('base_rewards\\mining.list', 'wb') as f:
	#	pickle.dump(rewards, f)
