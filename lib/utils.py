import json


def read_json(filename):
    with open(f"{filename}.json", "r", encoding="utf-8-sig") as f:
        data = json.load(f)
    return data

def write_json(data, filename):
    with open(f"{filename}.json", "w", encoding="utf-8-sig") as f:
        json.dump(data, f, indent=4)

def read_txt(filename):
    return open(filename + ".txt", "r").read()

def fmat(number):
    return "{:,}".format(number)

async def add_emojis(emojis, message):
    for emoji in emojis:
        await message.add_reaction(emoji)

async def remove_emojis(emojis, message):
    for emoji in emojis:
        await message.clear_reaction(emoji)
