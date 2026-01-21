import json
import sqlite3

class Database:
    def __init__(self, db_name):
        self.db_name = db_name

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()

    def create_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            data JSON
        )
        '''
        self.cursor.execute(query)

    def save_the_game(self, player):
        player_data = {
            "name": player.name,
            "hp": player.hp,
            "max_hp": player.max_hp,
            "mp": player.mp,
            "max_mp": player.max_mp,
            "experience": player.experience,
            "strength": player.strength,
            "inventory": [item.to_dict() for item in player.inventory.items],
            "spells": [spell.to_dict() for spell in player.spells],
            "equipped_weapon_name": player.equipped_weapon.to_dict() if player.equipped_weapon else None
        }

        json_data = json.dumps(player_data)

        self.cursor.execute(
            "INSERT OR REPLACE INTO players (name, data) VALUES (?, ?)",
            (player.name, json_data)
        )


    def delete_save_file(self, player_name):
        self.cursor.execute("DELETE FROM players WHERE name = ?",(player_name,))


    def fetch_save_file(self, player_name):
        self.cursor.execute("SELECT data FROM players WHERE name = ?", (player_name,))
        result = self.cursor.fetchone()

        if result:
            return json.loads(result[0])

        return None

    def fetch_all_save_files(self):
        self.cursor.execute("SELECT name FROM players")
        result = self.cursor.fetchall()

        if result:
            return [row[0] for row in result]

        return []