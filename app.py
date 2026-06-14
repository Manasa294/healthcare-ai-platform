from flask import Flask, render_template, request

import joblib
import numpy as np

from models import (
    db,
    Patient,
    Doctor,
    Appointment,
    Prediction
)

app = Flask(__name__)



def explain_risk(patient):

    reasons = []

    if patient.age > 65:
        reasons.append(
            "Age Above 65"
        )

    if patient.previous_noshows >= 2:
        reasons.append(
            "Multiple No Shows"
        )

    if patient.sms_received == 0:
        reasons.append(
            "No Reminder Sent"
        )

    return reasons
def send_reminder(patient):

    print(
        f"Email sent to {patient.email}"
    )

model = joblib.load(
    "ml/no_show_model.pkl"
)

# SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///healthcare.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Connect database to Flask
db.init_app(app)

# Create tables automatically
with app.app_context():
    db.create_all()


# Home Page
@app.route("/")
def home():
    return render_template("patient_form.html")


# Register Patient
@app.route("/register", methods=["POST"])
def register():

    patient = Patient(

    name=request.form["name"],

    age=int(
        request.form["age"]
    ),

    gender=
    request.form["gender"],

    address=
    request.form["address"],

    previous_noshows=
    int(
        request.form[
            "previous_noshows"
        ]
    ),

    sms_received=
    int(
        request.form[
            "sms_received"
        ]
    )
)
    db.session.add(patient)
    db.session.commit()

    return "Patient Saved Successfully"


# View All Patients
@app.route("/patients")
def patients():

    all_patients = Patient.query.all()

    result = "<h2>Patients List</h2>"

    for patient in all_patients:

        result += f"""
        ID: {patient.patient_id}<br>
        Name: {patient.name}<br>
        email={patient.email}<br>
        Age: {patient.age}<br>

        Gender: {patient.gender}<br>
        Address: {patient.address}<br>
        <hr>
        """

    return result
@app.route("/doctor")
def doctor():

    return render_template(
        "doctor_form.html"
    )



@app.route("/add_doctor", methods=["POST"])
def add_doctor():

    doctor = Doctor(
        name=request.form["name"],
        specialization=request.form["specialization"]
    )

    db.session.add(doctor)
    db.session.commit()

    return "Doctor Saved Successfully"


@app.route("/doctors")
def doctors():

    doctors = Doctor.query.all()

    result = "<h1>Doctors List</h1>"

    for doctor in doctors:

        result += f"""
        ID: {doctor.doctor_id}
        -
        Name: {doctor.name}
        -
        Specialization: {doctor.specialization}
        <br><br>
        """

    return result

@app.route("/appointment")
def appointment():

    return render_template(
        "appointment_form.html"
    )
@app.route(
    "/schedule_appointment",
    methods=["POST"]
)
def schedule_appointment():

    appointment = Appointment(

        patient_id=
        request.form["patient_id"],

        doctor_id=
        request.form["doctor_id"],

        appointment_date=
        request.form[
            "appointment_date"
        ],

        status="Scheduled"
    )

    db.session.add(
        appointment
    )

    db.session.commit()

    return (
        "Appointment Scheduled"
    )
@app.route("/appointments")
def appointments():

    appointments = (
        Appointment.query.all()
    )

    result = (
        "<h1>Appointments</h1>"
    )

    for a in appointments:

        result += f"""
        Appointment ID:
        {a.appointment_id}

        <br>

        Patient ID:
        {a.patient_id}

        <br>

        Doctor ID:
        {a.doctor_id}

        <br>

        Date:
        {a.appointment_date}

        <br>

        Status:
        {a.status}

        <hr>
        """

    return result

@app.route("/predict")
def predict():

    patient = Patient.query.first()

    if patient is None:
        return "No patient found"

    data = np.array([[
        patient.age,
        patient.previous_noshows,
        patient.sms_received
    ]])

    probability = model.predict_proba(
        data
    )[0][1]

    return (
        f"No Show Risk: "
        f"{round(probability*100,2)}%"
    )


@app.route("/predictions")
def predictions():

    predictions = Prediction.query.all()

    result = "<h1>Predictions</h1>"

    for p in predictions:

        result += f"""
        Risk Score:
        {p.risk_score}%

        <br>

        Date:
        {p.prediction_date}

        <hr>
        """
        return result
    
@app.route("/appointment/<int:id>")
def appointment_details(id):

    appointment = Appointment.query.get(id)

    if appointment is None:
        return "Appointment Not Found"

    patient = Patient.query.get(
        appointment.patient_id
    )

    return f"""
    <h1>Appointment Details</h1>

    Appointment ID:
    {appointment.appointment_id}

    <br><br>

    Patient:
    {patient.name}

    <br><br>

    Date:
    {appointment.appointment_date}
    """
@app.route("/predict/<int:id>")
def predict_appointment(id):

    appointment = Appointment.query.get(id)

    if appointment is None:
        return "Appointment Not Found"

    patient = Patient.query.get(
        appointment.patient_id
    )

    data = np.array([[
        patient.age,
        patient.previous_noshows,
        patient.sms_received
    ]])

    probability = (
        model.predict_proba(data)[0][1]
    )
    if probability > 0.70:
        send_reminder(
        patient
    )

    reasons = explain_risk(
        patient
    )

    return f"""
    <h1>
    Risk Score:
    {round(probability*100,2)}%
    </h1>

    <h2>
    Why?
    </h2>

    <ul>

    {''.join(
    f'<li>{reason}</li>'
    for reason in reasons
    )}

    </ul>
    """
@app.route("/dashboard")
def dashboard():

    return render_template(

        "dashboard.html",

        patients=Patient.query.count(),

        doctors=Doctor.query.count(),

        appointments=Appointment.query.count(),

        predictions=Prediction.query.count()
    )
@app.route("/high-risk")
def high_risk():

    predictions = (
        Prediction.query.filter(
            Prediction.risk_score >= 70
        ).all()
    )

    result = (
        "<h1>High Risk Patients</h1>"
    )

    for p in predictions:

        result += f"""
        Appointment:
        {p.appointment_id}

        <br>

        Risk:
        {p.risk_score}%

        <hr>
        """

    return result
@app.route("/risk-chart")

def risk_chart():

    predictions = Prediction.query.all()

    risks = [
        p.risk_score
        for p in predictions
    ]

    return str(risks)


if __name__ == "__main__":
    app.run(debug=True)


