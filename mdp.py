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
		general_probability = round(100.00 / len(self.__possible_actions), 2)
		#remainder = 100 - (general_probability * len(self.__possible_actions))

		for key in self.__possible_actions:
			self.__possible_actions[key][0] = general_probability

	def get_state_name(self):
		return self.__state_name

	def get_next_move(self):
		probability_weights = [value[0] for key, value in self.__possible_actions.items()]
		next_action = choices([key for key in self.__possible_actions], weights=probability_weights)[0]

		return next_action, self.__possible_actions[next_action][1]

	def add_action(self, action_name, probability_value, reward_value):
		self.__possible_actions[action_name] = [probability_value, reward_value]

	def remove_action(self, action_name):
		del self.__possible_actions[action_name]

class MDP:
	def __init__(self):
		self.__node_list = []
		self.__head_node = None
		self.__current_node = None
		self.__cummulative_reward = 0

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

	def reset_mdp(self):
		self.__current_node = self.__head_node
		self.__cummulative_reward = 0


	# node management
	def add_node(self, node):
		self.__node_list.append(node)

	def remove_node(self, state_name):
		for index, node in enumerate(self.__node_list):
			if node.get_state_name() != state_name: continue

			self.__node_list.pop(index)
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



	def get_mdp_size(self):
		return len(self.__node_list)

	def print_current_information(self):
		print()
		print('Current Node:', self.__current_node.get_state_name())
		print('Cummulative Reward:', self.__cummulative_reward)
		print()

	def take_next_step(self):
		next_step, reward_change = self.__current_node.get_next_move()
		self.__cummulative_reward += reward_change

		for index, node in enumerate(self.__node_list):
			if node.get_state_name() == state_name: self.__current_node = node


