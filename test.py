import json
import os
import sqlite3


with open("skinlines.json", encoding="utf-8") as f:
    skinlines = json.load(f)
skinlines = {x["id"]: x["name"] for x in skinlines}

directory = "./downloaded_files"
json_files = [
    f
    for f in os.listdir(directory)
    if f.endswith(".json") and os.path.isfile(os.path.join(directory, f))
]

champions_objs = []
skin_objs = []
skinline_objs = []
for file in json_files:
    path = f"{directory}/{file}"
    with open(path, "r", encoding="utf-8") as f:
        aux = json.load(f)
        champions_objs.append({"champion_id": aux["id"], "champion_name": aux["name"]})

        for skin in aux.get("skins", []):
            skin_objs.append({
                "champion_id": aux["id"],
                "skin_id": skin["id"],
                "skin_name": skin["name"],
            })

            skins_skinline_ids = [
                x["id"] for x in (skin["skinLines"] if skin["skinLines"] else [])
            ]
            for skinline_id in skins_skinline_ids:
                skinline_name = skinlines[skinline_id]
                skinline_objs.append({
                    "skin_id": skin["id"],
                    "skinline_id": skinline_id,
                    "name": skinline_name,
                })

con = sqlite3.connect("funkyrolls.db")
cur = con.cursor()
d = open("sksek.txt","w")
for x in range(len(skinline_objs)):
    if skinline_objs[x]["skinline_id"] == 92 and skinline_objs[x]["skin_id"] == 56007:
        continue
    cur.execute("INSERT INTO skinlines (skin_id, skinline_id, skinline_name) VALUES (?, ?, ?)",
    (skinline_objs[x]["skin_id"], skinline_objs[x]["skinline_id"], skinline_objs[x]["name"]))


for x in range(len(skin_objs)):
    cur.execute("INSERT INTO skins (champion_id, skin_id, skin_name) VALUES (?, ?, ?)",
    (skin_objs[x]["champion_id"], skin_objs[x]["skin_id"], skin_objs[x]["skin_name"]))
   
con.commit()
con.close()