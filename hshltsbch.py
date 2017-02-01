#!/usr/bin/env python
from flask import Flask, render_template, request, flash, session, url_for, redirect
import functools
import datetime

import sqlite3 as sql

app = Flask(__name__)

DATABASE = "hshltsbch.db"

def get_db():
    db = sql.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = get_db()
    if db is not None:
        db.close()

def login_required(fn):
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        if session.get('logged_in'):
            return fn(*args, **kwargs)
        return redirect(url_for('login', next=request.path))
    return inner

def get_all_months():
    cur = get_db().cursor()
    cur.execute("select strftime('%Y', erstellt) ,strftime('%m', erstellt) from eintrag group by strftime('%Y', erstellt) ,strftime('%m', erstellt)")
    return cur.fetchall()

def get_current_month():
    now = datetime.datetime.now()
    return "%d/%02d" % (now.year, now.month)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST' and request.form.get('username') and request.form.get('password'):
        print(request.form.get('username'))
        print(request.form.get('password'))
        
        if request.form.get('username') == app.config['USER'] and \
           request.form.get('password') == app.config['PASS']:
               session['logged_in'] = True
               return redirect('/')
        else:
            flash('Nö')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/test')
def test():
    get_all_months()
    return render_template('base.html')

@app.route('/month/<int:year>/<int:month>')
@login_required
def month(year, month):

    list_months_sidebar = get_all_months()
    current_month = get_current_month()
    
    query = "SELECT strftime('%%d.%%m.%%Y',erstellt), name, printf('%%.02f', betrag), kommentar  FROM eintrag INNER JOIN kostenstelle ON kostenstelle.id = eintrag.kostenstelle_id  WHERE strftime('%%m', erstellt) = '%02d' AND strftime('%%Y', erstellt) = '%d' AND abschreibung='tag' AND kostenart='ausgaben'" % (month, year)
    cur = get_db().cursor()
    cur.execute(query)
    expenses  = cur.fetchall()
    nice_expenses = expenses

    query = "SELECT strftime('%%d.%%m.%%Y',erstellt), name, printf('%%.02f', betrag), kommentar  FROM eintrag INNER JOIN kostenstelle ON kostenstelle.id = eintrag.kostenstelle_id  WHERE strftime('%%m', erstellt) = '%02d' AND strftime('%%Y', erstellt) = '%d' AND abschreibung='tag' AND kostenart='einnahmen'" % (month, year)
    cur.execute(query)
    incomes = cur.fetchall()

    query = "SELECT name, printf('%%.02f', sum(betrag)) AS summe FROM eintrag INNER JOIN kostenstelle ON kostenstelle.id = eintrag.kostenstelle_id  WHERE strftime('%%m', erstellt) = '%02d' AND strftime('%%Y', erstellt) = '%d' AND abschreibung='tag' AND kostenart='ausgaben' GROUP BY kostenstelle_id ORDER BY CAST(summe as REAL) DESC" % (month, year)
    cur.execute(query)
    month_summary_out = cur.fetchall()

    query = "SELECT name, printf('%%.02f', sum(betrag)) AS summe FROM eintrag INNER JOIN kostenstelle ON kostenstelle.id = eintrag.kostenstelle_id  WHERE strftime('%%m', erstellt) = '%02d' AND strftime('%%Y', erstellt) = '%d' AND abschreibung='tag' AND kostenart='einnahmen' GROUP BY kostenstelle_id ORDER BY CAST(summe as REAL) DESC" % (month, year)
    cur.execute(query)
    month_summary_in = cur.fetchall()
    
    query = "SELECT printf('%%.02f', sum(betrag)) FROM eintrag WHERE strftime('%%m', erstellt) = '%02d' AND strftime('%%Y', erstellt) = '%d' AND abschreibung='tag' AND kostenart='einnahmen'" % (month, year)
    cur.execute(query)
    month_total_in = cur.fetchall()
  
    query = "SELECT printf('%%.02f', sum(betrag)) FROM eintrag WHERE strftime('%%m', erstellt) = '%02d' AND strftime('%%Y', erstellt) = '%d' AND abschreibung='tag' AND kostenart='ausgaben'" % (month, year)
    print(query)
    cur.execute(query)
    month_total_out = cur.fetchall()

    
    return render_template("month.html", list_months_sidebar=list_months_sidebar, current_month=current_month, incomes=incomes, expenses=nice_expenses, year=year, month=month, month_summary_in=month_summary_in, month_summary_out = month_summary_out, month_total_in=month_total_in, month_total_out=month_total_out)


@app.route('/')
@login_required
def index():
    list_months_sidebar = get_all_months()
    current_month = get_current_month()
    
    cur = get_db().cursor()
    query="SELECT strftime('%Y', erstellt), printf('%.02f', SUM(betrag)/12) from eintrag where kostenart='ausgaben' and abschreibung='jahr' group by strftime('%Y', erstellt)"
    cur.execute(query)
    expenses_year = cur.fetchall()
    expenses_year_dict = dict((k[0],k[1]) for k in expenses_year)
    print("Jährliches")
    for e in expenses_year:
        print(e)
    
    query="SELECT strftime('%Y', erstellt), printf('%.02f', sum(betrag)) from eintrag where kostenart='ausgaben' and abschreibung='monat' group by strftime('%Y', erstellt)"
    cur.execute(query)
    expenses_month = cur.fetchall()
    expenses_month_dict = dict((k[0],k[1]) for k in expenses_month)
    print("Monatliche Fixkosten")
    for e in expenses_month:
        print(e)
    
    query="SELECT strftime('%Y', erstellt), strftime('%m', erstellt), printf('%.02f', sum(betrag)) from eintrag where kostenart='ausgaben' and abschreibung='tag' group by strftime('%Y', erstellt),strftime('%m', erstellt)"
    cur.execute(query)
    expenses_day = cur.fetchall()
    print("Monatliche Ausgaben")
    for e in expenses_day:
        print(e)
    
    query="SELECT strftime('%Y', erstellt), strftime('%m', erstellt), printf('%.02f', sum(betrag)) from eintrag where kostenart='einnahmen' and abschreibung='tag' group by strftime('%Y', erstellt),strftime('%m', erstellt)"
    cur.execute(query)
    income = cur.fetchall()
    print("Monatliche Einnahmen")
    for r in income:
        print(r)

    print("lets go")
    stats = [] 
    for i in range(0, len(income)):
        item = (income[i][0], income[i][1], expenses_year_dict[income[i][0]], expenses_month_dict[income[i][0]], expenses_day[i][2],None , income[i][2], None)
        stats.append(list(item))
        print(item)
    
    print("done") 
    for i in range(0, len(income)):
        stats[i][5] = float(stats[i][2]) +float(stats[i][3]) + float(stats[i][4])
    
    for i in range(0, len(income)):
        stats[i][7] = float(stats[i][6]) - float(stats[i][5]) - 41.89
        stats[i][7] = round(stats[i][7], 2) 
        print(stats[i])
 
    return render_template('summary.html', list_months_sidebar=list_months_sidebar, current_month=current_month, stats=stats)

@app.route('/new', methods = [ 'POST', 'GET'])
@login_required
def new():
    list_months_sidebar = get_all_months()
    current_month = get_current_month()

    if request.method == 'POST':
        if request.form.get('kostenart') and  request.form.get('kostenstelle') and request.form.get('betrag') and request.form.get('abschreibung') :
            erstellt = request.form.get('erstellt')
            kostenart = request.form.get('kostenart')
            kostenstelle = request.form.get('kostenstelle')
            betrag = float(request.form.get('betrag').replace(',','.'))
            if betrag < 0:
                betrag = betrag *-1
            kommentar = request.form.get('kommentar')
            abschreibung = request.form.get('abschreibung')

            con = get_db()
            cur = con.cursor()
            print(kostenstelle)
            cur.execute("SELECT id from kostenstelle where name = (?)", (kostenstelle,))
            row = cur.fetchone()
            if row == None:
                flash('Die Kostenstelle gibt es nicht!', 'red')
                return render_template('new.html')
            kostenstelle_id = row[0]
            cur.execute("INSERT INTO eintrag (erstellt, kostenart, betrag, kostenstelle_id, kommentar, abschreibung) VALUES (?,?,?,?,?,?)" , ('2017-01-11 10:00:00', kostenart, betrag, kostenstelle_id, kommentar, abschreibung))
            con.commit()
            flash('OK', 'green')
            return render_template('new.html', list_months_sidebar=list_months_sidebar, current_month=current_month )
        else:
            flash('Alles ausfüllen!', 'red')
            return render_template('new.html')
            
    cur = get_db().cursor()
    cur.execute("SELECT name from kostenstelle")
    kostenstellen = cur.fetchall()
    return render_template('new.html',  list_months_sidebar=list_months_sidebar, current_month=current_month, kostenstellen=kostenstellen)



app.secret_key = 'yolo'
app.config['USER'] = "admin"
app.config['PASS'] = "admin"

app.run(debug=True, host='0.0.0.0')
