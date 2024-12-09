from random import choices

class Node:
	def __init__(self, name):
		self.__state_name = name
		self.__possible_actions = {}

	def print_actions(self):
		i = 1
		for action, probability in self.__possible_actions.items():
			print(f'{i}.', action, probability)
			i+=1

	def balance_probabilities(self):
		general_probability = round(round(100.00 / len(self.__possible_actions), 2) / 100, 2)
		#remainder = 100 - (general_probability * len(self.__possible_actions))

		for key in self.__possible_actions:
			self.__possible_actions[key][0] = general_probability

	def get_state_name(self):
		return self.__state_name

	def get_an_action(self):
		probability_weights = [value[0] for key, value in self.__possible_actions.items()]
		next_action = choices([key for key in self.__possible_actions], weights=probability_weights)[0]

		return next_action, self.__possible_actions[next_action][1]

	def add_action(self, action_name, probability_value, reward_value):
		self.__possible_actions[action_name] = [probability_value, reward_value]

	def remove_action(self, action_name):
		del self.__possible_actions[action_name]

	def return_possibilities(self):
		return self.__possible_actions

# =======================

class MDP:
	def __init__(self):
		self.__node_list = []
		self.__head_node = None
		self.__current_node = None
		self.__cummulative_reward = 0

	# print series
	def print_state_space(self):
		for node in self.__node_list:
			print(node.get_state_name())

	def print_action_space(self):
		for index, node in enumerate(self.__node_list):
			print()
			print(f'{index+1})', node.get_state_name())
			print('===========')
			node.print_actions()
			print('===========')

	def print_node_list(self):
		print('| ', end='')
		[print(node.get_state_name(), end=' | ') for node in self.__node_list]
		print()

	def print_current_information(self):
		print('Current Node:', self.__current_node.get_state_name())
		print('Cummulative Reward:', self.__cummulative_reward)



	# node management series
	def reset_mdp(self):
		self.__current_node = self.__head_node
		self.__cummulative_reward = 0

	def add_node(self, node):
		self.__node_list.append(node)
		if self.get_num_of_nodes() == 1:
			self.__head_node = self.__node_list[0]
			self.__current_node = self.__head_node

	def remove_node(self, state_name):
		for index, node in enumerate(self.__node_list):
			if node.get_state_name() != state_name: continue

			self.__node_list.pop(index)
			if index == 0:
				self.__head_node = self.__node_list[0]
				self.__current_node = self.__head_node
			return

	def replace_node(self, state_name, new_node):	# used to edit node, create copy with changes & replace
		for index, node in enumerate(self.__node_list):
			if node.get_state_name() != state_name: continue 
			self.__node_list[index] = new_node
			return 
		
	def get_node(self, state_name):
		for node in self.__node_list:
			if node.get_state_name() == state_name: return node
		return None

	def get_current_node(self):
		return self.__current_node

	def get_num_of_nodes(self):
		return len(self.__node_list)


	# movement series
	def add_to_reward(self, reward_value):
		self.__cummulative_reward += reward_value

	def take_action(self):
		return self.__current_node.get_an_action()

	def move_to_state(self, state_name):
		for node in self.__node_list:
			if node.get_state_name() == state_name: self.__current_node = node

	def return_current_rewards(self):
		return self.__cummulative_reward



def create_base_model(state_names):
	if type(state_names) != list: raise TypeError('create_model: state_names must be a list.')
	if not state_names: raise ValueError('create_model: state_names can not be empty.')

	model = MDP()
	[model.add_node(Node(name)) for name in state_names]


	return model





if __name__ == '__main__':
	model = create_model(['get'])