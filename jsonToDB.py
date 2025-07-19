import codecs
import json
import sqlite3
import argparse



con = sqlite3.connect("funkyrolls.db")
cur = con.cursor()

parser = argparse.ArgumentParser()
parser.add_argument("username", help=" input username", type=str)
args = parser.parse_args()

owned_skins = set()
with codecs.open("skins2.json", "r", encoding="utf-8-sig") as inputFile:
    jsonData = json.load(inputFile)
    for skin in jsonData:
        if skin.get("ownership", {}).get("owned", False):
            skin_id = skin.get("id")
            owned_skins.add(skin_id)



cur.execute("INSERT INTO players (username) VALUES (?)", (args.username,))
cur.execute("SELECT id FROM players WHERE username = ?", (args.username,))
user_id = cur.fetchone()[0]

for skin_id in owned_skins:
    #print(skin_id)
    cur.execute("INSERT INTO player_skins (player_id, skin_id) VALUES (?,?)", (user_id, skin_id))
        

con.commit()
con.close()
