"""
Babylab database Fask application
"""

import os
from functools import wraps
import datetime
import requests
from flask import Flask, render_template, request, redirect, url_for, flash
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
    return render_template("participants.html", data=data, data_dict=data_dict)


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
    data: dict = None,
):
    """Studies page"""
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

        data = utils.prepare_studies(records, data_dict=data_dict, study=selected_study)

        return render_template(
            "studies.html",
            data_dict=data_dict,
            selected_study=selected_study,
            data=data,
        )
    return render_template("studies.html", data_dict=data_dict, data=data)


@app.route("/questionnaires/")
@token_required
def questionnaires(records: api.Records = None, data_dict: dict = None):
    """Participants database"""
    if records is None:
        records = api.Records(url=app.config["API_URL"], token=app.config["API_KEY"])
    data_dict = api.get_data_dict(
        url=app.config["API_URL"], token=app.config["API_KEY"]
    )
    data = utils.prepare_questionnaires(records, data_dict=data_dict)
    return render_template("questionnaires.html", data=data, data_dict=data_dict)


@app.route("/participants/<string:ppt_id>/questionnaires/<string:quest_id>")
@token_required
def questionnaire_id(
    records: api.Records = None,
    ppt_id: str = None,
    quest_id: str = None,
    data: dict = None,
):
    """Show a language questionnaire"""
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
    data = records.questionnaires.records[quest_id].data
    data = utils.replace_labels(data, data_dict=data_dict)
    # for k, v in data.items():
    #     dict_key = "language_" + k
    #     if dict_key in data_dict and v:
    #         data[k] = data_dict[dict_key][v]
    return render_template(
        "questionnaire_id.html",
        ppt_id=ppt_id,
        quest_id=quest_id,
        data=data,
    )


@app.route(
    "/participants/<string:ppt_id>/questionnaires/questionnaire_new",
    methods=["GET", "POST"],
)
@token_required
def questionnaire_new(ppt_id: str, data_dict: dict = None):
    """New langage questionnaire page"""
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
            "redcap_repeat_instrument": "language",
            "language_updated": date_now,
            "language_lang1": (
                finput["inputLang1"] if "inputLang1" in finput.keys() else "0"
            ),
            "language_lang1_exp": finput["inputLang1Exp"],
            "language_lang2": (
                finput["inputLang2"] if "inputLang2" in finput.keys() else "0"
            ),
            "language_lang2_exp": finput["inputLang2Exp"],
            "language_lang3": (
                finput["inputLang3"] if "inputLang3" in finput.keys() else "0"
            ),
            "language_lang3_exp": finput["inputLang3Exp"],
            "language_lang4": (
                finput["inputLang4"] if "inputLang4" in finput.keys() else "0"
            ),
            "language_lang4_exp": finput["inputLang4Exp"],
            "language_comments": finput["inputComments"],
            "language_complete": "2",
        }
        api.add_questionnaire(
            data,
            url=app.config["API_URL"],
            token=app.config["API_KEY"],
        )
        try:
            flash("Questionnaire added!", "success")
            return redirect(url_for("questionnaires"))
        except requests.exceptions.HTTPError as e:
            flash(f"Something went wrong! {e}", "error")
            return redirect(url_for("questionnaires"))
    return render_template("questionnaire_new.html", ppt_id=ppt_id, data_dict=data_dict)


@app.route(
    "/participants/<string:ppt_id>/questionnaires/<string:quest_id>/questionnaire_modify",
    methods=["GET", "POST"],
)
@token_required
def questionnaire_modify(
    quest_id: str,
    ppt_id: str,
    data_dict: dict = None,
):
    """Modify language questionnaire page"""
    if data_dict is None:
        data_dict = api.get_data_dict(
            url=app.config["API_URL"], token=app.config["API_KEY"]
        )
    data = (
        api.Records(url=app.config["API_URL"], token=app.config["API_KEY"])
        .questionnaires.records[quest_id]
        .data
    )
    for k, v in data.items():
        if "exp" in k:
            data[k] = str(round(v, None) * 100)
    if request.method == "POST":
        finput = request.form
        date_now = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M")
        data = {
            "record_id": ppt_id,
            "redcap_repeat_instance": quest_id.split(":")[1],
            "redcap_repeat_instrument": "language",
            "language_updated": date_now,
            "language_lang1": finput["inputLang1"],
            "language_lang1_exp": finput["inputLang1Exp"],
            "language_lang2": finput["inputLang2"],
            "language_lang2_exp": finput["inputLang2Exp"],
            "language_lang3": finput["inputLang3"],
            "language_lang3_exp": finput["inputLang3Exp"],
            "language_lang4": finput["inputLang4"],
            "language_lang4_exp": finput["inputLang4Exp"],
            "language_comments": finput["inputComments"],
            "language_complete": "2",
        }
        try:
            api.add_questionnaire(
                data,
                url=app.config["API_URL"],
                token=app.config["API_KEY"],
            )
            flash("Questionnaire modified!", "success")
            return redirect(url_for("questionnaires"))
        except requests.exceptions.HTTPError as e:
            flash(f"Something went wrong! {e}", "error")
            return render_template("questionnaires.html", ppt_id=ppt_id)
    return render_template(
        "questionnaire_modify.html",
        ppt_id=ppt_id,
        quest_id=quest_id,
        data=data,
        data_dict=data_dict,
    )
