import mdp
import testing_environments as te
from helper_functions import *
import pickle
import numpy as np
import random




# model setup ==========================
def set_get_state(mdp_model):
	work_node = mdp_model.get_node('get')
	work_node.add_action('wood', 0.4, 1)
	work_node.add_action('ore', 0.4, 1)
	work_node.add_action('leave', 0.2, 1)

	transition_probabilities = {
		'wood': [0.4, 1, 'get'],
		'ore': [0.4, 1, 'get'],
		'leave': [0.2, 1, 'wait']

	}
	return transition_probabilities

def set_craft_state(mdp_model):
	work_node = mdp_model.get_node('craft')
	work_node.add_action('axe', 0.40, 5)
	work_node.add_action('pickaxe', 0.40, 5)
	work_node.add_action('sticks', 0.15, 1)
	work_node.add_action('leave', 0.05, 1)

	transition_probabilities = {
		'axe': [0.4, 5, 'craft'],
		'pickaxe': [0.4, 5, 'craft'],
		'sticks': [0.15, 1, 'craft'],
		'leave': [0.05, 1, 'wait']

	}
	return transition_probabilities

def set_wait_state(mdp_model):
	work_node = mdp_model.get_node('wait')
	work_node.add_action('move_to_craft', 0.5, 1)
	work_node.add_action('move_to_get', 0.5, 1)
	work_node.add_action('move_to_eat', 0.5, 1)
	work_node.balance_probabilities()

	transition_probabilities = {
		'move_to_craft': [0.33, 1, 'craft'],
		'move_to_get': [0.33, 1, 'get'],
		'move_to_eat': [0.33, 1, 'eat']

	}
	return transition_probabilities

def set_eat_state(mdp_model):
	work_node = mdp_model.get_node('eat')
	work_node.add_action('eat_food', 0.8, 1)
	work_node.add_action('leave', 0.2, 1)

	transition_probabilities = {
		'eat_food': [0.8, 1, 'eat'],
		'leave': [0.2, 1, 'wait']

	}
	return transition_probabilities

def create_crafting_model():
	names = [
		'craft',
		'get',
		'eat',
		'wait'
		]
	model = mdp.create_base_model(names)

	transition_probabilities = {}
	transition_probabilities['get'] = set_get_state(model)
	transition_probabilities['craft'] = set_craft_state(model)
	transition_probabilities['wait'] = set_wait_state(model)
	transition_probabilities['eat'] = set_eat_state(model)

	return model, transition_probabilities

# ======================================

# crafting =============================
def craft_state_logic(inventory, action, counts):
	craft_stick = action == 'stick' and can_craft_sticks(counts[1])
	craft_axe = action == 'axe' and can_craft_axe(counts)
	craft_pickaxe = action == 'pickaxe' and can_craft_pickaxe(counts)

	if craft_axe:
		inventory.remove_from_inventory(('wood',3))
		inventory.remove_from_inventory(('sticks',2))
		inventory.add_to_inventory(('axe', 1))
		return True
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
			x = craft_state_logic(inventory,action,counts)
			if x: continue	# if craft chosen and 
							# model doesn't have
							# material, restart loop
		if curr_state == 'get':
			if action == 'wood': player_inventory.add_to_inventory(('wood', 1))
			if action == 'ore': player_inventory.add_to_inventory(('iron', 1))

		model.add_to_reward(reward)
		reward_data.append(model.return_current_rewards())
		# value iteration policy


	return model, reward_data

def policy_iteration(transition_probabilities):
	states = [
		'craft',
		'get',
		'eat',
		'wait'
		]

	policy = {
		s: list(transition_probabilities[s].keys())[0] for s in states
	}
	V = {s: 0 for s in states}
	gamma = 1

	while True:
		while True:
			delta = 0

			for s in states:
				new_value = sum([
					transition_probabilities[s][policy[s]][0] * (transition_probabilities[s][policy[s]][1] + gamma * V[s]) for _ in states
					])
				
				delta = max(delta, abs(V[s] - new_value))
				V[s] = new_value

			if delta < 1**-6: break


		policy_stable = True
		
		for s in states:
			old_action = policy[s]

			best_action = None
			best_value = float('-inf')

			for a in transition_probabilities:
				print(a, transition_probabilities[a])
				print()
				action_value = sum([
					transition_probabilities[s][policy[s]][0] * (transition_probabilities[s][policy[s]][1] + gamma * V[s]) for _ in states
				])
				if action_value > best_value:
					best_value = action_value
					best_action = a

			policy[s] = best_action
			if old_action != best_action:
				policy_stable = False

		if policy_stable: break



	




if __name__ == '__main__':
	m, tp = create_crafting_model()
	player_inventory = te.Inventory()

	#m.print_action_space()
	m, rewards = train_model(m, player_inventory, 100, False)

	policy_iteration(tp)
	#with open('base_rewards\\crafting.list', 'wb') as f:
	#	pickle.dump(rewards, f)


