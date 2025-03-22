import json


# players=['test_player_1', 'test_player_2', 'test_player_3', 'test_player_4', 'test_player_5']

def load_config():
	with open('src/config.json', 'r', encoding="utf8") as openfile:
	# Reading from json file
		json_object = json.load(openfile)
		openfile.close()
	return json_object


def check_roles(ctx, config):
	returning=[False, False, None]
	for r in ctx.author.roles:
		if str(r).lower() == config['game_master_role']:
			returning[0]=True
		elif str(r).lower() == config['player_role']:
			returning[1]=True
		elif str(r).lower() in config['all_player_roles']:
			returning[2]=str(r).lower()
	print(returning)
	return returning


def read_db():
	with open('json_database/players.json', 'r', encoding="utf8") as openfile:
	# Reading from json file
		json_object = json.load(openfile)
		openfile.close()
	return json_object

def write_db(database):
	with open('json_database/players.json', 'w', encoding="utf8") as openfile:
		database=json.dumps(database, indent=4)
		openfile.write(database)
		openfile.close()


def reset_orders(database):

	for player in database:
		database[player]['orders'].clear()
		database[player]['science'][0] = database[player]['science'][1]
		for res in database[player]['research']:
			database[player]['research'][res]['researched'] += database[player]['research'][res]['invested']
			database[player]['research'][res]['invested'] = 0

		
	return database


def make_stats(config, database, player, sort_orders = False):
	if config['player_flags'][player]['emoji_name'] == None:
		final_messages = [f"**{config['player_full_names'][player]}**\n\n"]
	else:
		final_messages = [f"**{config['player_full_names'][player]}**     <:{config['player_flags'][player]['emoji_name']}:{config['player_flags'][player]['emoji_id']}>\n\n"]
	gold=database[player]['gold']
	food=database[player]['food']
	pop=database[player]['pop']
	ore=database[player]['ore']
	aether=database[player]['aether']
	mythical=database[player]['mythical']
	science = database[player]['science']
	regions=' '.join(database[player]['regions'])
	final_messages[-1] += f"**Gold:** {gold}\n**Food:** {food}\n**Pop:** {pop}\n**Ore:** {ore}\n**Aether:** {aether}\n**Mythical:** {mythical}\n**Science:** {science[0]} ({science[1]} per turn)\n**Regions:** {regions}\n**Orders:**\n"
	if sort_orders:
		sorted_orders = []
		order_types = ['build', 'upgrade', 'move', 'attack', 'resesrch']
		for type in order_types:
			for order in database[player]['orders']:
				if type == order['type']:
					sorted_orders.append(order)
	else:
		sorted_orders = database[player]['orders']
	n = 1
	for order in sorted_orders:
		if order['type'] in ['upgrade', 'build']:
			order_txt = f"{n}.  {order['type']} **{order['building']}** in **{order['region']}**\n"
		elif order['type'] in ['attack', 'move']:
			order_txt = f"{n}.  **{order['type']}** {order['text']}\n"
		elif order['type'] == 'research':
			order_txt = f"{n}.  invest **{order['amount']}** into **{order['field']}**\n"
		if len(final_messages[-1]) + len(order_txt) > 1999:
			final_messages.append(order_txt)
		else:
			final_messages[-1] += order_txt
		n += 1
	final_messages[-1] += "\n\n"
	return final_messages