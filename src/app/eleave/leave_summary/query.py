#
#   +-------------------------------------------------------+
#   | Copyright (c)ftb bank.                          |
#   +-------------------------------------------------------+
#   | NAME : SOY DARA                                       |
#   | EMAIL: soydara168@gmail.com                           |
#   | DUTY : FTB BANK (HEAD OFFICE)                         |
#   | ROLE : Software Developer                             |
#   +-------------------------------------------------------+
#   | Released: Copyright (c)  18/12/2023.
#   +-------------------------------------------------------+
#

from django.db import connection
import cx_Oracle
from datetime import datetime
from decimal import Decimal


# Function to convert cx_Oracle.LOB to string
def convert_lob_to_string(lob_data):
    if lob_data is not None and isinstance(lob_data, cx_Oracle.LOB):
        return lob_data.read()
    return lob_data


def query_fetch_leave_request(user_id):
    with connection.cursor() as cursor:
        query = "SELECT * FROM REPORT_ELEAVE_3_MONTHS_LATEST WHERE USER_ID = :user_id"
        cursor.execute(query, {"user_id": user_id})  # Pass parameters as a dictionary
        result = cursor.fetchall()

    columns = [
        "id",
        "user_id",
        "staff_id",
        "staff_name",
        "staff_position",
        "staff_department",
        "start_date",
        "end_date",
        "from_time",
        "to_time",
        "hours",
        "minute",
        "total_time",
        "reason",
        "requested_at",
        "certifier_at",
        "authorizer_at",
        "rejected_at",
        "rejected_reason",
        "incharge_request",
        "incharge_certifier",
        "incharge_authorizer",
        "created_at",
        "updated_at",
        "authorizer",
        "authorizer_by",
        "certifier",
        "certifier_by",
        "created_by",
        "leave_status",
        "leave_type",
        "rejected_by",
        "requested_by",
        "updated_by",
        "canceled_at",
        "canceled_by",
        "canceled_reason",
    ]

    output = []
    for row in result:
        item = dict(zip(columns, row))
        # Convert LOB fields to strings
        item["reason"] = convert_lob_to_string(item["reason"])
        item["rejected_reason"] = convert_lob_to_string(item["rejected_reason"])
        item["canceled_reason"] = convert_lob_to_string(item["canceled_reason"])
        # item["requested_at"] = (
        #     item["requested_at"].strftime("%d-%m-%Y %H:%M:%S")
        #     if isinstance(item["requested_at"], datetime)
        #     else None
        # )
        # Handling datetime and Decimal fields
        item["start_date"] = (
            item["start_date"].strftime("%Y-%m-%d")
            if isinstance(item["start_date"], datetime)
            else None
        )
        item["end_date"] = (
            item["end_date"].strftime("%Y-%m-%d")
            if isinstance(item["end_date"], datetime)
            else None
        )

        output.append(item)

    return output
