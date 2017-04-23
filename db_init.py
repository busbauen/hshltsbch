#!/usr/bin/env python
import sqlite3  as sql


con = sql.connect("hshltsbch.db")
print("dropping tables")
#con.execute("drop table kostenstelle;")
#con.execute("drop table eintrag;")
#con.commit()
print("creating tables")
con.execute("CREATE TABLE IF NOT EXISTS kostenstelle (id integer PRIMARY KEY,name varchar(30));")
con.commit()

create_eintrag = '''CREATE TABLE IF NOT EXISTS eintrag (
id integer PRIMARY KEY,
erstellt date,
kostenart varchar(20),
betrag real,
kostenstelle_id integer,
kommentar varchar(40),
abschreibung varchar(20),
FOREIGN KEY(kostenstelle_id) REFERENCES kostenstelle(id)
);
'''

con.execute(create_eintrag)
con.commit()

kategorien = ("Bildung", "Spielzeug", "Miete", "Urlaub", "Internet/Handy", "Sparen", "Haushalt", "Kleidung", "GEZ", "Friseur", "Apotheke/Arzt", "Gehalt", "Geburtstage & Weihnachten", "passives Einkommen", "Essen & Trinken", "Sport", "Versicherungen", "Freizeit", "Auto", "Zinsen")

for kat in kategorien:
    cur = con.cursor()
    print(kat)
    cur.execute("INSERT INTO kostenstelle (name) VALUES (?)", (kat,))
    print("inserted %s" % kat)
    con.commit()


con.close()

