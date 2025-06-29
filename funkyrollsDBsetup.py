import sqlite3

def setup_database():
    con = sqlite3.connect("funkyrolls.db")
    cur = con.cursor()
    create_champions_table = """
        CREATE TABLE IF NOT EXISTS champions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            release_date TEXT NOT NULL
    );"""

    create_tags_table = """
        CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            subgroup BOOLEAN NOT NULL DEFAULT 0,
            description TEXT NOT NULL
    );"""

    create_tags_subgroup_table = """
            CREATE TABLE IF NOT EXISTS subgroups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tag_name TEXT NOT NULL,
            tag_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            FOREIGN KEY (tag_id) REFERENCES tags(id)
            
    );"""

    create_champion_tags_table = """
        CREATE TABLE IF NOT EXISTS champion_tags (
            champion_id INTEGER NOT NULL,
            tag_id INTEGER NOT NULL,
            subgroup_id INTEGER DEFAULT NULL,
            PRIMARY KEY (champion_id, tag_id),
            FOREIGN KEY (champion_id) REFERENCES champions(id),
            FOREIGN KEY (tag_id) REFERENCES tags(id),
            FOREIGN KEY (subgroup_id) REFERENCES subgroups(id)
            
    );"""

    cur.execute(create_champions_table)
    cur.execute(create_tags_table)
    cur.execute(create_tags_subgroup_table)
    cur.execute(create_champion_tags_table)
    con.commit()
    con.close()

def add_champion(name, release_date):
    con = sqlite3.connect("funkyrolls.db")
    cur = con.cursor()
    cur.execute("INSERT INTO champions (name, release_date) VALUES (?, ?)", (name, release_date))
    con.commit()
    con.close()

def add_tag(name, subgroup_present ,description):
    con = sqlite3.connect("funkyrolls.db")
    cur = con.cursor()
    cur.execute("INSERT INTO tags (name, subgroup, description) VALUES (?, ?, ?)", (name, subgroup_present, description))
    con.commit()
    con.close()

def add_and_connect_subgroup_tag(tag_name, name, description):
    con = sqlite3.connect("funkyrolls.db")
    cur = con.cursor()
    cur.execute("SELECT id FROM tags WHERE name = ?", (tag_name,))
    tag_id = cur.fetchone()[0]
    cur.execute("INSERT INTO subgroups (tag_name, tag_id, name, description) VALUES (?, ?, ?, ?)", (tag_name, tag_id, name, description))
    con.commit()
    con.close()

def connect_champion_tag(champion_id, tag_id):
    con = sqlite3.connect("funkyrolls.db")
    cur = con.cursor()
    cur.execute("INSERT INTO champion_tags (champion_id, tag_id) VALUES (?, ?)", (champion_id, tag_id))
    con.commit()
    con.close()

