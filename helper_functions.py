def get_wood_count(inv):
	wood_coords = inv.search_inventory('wood')
	if (-1,-1) == wood_coords: return 0

	return inv.get_slot_data(wood_coords)[1]

def get_stick_count(inv):
	stick_coords = inv.search_inventory('stick')
	if (-1,-1) == stick_coords: return 0

	return inv.get_slot_data(stick_coords)[1]

def can_eat(hunger):
	if hunger < 20: return True
	return False

def can_equip(armor_inv, armor_name):
	if not armor_inv[armor_name]: return True
	return False

def can_craft_axe(counts):
	wood, sticks = counts
	if wood < 3: return False
	if sticks < 2: return False

def can_craft_pickaxe(counts):
	wood, sticks = counts
	if wood < 3: return False
	if sticks < 2: return False

def can_craft_sticks(wood_count):
	if wood < 2: return False
	return True
