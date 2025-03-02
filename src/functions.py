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
			database[player]['research'][res]['completed'] += database[player]['research'][res]['invested']
			database[player]['research'][res]['invested'] = 0

		
	return database
