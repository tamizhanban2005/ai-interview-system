import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "mysecretkey"

# Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="ai_interview_system"
)

print("Database Connected")

# ==================== LOGIN ROUTE ====================
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )
        user = cursor.fetchone()
        cursor.close()
        
        if user:
            session['username'] = username
            return redirect(url_for('dashboard'))  
        else:
            return "Invalid Username or Password"

    return render_template('login.html')


# ==================== REGISTER ROUTE ====================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO users (fullname, email, username, password) VALUES (%s, %s, %s, %s)",
            (fullname, email, username, password)
        )
        db.commit()
        cursor.close()
        return redirect(url_for('login'))

    return render_template('register.html')


# ==================== RESULT ROUTE ====================
@app.route('/result')
def result():
    return render_template('result.html')


# ==================== DASHBOARD ROUTE ====================
@app.route('/dashboard')
def dashboard():

    if 'username' not in session:
        return redirect(url_for('login'))

    cursor = db.cursor()

    # Aptitude count
    cursor.execute(
        "SELECT COUNT(*) FROM results WHERE username=%s AND test_type='Aptitude'",
        (session['username'],)
    )
    aptitude_count = cursor.fetchone()[0]

    # Technical count
    cursor.execute(
        "SELECT COUNT(*) FROM results WHERE username=%s AND test_type='Technical'",
        (session['username'],)
    )
    technical_count = cursor.fetchone()[0]

    cursor.close()

    return render_template(
        'dashboard.html',
        username=session['username'],
        aptitude_count=aptitude_count,
        technical_count=technical_count
    )
# ==================== CHECK APTITUDE ====================
@app.route('/check_aptitude', methods=['POST'])
def check_aptitude():

    score = 0

    q1 = request.form.get('q1')
    q2 = request.form.get('q2')

    if q1 == "10":
        score += 1

    if q2 == "20":
        score += 1

    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO results (username, test_type, score) VALUES (%s, %s, %s)",
        (session['username'], 'Aptitude', score)
    )

    db.commit()
    cursor.close()

    return render_template("result.html", score=score, total=2)

# ==================== APTITUDE ROUTE ====================
@app.route('/aptitude')
def aptitude():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('aptitude.html')


# ==================== LOGOUT ROUTE ====================
@app.route('/logout')
def logout():
    session.pop('username', None) 
    return redirect(url_for('login'))


# ==================== TECHNICAL ROUTE ====================
@app.route('/technical')
def technical():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('technical.html')


# ==================== CHECK TECHNICAL ====================
@app.route('/check_technical', methods=['POST'])
def check_technical():

    score = 0

    if request.form.get('q1') == "Python":
        score += 1

    if request.form.get('q2') == "Programming Language":
        score += 1

    if request.form.get('q3') == "Structured Query Language":
        score += 1

    if request.form.get('q4') == "Database Management System":
        score += 1

    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO results (username, test_type, score) VALUES (%s, %s, %s)",
        (session['username'], 'Technical', score)
    )

    db.commit()
    cursor.close()

    return render_template("result.html", score=score, total=4)
#=====================hr============
@app.route('/hr')
def hr():
    if 'username' not in session:
        return redirect(url_for('login'))

    return render_template('hr.html')

#=====submit hr====
@app.route('/submit_hr', methods=['POST'])
def submit_hr():

    return """
    <h1>HR Round Submitted Successfully ✅</h1>
    <br>
    <a href='/dashboard'>
        <button>Back to Dashboard</button>
    </a>
    """

# ==================== MAIN START ====================
if __name__ == '__main__':
    app.run(debug=True)