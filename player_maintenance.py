import mdp
import testing_environments as te
from helper_functions import *
import pickle



# model setup ==========================
def set_health_state(mdp_model):
	work_node = mdp_model.get_node('health')
	work_node.add_action('eat', 0.25, 2)
	work_node.add_action('leave', 0.25, 0)
	work_node.balance_probabilities()

def set_hunger_state(mdp_model):
	work_node = mdp_model.get_node('hunger')
	work_node.add_action('eat', 0.01, 2)
	work_node.add_action('leave', 0.01, 1)
	work_node.balance_probabilities()

def set_armor_state(mdp_model):
	work_node = mdp_model.get_node('armor')
	work_node.add_action('equip_helmet', 0.01, 1)
	work_node.add_action('dequip_helmet', 0.01, -1)
	work_node.add_action('equip_chestplate', 0.01, 1)
	work_node.add_action('dequip_chestplate', 0.01, -1)
	work_node.add_action('equip_leggings', 0.01, 1)
	work_node.add_action('dequip_leggings', 0.01, -1)
	work_node.add_action('equip_boots', 0.01, 1)
	work_node.add_action('dequip_boots', 0.01, -1)
	work_node.add_action('leave', 0.01, 1)
	work_node.balance_probabilities()

def set_wait_state(mdp_model):
	work_node = mdp_model.get_node('wait')
	work_node.add_action('move_to_health', 0.5, 1)
	work_node.add_action('move_to_hunger', 0.5, 1)
	work_node.add_action('move_to_armor', 0.5, 1)
	work_node.add_action('move_to_inventory', 0.5, 1)
	work_node.balance_probabilities()

def creating_player_maintenance_model():
	names = [
		'health',
		'hunger',
		'armor',
		'wait'
		]
	model = mdp.create_base_model(names)
	set_wait_state(model)
	set_health_state(model)
	set_hunger_state(model)
	set_armor_state(model)

	return model
# ======================================

# state logic ==========================

def health_state_logic(player_status):
	health = player_status.get_health_levels()
	hunger = player_status.get_hunger_levels()
	
	if 0 < health < 20 and can_eat(): 
		player_status.eat(1)
		player_status.heal(1)
		return True
	return False

def armor_state_logic(inventory, action):
	action = action.split('_')
	action, armor_piece = action[0], action[-1]

	if action == 'equip' and can_equip(inventory.armor, armor_piece):
		inventory.armor[armor_piece] = True
		return True
	if action == 'dequip' and can_equip(inventory.armor, armor_piece):
		inventory.armor[armor_piece] = False
		return True

	return False

def is_change_state_action(current_action, model):
	if current_action == 'leave': 
		model.move_to_state('wait')
		return True
	if current_action[:4] == 'move': 
		model.move_to_state(current_action.split('_')[-1])
		return True
	return False

# ======================================

def train_model(model, inventory, player_status, epochs, verbose):
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
		match action:
			case 'health':
				health_state_logic(player_status)
			case 'hunger':
				if can_eat(player_status.get_hunger_levels()):
					player_status.eat(1)
			case 'armor':
				armor_state_logic(inventory, action)
		


		model.add_to_reward(reward)
		reward_data.append(model.return_current_rewards())
		# value iteration policy


		# starving character per iteration
		player_status.starve(0.5)

	return model, reward_data









if __name__ == '__main__':
	m = creating_player_maintenance_model()
	ps = te.PlayerStatus()
	pi = te.Inventory()

	#m.print_action_space()
	m, rewards = train_model(m, pi, ps, 100, True)

	#with open('base_rewards\\player_maintenance.list', 'wb') as f:
	#	pickle.dump(rewards, f)

