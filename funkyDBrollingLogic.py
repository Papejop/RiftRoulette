import sqlite3
import random

con = sqlite3.connect("funkyrolls.db")
cur = con.cursor()

cur.execute("SELECT COUNT(*) FROM tags")
number_of_categories = cur.fetchone()[0]
roles = ["Top", "Jungle", "Mid", "ADC", "Support"]


def roll_subgroup(random_number):
    cur.execute("SELECT count(*) FROM subgroups WHERE tag_id = ?", (random_number,))
    subgroup_count = cur.fetchone()[0]
    rand_helper = random.randint(1, subgroup_count)
    cur.execute("SELECT id from subgroups WHERE tag_id = ?", (random_number,))
    help = [row[0] for row in cur.fetchall()]
    return help[rand_helper-1]

def rolling_dice():
    output = ""
    for i in range(5):
        random_number = random.randint(1, number_of_categories)

        cur.execute("SELECT name FROM tags WHERE id = ?", (random_number,))
        tag = cur.fetchone()[0]

        cur.execute("SELECT subgroup FROM tags WHERE id = ?", (random_number,))
        subgroup = cur.fetchone()[0]

        if subgroup == 1:
            subgroup_id = roll_subgroup(random_number)
            cur.execute("SELECT name FROM subgroups WHERE id = ?", (subgroup_id,))
            subg_name = cur.fetchone()[0]
            output += f"{roles[i]}: {tag} - {subg_name} \n"
            cur.execute("SELECT name FROM champions WHERE id IN (SELECT champion_id FROM champion_tags WHERE subgroup_id = ?)", (subgroup_id,))
        else:
            output += f"{roles[i]}: {tag} \n"
            cur.execute("SELECT name FROM champions WHERE id IN (SELECT champion_id FROM champion_tags WHERE tag_id = ?)", (random_number,))
            
        champion = [row[0] for row in cur.fetchall()]
        champios_text = ", ".join(champion)
        output += champios_text + "\n\n"
    return output

