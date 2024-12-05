#!/usr/bin/env python

"""
Functions to interact with the RedCAP API
"""
import re
import json
from collections import OrderedDict
from dataclasses import dataclass
import requests
import pandas as pd


class CredentialsMissingException(Exception):
    """Missing dotenv file

    Args:
        Exception (Exception): .env file missing.
    """

    def __init__(self):
        print("Could not find .env file")


class CredentialsKeysException(Exception):
    """Missing fields

    Args:
        Exception (Exception): If .env does not have "API_URL" and "API_KEY" fields.
    """

    def __init__(self):
        print("'API_URL' or 'API_KEY' fields missing in .env")


class CredentialsAuthException(Exception):
    """Incorrect credentials

    Args:
        Exception (Exception): If incorrect credentials to the RedCAP API.
    """

    def __init__(self):
        print("Incorrect credentials")


def redcap_login(url: str, token: str) -> None:
    """Log into RedCAP using API token.

    Raises:
        CredentialsError: If log in fails.

    Returns:
        dict: Dictionary of credentials.
    """
    return {"API_URL": url, "API_KEY": token}


def post_request(
    fields: dict,
    timeout: int = 10,
    **kwargs,
) -> dict:
    """Make a POST request to the REDCap database.

    Args:
        fields (dict): Fields to retrieve.
        file (str, optional): Path to the dotenv files with the credentials. Defaults to ".env".
        timeout (int, optional): Timeout of HTTP request in seconds. Defaults to 10.
        **kwargs: Additional aguments passed to ``requests.post``.
    Returns:
        dict: HTTP request response in JSON format.
    """
    creds = redcap_login(**kwargs)
    fields = OrderedDict(fields)
    fields["token"] = creds["API_KEY"]
    fields.move_to_end("token", last=False)
    r = requests.post(creds["API_URL"], data=fields, timeout=timeout)
    r.raise_for_status()
    return r


def get_redcap_version(**kwargs) -> str:
    """Get REDCap version.
    Args:
        **kwargs: Arguments passed to ``post_request``.
    Returns:
        str: REDCAp version number.
    """
    fields = {
        "content": "version",
    }
    try:
        r = post_request(fields=fields, **kwargs).content.decode("utf-8")
        return r
    except requests.exceptions.HTTPError:
        return ""


def get_records(**kwargs):
    """Return records as JSON.

    Args:
        url (str): REDCap URL.

    Returns:
        dict: REDCap records in JSON format.
    """
    fields = {
        "content": "record",
        "format": "json",
        "type": "flat",
    }
    return post_request(fields=fields, **kwargs).json()


def add_participant(data: dict, modifying: bool = False, **kwargs):
    """Add new participant to REDCap database.

    Args:
        data (dict): Participant data.
        modifying (bool, optional): Modifying existent participant?
        *kwargs: Additional arguments passed to ``post_request``.
    """
    fields = {
        "content": "record",
        "action": "import",
        "format": "json",
        "type": "flat",
        "overwriteBehavior": "normal" if modifying else "overwrite",
        "forceAutoNumber": "false" if modifying else "true",
        "data": f"[{json.dumps(data)}]",
    }
    return post_request(fields=fields, **kwargs)


def add_appointment(data: dict, **kwargs):
    """Add new appointment to REDCap database.

    Args:
        record_id (dict): ID of participant.
        data (dict): Appointment data.
        *kwargs: Additional arguments passed to ``post_request``.
    """
    fields = {
        "content": "record",
        "action": "import",
        "format": "json",
        "type": "flat",
        "overwriteBehavior": "overwrite",
        "forceAutoNumber": "false",
        "data": f"[{json.dumps(data)}]",
    }
    return post_request(fields=fields, **kwargs)


def get_data_dict(**kwargs):
    """Get data dictionaries for categorical variables

    Returns:
        **kwargs: Additional arguments passed tp ``post_request``.
    """
    items = [
        "participant_sex",
        "participant_birth_type",
        "participant_hearing",
        "appointment_study",
        "appointment_status",
    ]
    fields = {
        "token": "483E2949BD1C411C9B2781D27011A434",
        "content": "metadata",
        "format": "json",
        "returnFormat": "json",
    }

    for idx, i in enumerate(items):
        fields[f"fields[{idx}]"] = i
    r = json.loads(post_request(fields=fields, **kwargs).text)
    dicts = {}
    for k, v in zip(items, r):
        options = v["select_choices_or_calculations"].split(" | ")
        options_parsed = {}
        for o in options:
            x = o.split(", ")
            options_parsed[x[0]] = x[1]
        dicts[k] = options_parsed
    return dicts


class Participant:
    """Participant in database"""

    def __init__(self, data):
        self.record_id = data["record_id"]
        self.data = data
        self.appointments = {}

    def __repr__(self):
        return f" Participant {self.record_id}"

    def __str__(self):
        return f" Participant {self.record_id}"


class Appointment:
    """Appointment in database"""

    def __init__(self, data):
        self.record_id = data["record_id"]
        self.data = data
        self.appointment_id = (
            data["record_id"] + ":" + str(data["redcap_repeat_instance"])
        )
        self.status = data["status"]
        self.date = data["date"]

    def __repr__(self):
        return f"Appointment {self.appointment_id}, participant {self.record_id}, {self.date}, {self.status}"  # pylint: disable=line-too-long

    def __str__(self):
        return f"Appointment {self.appointment_id}, participant {self.record_id}, {self.date}, {self.status}"  # pylint: disable=line-too-long


class Questionnaire:
    """Language questionnaire in database"""

    def __init__(self, data):
        self.record_id = data["record_id"]
        self.language_id = data["id"]
        self.data = data
        for i in range(1, 5):
            l = f"lang{i}_exp"
            self.data[l] = float(self.data[l]) / 100 if self.data[l] else 0.0

    def __repr__(self):
        return (
            f" Language questionnaire {self.language_id} from participant {self.record_id}"
            + f"\n- L1 ({self.data["lang1"]}) = {self.data["lang1_exp"]}%"
            + f"\n- L2 ({self.data["lang2"]}) = {self.data["lang2_exp"]}%"
            + f"\n- L3 ({self.data["lang3"]}) = {self.data["lang3_exp"]}%"
            + f"\n- L4 ({self.data["lang4"]}) = {self.data["lang4_exp"]}%"
        )  # pylint: disable=line-too-long

    def __str__(self):
        return (
            f" Language questionnaire {self.language_id} from participant {self.record_id}"
            + f"\n- L1 ({self.data["lang1"]}) = {self.data["lang1_exp"]}%"
            + f"\n- L2 ({self.data["lang2"]}) = {self.data["lang2_exp"]}%"
            + f"\n- L3 ({self.data["lang3"]}) = {self.data["lang3_exp"]}%"
            + f"\n- L4 ({self.data["lang4"]}) = {self.data["lang4_exp"]}%"
        )  # pylint: disable=line-too-long


@dataclass
class RecordList:
    """List of records"""

    records: dict

    def to_df(self) -> pd.DataFrame:
        """Transform a dictionary dataset to a Pandas DataFrame.
        Returns:
        pd.DataFrame: Tabular dataset.
        """
        db_list = []
        for v in self.records.values():
            d = pd.DataFrame(v.data.items())
            d = d.set_index([0])
            db_list.append(d.transpose())
        df = pd.concat(db_list)
        df.index = pd.Index(df[df.columns[0]])
        df = df[df.columns[1:]]
        return df


class Records:
    """RedCAP records"""

    def __init__(self, **kwargs):

        records = get_records(**kwargs)
        participants = {}
        appointments = {}
        questionnaires = {}
        for r in records:
            if r["redcap_repeat_instance"]:
                data = {
                    re.sub("appointment_", "", k): v
                    for k, v in r.items()
                    if "appointment_" in k
                    or k in ["record_id", "redcap_repeat_instance"]
                }
                data["appointment_id"] = (
                    data["record_id"] + ":" + str(data["redcap_repeat_instance"])
                )
                appointments[data["appointment_id"]] = Appointment(data)
            if r["language_id"]:
                data = {
                    re.sub("language_", "", k): v
                    for k, v in r.items()
                    if "language_" in k or k == "record_id"
                }
                questionnaires[r["appointment_id"]] = Questionnaire(data)
            if not r["redcap_repeat_instance"]:
                data = {
                    re.sub("participant_", "", k): v
                    for k, v in r.items()
                    if "participant_" in k or k == "record_id"
                }
                participants[r["record_id"]] = Participant(data)
        for p, _ in participants.items():
            apps = {k: v for k, v in appointments.items() if v.record_id == p}
            participants[p].appointments = RecordList(apps)

        self.participants = RecordList(participants)
        self.appointments = RecordList(appointments)
        self.questionnaires = RecordList(questionnaires)

    def __repr__(self):
        return (
            "RedCAP database:"
            + f"\n- {len(self.participants.records)} participants"
            + f"\n- {len(self.appointments.records)} appointments"
            + f"\n- {len(self.questionnaires.records)} language questionnaires"  # pylint: disable=line-too-long
        )

    def __str__(self):
        return (
            "RedCAP database:"
            + f"\n- {len(self.participants.records)} participants"
            + f"\n- {len(self.appointments.records)} appointments"
            + f"\n- {len(self.questionnaires.records)} language questionnaires"  # pylint: disable=line-too-long
        )
