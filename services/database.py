# create a new database file and add a table
# import sqlite3 library
import sqlite3

from models.card_dto import CardDto
from models.location_dto import LocationDto

database_name = "storage.db"

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(database_name)
        self.cur = self.conn.cursor()

        self.create_tables()

    def create_tables(self):
        # Cards table
        self.cur.execute("""CREATE TABLE IF NOT EXISTS cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_id TEXT,
            name TEXT,
            type TEXT,
            subtype TEXT,
            rarity TEXT,
            set_id TEXT,
            printing_type TEXT,
            condition INTEGER,
            condition_notes TEXT,
            location INTEGER REFERENCES locations(id),
            date_obtained DATE,
            obtained_how TEXT,
            card_market TEXT,
            comment TEXT,
            date_created DATETIME DEFAULT CURRENT_TIMESTAMP
        )""")

        # Locations table
        self.cur.execute("""CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            date_created DATETIME DEFAULT CURRENT_TIMESTAMP
        )""")

        self.conn.commit()

    def insert_card(self, card: CardDto):
        self.cur.execute("""INSERT INTO cards VALUES (
            NULL,
            :card_id,
            :name,
            :card_type,
            :card_subtype,
            :rarity,
            :set_id,
            :printing_type,
            :condition,
            :condition_notes,
            :location,
            :date_obtained,
            :obtained_how,
            :card_market,
            :comment,
            datetime('now')
        )""", {
            'card_id': card.CardId,
            'name': card.Name,
            'card_type': card.getType(),
            'card_subtype': card.getSubType(),
            'rarity': card.Rarity,
            'set_id': card.SetId,
            'printing_type': card.PrintingType,
            'condition': card.Condition,
            'condition_notes': card.ConditionNotes,
            'location': card.Location.id,
            'date_obtained': card.DateObtained,
            'obtained_how': card.ObtainedHow,
            'card_market': card.CardMarket,
            'comment': card.Comment
        })

        self.conn.commit()
        print(f"Inserted card {card.Name} into database")

    def insert_location(self, location):
        self.cur.execute("""INSERT INTO locations VALUES (
            NULL,
            :name,
            datetime('now')
        )""", {
            'name': location.Name
        })

        self.conn.commit()
        print(f"Inserted location {location.Name} into database")

    def get_locations(self) -> list[LocationDto]:
        self.cur.execute("SELECT * FROM locations")
        rows = self.cur.fetchall()
        
        return [LocationDto(row) for row in rows]
    
    def insert_location(self, name):
        self.cur.execute("""INSERT INTO locations VALUES (
            NULL,
            :name,
            datetime('now')
        )""", {
            'name': name
        })

        self.conn.commit()
    
    def delete_location(self, id):
        self.cur.execute("DELETE FROM locations WHERE id=?", (id,))
        self.conn.commit()

