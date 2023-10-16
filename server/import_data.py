import sqlite3
import json

# Collegarsi al database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Creare la tabella dealerships se non esiste
cursor.execute("""
    CREATE TABLE IF NOT EXISTS dealerships (
        id INTEGER PRIMARY KEY,
        city TEXT,
        state TEXT,
        st TEXT,
        address TEXT,
        zip TEXT,
        lat REAL,
        long REAL,
        short_name TEXT,
        full_name TEXT
    )
""")

# Creare la tabella reviews se non esiste
cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY,
        name TEXT,
        dealership INTEGER,
        review TEXT,
        purchase BOOLEAN,
        purchase_date TEXT,
        car_make TEXT,
        car_model TEXT,
        car_year INTEGER
    )
""")

# Leggere e inserire i dati dei dealerships
with open('../cloudant/data/dealerships.json', 'r') as f:
    data = json.load(f)
    dealerships = data['dealerships']

    for dealership in dealerships:
        cursor.execute("""
            INSERT INTO dealerships (id, city, state, st, address, zip, lat, long, short_name, full_name)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (dealership['id'], dealership['city'], dealership['state'], dealership['st'], dealership['address'], dealership['zip'], dealership['lat'], dealership['long'], dealership['short_name'], dealership['full_name']))

# Leggere e inserire i dati dei reviews
with open('../cloudant/data/reviews-full.json', 'r') as f:
    data = json.load(f)
    reviews = data['reviews']

    for review in reviews:
        cursor.execute("""
            INSERT INTO reviews (id, name, dealership, review, purchase, purchase_date, car_make, car_model, car_year)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (review['id'], review['name'], review['dealership'], review['review'], review['purchase'], review['purchase_date'], review['car_make'], review['car_model'], review['car_year']))

# Fare commit delle modifiche e chiudere la connessione
conn.commit()
conn.close()
