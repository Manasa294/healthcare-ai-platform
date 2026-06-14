from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Patient(db.Model):

    __tablename__ = "patients"

    patient_id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100)
    )

    age = db.Column(
        db.Integer
    )
    email = db.Column(
        db.String(100)
    )

    gender = db.Column(
        db.String(20)
    )

    address = db.Column(
        db.String(200)
    )

    previous_noshows = db.Column(
        db.Integer,
        default=0
    )

    sms_received = db.Column(
        db.Integer,
        default=1
    )
class Doctor(db.Model):

    __tablename__ = "doctors"

    doctor_id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100)
    )

    specialization = db.Column(
        db.String(100)
    )


class Appointment(db.Model):

    __tablename__ = "appointments"

    appointment_id = db.Column(
        db.Integer,
        primary_key=True
    )

    patient_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "patients.patient_id"
        )
    )

    doctor_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "doctors.doctor_id"
        )
    )

    appointment_date = db.Column(
        db.String(50)
    )

    status = db.Column(
        db.String(50)
    )


class Prediction(db.Model):

    __tablename__ = "predictions"

    prediction_id = db.Column(
        db.Integer,
        primary_key=True
    )

    appointment_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "appointments.appointment_id"
        )
    )

    risk_score = db.Column(
        db.Float
    )

    prediction_date = db.Column(
        db.String(50)
    )