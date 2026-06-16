
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///healthcare.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/patients')
def patients():
    return render_template('patients.html')

@app.route('/prediction')
def prediction():
    return render_template('prediction.html')

@app.route('/forecast')
def forecast():
    return render_template('forecast.html')

if __name__ == "__main__":
    app.run(debug=True)
