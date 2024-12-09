import mdp
import pickle
import random


# player series
class Inventory:
	def __init__(self):
		self.hotbar, self.__inventory, self.armor = self.inventory_frame()


	def inventory_frame(self):
		row = [ (-1,-1) for i in range(0,9) ]
		inventory = [ row.copy() for i in range(0,3) ]

		hotbar = []
		armor = {
			'helmet': None,
			'chestplate': None,
			'leggings': None,
			'boots': None
		}


		return hotbar, inventory, armor

	# inventory change series
	def add_to_inventory(self, item_data):
		# filtering bad inputs
		if type(item_data) != tuple:
			print('Item format: (string, positive integer)')
			return False
		elif type(item_data[0]) == str:
			print('Item format: (string, positive integer)')
			return False
		elif item_data[1] < 1 or type(item_data[1]) == int:
			print('Item format: (string, positive integer)')
			return False

		# adding to first free space
		for y, row in enumerate(self.__inventory):
			for x, item in enumerate(row):
				if item == (-1,-1): 
					self.__inventory[y][x] = item_data
					return True
		return False

	def remove_from_inventory(self, item_data):
		# filtering bad inputs
		if type(item_data) != type( () ):
			print('Item format: (string, positive integer)')
			return False
		elif type(item_data[0]) == str:
			print('Item format: (string, positive integer)')
			return False
		elif item_data[1] > 0 or type(item_data[1]) == int:
			print('Item format: (string, positive integer)')
			return False


		# removing first entry of item
		for y, row in enumerate(self.__inventory):
			for x, item in enumerate(row):
				if item[0] == item_data[0]: 
					self.__inventory[y][x][1] -= item_data[1]
					if self.__inventory[y][x][1] < 0: self.__inventory[y][x][1] = 0
					return True
		return False

	def search_inventory(self, item_name):
		# removing first entry of item
		for y, row in enumerate(self.__inventory):
			for x, item in enumerate(row):
				if item[0] == item_name: 
					return (x,y)
		return (-1,-1)

	def print_inventory(self, inventory_data):
		hotbar, inv, armor = inventory_data
		print('hotbar =>', hotbar)

		print('Armor =>')
		[print('\t', armor_type, '=>', state) for armor_type, state in armor.items()]
		
		print('Inventory =>')
		for row in inv:
			print('\t',row)

	def get_slot_data(self, coordinates):
		x, y = coordinates
		return self.__inventory[y][x]

class PlayerStatus:
	def __init__(self):
		self.__x, self.__y = 0,0
		self.__health = 20
		self.__armor_rating = 0
		self.__hunger = 20
		self.__inventory = Inventory()

	# coordinate series
	def get_coordinates(self):
		return (self.__x, self.__y)
	def move(self, x_change, y_change):
		# make sure to update PhysicalEnvironment with place_player
		self.__x += int(x_change)
		self.__y += int(y_change)


	# health series
	def get_health_level(self):
		return self.__health
	def heal(self, health_to_gain):
		self.__health += health_to_gain
		if self.__health > 20: self.__health = 20
	def damage(self, health_to_lose):
		self.__health -= health_to_lose

	# hunger series
	def get_hunger_level(self):
		return self.__hunger
	def eat(self, hunger_points_to_gain):
		self.__hunger += int(abs(hunger_points_to_gain))
		if self.__hunger > 20: self.__hunger = 20
	def starve(self, hunger_points_to_lose):
		self.__hunger -= int(abs(hunger_points_to_lose))
		if self.__hunger > 0: 
			self.__hunger = 0
			self.__health -= 1
	
	# armor series
	def get_armor_rating(self):
		return self.__armor_rating
	def add_armor(self, armor_points_to_gain):
		self.__armor_rating += int(abs(armor_points_to_gain))
		if self.__armor_rating > 24: self.__armor_rating = 24
	def remove_armor(self, armor_points_to_lose):
		self.__armor_rating -= int(abs(armor_points_to_lose))
		if self.__armor_rating < 0: self.__armor_rating = 0


# environment series
class CraftingEnvironment:
	def __init__(self):
		self.__inventory = Inventory()
		self.__crafting_slots = {f'slot{i}': None for i in range(1, 10)}
		self.__output_slot = None
		self.__recipes = {
	        ('log',): 'wood',
	        ('wood', 'wood', 'wood', 'wood'): 'crafting_table',
	        ('cobblestone', 'cobblestone', 'cobblestone', 'cobblestone', 'cobblestone', 'cobblestone', 'cobblestone', 'cobblestone'): 'furnace',
	        ('coal', 'stick'): 'torch',
	        ('wood', 'wood', 'wood' 'stick', 'stick'): 'wood pickaxe',
	        ('stone', 'stone', 'stone' 'stick', 'stick'): 'stone pickaxe',
	        ('iron_ingot', 'iron_ingot', 'iron_ingot' 'stick', 'stick'): 'iron pickaxe',
	        ('gold_ingot', 'gold_ingot', 'gold_ingot' 'stick', 'stick'): 'gold pickaxe',
	        ('diamond', 'diamond', 'diamond' 'stick', 'stick'): 'diamond pickaxe',
	        ('wood', 'stick', 'stick', 'plank'): 'axe',
	        ('iron_ingot', 'iron_ingot', 'iron_ingot'): 'iron_helmet',
	        ('iron_ingot', 'iron_ingot', 'iron_ingot', 'iron_ingot', 'iron_ingot', 'iron_ingot', 'iron_ingot'): 'iron_chestplate',
	        ('iron_ingot', 'iron_ingot', 'iron_ingot', 'iron_ingot', 'iron_ingot', 'iron_ingot'): 'iron_leggings',
	        ('iron_ingot', 'iron_ingot', 'iron_ingot', 'iron_ingot'): 'iron_boots',
	        ('gold_ingot', 'gold_ingot', 'gold_ingot'): 'gold_helmet',
	        ('gold_ingot', 'gold_ingot', 'gold_ingot', 'gold_ingot', 'gold_ingot', 'gold_ingot', 'gold_ingot'): 'gold_chestplate',
	        ('gold_ingot', 'gold_ingot', 'gold_ingot', 'gold_ingot', 'gold_ingot', 'gold_ingot'): 'gold_leggings',
	        ('gold_ingot', 'gold_ingot', 'gold_ingot', 'gold_ingot'): 'gold_boots',
	        ('diamond', 'diamond', 'diamond'): 'diamond_helmet',
	        ('diamond', 'diamond', 'diamond', 'diamond', 'diamond', 'diamond', 'diamond'): 'diamond_chestplate',
	        ('diamond', 'diamond', 'diamond', 'diamond', 'diamond', 'diamond'): 'diamond_leggings',
	        ('diamond', 'diamond', 'diamond', 'diamond'): 'diamond_boots',
	        ('wood', 'wood', 'wood', 'wood', 'wood', 'wood', 'wood', 'wood'): 'chest'
	    }

	def add_item_to_slot(self, slot, item_name):
		if type(item_name) != str: 
			print('item_name in add_item_to_slot must be string')
			return False
		if slot[:-1] != 'slot':
			slot = 'slot' + str(slot)
			

		if slot in self.__crafting_slots and self.__crafting_slots[slot] is None:
			self.__crafting_slots[slot] = item_name
			return True
		return False

	def craft(self):
		# get the items in the slots and sort to match recipe format
		items = tuple(sorted(filter(None, self.__crafting_slots.values())))

		# matches crafting slots to recipes
		if items in self.__recipes:
			crafted_item = self.__recipes[items]
			self.__output_slot = crafted_item
			# Clear crafting slots
			for slot in self.__crafting_slots:
			    self.__crafting_slots[slot] = None
			return f'Crafted {crafted_item}!'

		return 'Crafting failed. No matching recipe.'
    
	def take_output(self):
		if self.__output_slot:
			item = self.__output_slot
			self.__output_slot = None
			return f'{item}'
		return 'No item to retrieve in output slot.'

class PhysicalEnvironment:
	def __init__(self):
		self.environment = [ [-1,-1,-1,-1,-1,-1,-1] for i in range(0,8) ]
		self.player = PlayerStatus()

	def print_environment(self):
		for row in self.environment:
			print(row)

	def place_player(self):
		for y in range(len(self.environment)-1):
		    for x in range(len(self.environment)-1):
    			if self.environment[y][x] == 0: self.environment[y][x] = -1
		x, y = self.player.get_coordinates()
		self.environment[y][x] = 0

	def generate_environment(self, resources, weights):
		'''
		resources => [-1, int, ..., int]
		weights => same length list
		'''
		'''
		player => 0
		log => 1
		stone block => 2
		coal ore block => 3
		iron ore block => 4
		gold ore block => 5
		diamond block => 6
		'''
		if type(resources) != list:
			print('resources must be a list')
			return
		if type(weights) != list: 
			print('weights must be a list')
			return
		if len(resources) != len(weights):
			print('weights and resources must be an equal length')
			return

		self.place_player()
		for y in range(len(self.environment)-1):
		    for x in range(len(self.environment)-1):
		        if self.environment[y][x] == 0: continue
		        self.environment[y][x] = random.choices(
		            resources,
		            weights=weights
		        )[0]


if __name__ == '__main__':
	craft_env = CraftingEnvironment()
	# Crafting example
	print(craft_env.add_item_to_slot('slot1', 'log'))
	print(craft_env.craft())  # Attempt to craft with only one log
	print(craft_env.add_item_to_slot('slot2', 'log'))
	print(craft_env.craft())  # Should now create 'wood'
