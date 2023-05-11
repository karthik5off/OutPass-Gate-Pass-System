from operator import itemgetter
from flask import Flask,render_template,request
import sqlite3
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app=Flask('__name__')

credential = ServiceAccountCredentials.from_json_keyfile_name("google.json",["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"])
client = gspread.authorize(credential)
gsheet = client.open("GTPS").sheet1



@app.route('/')
def start():
    return login()

@app.route('/accept',methods=['GET','POST'])
def accept():
    if(request.method == 'POST'):
        regnos = request.form.get('accept')
        print(regnos)
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        cur.execute("insert into pass select * from temp_pass where regno = (?)",(regnos,))
        cur.execute("select * from pass")
        t = cur.fetchall()
        print(t)
        for i in range(len(t)):
            print(t[i])
            gsheet.insert_row(t[i])
        cur.execute('delete from temp_pass where regno = (?)',(regnos,))
        conn.commit()
        conn.close()
        return index()
    return render_template('Acpt&Data.html')

@app.route('/dec',methods=['GET','POST'])
def dec():
    if(request.method == 'POST'):
        if(request.form.get('submit_button') == 'accept'):
            conn = sqlite3.connect('data.db')
            cur = conn.cursor()
            cur.execute("select * from temp_pass")
            t = cur.fetchall()
            conn.commit()
            conn.close()
            nos = len(t)
            names = list(map(itemgetter(0),t))
            regnos = list(map(itemgetter(1),t))
            students = list(map(itemgetter(2),t))
            phones = list(map(itemgetter(3),t))
            depts = list(map(itemgetter(4),t))
            years = list(map(itemgetter(5),t))
            dates = list(map(itemgetter(6),t))
            times = list(map(itemgetter(7),t))
            purposes = list(map(itemgetter(8),t))
            indates = list(map(itemgetter(9),t))
            intimes = list(map(itemgetter(10),t))
            print(nos)
            return render_template('Accept.html',n = nos,a=names,b=regnos,c=students,d=phones,e=depts,f=years,g=dates,h=times,j=purposes,k=indates,l=intimes,m=regnos)
        elif(request.form.get('submit_button') == 'view'):
            return index()
    return render_template('Acpt&Data.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        adminpass = request.form.get('adminpass')
        adminname = request.form.get('adminname')
        username = request.form.get('username')
        password = request.form.get('password')
        if(adminname == 'admin' and adminpass == 'Care@360'):
            return dec()
        elif(username == 'student' and password == 'Care@123'):
            return(render_template('Gate Pass Generator.html'))
        else:
            return(render_template("TT.html",x="Wrong Credentials !!!"))
    return(render_template('TT.html'))

@app.route('/user',methods=['GET','POST'])
def home():
    if request.method == 'POST':
        name = request.form.get('name')
        regno = request.form.get('regno')
        student = request.form.get('student')
        phone = request.form.get('phone')
        dept = request.form.get('dept')
        year = request.form.get('year')
        date = request.form.get('date')
        time = request.form.get('time')
        purpose = request.form.get('purpose')
        indate = request.form.get('indate')
        intime = request.form.get('intime')
        print(date)
        print(time)   
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO temp_pass VALUES(?,?,?,?,?,?,?,?,?,?,?)",(name,regno,student,phone,dept,year,date,time,purpose,indate,intime))
        cur.execute("select * from pass")
        t = cur.fetchall()
        for i in t:
            print(i)
        conn.commit()
        conn.close()
        return render_template('Result.html',a=name,b=regno,c=student,d=phone,e=dept,f=year,g=date,h=time,j=purpose,k=indate,l=intime)
    return render_template('Gate Pass Generator.html')
@app.route('/index')
def index():
    # dsg = list()
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    cur.execute("select * from pass")
    t = cur.fetchall()
    conn.commit()
    conn.close()
    nos = len(t)
    names = list(map(itemgetter(0),t))
    regnos = list(map(itemgetter(1),t))
    students = list(map(itemgetter(2),t))
    phones = list(map(itemgetter(3),t))
    depts = list(map(itemgetter(4),t))
    years = list(map(itemgetter(5),t))
    dates = list(map(itemgetter(6),t))
    times = list(map(itemgetter(7),t))
    purposes = list(map(itemgetter(8),t))
    indates = list(map(itemgetter(9),t))
    intimes = list(map(itemgetter(10),t))
    print(nos)
    return render_template('Gate Pass Index.html',n = nos,a=names,b=regnos,c=students,d=phones,e=depts,f=years,g=dates,h=times,j=purposes,k=indates,l=intimes)

if __name__ == "__main__":
    app.run(debug=True)