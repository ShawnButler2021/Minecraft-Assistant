import mdp
import testing_environments as te
from helper_functions import *
import pickle


# model setup ==========================
def set_get_state(mdp_model):
	work_node = mdp_model.get_node('get')
	work_node.add_action('wood', 0.6, 1)
	work_node.add_action('leave', 0.4, 1)

def set_craft_state(mdp_model):
	work_node = mdp_model.get_node('craft')
	work_node.add_action('axe', 0.60, 5)
	work_node.add_action('sticks', 0.20, 1)
	work_node.add_action('leave', 0.20, 1)

def set_wait_state(mdp_model):
	work_node = mdp_model.get_node('wait')
	work_node.add_action('move_to_craft', 0.5, 1)
	work_node.add_action('move_to_get', 0.5, 1)
	work_node.balance_probabilities()

def create_tree_harvesting_model():
	state_names = [
		'wait',
		'craft',
		'get'
	]
	model = mdp.create_base_model(state_names)
	set_get_state(model)
	set_craft_state(model)
	set_wait_state(model)

	return model

# ======================================

# crafting =============================
def craft_state_logic(inventory, action, counts):
	craft_stick = action == 'stick' and can_craft_sticks(counts[1])
	craft_axe = action == 'axe' and can_craft_axe(counts)

	if craft_axe:
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
def is_change_state_action(current_action, model):
	if current_action == 'leave': 
		model.move_to_state('wait')
		return True
	if current_action[:4] == 'move': 
		model.move_to_state(current_action.split('_')[-1])
		return True
	return False


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

		if is_change_state_action(action, model): continue
		
		# special actions
		if action == 'craft':
			x = craft_action_logic(inventory,action,counts)
			if x: continue	# if craft chosen and 
							# model doesn't have
							# material, restart loop
		if action == 'get':
			player_inventory.add_to_inventory(('wood', 1))


		model.add_to_reward(reward)
		reward_data.append(model.return_current_rewards())
		# value iteration policy


	return model, reward_data




if __name__ == '__main__':
	m = create_tree_harvesting_model()
	player_inventory = te.Inventory()

	m.print_action_space()
	m, rewards = train_model(m, player_inventory, 100, True)

	#with open('base_rewards\\tree_harvesting.list', 'wb') as f:
	#	pickle.dump(rewards, f)