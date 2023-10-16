import sqlite3
import json

# Collegarsi al database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Non c'è bisogno di creare di nuovo le tabelle; avendo già fatto le migrazioni con Django, le tabelle dovrebbero già esistere con la struttura corretta.

# Leggere e inserire i dati dei dealerships
with open('../cloudant/data/dealerships.json', 'r') as f:
    data = json.load(f)
    dealerships = data['dealerships']

    for dealership in dealerships:
        cursor.execute("""
            INSERT INTO djangoapp_dealership (id, city, state, st, address, zip, lat, long, full_name, short_name)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (dealership['id'], dealership['city'], dealership['state'], dealership['st'], dealership['address'], dealership['zip'], dealership['lat'], dealership['long'], dealership.get('full_name', "Unknown Dealer"), dealership.get('short_name', "Unknown Dealer")))

# Leggere e inserire i dati dei reviews
with open('../cloudant/data/reviews-full.json', 'r') as f:
    data = json.load(f)
    reviews = data['reviews']

    for review in reviews:
        cursor.execute("""
            INSERT INTO djangoapp_review (id, name, dealership_id, review, purchase, purchase_date, car_make, car_model, car_year)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (review['id'], review['name'], review['dealership'], review['review'], review['purchase'], review['purchase_date'], review['car_make'], review['car_model'], review['car_year']))

# Fare commit delle modifiche e chiudere la connessione
conn.commit()
conn.close()
