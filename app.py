from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "mysecretkey"

# ==================== POSTGRESQL DATABASE CONFIG ====================
# Render-ல் காப்பி செய்த Internal Database URL-ஐ கீழே உள்ள ஒற்றை மேற்கோள் குறிக்குள் (' ') பேஸ்ட் செய்யவும்.
# குறிப்பு: லிங்க் 'postgres://' என்று தொடங்கினால், அதை 'postgresql://' என்று மாற்றவும்.
app.config['SQLALCHEMY_DATABASE_URI'] = 'உங்களோட_Render_Internal_Database_URL_இங்கே_போடவும்'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==================== DATABASE MODELS (TABLES) ====================
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Result(db.Model):
    __tablename__ = 'results'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    test_type = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer, nullable=False)

# ஆன்லைனில் ரன் ஆகும்போது தானாக டேபிள்களை உருவாக்க இது உதவும்
with app.app_context():
    db.create_all()

print("PostgreSQL Database Connected & Tables Checked Successfully!")


# ==================== LOGIN ROUTE ====================
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # SQLAlchemy மூலம் பயனர் விவரங்களைச் சரிபார்த்தல்
        user = User.query.filter_by(username=username, password=password).first()
        
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
        
        # புதிய பயனரை உருவாக்குதல்
        new_user = User(fullname=fullname, email=email, username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        
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

    # SQLAlchemy மூலம் தேர்வுகளின் எண்ணிக்கையைக் கணக்கிடுதல்
    aptitude_count = Result.query.filter_by(username=session['username'], test_type='Aptitude').count()
    technical_count = Result.query.filter_by(username=session['username'], test_type='Technical').count()

    return render_template(
        'dashboard.html',
        username=session['username'],
        aptitude_count=aptitude_count,
        technical_count=technical_count
    )


# ==================== CHECK APTITUDE ====================
@app.route('/check_aptitude', methods=['POST'])
def check_aptitude():
    if 'username' not in session:
        return redirect(url_for('login'))

    score = 0
    q1 = request.form.get('q1')
    q2 = request.form.get('q2')

    if q1 == "10":
        score += 1
    if q2 == "20":
        score += 1

    # தேர்வு முடிவைச் சேமித்தல்
    new_result = Result(username=session['username'], test_type='Aptitude', score=score)
    db.session.add(new_result)
    db.session.commit()

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
    if 'username' not in session:
        return redirect(url_for('login'))

    score = 0
    if request.form.get('q1') == "Python":
        score += 1
    if request.form.get('q2') == "Programming Language":
        score += 1
    if request.form.get('q3') == "Structured Query Language":
        score += 1
    if request.form.get('q4') == "Database Management System":
        score += 1

    # தேர்வு முடிவைச் சேமித்தல்
    new_result = Result(username=session['username'], test_type='Technical', score=score)
    db.session.add(new_result)
    db.session.commit()

    return render_template("result.html", score=score, total=4)


# ==================== HR ROUTE ====================
@app.route('/hr')
def hr():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('hr.html')


# ==================== SUBMIT HR ====================
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