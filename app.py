from flask import Flask,render_template,request,redirect,session
import sqlite3

app = Flask(__name__)
app.secret_key="secret123"

def connect_db():
    return sqlite3.connect("database.db")

# create tables
def init_db():
    conn=connect_db()
    cur=conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT)
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    task TEXT,
    deadline TEXT,
    status TEXT)
    """)

    conn.commit()
    conn.close()

init_db()

# LOGIN PAGE
@app.route("/")
def login():
    return render_template("login.html")

# LOGIN
@app.route("/login",methods=["POST"])
def user_login():

    username=request.form["username"]
    password=request.form["password"]

    conn=connect_db()
    cur=conn.cursor()

    cur.execute("SELECT * FROM users WHERE username=? AND password=?",(username,password))

    user=cur.fetchone()

    if user:
        session["user"]=user[0]
        return redirect("/dashboard")
    else:
        return "Invalid Login"

# SIGNUP PAGE
@app.route("/signup")
def signup():
    return render_template("signup.html")

# REGISTER
@app.route("/register",methods=["POST"])
def register():

    username=request.form["username"]
    password=request.form["password"]

    conn=connect_db()
    cur=conn.cursor()

    cur.execute("INSERT INTO users(username,password) VALUES(?,?)",(username,password))

    conn.commit()
    conn.close()

    return redirect("/")

# DASHBOARD
@app.route("/dashboard")
def dashboard():

    user=session["user"]

    conn=connect_db()
    cur=conn.cursor()

    cur.execute("SELECT * FROM tasks WHERE user_id=?",(user,))
    tasks=cur.fetchall()

    return render_template("dashboard.html",tasks=tasks)

# ADD TASK
@app.route("/add",methods=["POST"])
def add():

    task=request.form["task"]
    deadline=request.form["deadline"]
    user=session["user"]

    conn=connect_db()
    cur=conn.cursor()

    cur.execute("INSERT INTO tasks(user_id,task,deadline,status) VALUES(?,?,?,?)",(user,task,deadline,"Pending"))

    conn.commit()
    conn.close()

    return redirect("/dashboard")

# COMPLETE TASK
@app.route("/complete/<int:id>")
def complete(id):

    conn=connect_db()
    cur=conn.cursor()

    cur.execute("UPDATE tasks SET status='Completed' WHERE id=?",(id,))

    conn.commit()
    conn.close()

    return redirect("/dashboard")

# DELETE TASK
@app.route("/delete/<int:id>")
def delete(id):

    conn=connect_db()
    cur=conn.cursor()

    cur.execute("DELETE FROM tasks WHERE id=?",(id,))

    conn.commit()
    conn.close()

    return redirect("/dashboard")

app.run(debug=True)