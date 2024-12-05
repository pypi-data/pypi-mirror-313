"""
Util functions for the app
"""

from collections import OrderedDict
from datetime import datetime
from pandas import DataFrame
from babylab import api
from babylab import calendar


def get_participants_table(records: api.Records, data_dict: dict = None) -> DataFrame:
    """Get participants table

    Args:
        records (api.Records): _description_

    Returns:
        pd.DataFrame: Table of partcicipants.
    """
    cols = ["name", "age_now_months", "age_now_days", "sex", "comments", "date_added"]
    if not records.participants.records:
        return DataFrame([], columns=cols)

    new_age_months = []
    new_age_days = []
    for _, v in records.participants.records.items():
        age = calendar.get_age(
            birth_date=calendar.get_birth_date(
                age=f"{v.data["age_now_months"]}:{v.data["age_now_days"]}"
            )
        )
        new_age_months.append(int(age[0]))
        new_age_days.append(int(age[1]))
    df = records.participants.to_df()
    df["age_now_months"] = new_age_months
    df["age_now_days"] = new_age_days
    for col_name, col_values in df.items():
        kdict = "participant_" + col_name
        if kdict in data_dict:
            df[col_name] = [data_dict[kdict][v] if v else "" for v in col_values]
    return df


def get_appointments_table(
    records: api.Records, data_dict: dict = None, ppt_id: str = None
) -> DataFrame:
    """Get appointments table.

    Args:
        records (api.Records): _description_

    Returns:
        pd.DataFrame: Table of appointments.
    """
    if ppt_id is None:
        apts = records.appointments
    else:
        apts = records.participants.records[ppt_id].appointments

    if not apts.records:
        return DataFrame(
            [],
            columns=[
                "appointment_id",
                "record_id",
                "study",
                "date",
                "date_made",
                "taxi_address",
                "taxi_isbooked",
                "status",
                "comments",
            ],
        )
    new_age_now_months = []
    new_age_now_days = []
    new_age_apt_months = []
    new_age_apt_days = []
    for v in apts.records.values():
        age_now_months = records.participants.records[v.record_id].data[
            "age_now_months"
        ]
        age_now_days = records.participants.records[v.record_id].data[
            "age_now_days"
        ]
        age_now = calendar.get_age(
            birth_date=calendar.get_birth_date(
                age=f"{age_now_months}:{age_now_days}"
            ),
            timestamp=datetime.strptime(
                records.participants.records[v.record_id].data[
                    "date_added"
                ],
                "%Y-%m-%d %H:%M:%S",
            ),
        )
        age_apt = calendar.get_age(
            birth_date=calendar.get_birth_date(
                age=f"{age_now_months}:{age_now_days}",
                timestamp=datetime.strptime(
                    v.data["date"],
                    "%Y-%m-%d %H:%M",
                ),
            )
        )
        new_age_now_months.append(int(age_now[0]))
        new_age_now_days.append(int(age_now[1]))
        new_age_apt_months.append(int(age_apt[0]))
        new_age_apt_days.append(int(age_apt[1]))
    df = apts.to_df()
    df["age_now_months"] = new_age_now_months
    df["age_now_days"] = new_age_now_days
    df["age_apt_months"] = new_age_apt_months
    df["age_apt_days"] = new_age_apt_days
    for col_name, col_values in df.items():
        kdict = "appointment_" + col_name
        if kdict in data_dict:
            df[col_name] = [data_dict[kdict][v] if v else "" for v in col_values]
    return df



def prepare_dashboard(records: api.Records = None, data_dict: dict = None):
    """Prepare data for dashboard"""
    ppts = get_participants_table(records,data_dict=data_dict)
    apts = get_appointments_table(records, data_dict=data_dict)

    age_dist = (
        (ppts["age_now_days"] + (ppts["age_now_months"] * 30.437))
        .astype(int)
        .value_counts()
        .to_dict()
    )
    age_dist = {"Missing" if not k else k: v for k, v in age_dist.items()}

    sex_dist = ppts["sex"].value_counts().to_dict()
    sex_dist = {"Missing" if not k else k: v for k, v in sex_dist.items()}

    date_added = ppts["date_added"].value_counts().to_dict()
    date_added = OrderedDict(sorted(date_added.items()))
    for idx, (k, v) in enumerate(date_added.items()):
        if idx > 0:
            date_added[k] = v + list(date_added.values())[idx - 1]

    date_made = apts["date_made"].value_counts().to_dict()
    date_made = OrderedDict(sorted(date_made.items()))
    for idx, (k, v) in enumerate(date_made.items()):
        if idx > 0:
            date_made[k] = v + list(date_made.values())[idx - 1]
    return {
        "n_ppts": ppts.shape[0],
        "n_apts": apts.shape[0],
        "age_dist_labels": list(age_dist.keys()),
        "age_dist_values": list(age_dist.values()),
        "sex_dist_labels": list(sex_dist.keys()),
        "sex_dist_values": list(sex_dist.values()),
        "date_made_labels": list(date_made.keys()),
        "date_made_values": list(date_made.values()),
        "date_added_labels": list(date_added.keys()),
        "date_added_values": list(date_added.values()),
    }


def prepare_participants(records: api.Records = None, data_dict: dict = None):
    """Prepare data for participants page"""
    df = get_participants_table(records, data_dict = data_dict)
    classes = "table table-striped table-hover table-sm dt-responsive nowrap w-100 data-toggle='table'"  # pylint: disable=line-too-long
    df["record_id"] = [
        f"<a href=/participants/{str(i)}>{str(i)}</a>" for i in df.index
    ]
    df.index = df.index.astype(int)
    df = df.sort_index(ascending=False)
    df = df[
        [
            "record_id",
            "name",
            "age_now_months",
            "age_now_days",
            "sex",
            "comments",
            "date_added",
        ]
    ]
    df = df.rename(
        columns={
            "record_id": "ID",
            "name": "Name",
            "age_now_months": "Age (months)",
            "age_now_days": "Age (days)",
            "sex": "Sex",
            "comments": "Comments",
            "date_added": "Added on",
        }
    )
    return {
        "table": df.to_html(
            classes=classes, escape=False, justify="left", index=False, bold_rows=True
        )
    }


def prepare_record_id(ppt_id: str, records: api.Records = None, data_dict: dict = None):
    """Prepare record ID page"""
    data = records.participants.records[ppt_id].data
    for k, v in data.items():
        kdict = "participant_" + k
        if kdict in data_dict:
            data[k] = data_dict[kdict][v] if v else ""
    data["age_now_months"] = (
        str(data["age_now_months"]) if data["age_now_months"] else ""
    )
    data["age_now_days"] = str(data["age_now_days"]) if data["age_now_days"] else ""
    
    df = get_appointments_table(
        records, data_dict=data_dict, ppt_id=ppt_id
    )
    classes = "table table-striped table-hover table-sm table-condensed"

    df["record_id"] = [f"<a href=/participants/{i}>{i}</a>" for i in df.index]
    df["appointment_id"] = [
        f"<a href=/appointments/{i}>{i}</a>" for i in df["appointment_id"]
    ]
    df = df.sort_values(by='date', ascending=False) 
    df = df[
        [
            "record_id",
            "appointment_id",
            "study",
            "date",
            "date_made",
            "taxi_address",
            "taxi_isbooked",
            "status",
            "comments",
        ]
    ]
    df = df.rename(
        columns={
            "record_id": "Participant ID",
            "appointment_id": "Appointment ID",
            "study": "Study",
            "date": "Date",
            "date_made": "Made on the",
            "taxi_address": "Taxi address",
            "taxi_isbooked": "Taxi booked",
            "status": "Status",
            "comments": "Comments:",
        }
    )
    table = df.to_html(
        classes=classes,
        escape=False,
        justify="left",
        index=False,
        bold_rows=True,
    )

    return {"data": data, "table": table}


def prepare_appointments(records: api.Records, data_dict: dict = None):
    """Prepare appointments page"""
    df = get_appointments_table(records, data_dict = data_dict)
    classes = "table table-striped table-hover table-sm table-condensed"
    df["appointment_id"] = [
        f"<a href=/appointments/{i}>{i}</a>" for i in df["appointment_id"]
    ]
    df["record_id"] = [f"<a href=/participants/{i}>{i}</a>" for i in df.index]
    df = df[
        [
            "appointment_id",
            "record_id",
            "study",
            "date",
            "date_made",
            "taxi_address",
            "taxi_isbooked",
            "status",
            "comments",
        ]
    ]
    df = df.sort_values("date", ascending = False)

    df = df.rename(
        columns={
            "appointment_id": "Appointment ID",
            "record_id": "Participant ID",
            "study": "Study",
            "date": "Date",
            "date_made": "Made on the",
            "taxi_address": "Taxi address",
            "taxi_isbooked": "Taxi booked",
            "status": "Appointment status",
            "comments": "Comments",
        }
    )
    df.reset_index(inplace=True)

    table = df.to_html(
        classes=classes,
        escape=False,
        justify="left",
        index=False,
        bold_rows=True,
    )

    return {"table": table}


