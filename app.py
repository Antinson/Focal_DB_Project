from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/logout')
def logout():
    return render_template('logout.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/addcamera')
def addcamera():
    return render_template('addcamera.html')

@app.route('/editcamera')
def editcamera():
    return render_template('editcamera.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
