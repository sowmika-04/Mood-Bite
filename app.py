from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db  # Centralized DB access
from routes import explore_bp  # Blueprint for /explore

app = Flask(__name__)
app.secret_key = 'moodscoop_super_secret_123'  # Needed for session management

# Register Blueprints
app.register_blueprint(explore_bp)  # Routes for /explore page

# Home Page
@app.route('/')
def index():
    return render_template("index.html")


# Handle Mood Recommendation
@app.route('/recommend', methods=['POST'])
def recommend():
    mood = request.form.get('mood')
    note = request.form.get('note')

    flavor_map = {
        "happy": "Sunny Mango Sorbet",
        "sad": "Chocolate Fudge Brownie",
        "excited": "Rainbow Sherbet",
        "calm": "Lavender Honey",
        "angry": "Spicy Cinnamon",
        "bored": "Classic Vanilla",
        "romantic": "Strawberry Cheesecake",
        "anxious": "Mint Chocolate Chip"
    }

    flavor = flavor_map.get(mood.lower(), "Vanilla Dream")

    return render_template("suggestion.html", mood=mood.capitalize(), flavor=flavor, note=note)

# Registration Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        hashed_password = generate_password_hash(password)
        db = get_db()
        cursor = db.cursor()

        try:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                           (username, email, hashed_password))
            db.commit()
            return redirect(url_for('login'))
        except Exception as e:
            return f"Registration failed: {e}"

    return render_template('register.html')

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        db = get_db()  # Get DB connection
        cursor = db.cursor()
        query = "SELECT id, password FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        if result and check_password_hash(result[1], password):
            session['username'] = username
            session['user_id'] = result[0]
            return redirect(url_for('explore.explore'))  # Redirect to explore page
        else:
            error = "Invalid username or password"

    return render_template('login.html', error=error)

# Logout Route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
@app.route('/mood')
def mood_input():
    return render_template("mood_input.html")
from flask import request, render_template

@app.route('/order')
def order():
    flavor = request.args.get('flavor', 'Default Flavor')  # get flavor from URL param
    return render_template('order.html', flavor=flavor)


if __name__ == '__main__':
    app.run(debug=True)
