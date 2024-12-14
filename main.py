from dotenv import load_dotenv
from bricklink import BrickLink
import os
import json

load_dotenv()

consumer_key = os.getenv('BRICKLINK_CONSUMER_KEY')
consumer_secret = os.getenv('BRICKLINK_CONSUMER_SECRET')

token_value = os.getenv('BRICKLINK_TOKEN_VALUE')
token_secret = os.getenv('BRICKLINK_TOKEN_SECRET')

bricklink: BrickLink = BrickLink(consumer_key, consumer_secret, token_value, token_secret)

inventories: list = bricklink.get_inventories()
blocks: list = json.loads(open('blocks.json', 'r').read())['blocks']

all_categories: list = bricklink.get_catory_list()
categories_dictionary:  dict = {}
for category in all_categories:
    categories_dictionary[str(category['category_id'])] = category['category_name']

while True:
    print("Select a Block: ")
    print("[0]: Minifigures")
    for i, block in enumerate(blocks):
        print(f"[{i+1}]: {block['title']}")

    block_id: int = int(input('\n'))
    valid_types: list = []
    if block_id == 0:
        valid_types.append("MINIFIG")
    
    block: dict = blocks[block_id-1]
    valid_categories: list = block['category_ids']

    valid_inventories: list = []
    for inventory in inventories:
        if len(valid_types) > 0:
            if inventory['item']['type'] in valid_types:
                valid_inventories.append(inventory)
            continue

        if inventory['item']['category_id'] not in valid_categories:
            continue
        
        if 'description' in inventory:
            if inventory['description'] != "":
                continue

        valid_inventories.append(inventory)

    sorted_inventories = sorted(valid_inventories, key=lambda inv: inv['unit_price'], reverse=True)
    top_inventories = sorted_inventories[0:12]

    with open('pieces.txt', 'w') as file:
        for i, inventory in enumerate(top_inventories):
            file.write(f"[{i+1}]: {categories_dictionary[str(inventory['item']['category_id'])]} -- {inventory['item']['name']}\n")