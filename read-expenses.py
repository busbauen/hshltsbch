#!/usr/bin/env python
import pyoo
import sqlite3 as sql
import datetime


def get_date(month):
    if month == "September":
        return "2016-09-01 10:00:00"
    if month == "Oktober":
        return "2016-10-01 10:00:00"
    elif month == "November":
        return "2016-11-01 10:00:00"
    elif month == "Dezember":
        return "2016-12-01 10:00:00"
    elif month == "Januar":
        return "2017-01-01 10:00:00"
    elif month == "Februar":
        return "2017-02-01 10:00:00"
        
def fix(sheet, year, x=1, y=5):
    print("processing monthly/yearly for %s " % year)
    expenses = sheet[7:50, x:y].values
    for expense in expenses:
        if expense[0] == "":
            break
        kostenart = expense[0].lower()
        kostenstelle = expense[1]
        betrag = expense[2]
        kommentar = expense [3]
        print(kostenart, kostenstelle, str(betrag),kommentar)

        dat = "%s-01-01 10:00:00" % year
    
        con = sql.connect("hshltsbch.db")
        cur = con.cursor()
        cur.execute("SELECT id FROM kostenstelle WHERE name =?", (kostenstelle,))
        row = cur.fetchone()
        kostenstelle_fk = row[0]
        if x==1:
            abschreibung = "jahr"
        else:
            abschreibung = "monat"
        con.execute('INSERT INTO eintrag(erstellt, kostenart, betrag, kostenstelle_id, kommentar, abschreibung)       VALUES (?,?,?,?,?,?)', (dat, kostenart, betrag, kostenstelle_fk, kommentar, abschreibung))
        con.commit()
        con.close()

    if x==1:
        fix(sheet, year, 6, 11)
  


def do_expense_or_earning(sheet, x=1, y=5):
    month = sheet.name.split('-')[1]
    print("Processing %s" % month)
    print("Processing expenses")
    expenses = sheet[7:50, x:y].values
    for expense in expenses:
        if expense[0] == "":
            break
    
        kostenart = expense[0].lower()
        kostenstelle = expense[1]
        betrag = expense[2]
        kommentar = expense [3]
        print(kostenart, kostenstelle, str(betrag),kommentar)
        
        con = sql.connect("hshltsbch.db")
        cur = con.cursor()
        cur.execute("SELECT id FROM kostenstelle WHERE name = ?", (kostenstelle,))
        row = cur.fetchone()
        kostenstelle_fk = row[0] 
        dat = get_date(month)
        con.execute('INSERT INTO eintrag(erstellt, kostenart, betrag, kostenstelle_id, kommentar, abschreibung) VALUES (?,?,?,?,?,?)', (dat, kostenart, betrag, kostenstelle_fk, kommentar, "tag"))
        con.commit()
        con.close()
    if(x==1):
        do_expense_or_earning(sheet, 6, 11)

def do_sprit(sheet,x=1, y=3):
   return # hat nie gefuntzt und suckt
   print("Processing Sprit")
   for eintrag in sheet[4:100, x:y].values:
        if eintrag[0] == "":
            break
        
        betrag = eintrag[0]
        datum_erstellt = str(eintrag[1])
        #datum_erstellt = datum_erstellt.replace('.','-')  
        print(datum_erstellt)
        datum_erstellt = "-".join((k[1],k[0]) for k in datum_erstellt.split('.'))
        print("Betrag %.02f Datum %s" % (betrag, datum_erstellt))
        con = sql.connect("hshltsbch.db")
        cur = con.cursor("SELECT id from kostenstelle where name = 'Auto'")
        kostenstelle_fk = row.fetchone()[0]
        cur = con.cursor("INSERT INTO eintrag(erstellt, kostenart, betrag, kostenstelle_id, kommentar, abschreibung) VALUES (?, ?, ?, ?, ?, ?)", (strftime('%d.%Y', datum_erstellt),"ausgaben", betrag, kostenstelle_fk, "Sprit", "tag"))
        cur.execute()
        con.commit()
        con.close

#todo: date konvertieren suckt. jahre noch mit reinkriegen + in die db schreiben

#soffice --accept="pipe,name=hello;urp;" --norestore --nologo --nodefault  --headless
desktop = pyoo.Desktop(pipe='hello')
doc = desktop.open_spreadsheet("Buch.ods")
for sheet in doc.sheets:
    if sheet.name.startswith("20"):
        do_expense_or_earning(sheet)
        print("\n\n")
    if sheet.name == "Fixkosten-2016":
        fix(sheet, "2016") 
        print("\n\n")
    if sheet.name == "Fixkosten-2017":
        fix(sheet, "2017")
        print("\n\n")
    if sheet.name == "Sprit":
        pass
        #do_sprit(sheet)
doc.close()

