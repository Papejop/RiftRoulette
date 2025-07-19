import sqlite3
import random
import re


def get_db_connection():
    con = sqlite3.connect("funkyrolls.db")
    cur = con.cursor()
    return con


def roll_subgroup(random_number):
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("SELECT count(*) FROM subgroups WHERE tag_id = ?", (random_number,))
    subgroup_count = cur.fetchone()[0]
    rand_helper = random.randint(1, subgroup_count)
    cur.execute("SELECT id from subgroups WHERE tag_id = ?", (random_number,))
    help = [row[0] for row in cur.fetchall()]
    return help[rand_helper - 1]


def rolling_dice():
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM tags")
    number_of_tags = cur.fetchone()[0]
    roles = ["Top", "Jungle", "Mid", "ADC", "Support"]
    output = ""
    for i in range(5):
        random_number = random.randint(1, number_of_tags)

        cur.execute("SELECT name FROM tags WHERE id = ?", (random_number,))
        tag = cur.fetchone()[0]

        cur.execute("SELECT subgroup FROM tags WHERE id = ?", (random_number,))
        subgroup = cur.fetchone()[0]

        if subgroup == 1:
            subgroup_id = roll_subgroup(random_number)
            cur.execute("SELECT name FROM subgroups WHERE id = ?", (subgroup_id,))
            subg_name = cur.fetchone()[0]
            output += f"{roles[i]}: {tag} - {subg_name} \n"
            cur.execute(
                "SELECT name FROM champions WHERE id IN (SELECT champion_id FROM champion_tags WHERE subgroup_id = ?)",
                (subgroup_id,),
            )
        else:
            output += f"{roles[i]}: {tag} \n"
            cur.execute(
                "SELECT name FROM champions WHERE id IN (SELECT champion_id FROM champion_tags WHERE tag_id = ?)",
                (random_number,),
            )

        champion = [row[0] for row in cur.fetchall()]
        champios_text = ", ".join(champion)
        output += champios_text + "\n\n"
    con.close()
    return output


def assign_champions(player_owners):
    assigned = {}
    used_champions = set()

    def backtrack(players, idx):
        if idx == len(players):
            return True

        player = players[idx]
        for champ in player_owners[player]:
            if champ not in used_champions:
                assigned[player] = champ
                used_champions.add(champ)

                if backtrack(players, idx + 1):
                    return True

                # backtrack
                used_champions.remove(champ)
                del assigned[player]
        return False

    players = list(player_owners.keys())
    if backtrack(players, 0):
        return assigned
    else:
        return None


def rolling_dice_skinline(usernames):
    con = get_db_connection()
    cur = con.cursor()
    potential_skinlines = list()
    verified_skinlines = list()
    user_skins = {}

    cur.execute(
        """
                SELECT sl.skinline_id 
                FROM skinlines sl
                JOIN skins s ON sl.skin_id = s.skin_id
                JOIN player_skins ps ON s.skin_id = ps.skin_id
                JOIN players p ON ps.player_id = p.id
                WHERE p.username IN (?, ?, ?, ?, ?)
                GROUP BY sl.skinline_name
                HAVING COUNT(DISTINCT p.id) = 5
                """,
        (usernames[0], usernames[1], usernames[2], usernames[3], usernames[4]),
    )
    potential_skinline_ids = [r[0] for r in cur.fetchall()]

    for skinline_id in potential_skinline_ids:
        for username in usernames:
            cur.execute(
                """
                        SELECT s.skin_id
                        FROM skins s
                        JOIN player_skins ps ON s.skin_id  = ps.skin_id
                        JOIN players p ON p.id = ps.player_id
                        JOIN skinlines sl ON sl.skin_id = s.skin_id
                        WHERE p.username = ? AND sl.skinline_id = ?
                        """,
                (username, skinline_id),
            )
            skinline_skins = [row[0] for row in cur.fetchall()]
            user_skins[username] = skinline_skins

        res = assign_champions(user_skins)

        if res:
            res["skinline_id"] = skinline_id
            verified_skinlines.append(res)

    random_skinline = random.choice(verified_skinlines)

    cur.execute(
    """
    SELECT skinline_name
    FROM skinlines
    WHERE skinline_id = ? 
    """,
    (random_skinline["skinline_id"],))

    kek = cur.fetchall()
    output = f"skinline name: {kek[0]}\n"
    output = re.sub(r"[,]","", output)

    for username in usernames:
        
        cur.execute(
            """
            SELECT skin_name
            FROM skins
            WHERE skin_id = ? 
            """,
            (random_skinline[username],),
        )
        kek = cur.fetchone()  
        first_skin = kek[0] if kek else "Unknown Skin"

        cur.execute(
            """
            SELECT s.skin_name
            FROM skins s
            JOIN player_skins ps ON s.skin_id = ps.skin_id
            JOIN players p ON p.id = ps.player_id
            JOIN skinlines sl ON sl.skin_id = s.skin_id
            WHERE p.username = ? AND sl.skinline_id = ?
            """,
            (username, random_skinline["skinline_id"]),
        )

        skin_names = [row[0] for row in cur.fetchall()]
        output += f"{username} - {first_skin}\n all skins : {', '.join(skin_names)}\n\n"


    output = re.sub(r"[\[\]()'']", "", output)
    con.close()
    return output
