pip install flask flask-login scikit-learn numpy
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np
import pickle

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a strong key

login_manager = LoginManager()
login_manager.init_app(app)

# Fake News Detection Model (you can replace this with your own trained model)
class FakeNewsDetector:
    def __init__(self):
        # Example of training a simple model
        self.vectorizer = CountVectorizer(stop_words='english')
        self.model = MultinomialNB()

        # Sample dataset for fake news detection
        fake_news = ["This is fake news", "This is real news"]
        labels = [1, 0]  # 1 = fake, 0 = real

        # Vectorize the text and train the model
        X = self.vectorizer.fit_transform(fake_news)
        self.model.fit(X, labels)

    def predict(self, text):
        X = self.vectorizer.transform([text])
        prediction = self.model.predict(X)
        return "Fake" if prediction[0] == 1 else "Real"

# Initialize fake news detector
fake_news_detector = FakeNewsDetector()

# User management
class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# User data (In a production environment, use a database)
users = {'testuser': {'password': 'password123'}}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for('dashboard'))

        flash('Invalid credentials', 'danger')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Add new user to the users dictionary
        if username not in users:
            users[username] = {'password': password}
            flash('Registration successful', 'success')
            return redirect(url_for('login'))

        flash('User already exists', 'danger')

    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    news_text = ""
    prediction = ""
    if request.method == 'POST':
        news_text = request.form['news_text']
        prediction = fake_news_detector.predict(news_text)
    
    return render_template('dashboard.html', prediction=prediction, news_text=news_text)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
