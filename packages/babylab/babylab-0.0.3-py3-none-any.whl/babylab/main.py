"""
Babylab database Fask application
"""

import os
import collections
from functools import wraps
import datetime
import requests
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.exceptions import NotFound
from babylab import api
from babylab import utils

app = Flask(__name__, template_folder="templates")
app.secret_key = os.urandom(24)
app.permanent_session_lifetime = datetime.timedelta(minutes=10)

app.config["API_URL"] = "https://apps.sjdhospitalbarcelona.org/redcap/api/"
app.config["API_KEY"] = ""


def token_required(f):
    """Require login"""

    @wraps(f)
    def decorated(*args, **kwargs):
        redcap_version = api.get_redcap_version(
            url=app.config["API_URL"], token=app.config["API_KEY"]
        )
        if redcap_version:
            return f(*args, **kwargs)
        flash("Access restricted. Please, log in", "error")
        return redirect(url_for("index", redcap_version=redcap_version))

    return decorated


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index(redcap_version: str = None):
    """Index page"""
    if not redcap_version:
        redcap_version = api.get_redcap_version(
            url=app.config["API_URL"], token=app.config["API_KEY"]
        )
    if request.method == "POST":
        finput = request.form
        app.config["API_KEY"] = finput["apiToken"]
        redcap_version = api.get_redcap_version(
            url=app.config["API_URL"], token=app.config["API_KEY"]
        )
        if redcap_version:
            flash("Logged in", "success")
            return render_template("index.html", redcap_version=redcap_version)
        flash("Incorrect token", "error")
    return render_template("index.html", redcap_version=redcap_version)


@app.route("/dashboard")
@token_required
def dashboard(records: api.Records = None, data: dict = None):
    """Dashboard page"""
    redcap_version = api.get_redcap_version(
        url=app.config["API_URL"], token=app.config["API_KEY"]
    )
    if records is None:
        try:
            records = api.Records(
                url=app.config["API_URL"], token=app.config["API_KEY"]
            )
        except Exception:  # pylint: disable=broad-exception-caught
            return redirect(url_for("index", redcap_version=redcap_version))
    data_dict = api.get_data_dict(
        url=app.config["API_URL"], token=app.config["API_KEY"]
    )
    data = utils.prepare_dashboard(records, data_dict)
    return render_template("dashboard.html", data=data)


@app.route("/participants/")
@token_required
def participants(records: api.Records = None, data_dict: dict = None):
    """Participants database"""
    if records is None:
        records = api.Records(url=app.config["API_URL"], token=app.config["API_KEY"])
    data_dict = api.get_data_dict(
        url=app.config["API_URL"], token=app.config["API_KEY"]
    )
    data = utils.prepare_participants(records, data_dict=data_dict)
    return render_template("participants.html", data=data, data_dict = data_dict)


@app.route("/participants/<string:ppt_id>")
@token_required
def record_id(records: api.Records = None, ppt_id: str = None, data_dict: dict = None):
    """Show the record_id for that participant"""
    if data_dict is None:
        data_dict = api.get_data_dict(
            url=app.config["API_URL"], token=app.config["API_KEY"]
        )
    redcap_version = api.get_redcap_version(
        url=app.config["API_URL"], token=app.config["API_KEY"]
    )
    if records is None:
        try:
            records = api.Records(
                url=app.config["API_URL"], token=app.config["API_KEY"]
            )
        except Exception:  # pylint: disable=broad-exception-caught
            return redirect(url_for("index", redcap_version=redcap_version))
    data = utils.prepare_record_id(ppt_id, records, data_dict)
    return render_template(
        "record_id.html",
        ppt_id=ppt_id,
        data=data,
    )


@app.route("/participant_new", methods=["GET", "POST"])
@token_required
def participant_new(data_dict: dict = None):
    """New participant page"""
    if data_dict is None:
        data_dict = api.get_data_dict(
            url=app.config["API_URL"], token=app.config["API_KEY"]
        )
    if request.method == "POST":
        finput = request.form
        date_now = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M")
        data = {
            "record_id": "0",
            "participant_date_added": date_now,
            "participant_name": finput["inputName"],
            "participant_age_now_months": finput["inputAgeMonths"],
            "participant_age_now_days": finput["inputAgeDays"],
            "participant_sex": finput["inputSex"],
            "participant_twin": finput["inputTwinID"],
            "participant_parent1_name": finput["inputParent1Name"],
            "participant_parent1_surname": finput["inputParent1Surname"],
            "participant_parent2_name": finput["inputParent2Name"],
            "participant_parent2_surname": finput["inputParent2Surname"],
            "participant_email1": finput["inputEmail1"],
            "participant_phone1": finput["inputPhone1"],
            "participant_email2": finput["inputEmail2"],
            "participant_phone2": finput["inputPhone2"],
            "participant_address": finput["inputAddress"],
            "participant_city": finput["inputCity"],
            "participant_postcode": finput["inputPostcode"],
            "participant_birth_type": finput["inputDeliveryType"],
            "participant_gest_weeks": finput["inputGestationalWeeks"],
            "participant_birth_weight": finput["inputBirthWeight"],
            "participant_head_circumference": finput["inputHeadCircumference"],
            "participant_apgar1": finput["inputApgar1"],
            "participant_apgar2": finput["inputApgar2"],
            "participant_apgar3": finput["inputApgar3"],
            "participant_hearing": finput["inputNormalHearing"],
            "participant_diagnoses": finput["inputDiagnoses"],
            "participant_comments": finput["inputComments"],
            "participants_complete": "2",
        }
        api.add_participant(
            data,
            modifying=False,
            url=app.config["API_URL"],
            token=app.config["API_KEY"],
        )
        try:
            flash("Participant added!", "success")
            return redirect(url_for("participants"))
        except requests.exceptions.HTTPError as e:
            flash(f"Something went wrong! {e}", "error")
            return redirect(url_for("participant_new", data_dict=data_dict))
    return render_template("participant_new.html", data_dict=data_dict)


@app.route("/participants/<string:ppt_id>/participant_modify", methods=["GET", "POST"])
@token_required
def participant_modify(
    ppt_id: str, records: api.Records = None, data: dict = None, data_dict: dict = None
):
    """Modify participant page"""
    if data_dict is None:
        data_dict = api.get_data_dict(
            url=app.config["API_URL"], token=app.config["API_KEY"]
        )
    if records is None:
        data = (
            api.Records(url=app.config["API_URL"], token=app.config["API_KEY"])
            .participants.records[ppt_id]
            .data
        )
    if request.method == "POST":
        finput = request.form
        date_now = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M")
        data = {
            "record_id": ppt_id,
            "participant_date_added": date_now,
            "participant_name": finput["inputName"],
            "participant_age_now_months": finput["inputAgeMonths"],
            "participant_age_now_days": finput["inputAgeDays"],
            "participant_sex": finput["inputSex"],
            "participant_twin": finput["inputTwinID"],
            "participant_parent1_name": finput["inputParent1Name"],
            "participant_parent1_surname": finput["inputParent1Surname"],
            "participant_parent2_name": finput["inputParent2Name"],
            "participant_parent2_surname": finput["inputParent2Surname"],
            "participant_email1": finput["inputEmail1"],
            "participant_phone1": finput["inputPhone1"],
            "participant_email2": finput["inputEmail2"],
            "participant_phone2": finput["inputPhone2"],
            "participant_address": finput["inputAddress"],
            "participant_city": finput["inputCity"],
            "participant_postcode": finput["inputPostcode"],
            "participant_birth_type": finput["inputDeliveryType"],
            "participant_gest_weeks": finput["inputGestationalWeeks"],
            "participant_birth_weight": finput["inputBirthWeight"],
            "participant_head_circumference": finput["inputHeadCircumference"],
            "participant_apgar1": finput["inputApgar1"],
            "participant_apgar2": finput["inputApgar2"],
            "participant_apgar3": finput["inputApgar3"],
            "participant_hearing": finput["inputNormalHearing"],
            "participant_diagnoses": finput["inputDiagnoses"],
            "participant_comments": finput["inputComments"],
            "participants_complete": "2",
        }
        try:
            api.add_participant(
                data,
                modifying=True,
                url=app.config["API_URL"],
                token=app.config["API_KEY"],
            )
        except requests.exceptions.HTTPError as e:
            flash(f"Something went wrong! {e}", "error")
            return render_template(
                "participant_modify.html", ppt_id=ppt_id, data=data, data_dict=data_dict
            )
    return render_template(
        "participant_modify.html", ppt_id=ppt_id, data=data, data_dict=data_dict
    )


@app.route("/appointments/")
@token_required
def appointments(records: api.Records = None, data_dict: dict = None):
    """Appointments database"""
    if records is None:
        records = api.Records(url=app.config["API_URL"], token=app.config["API_KEY"])
    data_dict = api.get_data_dict(
        url=app.config["API_URL"], token=app.config["API_KEY"]
    )
    data = utils.prepare_appointments(records, data_dict=data_dict)
    return render_template("appointments.html", data=data)


@app.route("/appointments/<string:appt_id>")
@token_required
def appointment_id(
    records: api.Records = None, appt_id: str = None, data_dict: dict = None
):
    """Show the record_id for that appointment"""
    if data_dict is None:
        data_dict = api.get_data_dict(
            url=app.config["API_URL"], token=app.config["API_KEY"]
        )
    if records is None:
        try:
            records = api.Records(
                url=app.config["API_URL"], token=app.config["API_KEY"]
            )
        except Exception:  # pylint: disable=broad-exception-caught
            return render_template("index.html", login_status="incorrect")
    data = records.appointments.records[appt_id].data
    for k, v in data.items():
        dict_key = "appointment_" + k
        if dict_key in data_dict and v:
            data[k] = data_dict[dict_key][v]
    participant = records.participants.records[data["record_id"]].data
    participant["age_now_months"] = str(participant["age_now_months"])
    participant["age_now_days"] = str(participant["age_now_days"])
    return render_template(
        "appointment_id.html",
        appt_id=appt_id,
        ppt_id=data["record_id"],
        data=data,
        participant=participant,
    )


@app.route("/participants/<string:ppt_id>/appointment_new", methods=["GET", "POST"])
@token_required
def appointment_new(ppt_id: str, data_dict: dict = None):
    """New appointment page"""
    if data_dict is None:
        data_dict = api.get_data_dict(
            url=app.config["API_URL"], token=app.config["API_KEY"]
        )
    if request.method == "POST":
        finput = request.form
        date_now = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M")
        data = {
            "record_id": ppt_id,
            "redcap_repeat_instance": "new",
            "redcap_repeat_instrument": "appointments",
            "appointment_study": finput["inputStudy"],
            "appointment_date_made": date_now,
            "appointment_date": finput["inputDate"],
            "appointment_taxi_address": finput["inputTaxiAddress"],
            "appointment_taxi_isbooked": (
                "1" if "inputTaxiIsbooked" in finput.keys() else "0"
            ),
            "appointment_status": finput["inputStatus"],
            "appointment_comments": finput["inputComments"],
            "appointments_complete": "2",
        }
        try:
            api.add_appointment(
                data, url=app.config["API_URL"], token=app.config["API_KEY"]
            )
            flash("Appointment added!", "success")
            records = api.Records(
                url=app.config["API_URL"], token=app.config["API_KEY"]
            )
            return redirect(url_for("appointments", records=records))
        except requests.exceptions.HTTPError as e:
            flash(f"Something went wrong! {e}", "error")
            return render_template(
                "appointment_new.html", ppt_id=ppt_id, data_dict=data_dict
            )
    return render_template("appointment_new.html", ppt_id=ppt_id, data_dict=data_dict)


@app.route(
    "/participants/<string:ppt_id>/<string:appt_id>/appointment_modify",
    methods=["GET", "POST"],
)
@token_required
def appointment_modify(
    appt_id: str,
    ppt_id: str,
    records: api.Records = None,
    data_dict: dict = None,
):
    """Modify appointment page"""
    if data_dict is None:
        data_dict = api.get_data_dict(
            url=app.config["API_URL"], token=app.config["API_KEY"]
        )
    if records is None:
        data = (
            api.Records(url=app.config["API_URL"], token=app.config["API_KEY"])
            .appointments.records[appt_id]
            .data
        )
        for k, v in data.items():
            dict_key = "appointment_" + k
            if dict_key in data_dict and v:
                data[k] = data_dict[dict_key][v]
    if request.method == "POST":
        finput = request.form
        date_now = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M")
        data = {
            "record_id": ppt_id,
            "redcap_repeat_instance": appt_id.split(":")[1],
            "redcap_repeat_instrument": "appointments",
            "appointment_study": finput["inputStudy"],
            "appointment_date_made": date_now,
            "appointment_date": finput["inputDate"],
            "appointment_taxi_address": finput["inputTaxiAddress"],
            "appointment_taxi_isbooked": (
                "1" if "inputTaxiIsbooked" in finput.keys() else "0"
            ),
            "appointment_status": finput["inputStatus"],
            "appointment_comments": finput["inputComments"],
            "appointments_complete": "2",
        }
        try:
            api.add_appointment(
                data,
                url=app.config["API_URL"],
                token=app.config["API_KEY"],
            )
            flash("Appointment modified!", "success")
            return redirect(url_for("appointments"))
        except requests.exceptions.HTTPError as e:
            flash(f"Something went wrong! {e}", "error")
            return render_template("appointments.html", ppt_id=ppt_id, appt_id=appt_id)
    return render_template(
        "appointment_modify.html",
        ppt_id=ppt_id,
        appt_id=appt_id,
        data=data,
        data_dict=data_dict,
    )


@app.route("/studies", methods=["GET", "POST"])
@token_required
def studies(
    records: api.Records = None,
    selected_study: str = None,
    data_dict: dict = None,
    apts=None,
    n_apts=None,
    date_labels=None,
    date_values=None,
):
    """Studies page"""
    # get data_dictionary
    if data_dict is None:
        data_dict = api.get_data_dict(
            url=app.config["API_URL"], token=app.config["API_KEY"]
        )
    if request.method == "POST":
        finput = request.form
        selected_study = finput["inputStudy"]
        redcap_version = api.get_redcap_version(
            url=app.config["API_URL"], token=app.config["API_KEY"]
        )
        if records is None:
            try:
                records = api.Records(
                    url=app.config["API_URL"], token=app.config["API_KEY"]
                )
            except Exception:  # pylint: disable=broad-exception-caught
                return redirect(url_for("index", redcap_version=redcap_version))
        apts = utils.get_appointments_table(records, data_dict=data_dict)
        apts = apts[apts["study"] == selected_study]
        classes = "table table-striped table-hover table-sm table-condensed"
        apts["appointment_id"] = [
            f"<a href=/appointments/{i}>{i}</a>" for i in apts["appointment_id"]
        ]
        apts["record_id"] = [f"<a href=/participants/{i}>{i}</a>" for i in apts.index]
        apts["age_now"] = [
            f"{m}:{d}" for m, d in zip(apts["age_now_months"], apts["age_now_days"])
        ]
        apts["age_apt"] = [
            f"{m}:{d}" for m, d in zip(apts["age_now_months"], apts["age_now_days"])
        ]
        apts = apts[
            [
                "appointment_id",
                "record_id",
                "date",
                "age_apt",
                "age_now",
                "date_made",
                "taxi_address",
                "taxi_isbooked",
                "status",
                "comments",
            ]
        ]
        apts = apts.rename(
            columns={
                "appointment_id": "Appointment ID",
                "record_id": "Participant ID",
                "date": "Date",
                "age_apt": "Age",
                "age_now": "Age now",
                "date_made": "Made on the",
                "taxi_address": "Taxi address",
                "taxi_isbooked": "Taxi booked",
                "status": "Appointment status",
                "comments": "Comments",
            }
        )
        n_apts = apts.shape[0]
        date = apts["Date"].value_counts().to_dict()
        date = collections.OrderedDict(sorted(date.items()))
        for idx, (k, v) in enumerate(date.items()):
            if idx > 0:
                date[k] = v + list(date.values())[idx - 1]
        apts.reset_index(inplace=True)

        return render_template(
            "studies.html",
            data_dict=data_dict,
            selected_study=selected_study,
            apts=apts.to_html(
                classes=classes,
                escape=False,
                justify="left",
                index=False,
                bold_rows=True,
            ),
            n_apts=n_apts,
            date_labels=list(date.keys()),
            date_values=list(date.values()),
        )
    return render_template(
        "studies.html",
        data_dict=data_dict,
        n_apts=n_apts,
        date_labels=date_labels,
        date_values=date_values,
    )


@token_required
@app.errorhandler(NotFound)
def page_not_found(e):
    """Error 404 page"""
    return render_template("404.html", e=e), 404
