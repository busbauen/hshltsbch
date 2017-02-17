#!/usr/bin/env python
# coding: utf8

from flask import Flask, render_template, request, flash, session, url_for, redirect
import functools
import datetime, sys
reload(sys)
sys.setdefaultencoding('utf-8')

import sqlite3 as sql

months = ["Januar", "Febraur", u"März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]

app = Flask(__name__)
app.secret_key = 'yolo'
app.config['USER'] = "admin"
app.config['PASS'] = "admin"

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
    return  cur.fetchall()

def get_current_month():
    now = datetime.datetime.now()
    return "%d/%02d" % (now.year, now.month)



@app.route('/fix')
def fix():
    list_months_sidebar = get_all_months()
    current_month = get_current_month()

    #year
    cur = get_db().cursor()
    cur.execute("select kostenstelle.name, betrag, kommentar from eintrag inner join kostenstelle ON kostenstelle.id = eintrag.kostenstelle_id where abschreibung = 'jahr' and kostenart='ausgaben' and strftime('%Y', erstellt) = '2017' order  by betrag desc")
    year_fixes = cur.fetchall()
    
    year_summ = sum(s[1] for s in year_fixes if s[1] )
    year_avg = round(year_summ/12,2)

    #month
    cur = get_db().cursor()
    cur.execute("select kostenstelle.name, betrag, kommentar from eintrag inner join kostenstelle ON kostenstelle.id = eintrag.kostenstelle_id where abschreibung = 'monat' and kostenart='ausgaben' and strftime('%Y', erstellt) = '2017' order  by betrag desc")
    month_fixes = cur.fetchall()
    month_sum = sum(s[1] for s in month_fixes if s[1])
    
    return render_template('fix.html', list_months_sidebar=list_months_sidebar, current_month=current_month, year_fixes=year_fixes, year_summ=year_summ, year_avg=year_avg, month_fixes=month_fixes, month_sum=month_sum)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST' and request.form.get('username') and request.form.get('password'):
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

@app.route('/month/<int:year>/<int:month>')
@login_required
def month(year, month):

    list_months_sidebar = get_all_months()
    current_month = get_current_month()
    
    #ausgaben
    query = "SELECT strftime('%%d.%%m.%%Y',erstellt), name, printf('%%.02f', betrag), kommentar  FROM eintrag INNER JOIN kostenstelle ON kostenstelle.id = eintrag.kostenstelle_id  WHERE strftime('%%m', erstellt) = '%02d' AND strftime('%%Y', erstellt) = '%d' AND abschreibung='tag' AND kostenart='ausgaben'" % (month, year)
    cur = get_db().cursor()
    cur.execute(query)
    expenses  = cur.fetchall()
    nice_expenses = expenses

    #einnahmen
    query = "SELECT strftime('%%d.%%m.%%Y',erstellt), name, printf('%%.02f', betrag), kommentar  FROM eintrag INNER JOIN kostenstelle ON kostenstelle.id = eintrag.kostenstelle_id  WHERE strftime('%%m', erstellt) = '%02d' AND strftime('%%Y', erstellt) = '%d' AND abschreibung='tag' AND kostenart='einnahmen'" % (month, year)
    cur.execute(query)
    incomes = cur.fetchall()

    
    #summe ausgaben kategorie monat
    query = "SELECT name, printf('%%.02f', sum(betrag)) AS summe FROM eintrag INNER JOIN kostenstelle ON kostenstelle.id = eintrag.kostenstelle_id  WHERE strftime('%%m', erstellt) = '%02d' AND strftime('%%Y', erstellt) = '%d' AND abschreibung='tag' AND kostenart='ausgaben' GROUP BY kostenstelle_id ORDER BY CAST(summe as REAL) DESC" % (month, year)
    cur.execute(query)
    month_summary_out = cur.fetchall()

    #summe einnahmen kategorie monat
    query = "SELECT name, printf('%%.02f', sum(betrag)) AS summe FROM eintrag INNER JOIN kostenstelle ON kostenstelle.id = eintrag.kostenstelle_id  WHERE strftime('%%m', erstellt) = '%02d' AND strftime('%%Y', erstellt) = '%d' AND abschreibung='tag' AND kostenart='einnahmen' GROUP BY kostenstelle_id ORDER BY CAST(summe as REAL) DESC" % (month, year)
    cur.execute(query)
    month_summary_in = cur.fetchall()

    
    #total in monat
    query = "SELECT printf('%%.02f', sum(betrag)) FROM eintrag WHERE strftime('%%m', erstellt) = '%02d' AND strftime('%%Y', erstellt) = '%d' AND abschreibung='tag' AND kostenart='einnahmen'" % (month, year)
    cur.execute(query)
    month_total_in = cur.fetchall()
  
    #total out monat
    query = "SELECT printf('%%.02f', sum(betrag)) FROM eintrag WHERE strftime('%%m', erstellt) = '%02d' AND strftime('%%Y', erstellt) = '%d' AND abschreibung='tag' AND kostenart='ausgaben'" % (month, year)
    cur.execute(query)
    month_total_out = cur.fetchall()

    return render_template("month.html", list_months_sidebar=list_months_sidebar, current_month=current_month, incomes=incomes, expenses=nice_expenses, year=year, month=month, month_summary_in=month_summary_in, month_summary_out = month_summary_out, month_total_in=round(float(month_total_in[0][0]),2), month_total_out=round(float(month_total_out[0][0]),2), month_name=months[month-1])


@app.route('/')
@login_required
def index():
    list_months_sidebar = get_all_months()
    current_month = get_current_month()
    
    #jährliches
    cur = get_db().cursor()
    query="SELECT strftime('%Y', erstellt), printf('%.02f', SUM(betrag)/12) from eintrag where kostenart='ausgaben' and abschreibung='jahr' group by strftime('%Y', erstellt)"
    cur.execute(query)
    expenses_year = cur.fetchall()
    expenses_year_dict = dict((k[0],k[1]) for k in expenses_year)
    
    #monatlich
    query="SELECT strftime('%Y', erstellt), printf('%.02f', sum(betrag)) from eintrag where kostenart='ausgaben' and abschreibung='monat' group by strftime('%Y', erstellt)"
    cur.execute(query)
    expenses_month = cur.fetchall()
    expenses_month_dict = dict((k[0],k[1]) for k in expenses_month)
    
    #ausgaben pro jahr und monat
    query="SELECT strftime('%Y', erstellt), strftime('%m', erstellt), printf('%.02f', sum(betrag)) from eintrag where kostenart='ausgaben' and abschreibung='tag' and kommentar is not 'tanken'  group by strftime('%Y', erstellt),strftime('%m', erstellt)"
    cur.execute(query)
    expenses_day = cur.fetchall()
    
    #einnahmen pro jahr und monat
    query="SELECT strftime('%Y', erstellt), strftime('%m', erstellt), printf('%.02f', sum(betrag)) from eintrag where kostenart='einnahmen' and abschreibung='tag'  group by strftime('%Y', erstellt),strftime('%m', erstellt)"
    cur.execute(query)
    income = cur.fetchall()

    stats = [] 
    
    for i in range(0, len(expenses_day)):
        item = (income[i][0], months[int(income[i][1])-1], expenses_year_dict[income[i][0]], expenses_month_dict[income[i][0]], expenses_day[i][2],None , income[i][2], None)
        stats.append(list(item))
    
    for i in range(0, len(income)):
        stats[i][5] = round(float(stats[i][2]) +float(stats[i][3]) + float(stats[i][4]),2)
        stats[i][7] = round(float(stats[i][6]) - float(stats[i][5]),2)

 
    return render_template('summary.html', list_months_sidebar=list_months_sidebar, current_month=current_month, stats=stats)

@app.route('/new', methods = [ 'POST', 'GET'])
@login_required
def new():
    list_months_sidebar = get_all_months()
    current_month = get_current_month()
    
    #autocoomplete kategorien
    cur = get_db().cursor()
    cur.execute("SELECT name from kostenstelle")
    kostenstellen = cur.fetchall()

    if request.method == 'POST':
        if request.form.get('kostenart') and  request.form.get('kostenstelle') and request.form.get('betrag') and request.form.get('abschreibung') :
            kommentar = request.form.get('kommentar')
            erstellt = request.form.get('erstellt')
            kostenart = request.form.get('kostenart').strip()
            if kostenart not in ['einnahmen', 'ausgaben']:
                flash("Falsche Kostenart", "orange")
                return render_template('new.html', list_months_sidebar=list_months_sidebar, current_month=current_month,kostenstellen=kostenstellen )

            kostenstelle = request.form.get('kostenstelle').strip()
            try:
                betrag = float(request.form.get('betrag').replace(',','.'))
            except:
                flash("Betrag ist keine Zahl", "orange")
                return render_template('new.html', list_months_sidebar=list_months_sidebar, current_month=current_month, kostenstellen=kostenstellen )

            if betrag < 0:
                betrag = betrag *-1
            abschreibung = request.form.get('abschreibung')
            if abschreibung not in ['tag', 'jahr', 'monat']:
                flash("Falsche Abschreibung", "orange")
                return render_template('new.html', list_months_sidebar=list_months_sidebar, current_month=current_month , kostenstellen=kostenstellen)

            con = get_db()
            cur = con.cursor()
            cur.execute("SELECT id from kostenstelle where name = (?)", (kostenstelle,))
            row = cur.fetchone()
            if row == None:
                flash('Die Kostenstelle gibt es nicht!', 'orange')
                return render_template('new.html', list_months_sidebar=list_months_sidebar, current_month=current_month,kostenstellen=kostenstellen)
            kostenstelle_id = row[0]
            cur.execute("INSERT INTO eintrag (erstellt, kostenart, betrag, kostenstelle_id, kommentar, abschreibung) VALUES (?,?,?,?,?,?)" , (erstellt + ' 10:00:00', kostenart, betrag, kostenstelle_id, kommentar, abschreibung))
            con.commit()
            flash('OK', 'green')
            return render_template('new.html', list_months_sidebar=list_months_sidebar, current_month=current_month,kostenstellen=kostenstellen )
        else:
            flash('Alles ausfüllen!', 'red')
            return render_template('new.html', list_months_sidebar=list_months_sidebar, current_month=current_month, kostenstellen=kostenstellen )
            
    return render_template('new.html',  list_months_sidebar=list_months_sidebar, current_month=current_month, kostenstellen=kostenstellen)



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
