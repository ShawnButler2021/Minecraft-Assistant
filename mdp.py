class Node:
	def __init__(self, name):
		self.__state_name = name
		self.__possible_actions = {}

	def print_actions(self):
		for action, probability in self.possible_actions.items():
			print(action, probability)

	def get_state_name(self):
		return self.__state_name

	def get_next_move(self):
		pass

	def add_action(self, action_name, probability_value):
		self.__possible_actions[action_name] = probability_value

	def remove_action(self, action_name):
		del self.__possible_actions[action_name]

class MDP:
	def __init__(self):
		self.__node_list = []
		self.__head_node = None
		self.__current_node = None

	def print_state_space(self):
		for node in self.__node_list:
			print(node.get_state_name())

	def print_action_space(self):
		for node in self.__node_list:
			print(node.get_state_name())
			node.print_actions()

	def reset_mdp(self):
		self.__current_node = self.__head_node

	def add_node(self, node):
		self.__node_list.append(node)

	def remove_node(self, state_name):
		for index, node in enumerate(self.__node_list):
			if node.get_state_name() == state_name: self.__node_list.pop(index)

